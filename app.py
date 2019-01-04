from flask import Flask, render_template, request, redirect,url_for
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/users', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        userDetails= request.form
        name = userDetails['name']
        dep=userDetails['dep']
        hall=userDetails['hall']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, dep,hall) VALUES(%s, %s ,%s)",(name, dep,hall))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')

@app.route('/',methods=['GET','POST'])
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)