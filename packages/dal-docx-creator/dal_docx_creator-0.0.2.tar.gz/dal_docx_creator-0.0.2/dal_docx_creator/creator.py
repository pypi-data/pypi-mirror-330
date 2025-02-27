from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileExtension
from yta_general_utils.programming.validator.parameter import ParameterValidator
from docx import Document
from typing import Union


class DocxCreator:
    """
    Class to simplify the creation of a DOCX.
    """

    @staticmethod
    def create(
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
        # TODO: Is this actually returning a bytearray (?)
        docx_bytearray = docx.save(output_filename)

        return output_filename