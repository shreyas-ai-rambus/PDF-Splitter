from PyPDF2 import PdfReader, PdfWriter
import argparse
import os

def parse_ranges(range_str):
    """Parse a string like "1-3,4-7,8-10" into a list of (start, end) tuples."""
    ranges = []
    for part in range_str.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_str, end_str = part.split("-", 1)
            start, end = int(start_str), int(end_str)
        else:
            # A single page number, e.g. "5"
            start = end = int(part)
        ranges.append((start, end))
    return ranges


def split_pdf(input_pdf, output_folder, split_ranges):
    """Split a PDF into separate files based on the given page ranges."""
    os.makedirs(output_folder, exist_ok=True)

    reader = PdfReader(input_pdf)
    total_pages = len(reader.pages)
    print(f"Number of pages: {total_pages}")

    for idx, (start, end) in enumerate(split_ranges, start=1):
        # Clamp the range to valid page numbers
        start = max(1, start)
        end = min(total_pages, end)
        if start > end:
            print(f"⚠️  Skipping invalid range: ({start}, {end})")
            continue

        writer = PdfWriter()
        for page_num in range(start, end + 1):
            writer.add_page(reader.pages[page_num - 1])

        output_filename = f"document_part_{idx}_pages_{start}-{end}.pdf"
        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"📄 Created {output_filename} (pages {start}-{end})")

    print("✅ PDF split into custom page ranges successfully!")


def main():
    parser = argparse.ArgumentParser(
        description="Split a PDF into multiple files at variable page ranges."
    )
    parser.add_argument(
        "-i", "--input",
        default="data/input.pdf",
        help="Path to the input PDF file (default: data/input.pdf)",
    )
    parser.add_argument(
        "-o", "--output",
        default="data/split_output",
        help="Output folder for the split files (default: data/split_output)",
    )
    parser.add_argument(
        "-r", "--ranges",
        required=True,
        help='Page ranges to split at, e.g. "1-3,4-7,8-10" or "1-5,6"',
    )
    args = parser.parse_args()

    split_ranges = parse_ranges(args.ranges)
    split_pdf(args.input, args.output, split_ranges)


if __name__ == "__main__":
    main()