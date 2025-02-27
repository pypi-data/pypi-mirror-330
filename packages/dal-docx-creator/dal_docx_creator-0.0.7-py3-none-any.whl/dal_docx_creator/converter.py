from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileExtension
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.programming.validator.parameter import ParameterValidator
from typing import Union

import os
import comtypes.client


def docx_to_pdf(
    docx_filename: str,
    output_filename: Union[str, None] = None
):
    """
    Convert the 'docx_filename' input file to a PDF
    file with the given 'output_filename' file name.

    This method needs the input file available to be
    opened and saved as PDF and can take a while to
    do it.
    """
    ParameterValidator.validate_mandatory_string('docx_filename', docx_filename, do_accept_empty = False)

    if not FileValidator.file_exists(docx_filename):
        raise Exception('The provided "docx_filename" file does not exist.')

    output_filename = Output.get_filename(output_filename, FileExtension.PDF)
    
    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(os.path.abspath(docx_filename))
    # 17 is the WordFormatPDF
    doc.SaveAs(os.path.abspath(output_filename), FileFormat = 17)
    doc.Close()
    word.Quit()