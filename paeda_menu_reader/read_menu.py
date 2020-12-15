from PyPDF2 import PdfFileReader
import re


def format_output(in_str):
    if '*' in in_str:
        in_str = in_str.replace('*', '')
    if ', dazu' in in_str:
        in_str = in_str.replace(', dazu', '')
    if ',' in in_str:
        in_str = in_str.replace(',', '')
    return in_str


class ReadFromMenu:

    def __init__(self, pdf_obj):
        self.pdf_str = PdfFileReader(pdf_obj).getPage(0).extractText()

    def get_lunch_list(self):
        # search
        pattern_launch = re.compile(r'Aushang\s{10,}(.*?)\s{2,}\n(.*?)\s{2,}')
        search_launch = re.finditer(pattern_launch, self.pdf_str)

        return [f'{format_output(match.group(1))} {format_output(match.group(2))}' if match.group(1) != '' else format_output(match.group(2)) for match in search_launch]

    def get_dinner_list(self):
        # search
        pattern_dinner = re.compile(r'\s*Abendbuffet\s+\n(.*[^\s+])\s')
        search_dinner = re.finditer(pattern_dinner, self.pdf_str)

        return [format_output(match.group(1)) for match in search_dinner]
