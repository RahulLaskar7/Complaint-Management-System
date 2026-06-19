from flask import Flask, render_template, request, redirect
import oracledb

app = Flask(__name__)

# Oracle Database Connection
connection = oracledb.connect(
    user="PROJ6THSEM",
    password="proj6thsem",
    dsn="localhost:1521/XE"
)

# =========================
# Login Page
# =========================
@app.route('/')
def login():
    return render_template('login.html')


# =========================
# Login Authentication
# =========================
@app.route('/login', methods=['POST'])
def user_login():

    email = request.form['email']
    password = request.form['password']

    # Student Login
    if email == "rahul@college.com" and password == "rahul123":
        return redirect('/complaint')
    
    elif email == "user@college.com" and password == "user123":
        return redirect('/complaint')

    # Admin Login
    elif email == "admin@college.com" and password == "admin123":
        return redirect('/admin')

    else:
        return "Invalid Email or Password"


# =========================
# Complaint Page
# =========================
@app.route('/complaint')
def complaint():
    return render_template('complaint.html')


# =========================
# Admin Dashboard
# =========================
@app.route('/admin')
def admin():

    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        complaint_id,
        dept_id,
        title,
        priority,
        status
    FROM complaint
    ORDER BY complaint_id DESC
""")

    complaints = cursor.fetchall()

    return render_template(
        'admin.html',
        complaints=complaints
    )


# =========================
# Submit Complaint
# =========================
@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():

    title = request.form['title']
    description = request.form['description']
    dept_id = request.form['dept_id']
    priority = request.form['priority']

    # Validation
    if title == "" or description == "":
        return "Please Fill All Fields!"

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO complaint
        VALUES (
            complaint_seq.NEXTVAL,
            1,
            :dept_id,
            1,
            :title,
            :description,
            :priority,
            'Pending',
            SYSDATE
        )
    """,
    {
        "dept_id": dept_id,
        "title": title,
        "description": description,
        "priority": priority
    })

    connection.commit()

    return "Complaint Submitted Successfully!"


# =========================
# Run Flask App
# =========================
if __name__ == '__main__':
    app.run(debug=True)