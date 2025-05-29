import db

def add_announcement(user_id, title, download_link, description, intented_price, age_restriction):
    sql_query = """INSERT INTO Announcements (user_id, title, download_link, about, intented_price, intented_age_restriction)
                   VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql_query, [user_id, title, download_link, description, intented_price, age_restriction])

def get_announcements():
    sql_query = """SELECT Announcement.id,
                          Announcement.title,
                          Announcement.created_at,
                          Users.username
                   FROM Announcements As Announcement
                   INNER JOIN Users
                   ON Announcement.user_id = Users.id
                   ORDER BY Announcement.id DESC"""
    return db.query(sql_query)

def get_announcement(announcement_id):
    sql_query = """SELECT Announcement.id,
                          Announcement.title,
                          Announcement.about,
                          Announcement.intented_price,
                          Announcement.intented_age_restriction,
                          Announcement.download_link,
                          Announcement.created_at,
                          Announcement.updated_at,
                          Users.username
                   FROM Announcements As Announcement
                   INNER JOIN Users
                   ON Announcement.user_id = Users.id AND Announcement.id = ?"""
    return db.query(sql_query, [announcement_id])[0]

