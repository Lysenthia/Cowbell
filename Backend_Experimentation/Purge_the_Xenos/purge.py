import sqlite3, hashlib
pw = input("Enter purge password: ").encode('utf-8')
password = hashlib.sha512(pw).hexdigest()
code = "1f3ee6bb8c39241cad74b6060f54d63a3cadf654cd179988bc84b0d397e8a9f90561d16b102ef30a39563e4a298f0d3b636c6c4d8e2f540f898fdfad98f6c79e"
if password == code:
    db = sqlite3.connect('database.db')
    print("Beginning db purge...")
    cursor = db.cursor()
    cursor.execute('''DELETE FROM users;''')
    db.commit()
    cursor.execute('''DELETE FROM songs;''')
    db.commit()
    cursor.close()
    db.close()
    print("Done!")
else:
    print("Error, incorrect password")