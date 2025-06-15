import db

def add_announcement(user_id, title, download_link, description, intented_price, age_restriction, classes):
    sql_query = """INSERT INTO Announcements (user_id, title, download_link, about, intented_price, intented_age_restriction)
                   VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql_query, [user_id, title, download_link, description, intented_price, age_restriction])

    announcement_id = db.last_insert_id()

    sql_query = "INSERT INTO Announcement_classes (announcement_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql_query, [announcement_id, title, value])

def get_announcements():
    sql_query = """SELECT Announcement.id,
                          Announcement.user_id,
                          Announcement.title,
                          Announcement.created_at,
                          Users.username
                   FROM Announcements AS Announcement
                   INNER JOIN Users
                   ON Announcement.user_id = Users.id
                   ORDER BY Announcement.id DESC"""
    return db.query(sql_query)

def get_one_announcement_classes(announcement_id):
    sql_query = """SELECT Announcement_classes.title AS title,
                          Announcement_classes.value AS value
                   FROM Announcement_classes
                   WHERE Announcement_classes.announcement_id = ?"""
    result = db.query(sql_query, [announcement_id])

    classes = {}
    for title, value in result:
        if title not in classes:
            classes[title] = []
        classes[title].append(value)

    lengths = {}
    for title, values in classes.items():
        lengths[title] = len(values)
    return (classes, lengths)

def get_announcement(announcement_id):
    sql_query = """SELECT Announcement.id,
                          Announcement.user_id,
                          Announcement.title,
                          Announcement.about,
                          Announcement.intented_price,
                          Announcement.intented_age_restriction,
                          Announcement.download_link,
                          Announcement.created_at,
                          Announcement.updated_at,
                          Users.username
                   FROM Announcements AS Announcement
                   INNER JOIN Users
                   ON Announcement.user_id = Users.id AND Announcement.id = ?"""
    result = db.query(sql_query, [announcement_id])
    return result[0] if result else None

def update_announcement(announcement_id, title, download_link, description, intented_price, age_restriction, classes):
    sql_query = """UPDATE Announcements
                   SET title = ?,
                       download_link = ?,
                       about = ?,
                       intented_price = ?,
                       intented_age_restriction = ?,
                       updated_at = (datetime('now', 'localtime'))
                   WHERE id = ?"""
    db.execute(sql_query, [title, download_link, description, intented_price, age_restriction, announcement_id])

    sql_query = """DELETE FROM Announcement_classes
                   WHERE announcement_id = ?"""
    db.execute(sql_query, [announcement_id])

    sql_query = "INSERT INTO Announcement_classes (announcement_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql_query, [announcement_id, title, value])

def remove_announcement(announcement_id):
    sql_query = """DELETE FROM Announcement_classes
                    WHERE announcement_id = ?"""
    db.execute(sql_query, [announcement_id])

    sql_query = """DELETE FROM Comments
                    WHERE announcement_id = ?"""
    db.execute(sql_query, [announcement_id])

    sql_query = """DELETE FROM Announcements
                   WHERE id = ?"""
    db.execute(sql_query, [announcement_id])

def search_announcements(search):
    sql_query = """SELECT Announcement.id,
                          Announcement.title,
                          Announcement.created_at,
                          Users.username
                   FROM Announcements AS Announcement
                   INNER JOIN Users
                   ON Announcement.user_id = Users.id
                   WHERE Announcement.title LIKE ? OR Announcement.about LIKE ?
                   ORDER BY Announcement.id DESC"""
    return db.query(sql_query, ["%" + search + "%", "%" + search + "%"])

def get_class_types(title):
    sql_query = """SELECT Class_types.type AS type
                   FROM Class_types
                   WHERE Class_types.class_title = ?"""
    return db.query(sql_query, [title])

def get_announcement_classes():
    sql_query = """SELECT Classes.title AS title,
                          Classes.value AS value
                   FROM Classes
                   ORDER BY Classes.id"""
    result = db.query(sql_query)

    classes = {}
    class_types = {}
    for title, value in result:
        if title not in classes:
            classes[title] = []
            class_types[title] = get_class_types(title)[0]["type"]
        classes[title].append(value)
    return classes, class_types

def add_comment(announcement_id, user_id, comment):
    sql_query = """INSERT INTO Comments (announcement_id, user_id, comment)
                   VALUES (?, ?, ?)"""
    db.execute(sql_query, [announcement_id, user_id, comment])

def get_comments(announcement_id):
    sql_query = """SELECT Comments.id,
                          Comments.user_id,
                          Comments.comment,
                          Comments.created_at,
                          Comments.updated_at,
                          Users.username AS username,
                          Users.id AS user_id
                   FROM Comments
                   INNER JOIN Users
                   ON Comments.user_id = Users.id AND Comments.announcement_id = ?
                   ORDER BY Comments.created_at DESC"""
    return db.query(sql_query, [announcement_id])

def get_comment(comment_id):
    sql_query = """SELECT Comments.id,
                          Comments.user_id,
                          Comments.comment
                   FROM Comments
                   WHERE Comments.id = ?"""
    result = db.query(sql_query, [comment_id])
    return result[0] if result else None

def update_comment(comment_id, comment):
    sql_query = """UPDATE Comments
                   SET comment = ?,
                       updated_at = (datetime('now', 'localtime'))
                   WHERE id = ?"""
    db.execute(sql_query, [comment, comment_id])

def remove_comment(comment_id):
    sql_query = """DELETE FROM Comments
                   WHERE id = ?"""
    db.execute(sql_query, [comment_id])
