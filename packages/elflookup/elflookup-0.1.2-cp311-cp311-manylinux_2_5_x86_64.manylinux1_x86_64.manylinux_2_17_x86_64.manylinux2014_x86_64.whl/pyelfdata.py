import argparse
import sys

import elflookup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", metavar="FILENAME")
    parser.add_argument("section", nargs="+", metavar="SECTION")
    parser.add_argument("-k", dest="key", action="store_true")
    parser.add_argument("-n", dest="newline", action="store_true")
    parser.add_argument("-q", dest="quote", action="store_true")
    args = parser.parse_args()

    fmt = ""
    if args.key:
        fmt += "{key}\t"
    if args.quote:
        fmt += '"{value}"'
    else:
        fmt += "{value}"
    if args.key or args.newline:
        fmt += "\n"

    for i, section in enumerate(args.section):
        value = elflookup.elf_section_file(section, args.filename)
        if i and not (args.key or args.newline):
            sys.stdout.write("\t")
        sys.stdout.write(fmt.format(key=section, value=value))


if __name__ == "__main__":
    main()
