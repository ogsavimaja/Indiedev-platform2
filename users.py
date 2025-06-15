import db

def get_user(User_id):
    sql_query = """SELECT User.id,
                          User.username,
                          User.created_at
                   FROM Users As User
                   WHERE User.id = ?"""
    result = db.query(sql_query, [User_id])
    return result[0] if result else None

def get_user_announcements(User_id):
    sql_query = """SELECT Announcement.id,
                          Announcement.title,
                          Announcement.created_at
                   FROM Announcements As Announcement
                   WHERE Announcement.user_id = ?
                   ORDER BY Announcement.id DESC"""
    return db.query(sql_query, [User_id])

def get_user_comments(User_id):
    sql_query = """SELECT Comment.id,
                          Comment.comment,
                          Comment.created_at,
                          Announcement.title AS announcement_title,
                          Announcement.id AS announcement_id
                   FROM Comments As Comment
                   INNER JOIN Announcements As Announcement
                   ON Comment.announcement_id = Announcement.id
                   WHERE Comment.user_id = ?
                   ORDER BY Comment.id DESC"""
    return db.query(sql_query, [User_id])
