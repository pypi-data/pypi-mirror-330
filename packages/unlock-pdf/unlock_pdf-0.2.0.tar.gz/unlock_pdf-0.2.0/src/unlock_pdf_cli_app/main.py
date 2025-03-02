import argparse
from pathlib import Path
import pikepdf

def unlock_pdf(path: Path, suffix="_unlocked"):
    with pikepdf.Pdf.open(path) as pdf:
        save_name = path.parent / f"{path.stem}{suffix}.pdf"
        pdf.save(save_name)


def main():
    parser = argparse.ArgumentParser(
        prog='Unlock PDF',
        description="Unlock a pdf",
        epilog="Written by Elvis Mak"
        )
    parser.add_argument("path", type=str, help="specify the file path")
    parser.add_argument("-d", "--directory", action="store_true", 
                        help='add this flag if the path provided is a directory and you need to unlock all PDFs in that directory')
    parser.add_argument("-s", "--suffix", type=str, default="_unlocked", help="specify the suffix for the unlocked pdf.")

    args = parser.parse_args()

    path = Path(args.path)
    print(args.directory)
    if args.directory:
        p = path.glob('**/*')
        _ = [unlock_pdf(path=x, suffix=args.suffix) for x in p if x.is_file()]
    else:
        unlock_pdf(path=path, suffix=args.suffix)


if __name__ == "__main__":
    main()