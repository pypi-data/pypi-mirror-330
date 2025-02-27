from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileExtension
from yta_general_utils.programming.validator.parameter import ParameterValidator
from docx.document import Document
from typing import Union

import io


class DocxCreator:
    """
    Class to simplify the creation of a DOCX.
    """

    @staticmethod
    def get_bytearray(
        docx: Document
    ) -> bytearray:
        """
        Get the 'docx' bytearray as if it was
        written to a file but without doing it.
        """
        ParameterValidator.validate_mandatory_instance_of('docx', docx, Document)

        out = io.BytesIO()
        docx.save(out)

        return out.getvalue()

    @staticmethod
    def write(
        docx: Document,
        output_filename: Union[str, None] = None
    ) -> str:
        """
        Create the provided 'docx' as a file and
        return the filename with which the file
        has been stored locally.
        """
        ParameterValidator.validate_mandatory_instance_of('docx', docx, Document)

        output_filename = Output.get_filename(output_filename, FileExtension.DOCX)
        # TODO: I could return the docx bytearray instead
        # (check 'get_bytearray' method) (?)
        docx_bytearray = docx.save(output_filename)

        return output_filename