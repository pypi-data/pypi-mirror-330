import argparse
from athanasius.archiver import archive
from athanasius.extractor import extract
from athanasius.utils import generate_archive_name

def main():
    parser = argparse.ArgumentParser(prog="ath", description="Athanasius Archival Tool")

    parser.add_argument("paths", nargs="*", help="Files or directories to archive.")
    parser.add_argument("-o", "--output", help="Specify output archive name.")
    parser.add_argument("-e", "--extract", help="Extract specified archive.")

    args = parser.parse_args()

    if args.extract:
        extract(args.extract)
    elif args.paths:
        output_file = args.output or generate_archive_name()
        archive(args.paths, output_file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
