import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM Users")
db.execute("DELETE FROM Comments")
db.execute("DELETE FROM Announcements")

user_count = 1000
announcement_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("""INSERT INTO Users (username, salt, hashed_password) 
               VALUES (?, ?, ?)""",
               ["user" + str(i), "salt" + str(i), "hashed_password" + str(i)])

for i in range(1, announcement_count + 1):
    db.execute("""INSERT INTO Announcements (user_id, title, about) 
               VALUES (?, ?, ?)""",
               ["thread" + str(i), "title" + str(i), "description" + str(i)])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    announcement_id = random.randint(1, announcement_count)
    db.execute("""INSERT INTO Comments (user_id, announcement_id, comment)
                  VALUES (?, ?, ?)""",
               [user_id, announcement_id, "message" + str(i)])

db.commit()
db.close()
