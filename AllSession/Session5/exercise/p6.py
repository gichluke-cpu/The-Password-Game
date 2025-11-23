import re
pattern = re.compile(r"""
\d{4} #hello
    -
\d{2} #Hello
    -
\d{2}
                     """,re.X)

date = input('Please type in date (YYYY-MM-DD): ')
match = pattern.search(date)
print("valid date!:", match.group())