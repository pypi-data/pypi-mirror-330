from pathlib import Path

from ragloader.indexing import File, Document


class ParsedFile(File):
    """This class provides an abstraction for a parsed file."""

    def __init__(self,
                 file_path: Path | str,
                 file_content: str
        ):
        super().__init__(file_path)

        self.file_content: str = file_content

    def __repr__(self):
        return f"ParsedFile(name={self.file_name})"


class ParsedDocument(Document):
    """This class provides an abstraction for a parsed document."""

    def __init__(self, document: Document):
        super().__init__(document.document_path, document.group)

        self.document_content: str = ""
        self.parsed_files: list[ParsedFile] = []

    def add_parsed_file(self, parsed_file: ParsedFile):
        """Adds a parsed file to the list of parsed files for a document."""
        self.document_content += ("\n\n" + parsed_file.file_content)
        self.parsed_files.append(parsed_file)

    def __repr__(self):
        parsed_files_repr: str = ", ".join(repr(parsed_file) for parsed_file in self.parsed_files)
        return (f"ParsedDocument(n_files={len(self.parsed_files)},"
                f" parsed_files=[\n\t\t\t\t{parsed_files_repr}\n\t\t\t])")
