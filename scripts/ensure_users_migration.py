#!/usr/bin/env python3
import sqlite3, os, datetime, sys
p = os.path.join(os.getcwd(), 'db.sqlite3')
print('DB PATH:', p)
if not os.path.exists(p):
    print('ERROR: db.sqlite3 not found')
    sys.exit(1)
conn = sqlite3.connect(p)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='django_migrations'")
if not cur.fetchone():
    print('ERROR: django_migrations table not found')
    conn.close()
    sys.exit(1)
cur.execute("SELECT COUNT(1) FROM django_migrations WHERE app=? AND name=?", ('users','0001_initial'))
count = cur.fetchone()[0]
if count == 0:
    cur.execute('INSERT INTO django_migrations(app,name,applied) VALUES (?,?,?)', ('users','0001_initial', datetime.datetime.now().isoformat()))
    conn.commit()
    print('Inserted users.0001_initial into django_migrations')
else:
    print('users.0001_initial already present in django_migrations')
conn.close()
