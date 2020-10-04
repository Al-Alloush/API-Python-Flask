import connectionSQLite as cs



conn = cs.Connect()
usertable = "CREATE TABLE IF NOT EXISTS users (id text PRIMARY KEY, username text, password text)"
conn.execute(usertable)
conn.close()