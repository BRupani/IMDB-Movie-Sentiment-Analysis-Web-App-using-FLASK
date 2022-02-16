import sqlite3
conn = sqlite3.connect('database.db')
print ("Opened database successfully")
conn.execute('CREATE TABLE moviereviewss (Reviewss TEXT, my_predictions TEXT)')
print ("Table created successfully")
conn.close()