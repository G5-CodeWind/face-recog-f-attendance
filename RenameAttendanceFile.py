from datetime import datetime

now = datetime.now()  # current date and time

year = now.strftime("%Y")

month = now.strftime("%m")

day = now.strftime("%d")

date_time = now.strftime("%m/%d/%Y")

name = date_time

attendance = name.replace('/','-')

#print(attendance)

filename = "%s.csv" % attendance

open(attendance+'.csv', 'w')
