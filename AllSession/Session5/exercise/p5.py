import re
text = """Line 1
Line 2
Line 3"""
import re
text = """Line 1
Line 2
Line 3"""

lines = re.findall(r'^.*Line.*$', text, re.MULTILINE)
print(lines)