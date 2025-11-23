import time
import timeit
from datetime import datetime
import re

print('===PYTHON CODE RUN TIME MEASURE===')
print('1.Timeit | 2.datetime | 3.time')

order = input('PLEASE SELECT YOUR MODULE OF CHOICE: ')
        
file1 = input('PLEASE TYPE IN YOUR FILE: ')
fileinserter = re.sub(r'"','',file1)
file = re.sub(r'\\','/',fileinserter)  #CHO PHÉP KÍ TỰ "\"




try:
        with open(file, 'r', encoding='utf-8') as f:
                code_content = f.read()
                

except FileNotFoundError:
            print("❌ Something Went Wrong with the File! ❌")
            exit()

                



if order == '1':
        print('Measuring with Timeit...')
        t = timeit.timeit(stmt= code_content, number = 1000)
        print(f'average time after 1000 runs is: {t:.6f} seconds')

elif order == '2':
        print('Measuring with Datetime...')
        start = datetime.now()
        exec(code_content)
        end = datetime.now()
        print(f"Execution time: {end-start}")
elif order == '3':
        print('Measuring with time...')
        counterstart = time.perf_counter()
        exec(code_content)
        counterend = time.perf_counter()
        print(f'execution time is {counterend - counterstart}')
else:
        print(' ❌ Error, Wrong syntax! ❌')