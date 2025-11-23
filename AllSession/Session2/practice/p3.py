import re
text = r"Hôm nay học #Python, mai học #Regex và #MachineLearning"
pattern = r'#([\w\.-]+)'
hashtag = re.findall(pattern,text)
if hashtag:
    print('All the hashtags are: ', hashtag)
    