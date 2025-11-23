import re
pattern = re.compile(r"""
\d{4} #hello
    -
\d{2} #Hello
    -
\d{2}
                     """,re.X)

match = pattern.search("Ngay: 2024-02-14")
print(match.group())