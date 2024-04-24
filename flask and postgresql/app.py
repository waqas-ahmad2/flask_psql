from flask import Flask,render_template,redirect,session,request,url_for,flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'the random string'


def db_conn():
    conn = psycopg2.connect(database='flask_db',host='localhost',user='postgres',password='root',port='5432')
    return conn

@app.route('/')
def index():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM courses ORDER BY ID;''')
    data=cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html',data=data)

@app.route('/create',methods=['POST'])
def create():
    conn = db_conn()
    cur = conn.cursor()

    # getting values from the form
    name = request.form.get('course_name')
    fees = request.form.get('fees')
    duration = request.form.get('duration')

    cur.execute(f"INSERT INTO courses (name,fees,duration) VALUES ('{name}','{fees}','{duration}')")
    conn.commit()
    flash('Course Added Successfully')
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    if request.method == 'POST':
        conn = db_conn()
        cur = conn.cursor()

        u_name = request.form.get('u_course_name')
        u_fees = request.form.get('u_fees')
        u_duration = request.form.get('u_duration')
        cur.execute(f"UPDATE courses SET name='{u_name}', fees='{u_fees}',duration='{u_duration}' WHERE id={id}")
        conn.commit()
        flash('Course Details Updated Successfully')
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    else:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute(f'''SELECT * FROM courses WHERE ID={id}''')
        n_data = cur.fetchall()[0]
        cur.close()
        conn.close()
        return render_template('update.html', data=n_data)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM courses WHERE id={id}")
    conn.commit()
    flash('Course Deleted Successfully')
    conn.close()
    cur.close()
    return redirect(url_for('index'))

app.run(debug=True)