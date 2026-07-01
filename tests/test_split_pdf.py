import os

import pytest
from PyPDF2 import PdfReader, PdfWriter

from main import parse_ranges, split_pdf


def make_pdf(path, num_pages):
    """Create a PDF with the given number of blank pages."""
    writer = PdfWriter()
    for _ in range(num_pages):
        writer.add_blank_page(width=200, height=200)
    with open(path, "wb") as f:
        writer.write(f)


# ---------- parse_ranges tests ----------

def test_parse_ranges_basic():
    assert parse_ranges("1-3,4-7,8-10") == [(1, 3), (4, 7), (8, 10)]


def test_parse_ranges_single_pages():
    assert parse_ranges("1,2,5") == [(1, 1), (2, 2), (5, 5)]


def test_parse_ranges_mixed():
    assert parse_ranges("1-3,4,5-8") == [(1, 3), (4, 4), (5, 8)]


def test_parse_ranges_ignores_whitespace_and_empty():
    assert parse_ranges(" 1-3 , , 4 ") == [(1, 3), (4, 4)]


# ---------- split_pdf tests ----------

def test_split_pdf_creates_expected_files(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_dir = tmp_path / "out"
    make_pdf(input_pdf, 10)

    split_pdf(str(input_pdf), str(output_dir), [(1, 3), (4, 7), (8, 10)])

    files = sorted(os.listdir(output_dir))
    assert files == [
        "document_part_1_pages_1-3.pdf",
        "document_part_2_pages_4-7.pdf",
        "document_part_3_pages_8-10.pdf",
    ]


def test_split_pdf_page_counts(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_dir = tmp_path / "out"
    make_pdf(input_pdf, 10)

    split_pdf(str(input_pdf), str(output_dir), [(1, 3), (4, 7), (8, 10)])

    assert len(PdfReader(str(output_dir / "document_part_1_pages_1-3.pdf")).pages) == 3
    assert len(PdfReader(str(output_dir / "document_part_2_pages_4-7.pdf")).pages) == 4
    assert len(PdfReader(str(output_dir / "document_part_3_pages_8-10.pdf")).pages) == 3


def test_split_pdf_clamps_to_valid_pages(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_dir = tmp_path / "out"
    make_pdf(input_pdf, 5)

    # End exceeds total pages -> clamped to 5
    split_pdf(str(input_pdf), str(output_dir), [(1, 100)])

    files = os.listdir(output_dir)
    assert files == ["document_part_1_pages_1-5.pdf"]
    assert len(PdfReader(str(output_dir / files[0])).pages) == 5


def test_split_pdf_skips_invalid_range(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_dir = tmp_path / "out"
    make_pdf(input_pdf, 5)

    # start > end after clamping -> skipped, no file produced
    split_pdf(str(input_pdf), str(output_dir), [(10, 12)])

    assert os.listdir(output_dir) == []
