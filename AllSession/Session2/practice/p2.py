import re
emails = ["hung.ngo@gmail.com", "teacher@fpt.edu.vn", "user123@yahoo.com"]
Pattern2 = r'@([\w\.-]+)'
domains = [re.findall(Pattern2, email)[0] for email in emails]
print('All the final parts of the mails are: ', domains)