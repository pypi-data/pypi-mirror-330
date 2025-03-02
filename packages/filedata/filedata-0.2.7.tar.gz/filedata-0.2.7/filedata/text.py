import re

blank_reg = re.compile(r'[\r\f\t\v\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff]+')
line_break_reg = re.compile(r'[\n]{2,}')
word_blank_reg = re.compile(r'([\u4E00-\u9FA5\n])[ ]+([\u4E00-\u9FA5\n])')


def normalize_file_content(content: str, limit: int = None) -> str:
    content = blank_reg.sub(' ', content)

    content = word_blank_reg.sub(r'\1\2', content)
    content = word_blank_reg.sub(r'\1\2', content)

    content = line_break_reg.sub('\n\n', content)

    if limit is not None and limit > 0:
        if len(content) > limit:
            content = content[:limit]
    return content
