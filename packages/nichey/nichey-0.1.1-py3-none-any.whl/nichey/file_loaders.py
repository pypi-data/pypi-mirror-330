# Would like to use auto file loader, but it likes to hide bugs!
from unstructured.partition.xlsx import partition_xlsx
from unstructured.partition.docx import partition_docx
from unstructured.partition.doc import partition_doc
from unstructured.partition.html import partition_html
from unstructured.partition.epub import partition_epub
from unstructured.partition.odt import partition_odt
from unstructured.partition.ppt import partition_ppt
from unstructured.partition.pptx import partition_pptx
from unstructured.partition.tsv import partition_tsv
import re

import warnings
with warnings.catch_warnings():  # This rigamarol prevents these stupid SwigPy warnings caused by pymupdf
    warnings.simplefilter("ignore")
    import fitz


# An iterable of RawChunks is returned by load_and_split
class RawChunk():
    page_content: str
    metadata: dict
    def __init__(self, page_content, metadata={}):
        self.page_content = page_content
        self.metadata = metadata

"""

Takes string and returns list of strings

The algorithm:
- Split on the first separator
- Combine chunks in order if possible (i.e., resulting chunk isn't too big)
- Any chunks that are too big get the recursive split called on them again

Why a class instead of a function? Mostly just to match langchain behavior, or to specify args just once before passing same parametrized text splitter elsewhere, like in a retriever.

"""
class TextSplitter():
    # max_chunk_size is in units determined by length function; by default, characters.
    def __init__(self, max_chunk_size=2048, length_function=len, chunk_overlap=0):
        self.max_chunk_size = max_chunk_size
        self.length_function=length_function
        self.chunk_overlap = 0  # NOTE: doesn't yet support anything > 0 (in here for legacy langchain reasons)

    def split_text(self, txt, separators=None):

        DEFAULT_SEPARATORS = [  # the point of the weird character codes is to support multiple languages. Recommended here: https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/recursive_text_splitter/
            "\n\n",
            "\n",
            "\t",
            " ",
            ".",
            ",",
            "\u200b",  # Zero-width space
            "\uff0c",  # Fullwidth comma
            "\u3001",  # Ideographic comma
            "\uff0e",  # Fullwidth full stop
            "\u3002",  # Ideographic full stop
        ]
        separators = separators if separators else DEFAULT_SEPARATORS

        def recursive_split(text, seps):
            max_chunks = []  # Holds chunks of their maximum size - not necessarily under max_chunk_size yet, though they'll never get bigger.

            sep = ""
            if not len(seps):
                # Means that some chunk is too big even after exhausting separators
                # Now just need to go in and dice it up without regard to separators
                splitsville = [text[:self.max_chunk_size], text[self.max_chunk_size:]]
            else:
                sep = seps[0]
                # Split on separator 
                splitsville = text.split(sep)

            # Max-combine chunks in order
            for split in splitsville:
                if not split:  # blanks are not allowed
                    continue
                if not len(max_chunks):  # first split creates new chunk 
                    max_chunks.append(split)
                elif self.length_function(max_chunks[len(max_chunks) - 1] + sep + split) < self.max_chunk_size:  # if we can add the current split to the previous without overflow, do it
                    max_chunks[len(max_chunks) - 1] += sep + split
                else:  # Otherwise, create a new chunk
                    max_chunks.append(split)

            # On any max_chunks that are not under max_chunk_size, split it again.
            final_chunks = []
            for max_chunk in max_chunks:
                if self.length_function(max_chunk) > self.max_chunk_size:
                    new_chunks = recursive_split(max_chunk, seps[1:])
                    final_chunks.extend(new_chunks)
                else:
                    final_chunks.append(max_chunk)
            
            return final_chunks
        
        if self.length_function(txt) <= self.max_chunk_size:
            if not txt:
                return []
            return [txt]
        
        return recursive_split(txt, separators)


class FileLoader():
    def __init__(self, fname):
        self.fname = fname

    # Returns iterable of RawChunks
    def load_and_split(self, text_splitter: TextSplitter):
        raise NotImplementedError("Function load_and_split not implemented for some file loader.")


# "Unstructured" being the name of a package
class UnstructuredLoader(FileLoader):
    def load_and_split(self, text_splitter):
        # This corresponds to mode=single in langchain
        elements = self._get_elements()
        total = "\n\n".join([str(el) for el in elements])
        splitsville = text_splitter.split_text(total)
        for split in splitsville:
            yield RawChunk(split, {})
    
    # For different file types, returns iterable
    def _get_elements(self):
        raise NotImplementedError("Function _get_elements not implemented for some file loader.")


class ExcelLoader(UnstructuredLoader):
    def _get_elements(self):
        return partition_xlsx(filename=self.fname)


class DocxLoader(UnstructuredLoader):
    def _get_elements(self):
        return partition_docx(filename=self.fname, infer_table_structure=True)


class HTMLLoader(UnstructuredLoader):
    def _get_elements(self):
        try:
            return partition_html(filename=self.fname)
        except AttributeError:
            # This ridiculous bug is from unstructured; it breaks down if it sees "<?xml ... ?>"
            existing = ""
            with open(self.fname, "r") as fhand:
                existing = fhand.read()
            new_str = re.sub(r'<\?xml[^?]*\?>', '', existing)
            with open(self.fname, 'w') as fhand:
                fhand.write(new_str)
            return partition_html(filename=self.fname)
    

class EpubLoader(UnstructuredLoader):
    def _get_elements(self):
        return partition_epub(filename=self.fname)


class OdtLoader(UnstructuredLoader):
    def _get_elements(self):
        return partition_odt(filename=self.fname)


class DocLoader(UnstructuredLoader):
    def _get_elements(self):
        return partition_doc(filename=self.fname)


class PptLoader(UnstructuredLoader):
    def _get_elements(self):
        return partition_ppt(filename=self.fname)


class PptxLoader(UnstructuredLoader):
    def _get_elements(self):
        return partition_pptx(filename=self.fname)


class TsvLoader(UnstructuredLoader):
    def _get_elements(self):
        return partition_tsv(filename=self.fname)


# Not using unstructured for CSV because it has a littany of bugs.
class CsvLoader(UnstructuredLoader):
    def load_and_split(self, text_splitter: TextSplitter):
        with open(self.fname, 'r') as file:
            original_contents = file.read()
        splitsville = text_splitter.split_text(original_contents)
        for split in splitsville:
            yield RawChunk(split, {})


# Divides by page, and then splits within each page.
class PdfLoader(FileLoader):
    def load_and_split(self, text_splitter: TextSplitter):
        doc = fitz.open(self.fname)
        for i, page in enumerate(doc): # iterate the document pages
            text = page.get_text()  # In the future, we should get images as well.
            split_text = text_splitter.split_text(text)
            for split in split_text:
                yield RawChunk(split, {'page': i})


class JsonLoader(FileLoader):
    def load_and_split(self, text_splitter: TextSplitter):
        with open(self.fname, 'r') as file:
            original_contents = file.read()
        splitsville = text_splitter.split_text(original_contents)
        for split in splitsville:
            yield RawChunk(split, {})


CODE_SUPPORTS = ['java', 'py', 'cpp', 'c', 'cs', 'js', 'ts', 'rs', 'swift', 'kt', 'm', 'scala', 'lua', 'sh', 'pl', 'sql', 'r']
class CodeLoader(FileLoader):
    def load_and_split(self, text_splitter: TextSplitter):
        all_code = ""
        with open(self.fname, 'r') as fhand:
            all_code = fhand.read()
        # TODO: use special text splitter for code.
        splits = text_splitter.split_text(all_code)
        for split in splits:
            yield RawChunk(page_content=split, metadata={})


class TextLoader(FileLoader):
    def load_and_split(self, text_splitter):
        content = ""
        with open(self.fname, 'r') as file:
            content = file.read()
        splitsville = text_splitter.split_text(content)
        for split in splitsville:
            yield RawChunk(split, {})


class MarkdownLoader(FileLoader):
    def load_and_split(self, text_splitter):
        content = ""
        with open(self.fname, 'r') as file:
            content = file.read()
        splitsville = text_splitter.split_text(content, separators=['\n\n', '#', '##', '###', '\n', '.', ','])
        for split in splitsville:
            yield RawChunk(split, {})


DISALLOWED_DOC_EXTENTIONS = ['pages', 'rtf', 'epub', 'key', 'mp4', 'mov', 'mpeg', 'flv', 'ico']
def get_loader(filetype, path) -> FileLoader:
    if filetype == 'docx':
        return DocxLoader(path)
    if filetype == 'doc':
        return DocLoader(path)
    elif filetype == 'xlsx': 
        return ExcelLoader(path)
    elif filetype in ['html']:
        return HTMLLoader(path)
    elif filetype == 'json':
        return JsonLoader(path)
    elif filetype == 'pdf':
        return PdfLoader(path)
    elif filetype == 'txt':
        return TextLoader(path)
    elif filetype == 'ppt':
        return PptLoader(path)
    elif filetype == 'pptx':
        return PptxLoader(path)
    elif filetype == 'md':
        return MarkdownLoader(path)
    elif filetype == 'odt':
        return OdtLoader(path)
    elif filetype == 'tsv':
        return TsvLoader(path)
    elif filetype == 'csv':
        return CsvLoader(path)
    elif filetype in CODE_SUPPORTS:
        return CodeLoader(path)
    
    # Note on missing file types: EPUB and RTF
    # Both seemed to fail due to missing pandoc installation

    return None
