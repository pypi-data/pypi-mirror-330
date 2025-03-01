"""
Copyright (c) 2019 - Present, Memfault
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code or in binary form must reproduce
the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the
distribution.

2. Neither the name of Memfault nor the names of its contributors may be
used to endorse or promote products derived from this software without
specific prior written permission.

3. Any software provided in binary form under this license must not be
reverse engineered, decompiled, modified and/or disassembled.

THIS SOFTWARE IS PROVIDED BY MEMFAULT "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
NONINFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
SHALL MEMFAULT OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
"""

"""
Converts a Memfault binary formatted coredump to one which can be loaded by GDB.

Reach out to Memfault at https://memfault.com/demo-request/ if you're interested
in learning about our observability offerings!
"""

import argparse
import dataclasses
import io
import json
import pathlib
import struct
import sys
from collections.abc import Iterator
from enum import IntEnum
from typing import Any

from elftools.elf import constants, enums


class MachineType(IntEnum):
    ARM = enums.ENUM_E_MACHINE["EM_ARM"]
    ARMV7_A_R = enums.ENUM_E_MACHINE["EM_ARM"] | 1 << 16
    ESP32 = enums.ENUM_E_MACHINE["EM_XTENSA"]
    ESP8266 = enums.ENUM_E_MACHINE["EM_XTENSA"] | 1 << 16
    ESP32_S2 = enums.ENUM_E_MACHINE["EM_XTENSA"] | 2 << 16
    ESP32_S3 = enums.ENUM_E_MACHINE["EM_XTENSA"] | 3 << 16
    AARCH64 = enums.ENUM_E_MACHINE["EM_AARCH64"]
    RISCV = enums.ENUM_E_MACHINE["EM_RISCV"]


class MemfaultCoredumpBlockType(IntEnum):
    CURRENT_REGISTERS = 0
    MEMORY_REGION = 1
    DEVICE_SERIAL = 2
    FIRMWARE_VERSION = 3
    HARDWARE_REVISION = 4
    TRACE_REASON = 5
    PADDING_REGION = 6
    MACHINE_TYPE = 7
    VENDOR_COREDUMP_ESP_IDF_V2_TO_V3_1 = 8
    ARM_V7M_MPU = 9
    SOFTWARE_VERSION = 10
    SOFTWARE_TYPE = 11
    BUILD_ID = 12


MEMFAULT_COREDUMP_MAGIC = 0x45524F43
MEMFAULT_COREDUMP_FOOTER_MAGIC = 0x504D5544

MEMFAULT_COREDUMP_VERSION = 1
MEMFAULT_COREDUMP_FILE_HEADER_FMT = (
    "<III"  # magic, version, file length (incl. file header)
)
MEMFAULT_COREDUMP_FILE_FOOTER_FMT = "<IIII"  # magic, flags, rsvd, rsvd
MEMFAULT_COREDUMP_BLOCK_HEADER_FMT = "<bxxxII"  # type, address, block payload length
MEMFAULT_CORE_FOOTER_SIZE = 16
MEMFAULT_CORE_HDR_SIZE = 12


class CoreParseError(Exception):
    pass


class MalformedCoreFile(CoreParseError):  # noqa: N818
    pass


class InvalidCoreMagic(CoreParseError):  # noqa: N818
    pass


class BadSectionDataError(CoreParseError):
    pass


class MemfaultCoredumpReader:
    @classmethod
    def from_filename(cls, filename: str | pathlib.Path) -> "MemfaultCoredumpReader":
        return cls(pathlib.Path(filename).read_bytes())

    def __init__(self, coredump_bin: bytes) -> None:
        self.coredump_bin = coredump_bin

        if len(coredump_bin) < MEMFAULT_CORE_HDR_SIZE:
            raise MalformedCoreFile("Short file header ... malformed core")

        header_bytes = coredump_bin[0:MEMFAULT_CORE_HDR_SIZE]
        hdr = struct.unpack(MEMFAULT_COREDUMP_FILE_HEADER_FMT, header_bytes)

        if hdr[0] != MEMFAULT_COREDUMP_MAGIC:
            raise InvalidCoreMagic("Not a memfault core file!")

        # A footer was added in coredump version 2
        footer_flags = 0
        footer_present = hdr[1] == 2
        if footer_present:
            footer_bytes = coredump_bin[hdr[2] - MEMFAULT_CORE_FOOTER_SIZE : hdr[2]]
            try:
                footer = struct.unpack(MEMFAULT_COREDUMP_FILE_FOOTER_FMT, footer_bytes)
            except struct.error as e:
                raise InvalidCoreMagic("Invalid coredump footer") from e

            if footer[0] != MEMFAULT_COREDUMP_FOOTER_MAGIC:
                raise InvalidCoreMagic("Invalid coredump footer")
            footer_flags = footer[1]

        # Is the truncated flag set?
        self.core_truncated = footer_flags & 0x1

        self.coredump_block_data = coredump_bin[MEMFAULT_CORE_HDR_SIZE : hdr[2]]
        if footer_present:
            self.coredump_block_data = self.coredump_block_data[
                0:-MEMFAULT_CORE_FOOTER_SIZE
            ]

    def metadata(self, *, extended: bool = False) -> dict:
        """
        Return metadata found in a coredump as a json dictionary
        """
        metadata: dict[str, Any] = {}

        extended_metadata: dict[str, Any] = {}

        for segment in self.iterate_sections():
            parser = SegmentParser.from_segment(segment)
            parser.parse(into=metadata, into_extended=extended_metadata)

        metadata["core_truncated"] = self.core_truncated

        # Default to ARM: Memfault coredumps did not contain the machine type, initially:
        if "machine_type" not in metadata:
            metadata["machine_type"] = enums.ENUM_E_MACHINE["EM_ARM"]

        if extended:
            metadata.update(extended_metadata)

        return metadata

    def iterate_sections(self) -> Iterator[dict[str, Any]]:
        core_file = io.BytesIO(self.coredump_block_data)

        while True:
            block_hdr_size = 12
            block_header_bytes = core_file.read(block_hdr_size)
            if len(block_header_bytes) == 0:
                # We've reached the end of the core
                break

            if len(block_header_bytes) != block_hdr_size:
                raise MalformedCoreFile("Short header read ... malformed core")

            block = struct.unpack(
                MEMFAULT_COREDUMP_BLOCK_HEADER_FMT, block_header_bytes
            )
            block_type = block[0]
            block_address = block[1]
            block_length = block[2]

            block_data = core_file.read(block_length)
            if len(block_data) != block_length:
                raise MalformedCoreFile(
                    f"Short block read ... malformed core. Expected: 0x{block_length:x}, got: 0x{len(block_data):x}"
                )

            res: dict[str, Any] = {}

            try:
                res["type"] = MemfaultCoredumpBlockType(block_type)
            except ValueError as e:
                raise BadSectionDataError(f"Bad type: {block_type}") from e

            res["address"] = block_address
            res["data"] = block_data

            yield res


@dataclasses.dataclass
class SegmentParser:
    type_: MemfaultCoredumpBlockType
    data: bytes
    segment: dict

    @classmethod
    def from_segment(cls, segment: dict) -> "SegmentParser":
        return cls(type_=segment["type"], data=segment["data"], segment=segment)

    def decode_ascii(self) -> str:
        try:
            return self.data.decode("ascii")
        except UnicodeDecodeError as e:
            raise BadSectionDataError(f"Bad data for {self.type_.name} section.") from e

    def unpack(self, format_: str) -> tuple:
        try:
            return struct.unpack(format_, self.data)
        except struct.error as e:
            raise BadSectionDataError(f"Bad data for {self.type_.name} section.") from e

    def parse(self, *, into: dict, into_extended: dict) -> None:
        if self.type_ == MemfaultCoredumpBlockType.HARDWARE_REVISION:
            into["hardware_version"] = self.decode_ascii()
        elif self.type_ == MemfaultCoredumpBlockType.SOFTWARE_VERSION:
            into["software_version"] = self.decode_ascii()
        elif self.type_ == MemfaultCoredumpBlockType.SOFTWARE_TYPE:
            into["software_type"] = self.decode_ascii()
        elif self.type_ == MemfaultCoredumpBlockType.DEVICE_SERIAL:
            into["device_serial"] = self.decode_ascii()
        elif self.type_ == MemfaultCoredumpBlockType.TRACE_REASON:
            into["trace_reason"] = self.unpack("<I")[0]
        elif self.type_ == MemfaultCoredumpBlockType.MACHINE_TYPE:
            into["machine_type"] = self.unpack("<I")[0]
        elif self.type_ == MemfaultCoredumpBlockType.VENDOR_COREDUMP_ESP_IDF_V2_TO_V3_1:
            into["has_esp_idf_coredump"] = True
        elif self.type_ == MemfaultCoredumpBlockType.BUILD_ID:
            into["build_id"] = self.data.hex()
        elif self.type_ == MemfaultCoredumpBlockType.MEMORY_REGION:
            into_extended.setdefault("memory_regions", []).append(
                {
                    "address": f"0x{self.segment['address']:x}",
                    "length": len(self.data),
                }
            )
        elif self.type_ == MemfaultCoredumpBlockType.CURRENT_REGISTERS:
            into_extended.setdefault("registers", []).append({"length": len(self.data)})
        # Deprecated:
        elif self.type_ == MemfaultCoredumpBlockType.FIRMWARE_VERSION:
            into["fw_version"] = self.decode_ascii()


# TODO: Generalize to other 64-bit archs, we only support ELF-64 for aarch64
def is_64_bit(e_machine: enums.ENUM_E_MACHINE) -> bool:
    """Function to determine if machine is 64-bit"""
    return e_machine == enums.ENUM_E_MACHINE["EM_AARCH64"]


@dataclasses.dataclass()
class ElfSegment:
    """Fields present in every segment"""

    p_type: int
    p_flags: int
    p_offset: int
    p_vaddr: int
    p_paddr: int
    p_filesz: int
    p_memsz: int
    p_align: int
    data: bytes

    def set_file_offset(self, file_offset: int):
        self.p_offset = file_offset

    def data_length(self):
        return len(self.data)

    def get_data(self):
        return self.data

    def _pad_data(self, data: bytes) -> bytes:
        padding_modulo = len(data) % self.p_align
        padding_bytes = bytes(self.p_align - padding_modulo) if padding_modulo else b""

        return data + padding_bytes

    def generate_header(self) -> bytes:
        return b""


class Elf64Segment(ElfSegment):
    HEADER_FMT = "<IIQQQQQQ"
    HEADER_SIZE = struct.calcsize(HEADER_FMT)

    # NB: ELF-64 has a different order for these fields
    def generate_header(self) -> bytes:
        return struct.pack(
            Elf64Segment.HEADER_FMT,
            self.p_type,
            self.p_flags,
            self.p_offset,
            self.p_vaddr,
            self.p_paddr,
            self.p_filesz,
            self.p_memsz,
            self.p_align,
        )


class Elf32Segment(ElfSegment):
    HEADER_FMT = "<IIIIIIII"
    HEADER_SIZE = struct.calcsize(HEADER_FMT)

    def generate_header(self) -> bytes:
        return struct.pack(
            Elf32Segment.HEADER_FMT,
            self.p_type,
            self.p_offset,
            self.p_vaddr,
            self.p_paddr,
            self.p_filesz,
            self.p_memsz,
            self.p_flags,
            self.p_align,
        )


class Elf64LoadSegment(Elf64Segment):
    def __init__(self, address: int, data: bytes):
        length = len(data)
        self.p_type = enums.ENUM_P_TYPE_BASE["PT_LOAD"]
        self.p_offset = 0  # Offset of header in ELF
        self.p_vaddr = address
        self.p_paddr = 0  # Unused
        self.p_filesz = length
        self.p_memsz = length
        self.p_flags = constants.P_FLAGS.PF_R
        self.p_align = 8

        self.data = self._pad_data(data)


class Elf32LoadSegment(Elf32Segment):
    def __init__(self, address: int, data: bytes):
        length = len(data)
        self.p_type = enums.ENUM_P_TYPE_BASE["PT_LOAD"]
        self.p_offset = 0  # Offset of header in ELF
        self.p_vaddr = address
        self.p_paddr = 0  # Unused
        self.p_filesz = length
        self.p_memsz = length
        self.p_flags = constants.P_FLAGS.PF_R
        self.p_align = 4

        self.data = self._pad_data(data)


# For whatever reason, ELF64 notes are the same as ELF32 notes.
# The spec specifies 8-byte alignment for note sections but in practice, none of the consumers/producers of ELF files follow the spec!
# See: https://github.com/bminor/binutils-gdb/blob/7f26d260ef76a4cb2873a7815bef187005528c19/bfd/elf.c#L12337-L12340
class ElfNote:
    def __init__(self, name: str, description: bytes, note_type: int) -> None:
        name_len = len(name) + 1

        name_byte_array = bytearray(name, "ascii")
        name_byte_array.append(0x0)
        if name_len % 4 != 0:
            round_number = (name_len + 4) - (name_len % 4)
            pad_bytes = bytearray(round_number - name_len)
            name_byte_array.extend(pad_bytes)

        self.namesz = len(name_byte_array)
        self.name = name_byte_array
        self.descsz = len(description)
        self.type = note_type
        self.desc = description

    def to_binary(self) -> bytes:
        note_header = struct.pack("<III", self.namesz, self.descsz, self.type)
        return note_header + bytes(self.name) + bytes(self.desc)


# TODO: Refactor ElfxNoteSegment types
class Elf64NoteSegment(Elf64Segment):
    def __init__(self, name: str, description: bytes, note_type: int) -> None:
        self.data = ElfNote(name, description, note_type).to_binary()

        # PHDR Contents
        self.p_type = enums.ENUM_P_TYPE_BASE["PT_NOTE"]
        self.p_offset = 0  # Offset of header in ELF
        self.p_vaddr = 0
        self.p_paddr = 0  # Unused
        self.p_filesz = len(self.data)
        self.p_memsz = 0
        self.p_flags = 0
        self.p_align = 0  # Convention seems to be to set this to 0 for notes


class Elf32NoteSegment(Elf32Segment):
    def __init__(self, name: str, description: bytes, note_type: int) -> None:
        self.data = ElfNote(name, description, note_type).to_binary()

        # PHDR Contents
        self.p_type = enums.ENUM_P_TYPE_BASE["PT_NOTE"]
        self.p_offset = 0  # Offset of header in ELF
        self.p_vaddr = 0
        self.p_paddr = 0  # Unused
        self.p_filesz = len(self.data)
        self.p_memsz = 0
        self.p_flags = 0
        self.p_align = 4  # Seems to be what people do?


# TODO: MFLT-152: Try to add names to the threads (part of NT_PRPSINFO/NT_PSINFO?):
# See https://github.com/bminor/binutils-gdb/blob/master/bfd/elf32-arm.c#L2172


def linux_thread_status_note_aarch64(
    regs: bytes, *, signal: int = 0, lwpid: int = 0
) -> Elf64NoteSegment:
    # https://elixir.bootlin.com/linux/v4.9/source/arch/arm64/include/uapi/asm/ptrace.h#L69
    # - Register packing for Linux (left) vs Memfault (right):
    #   - x0-x30 | sp
    #   - sp     | pc
    #   - pc     | cpsr
    #   - cpsr   | x0-x30
    # We can swap the first 24 bytes (3x registers) with the remaining bytes
    regs = regs[24:] + regs[0:24]

    # Based on format found in binutils-gdb:
    # https://github.com/bminor/binutils-gdb/blob/fd67aa1129fd006ad49ed5ecb2b063705211553a/bfd/elfxx-aarch64.c#L589
    # Bytes 0 -  11: don't care
    # Bytes 12 - 13: Signal (int16_t)
    # Bytes 14 - 31: don't care
    # Bytes 32 - 35: lwpid/thread ID (int32_t)
    # Bytes 36 - 111: don't care
    # Bytes 112 - 383: aarch64 registers
    # Bytes 384 - 391: padding 8-byte alignment, not clear why additional padding is needed
    description = struct.pack("< 12x h 18x i 76x 272s 8x", signal, lwpid, regs)
    assert len(description) == 392
    return Elf64NoteSegment(
        ".reg", description, enums.ENUM_CORE_NOTE_N_TYPE["NT_PRSTATUS"]
    )


def linux_thread_status_note_arm(
    regs: bytes, *, signal: int = 0, lwpid: int = 0
) -> Elf32NoteSegment:
    # This format lines up with the parsing here and is ARM specific:
    # https://github.com/bminor/binutils-gdb/blob/master/bfd/elf32-arm.c#L2142
    # related: https://github.com/torvalds/linux/blob/master/include/linux/elfcore.h#L32
    # - 12 : signal (signed? int16_t)
    # - 14 : 10x "don't care" bytes
    # - 24 : lwpid a.k.a. light weight process id (signed? int32_t)
    # - 28 : 44x "don't care" bytes
    # - 72 : regs (68 bytes)
    #        - regs are packed by Memfault in same order as Linux
    #          https://elixir.bootlin.com/linux/v4.9/source/arch/arm/include/uapi/asm/ptrace.h#L130
    # - 140: 8x "don't care" bytes (I suspect the first 4 are actually supposed to be part of regs, because
    #        in elf32_arm_nabi_grok_prstatus, a size of 72 is used.)
    description = struct.pack("< 12x h 10x i 44x 68s 8x", signal, lwpid, regs)
    assert len(description) == 148

    return Elf32NoteSegment(
        ".reg",
        description,
        enums.ENUM_CORE_NOTE_N_TYPE["NT_PRSTATUS"],
    )


def linux_thread_status_note_xtensa(
    regs: bytes, *, signal: int = 0, lwpid: int = 0
) -> Elf32NoteSegment:
    # This format lines up with the parsing here and is Xtensa specific:
    # https://sourceware.org/git/?p=binutils-gdb.git;a=blob;f=bfd/elf32-xtensa.c;hb=af969b14aedcc0ae27dcefab4327ff2d153dec8b#l3736
    # 0-11: don't care
    # 12-13: signal (int16_t)
    # 14-23: don't care
    # 24-27: lwpid (int32_t)
    # 28-71: don't care
    # 72+: regs
    #
    # Register order expected by gdb is here:
    # https://sourceware.org/git/?p=binutils-gdb.git;a=blob;f=gdb/arch/xtensa.h;hb=1d506c26d9772bcd84e1a7b3a8c8c5bc602dbf61#l28
    #
    # word (byte) offset | gdb             | memfault
    # -------------------|-----------------|---------
    # 0 (0)              | pc              | pc
    # 1 (4)              | ps              | ps
    # 2 (byte)           | lbeg            | ar0
    # 3 (byte)           | lend            | ar1
    # 4 (byte)           | lcount          | ar2
    # 5 (byte)           | sar             | ar3
    # 6 (byte)           | windowstart     | ar4
    # 7 (byte)           | windowbase      | ar5
    # 8 (byte)           | threadptr       | ar6
    # 9 (byte)           | reserved[0]     | ar7
    # 10 (byte)          | reserved[1]     | ar8
    # 11 (byte)          | reserved[2]     | ar9
    # 12 (byte)          | reserved[3]     | ar10
    # 13 (byte)          | reserved[4]     | ar11
    # 14 (byte)          | reserved[5]     | ar12
    # 15 (byte)          | reserved[6]     | ar13
    # 16 (byte)          | reserved[7]     | ar14
    # 17 (byte)          | reserved[8]     | ar15
    # 18 (byte)          | reserved[9]     | sar
    # 19 (byte)          | reserved[10]    | lbeg
    # 20 (byte)          | reserved[11]    | lcount
    # 21 (byte)          | reserved[12]    | exccause
    # 22 (byte)          | reserved[13]    | excvaddr
    # 23 (byte)          | reserved[14-55] | -
    # 48 (byte)          | ar[64]          | -

    # Reorder registers to match gdb expectations
    regs = regs[4:]  # strip off first word, it's the collection type

    gdb_regs = (
        regs[0:4]  # pc
        + regs[4:8]  # ps
        + regs[76:80]  # lbeg
        + bytes([0, 0, 0, 0])  # lend
        + regs[80:84]  # lcount
        + regs[72:76]  # sar
        + bytes([1, 0, 0, 0])  # windowstart, must be 1
        + bytes([0, 0, 0, 0])  # windowbase, must be 0
        + bytes([0, 0, 0, 0])  # threadptr
        + bytes([0, 0, 0, 0]) * 55  # reserved[0-55]
        + regs[8:72]  # ar[0-15]
    )

    description = struct.pack("< 12x h 10x i 44x 512s 4x", signal, lwpid, gdb_regs)
    assert len(description) == 588, f"Expected 588, got {len(description)}"

    return Elf32NoteSegment(
        ".reg",
        description,
        enums.ENUM_CORE_NOTE_N_TYPE["NT_PRSTATUS"],
    )


class ElfIdentBytes:
    def __init__(self, e_machine: enums.ENUM_E_MACHINE):
        ei_class = (
            enums.ENUM_EI_CLASS["ELFCLASS64"]
            if is_64_bit(e_machine)
            else enums.ENUM_EI_CLASS["ELFCLASS32"]
        )

        # The format for the identity bytes is pretty similar between ELF32 and ELF64
        # To simplify, we can ignore setting EI_OSABI and EI_ABIVERSION as these are very rarely non-zero
        self.eident = struct.pack(
            "<Bccc BBB 9x",
            0x7F,
            b"E",
            b"L",
            b"F",
            ei_class,
            enums.ENUM_EI_DATA["ELFDATA2LSB"],
            enums.ENUM_E_VERSION["EV_CURRENT"],
        )

    def data(self) -> bytes:
        return self.eident


class ElfHeader:
    def __init__(self, e_machine: enums.ENUM_E_MACHINE, num_program_headers: int):
        self.e_ident = ElfIdentBytes(e_machine)
        self.e_type = enums.ENUM_E_TYPE["ET_CORE"]
        # This value is defined by elftools.ENUM_E_MACHINE and our custom modifications to the upper 16-bits see gdb_helper.MachineType
        # The ELF spec requires this to be 16-bits max, so we must truncate down
        self.e_machine = e_machine & 0xFFFF
        self.e_version = enums.ENUM_E_VERSION["EV_CURRENT"]
        self.e_entry = 0
        # Size of the Elf64_Ehdr (64 bytes) or Elf32_Ehdr (52 bytes)
        self.e_ehsize = 64 if is_64_bit(e_machine) else 0x34
        self.e_flags = 0

        # Program Headers always follow the ELF Header, use size of ELF header to set Program Header offset
        self.e_phoff = self.e_ehsize
        self.e_phentsize = (
            Elf64Segment.HEADER_SIZE
            if is_64_bit(e_machine)
            else Elf32Segment.HEADER_SIZE
        )
        self.e_phnum = num_program_headers

        # No section header table included with core
        self.e_shoff = 0

        # Set to 0 for ELF64 and 40 for ELF32
        # GDB with ELF64 spits out garbage if we set this to the typical section header size (64 bytes).
        # Linux coredumps set this to 0
        self.e_shentsize = 0 if is_64_bit(e_machine) else 40
        self.e_shnum = 0
        self.e_shstrndx = enums.ENUM_ST_SHNDX["SHN_UNDEF"]

        # See ELF or ELF-64 spec for details on type sizes
        self.format_str = "<HHIQQQIHHHHHH" if is_64_bit(e_machine) else "<HHIIIIIHHHHHH"

    def to_binary(self):
        data = bytearray(self.e_ident.data())
        data.extend(
            bytearray(
                struct.pack(
                    self.format_str,
                    self.e_type,
                    self.e_machine,
                    self.e_version,
                    self.e_entry,
                    self.e_phoff,
                    self.e_shoff,
                    self.e_flags,
                    self.e_ehsize,
                    self.e_phentsize,
                    self.e_phnum,
                    self.e_shentsize,
                    self.e_shnum,
                    self.e_shstrndx,
                )
            )
        )
        return data


class CoreElf:
    def __init__(
        self, e_machine: enums.ENUM_E_MACHINE = enums.ENUM_E_MACHINE["EM_ARM"]
    ):
        self.program_headers: list[ElfSegment] = []
        self.registers: list[bytes] = []
        self.e_machine: enums.ENUM_E_MACHINE = e_machine
        if self.e_machine in (
            MachineType.ESP32,
            MachineType.ESP32_S2,
            MachineType.ESP32_S3,
        ):
            self.file_header_builder = ElfHeader
            self.header_size = Elf32Segment.HEADER_SIZE
            self.load_segment_builder = Elf32LoadSegment
            self.thread_note_builder = linux_thread_status_note_xtensa
        # Default to ARM: Memfault coredumps did not contain the machine
        # type, initially. This also covers the case where the machine
        # type is unsupported, eg MachineType.ESP8266/RISCV
        elif self.is_64_bit:
            self.file_header_builder = ElfHeader
            self.header_size = Elf64Segment.HEADER_SIZE
            self.load_segment_builder = Elf64LoadSegment
            self.thread_note_builder = linux_thread_status_note_aarch64
        else:
            self.file_header_builder = ElfHeader
            self.header_size = Elf32Segment.HEADER_SIZE
            self.load_segment_builder = Elf32LoadSegment
            self.thread_note_builder = linux_thread_status_note_arm

    @property
    def is_64_bit(self) -> bool:
        return self.e_machine == enums.ENUM_E_MACHINE["EM_AARCH64"]

    def add_program_header(self, header: ElfSegment):
        self.program_headers.append(header)

    def remove_program_header(self, header: ElfSegment):
        self.program_headers.remove(header)

    def set_machine(self, e_machine: enums.ENUM_E_MACHINE):
        self.e_machine = e_machine

    def add_register_set(self, data: bytes) -> None:
        self.registers.append(data)

    def add_thread_note(self, registers: bytes, lwpid: int) -> None:
        self.add_program_header(self.thread_note_builder(registers, lwpid=lwpid))

    def process_register_sections(self):
        if self.e_machine not in (
            MachineType.ARM,
            MachineType.AARCH64,
            MachineType.ESP32,
            MachineType.ESP32_S2,
            MachineType.ESP32_S3,
        ):
            # Today we only support register conversion for ARM + Xtensa
            return None

        threads_note = None
        for cpu_regs in self.registers:
            threads_note = self.thread_note_builder(cpu_regs)
            self.program_headers.insert(0, threads_note)
            # We only process the first register set today so break
            # In the future (i.e multi CPU architectures) we could
            # have several register sets to build
            break

        return threads_note

    def build_elf(self, out_filename: str | pathlib.Path):
        hdr = self.file_header_builder(self.e_machine, len(self.program_headers))

        data = hdr.to_binary()

        hdr_len = len(data)
        offset = hdr_len + len(self.program_headers) * self.header_size

        # Figure out where things are gonna be
        for phdr in self.program_headers:
            phdr.set_file_offset(offset)
            offset += phdr.data_length()

        # first, write the program header
        for phdr in self.program_headers:
            data.extend(phdr.generate_header())

        for phdr in self.program_headers:
            data.extend(phdr.get_data())

        with open(out_filename, "wb") as f:
            f.write(data)


def get_coredump_metadata(filename: str) -> dict[str, Any]:
    """
    Return metadata found in a coredump as a json dictionary
    """
    return MemfaultCoredumpReader.from_filename(filename).metadata()


def convert_core_to_elf_without_rtos_awareness(
    filename: str | pathlib.Path, out_filename: str | pathlib.Path
) -> tuple[CoreElf | None, Elf32NoteSegment | Elf64NoteSegment | None]:
    """
    Converts the binary formatted memfault coredump into an ELF suitable for parsing with an
    *-elf-linux-gdb build
    """
    threads_note = None

    reader = MemfaultCoredumpReader.from_filename(filename)
    e_machine = reader.metadata()["machine_type"]
    c = CoreElf(e_machine)
    for segment in reader.iterate_sections():
        if segment["type"] == MemfaultCoredumpBlockType.CURRENT_REGISTERS:
            c.add_register_set(segment["data"])
        elif segment["type"] == MemfaultCoredumpBlockType.MEMORY_REGION:
            c.add_program_header(
                c.load_segment_builder(segment["address"], segment["data"])
            )

    threads_note = c.process_register_sections()
    c.build_elf(out_filename)
    return c, threads_note


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Convert a Memfault binary coredump file to an ELF core file that can be loaded by GDB"
        )
    )
    parser.add_argument(
        "--file", required=True, help="The memfault binary core to convert"
    )
    parser.add_argument(
        "--out_elf",
        required=True,
        help="The file to save the converted elf in, required",
    )

    args = parser.parse_args()

    reader = MemfaultCoredumpReader.from_filename(args.file)
    metadata = reader.metadata()
    print("Coredump Valid")
    print(json.dumps(metadata, indent=1))

    if not args.out_elf:
        sys.exit(0)

    convert_core_to_elf_without_rtos_awareness(args.file, args.out_elf)


if __name__ == "__main__":
    main()
