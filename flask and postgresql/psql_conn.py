import psycopg2

conn = psycopg2.connect(database="flask_db",password="root",user='postgres',host="localhost",port='5432')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS courses (id serial PRIMARY KEY,name VARCHAR(100),fees integer, duration integer);''')

# cur.execute('''INSERT INTO courses(name,fees,duration) VALUES ('java','20000','12'),('python','25000','14');''')

conn.commit()
cur.close()
conn.close()


