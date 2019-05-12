from typing import Union, List
import re


def format_string(string: str, re_format: Union[List[str], str] = r'(.*)', re_to: str = r'\1') -> str:
    re_from = re_format
    if "list" in str(type(re_format)):
        if len(re_format) > 0:
            re_from = re_format[0]
        if len(re_format) > 1:
            re_to = re_format[1]

    try:
        string = re.sub(re_from, re_to, string)
    finally:
        return string


if __name__ == '__main__':
    s = format_string('ciao sono alex')
    print(s)
