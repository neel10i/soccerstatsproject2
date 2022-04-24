from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_mysqldb import MySQL
import yaml
  
app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        if request.form.get('Admin') == 'Admin':
            return redirect(url_for('loginPage'))
        elif request.form.get('Guest') == 'Guest':
            return redirect(url_for('guestPage'))
    return render_template("index.html")


#CHECKING WHICH TEAM THE USER SELECTS
@app.route('/guest', methods=['GET', 'POST'])
def guestPage():
    if request.method == 'POST':
        if request.form.get('Man City') == 'Man City':
            return redirect(url_for('manCity'))

        if request.form.get('PSG') == 'PSG':
            return redirect(url_for('psg'))
        
        if request.form.get('Liverpool') == 'Liverpool':
            return redirect(url_for('liverpool'))
        
        if request.form.get('Barcelona') == 'Barcelona':
            return redirect(url_for('barcelona'))
        
        if request.form.get('Man United') == 'Man United':
            return redirect(url_for('manchesterunited'))
        
    return render_template("guest.html")

@app.route('/manchestercity')
def manCity():
    cur = mysql.connection.cursor()
    users = cur.execute("SELECT * FROM playersCity")
    
    if users > 0:
        userDetails = cur.fetchall()
        return render_template("mancity.html",userDetails = userDetails)

@app.route('/psg')
def psg():
    cur = mysql.connection.cursor()
    users = cur.execute("SELECT * FROM playersPSG")
    
    if users > 0:
        userDetails = cur.fetchall()
        return render_template("psg.html",userDetails = userDetails)

@app.route('/liverpool')
def liverpool():
    cur = mysql.connection.cursor()
    users = cur.execute("SELECT * FROM playersLiverpool")

    if users > 0:
        userDetails = cur.fetchall()
        return render_template("liverpool.html",userDetails = userDetails)

@app.route('/barcelona')
def barcelona():
    cur = mysql.connection.cursor()
    users = cur.execute("SELECT * FROM playersFCB")

    if users > 0:
        userDetails = cur.fetchall()
        return render_template("barcelona.html",userDetails = userDetails)

@app.route('/manchesterunited')
def manchesterunited():
    cur = mysql.connection.cursor()
    users = cur.execute("SELECT * FROM playersUnited")

    if users > 0:
        userDetails = cur.fetchall()
        return render_template("manunited.html",userDetails = userDetails)

#LOGIN SYSTEM - CHECKING THE USERNAME AND PASSWORD
@app.route('/login')
def loginPage():
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def checkLogin():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        loginUpper = login.upper() 
        passwordUpper = password.upper()

        if loginUpper == "USERNAME" and passwordUpper == "PASSWORD":
            return redirect(url_for('adminPage'))
        
        else:
            flash('incorrect login or password')
            return redirect(url_for('loginPage'))

@app.route('/admin', methods=['GET', 'POST'])
def adminPage():
    cur = mysql.connection.cursor()
    users = cur.execute("SELECT * FROM playersLiverpool UNION ALL SELECT * FROM playersCity UNION ALL SELECT * FROM playersPSG UNION ALL SELECT * FROM playersFCB")

    if users > 0:
        userDetails = cur.fetchall()
        return render_template("admin.html",userDetails = userDetails)

@app.route('/postadmin', methods=['GET', 'POST'])
def postAdmin():
    if request.method == 'POST':
        userDetails = request.form

        playerName = userDetails['playerName']
        playerTeam  = userDetails['playerTeam']
        playerPosition = userDetails['playerPosition']
        totalGoals = userDetails['totalGoals']
        totalAssists = userDetails['totalAssists']
        teamTrophies = userDetails['teamTrophies']

        cur = mysql.connection.cursor()
        if request.form.get('playerTeam') == 'Manchester City':
            cur.execute("INSERT INTO playersCity(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies) VALUES(%s, %s, %s, %s, %s, %s)",(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('manCity'))
        
        if request.form.get('playerTeam') == 'Manchester United':
            cur.execute("INSERT INTO playersUnited(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies) VALUES(%s, %s, %s, %s, %s, %s)",(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('manchesterunited'))
        
        if request.form.get('playerTeam') == 'Liverpool':
            cur.execute("INSERT INTO playersLiverpool(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies) VALUES(%s, %s, %s, %s, %s, %s)",(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('liverpool'))
        
        if request.form.get('playerTeam') == 'PSG':
            cur.execute("INSERT INTO playersPSG(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies) VALUES(%s, %s, %s, %s, %s, %s)",(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('psg'))

        if request.form.get('playerTeam') == 'FC Barcelona':
            cur.execute("INSERT INTO playersFCB(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies) VALUES(%s, %s, %s, %s, %s, %s)",(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('barcelona'))

    return render_template('postadmin.html')  

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug = True)

'''
@app.route('/admin', methods=['GET', 'POST'])
def adminPage():
    cur = mysql.connection.cursor()
    users = cur.execute("SELECT * FROM soccer_clubs")
    if users > 0:
        userDetails = cur.fetchall()
        return render_template("admin.html",userDetails = userDetails)
'''
