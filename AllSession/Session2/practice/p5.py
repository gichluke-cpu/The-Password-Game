import re

pattern1 = r'\b[A-ZÀ-Ỹ][a-zà-ỹ]*\b'
text1 = r"Hôm nay trời Đẹp. Tôi sẽ Đi học Python ở Aptech."

matches = re.findall(pattern1, text1) 
if matches:
    print('capital words are: ', matches)


emails = ["hung.ngo@gmail.com", "teacher@fpt.edu.vn", "user123@yahoo.com"]
Pattern2 = r'@([\w\.-]+)'
domains = [re.findall(Pattern2, email)[0] for email in emails]
print('All the final parts of the mails are: ', domains)


text3 = r"Hôm nay học #Python, mai học #Regex và #MachineLearning"
pattern3 = r'#([\w\.-]+)'
hashtag = re.findall(pattern3,text3)
if hashtag:
    print('All the hashtags are: ', hashtag)


pattern = r'^(0[1-9]|[12][0-9]|3[01])/' \
              r'(0[1-9]|1[0-2])/' \
              r'(19[0-9]{2}|20[0-9]{2})$'

date_list = ['28/09/2025', '31/04/2025', '99/99/9999']


valid_dates = [d for d in date_list if re.fullmatch(pattern, d)]
valid_dates.sort()

print('All the valid dates are: ', valid_dates)