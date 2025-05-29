import db

def get_user(User_id):
    sql_query = """SELECT User.id,
                          User.username
                   FROM Users As User
                   WHERE User.id = ?"""
    result = db.query(sql_query, [User_id])
    return result[0] if result else None

def get_user_announcements(User_id):
    sql_query = """SELECT COUNT(*) AS count,
                          Announcement.id,
                          Announcement.title,
                          Announcement.created_at
                   FROM Announcements As Announcement
                   WHERE Announcement.user_id = ?
                   ORDER BY Announcement.id DESC"""
    return db.query(sql_query, [User_id])
