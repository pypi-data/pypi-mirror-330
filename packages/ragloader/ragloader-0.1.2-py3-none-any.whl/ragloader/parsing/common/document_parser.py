from ragloader.conf import Config
from ragloader.indexing import Document, File
from ragloader.parsing import ParsedFile, ParsedDocument
from ragloader.parsing import BaseFileParser
from ragloader.parsing.mapper import FileParsersMapper


class DocumentParser:
    """This class is used to parse a document (extract its content)."""

    def __init__(self, config: Config):
        self.extensions_parsers: dict = config["pipeline_stages"]["parsing"]["parsers"]
        self.extensions_parsers_instances: dict = dict().fromkeys(self.extensions_parsers.keys())

    def parse(self, document: Document) -> ParsedDocument | None:
        """
        This method converts a `Document` object to a `ParsedDocument` object.
        It iterates over all files in the document and combines all `ParsedFile` objects together.
        """
        files: list[File] = document.files

        parsed_document: ParsedDocument = ParsedDocument(document)

        for file in files:
            parser_name: str = self.extensions_parsers.get(file.extension)
            if parser_name is None:
                raise Exception(f"No parser available for extension: {file.extension}")

            if self.extensions_parsers_instances[file.extension] is not None:
                parser: BaseFileParser = self.extensions_parsers_instances[file.extension]
            else:
                try:
                    parser_class: type = FileParsersMapper[parser_name].value
                except KeyError:
                    raise NotImplementedError(f"Parser {parser_name} not implemented.")

                parser: BaseFileParser = parser_class()
                self.extensions_parsers_instances[file.extension]: BaseFileParser = parser

            parsed_file: ParsedFile = parser.parse(file)
            parsed_document.add_parsed_file(parsed_file)

        return parsed_document

    def __repr__(self):
        return f"DocumentParser(extensions_parsers={self.extensions_parsers})"
