from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

#create a flask instance
app = Flask(__name__)
#Secret key
app.secret_key = 'many random bytes'

#initialize the database
mydb = mysql.connector.connect(host="localhost", user="root", password="", database="songdb")

"""
mycursor = mydb.cursor()


#create database

mycursor.execute("Create database songdb")

#show databases
mycursor.execute("Show databases")

for db in mycursor:
    print(db)

#create table under database "songdb"
mycursor.execute("Create table song(ID int auto_increment primary key, Name varchar(100) NOT null, Datetime varchar(50) )")
"""

#Read all data
@app.route('/')
def index():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM song")
    data = mycursor.fetchall()
    mycursor.close()
    return render_template("index.html", song=data)

#insert data
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        flash("Data Inserted Successfully")
        # fetch from data
        name = request.form['name']
        time = request.form['time']
        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO song(Name, Datetime) VALUES(%s,%s)", (name, time))
        mydb.commit()
        return redirect(url_for('index'))

#update data
@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        time = request.form['time']
        mycursor= mydb.cursor()
        mycursor.execute("""
        UPDATE song
        SET Name=%s, Datetime=%s WHERE ID=%s""", (name, time, id))
        flash("Data Update Successfully")
        mydb.commit()
        return redirect(url_for('index'))

#delete data
@app.route('/delete/<string:id_data>', methods=['GET', 'POST'])
def delete(id_data):
    mycursor = mydb.cursor()
    mycursor.execute('DELETE FROM song WHERE ID = %s', (id_data,))
    mydb.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)