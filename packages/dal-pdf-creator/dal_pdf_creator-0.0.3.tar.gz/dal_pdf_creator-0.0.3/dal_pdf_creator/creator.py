from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileExtension
from yta_general_utils.programming.validator.parameter import ParameterValidator
from fpdf import FPDF
from typing import Union


class PdfCreator:
    """
    Class to simplify the creation of a PDF.
    """

    @staticmethod
    def create(
        fpdf: FPDF,
        output_filename: Union[str, None] = None
    ) -> str:
        """
        Create the provided 'pdf' as a file and
        return the filename with which the file
        has been stored locally.
        """
        ParameterValidator.validate_mandatory_instance_of('fpdf', fpdf, FPDF)

        output_filename = Output.get_filename(output_filename, FileExtension.PDF)
        # TODO: I could return the pdf bytearray instead
        pdf_bytearray = fpdf.output(output_filename)

        return output_filename