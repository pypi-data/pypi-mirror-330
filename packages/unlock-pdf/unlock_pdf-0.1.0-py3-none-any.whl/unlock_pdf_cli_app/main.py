import argparse
from pathlib import Path
import pikepdf

def unlock_pdf(path: Path, suffix):
    with pikepdf.Pdf.open(path) as pdf:
        save_name = path.parent / f"{path.stem}_unlocked.pdf"
        pdf.save(save_name)


def main():
    parser = argparse.ArgumentParser(description="Unlock a pdf")
    parser.add_argument("file", type=str, help="specify the file path")

    args = parser.parse_args()

    path = Path(args.file)
    unlock_pdf(path, '_unlocked.pdf')

if __name__ == "__main__":
    main()