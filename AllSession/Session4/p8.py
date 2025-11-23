
import re

expr ="9**(1/2)"
compiled_expr = compile(expr,'<string>','eval')
result = eval(compiled_expr)
print("Result: ",result)