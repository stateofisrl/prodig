import sqlite3, datetime, os

db_path = os.path.join(os.getcwd(), 'db.sqlite3')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
# Insert users 0001_initial if not exists
cur.execute("SELECT COUNT(1) FROM sqlite_master WHERE type='table' AND name='django_migrations'")
if cur.fetchone()[0] == 0:
    print('django_migrations table not found, aborting')
else:
    cur.execute("SELECT COUNT(1) FROM django_migrations WHERE app='users' AND name='0001_initial'")
    if cur.fetchone()[0] == 0:
        cur.execute('INSERT INTO django_migrations(app,name,applied) VALUES (?,?,?)', ('users','0001_initial', datetime.datetime.now().isoformat()))
        conn.commit()
        print('Inserted users 0001_initial into django_migrations')
    else:
        print('users 0001_initial already present')
conn.close()
