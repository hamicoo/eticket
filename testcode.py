# This gist contains a direct connection to a local PostgreSQL database
# called "suppliers" where the username and password parameters are "postgres"

# This code is adapted from the tutorial hosted below:
# http://www.postgresqltutorial.com/postgresql-python/connect/

import psycopg2

# Establish a connection to the database by creating a cursor object
# The PostgreSQL server must be accessed through the PostgreSQL APP or Terminal Shell

# conn = psycopg2.connect("dbname=suppliers port=5432 user=postgres password=postgres")

# Or:
conn = psycopg2.connect(host="localhost", port = 5432, database="suppliers", user="postgres", password="123")
cur = conn.cursor()

import psycopg2
import psycopg2.extras
cur = conn.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
cur.execute("SELECT * from review")
res = cur.fetchone()
res.key1
res.key2


cur.execute("""SELECT * FROM vendors""")
query_results = cur.fetchall()
print(query_results)

# Close the cursor and connection to so the server can allocate
# bandwidth to other requests
cur.close()
conn.close()