"""
A book written by chapters, based on this
tutorial:
- https://py-pdf.github.io/fpdf2/Tutorial.html#tuto-3-line-breaks-and-colors

TODO: I don't like using properties in the
way I'm using them, it could be private
methods because those are actions through
the fpdf instance.
"""
from dal_pdf_creator.creator import PdfCreator
from yta_general_utils.programming.validator.parameter import ParameterValidator
from fpdf import FPDF
from dataclasses import dataclass
from typing import Union


__all__ = [
    'PdfBookChapter',
    'PdfBook'
]

@dataclass
class PdfBookChapter:
    """
    Class to represent a chapter of a book.
    """

    def __init__(
        self,
        title: str,
        number: float,
        text: str,
        fpdf: FPDF
    ):
        ParameterValidator.validate_mandatory_string('title', title, do_accept_empty = True)
        ParameterValidator.validate_positive_number('number', number, do_include_zero = True)
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = True)
        ParameterValidator.validate_mandatory_instance_of('fpdf', fpdf, FPDF)

        self.title = title
        self.number = number
        self.text = text
        self.fpdf = fpdf

    @property
    def _title(
        self,
    ):
        # Setting font: helvetica 12
        self.fpdf.set_font("helvetica", size=12)
        # Setting background color
        self.fpdf.set_fill_color(200, 220, 255)
        # Printing chapter name:
        self.fpdf.cell(
            0,
            6,
            f"Chapter {self.number} : {self.title}",
            new_x="LMARGIN",
            new_y="NEXT",
            align="L",
            fill=True,
        )
        # Performing a line break:
        self.fpdf.ln(4)

    @property
    def _body(
        self
    ):
        # Setting font: Times 12
        self.fpdf.set_font("Times", size=12)
        # Printing justified text:
        self.fpdf.multi_cell(0, 5, self.text)
        # Performing a line break:
        self.fpdf.ln()
        # Final mention in italics:
        self.fpdf.set_font(style="I")
        self.fpdf.cell(0, 5, "(end of excerpt)")

    @property
    def output(
        self
    ):
        self.fpdf.add_page()
        # TODO: I don't like using these below as props
        self._title
        self._body

@dataclass
class PdfBook:
    """
    Class to wrap a book with different
    chapters on it.
    """

    def __init__(
        self,
        title: str,
        author: str,
        chapters: list[PdfBookChapter],
        fpdf: FPDF
    ):
        ParameterValidator.validate_mandatory_string('title', title, do_accept_empty = True)
        ParameterValidator.validate_mandatory_string('author', author, do_accept_empty = True)
        ParameterValidator.validate_mandatory_list_of_these_instances('chapters', chapters, [PdfBookChapter])
        ParameterValidator.validate_mandatory_instance_of('fpdf', fpdf, FPDF)

        self.title = title
        self.author = author
        self.chapters = chapters
        self.fpdf = fpdf

    @property
    def _header(
        self
    ):
        # Setting font: helvetica bold 15
        self.fpdf.set_font("helvetica", style="B", size=15)
        # Calculating width of title and setting cursor position:
        width = self.fpdf.get_string_width(self.title) + 6
        self.fpdf.set_x((210 - width) / 2)
        # Setting colors for frame, background and text:
        self.fpdf.set_draw_color(0, 80, 180)
        self.fpdf.set_fill_color(230, 230, 0)
        self.fpdf.set_text_color(220, 50, 50)
        # Setting thickness of the frame (1 mm)
        self.fpdf.set_line_width(1)
        # Printing title:
        self.fpdf.cell(
            width,
            9,
            self.title,
            border=1,
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
            fill=True,
        )
        # Performing a line break:
        self.fpdf.ln(10)

    @property
    def footer(
        self
    ):
        # Setting position at 1.5 cm from bottom:
        self.fpdf.set_y(-15)
        # Setting font: helvetica italic 8
        self.fpdf.set_font("helvetica", style="I", size=8)
        # Setting text color to gray:
        self.fpdf.set_text_color(128)
        # Printing page number
        self.fpdf.cell(0, 10, f"Page {self.fpdf.page_no()}", align="C")

    def write(
        self,
        output_filename: Union[str, None] = None
    ) -> str:
        # TODO: Make this write only once because I'm
        # using a previous fpdf instance if I call this
        # more than one timce
        self.fpdf.set_title(self.title)
        self.fpdf.set_author(self.author)
        for chapter in self.chapters:
            chapter.output

        return PdfCreator.create(self.fpdf, output_filename)