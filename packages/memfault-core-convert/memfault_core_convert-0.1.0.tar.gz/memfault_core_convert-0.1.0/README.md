# Memfault Core Convert

This is a small utility for converting Memfault coredumps to ELF core files. It
is intended to be used in conjunction with the
[Memfault Firmware SDK](https://github.com/memfault/memfault-firmware-sdk/).

Learn more about Memfault at [memfault.com](https://memfault.com/).

## Usage

The utility is a command line tool that takes two parameters: the path to the
Memfault coredump and the path to the ELF file to write. For example:

```bash
memfault-core-convert --in-file memfault-core.bin --out-file core.elf
```

The resulting ELF file can be loaded into a debugger for analysis, see the
instructions here:

<https://docs.memfault.com/docs/mcu/coredump-elf-with-gdb/>
