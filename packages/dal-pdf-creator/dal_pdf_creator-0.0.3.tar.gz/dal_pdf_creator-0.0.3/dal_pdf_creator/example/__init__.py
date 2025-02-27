"""
Module to hold some inspirational examples.

Tutorial here:
- https://py-pdf.github.io/fpdf2/Tutorial.html
"""
from dal_pdf_creator.example.book import PdfBookChapter, PdfBook
from fpdf import FPDF


__all__ = [
    'PdfExample'
]

class PdfExample:
    """
    Class to wrap some example of PFDs.
    """

    @staticmethod
    def test_one():
        fpdf = FPDF()

        PdfBook(
            title = 'Inventado ahora mismo',
            author = 'Yo, por supuesto',
            chapters = [
                PdfBookChapter(
                    title = 'Capítulo JAJA',
                    number = 1,
                    text = 'Capítulo inventado, ya está...',
                    fpdf = fpdf
                ),
                PdfBookChapter(
                    title = 'Capítulo JIJIJSAD',
                    number = 2,
                    text = 'Capítulo inventado, pero una chispa más largo que el anterior',
                    fpdf = fpdf
                )
            ],
            fpdf = fpdf
        ).write('test_book.pdf')