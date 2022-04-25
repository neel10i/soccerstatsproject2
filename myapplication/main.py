#importing the required libraries 
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask_mysqldb import MySQL
import yaml
  
app = Flask(__name__)

#establishes MySQL connections and configures 
#allows us to utilize MySQL queries inside Flask.
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

#configures / to the index function, contains both get and post methods
@app.route('/', methods=['GET', 'POST'])
def index():

    #checks if the method is POST
    if request.method == 'POST':
        #checks which button the user clicked, based on that 
        #the user is redirected to the specific page

        if request.form.get('Admin') == 'Admin':
            return redirect(url_for('loginPage'))
        elif request.form.get('Guest') == 'Guest':
            return redirect(url_for('guestPage'))
    return render_template("index.html")


#CHECKING WHICH TEAM THE USER SELECTS
@app.route('/guest', methods=['GET', 'POST'])
def guestPage():

    #checks if the method is POST
    if request.method == 'POST':

        #if the user clicks the button that says Man City, they are redirected to that page which contains the team stats along with
        #stats about the players on that team

        if request.form.get('Man City') == 'Man City':
            return redirect(url_for('manCity'))

        #if the user clicks the button that says PSG, they are redirected to that page which contains the team stats along with
        #stats about the players on that team
        if request.form.get('PSG') == 'PSG':
            return redirect(url_for('psg'))
        
        #if the user clicks the button that says liverpool, they are redirected to that page which contains the team stats along with
        #stats about the players on that team
        if request.form.get('Liverpool') == 'Liverpool':
            return redirect(url_for('liverpool'))
        
        #if the user clicks the button that says barcelona, they are redirected to that page which contains the team stats along with
        #stats about the players on that team
        if request.form.get('Barcelona') == 'Barcelona':
            return redirect(url_for('barcelona'))
        
        #if the user clicks the button that says Man United, they are redirected to that page which contains the team stats along with
        #stats about the players on that team
        if request.form.get('Man United') == 'Man United':
            return redirect(url_for('manchesterunited'))
    
    #loads the guest.html page at the route /guest
    return render_template("guest.html")


#configures the /manchestercity route to the funtion manCity
@app.route('/manchestercity')
def manCity():

    #establishes a connection to MySQL
    cur = mysql.connection.cursor()
    #sets users equal to a specific mysql query
    users = cur.execute("SELECT * FROM playersCity")

    #makes sure that the query is possible (there are rows which can be selected, etc.)
    if users > 0:
        #sets userdetails equal to cur.fetchall() gets all the rows in the query and returns false when there are none left
        userDetails = cur.fetchall()
        return render_template("mancity.html",userDetails = userDetails)

#configures the /psg route to the funtion psg
@app.route('/psg')
def psg():

    #establishes a connection to MySQL
    cur = mysql.connection.cursor()
    #sets users equal to a specific mysql query
    users = cur.execute("SELECT * FROM playersPSG")
    
    #makes sure that the query is possible (there are rows which can be selected, etc.)
    if users > 0:
        #sets userdetails equal to cur.fetchall() gets all the rows in the query and returns false when there are none left
        userDetails = cur.fetchall()
        return render_template("psg.html",userDetails = userDetails)

#configures the /liverpool route to the funtion liverpool
@app.route('/liverpool')
def liverpool():
    #establishes a connection to MySQL
    cur = mysql.connection.cursor()
    #sets users equal to a specific mysql query
    users = cur.execute("SELECT * FROM playersLiverpool")

    #makes sure that the query is possible (there are rows which can be selected, etc.)
    if users > 0:
        #sets userdetails equal to cur.fetchall() gets all the rows in the query and returns false when there are none left
        userDetails = cur.fetchall()
        return render_template("liverpool.html",userDetails = userDetails)

#configures the /barcelona route to the funtion barcelona
@app.route('/barcelona')
def barcelona():
    #establishes a connection to MySQL
    cur = mysql.connection.cursor()
    #sets users equal to a specific mysql query
    users = cur.execute("SELECT * FROM playersFCB")

    #makes sure that the query is possible (there are rows which can be selected, etc.)
    if users > 0:
        #sets userdetails equal to cur.fetchall() gets all the rows in the query and returns false when there are none left
        userDetails = cur.fetchall()
        return render_template("barcelona.html",userDetails = userDetails)

#configures the /manchesterunited route to the funtion manchesterunited
@app.route('/manchesterunited')
def manchesterunited():
    #establishes a connection to MySQL
    cur = mysql.connection.cursor()
    #sets users equal to a specific mysql query
    users = cur.execute("SELECT * FROM playersUnited")

    #makes sure that the query is possible (there are rows which can be selected, etc.)
    if users > 0:
        #sets userdetails equal to cur.fetchall() gets all the rows in the query and returns false when there are none left
        userDetails = cur.fetchall()
        return render_template("manunited.html",userDetails = userDetails)

#LOGIN SYSTEM - CHECKING THE USERNAME AND PASSWORD

#configures /login route to the function loginPage
@app.route('/login')
#returns login.html
def loginPage():
    return render_template("login.html")

#configures /login route to the function checkLogin, contains get and post methods
@app.route('/login', methods=['GET', 'POST'])
def checkLogin():

    #checks if the request method is a post call
    if request.method == 'POST':
        #gets what the user entered in the login textbox
        login = request.form.get('login')
        #gets what the user entered in the password textbox
        password = request.form.get('password')

        #converts the login and password to uppercase
        loginUpper = login.upper() 
        passwordUpper = password.upper()

        #checks if the user entered the following values USERNAME and PASSWORD
        if loginUpper == "USERNAME" and passwordUpper == "PASSWORD":
            #if it is correct the user is redirected to the admin page
            return redirect(url_for('adminPage'))
        
        #if the user enters something else then they get a pop up saying incorrect login/password 
        #and the loginPage is reloaded 
        else:
            flash('incorrect login or password')
            return redirect(url_for('loginPage'))

#routes /admin to the adminPage function, contains both get and post calls
@app.route('/admin', methods=['GET', 'POST'])
def adminPage():
    #establishes a mysql connection
    cur = mysql.connection.cursor()
    #sets users = to the mysql query - the query joins all the player tables using UNION ALL and displays all players when the admin logins in.
    users = cur.execute("SELECT * FROM playersLiverpool UNION ALL SELECT * FROM playersCity UNION ALL SELECT * FROM playersPSG UNION ALL SELECT * FROM playersFCB")

    #makes sure that the query is possible (there are rows which can be selected, etc.)
    if users > 0:
        #sets userdetails equal to cur.fetchall() gets all the rows in the query and returns false when there are none left
        userDetails = cur.fetchall()
        return render_template("admin.html",userDetails = userDetails)

#routes the /postadmin route to the function postAdmin
@app.route('/postadmin', methods=['GET', 'POST'])
def postAdmin():
    #checks the mtehod, then sets userDetails = request.form (to get the values entered into text entries)
    if request.method == 'POST':
        userDetails = request.form

        #createes a varaible for all of the values which the user enters into the 6 different text boxes
        playerName = userDetails['playerName']
        playerTeam  = userDetails['playerTeam']
        playerPosition = userDetails['playerPosition']
        totalGoals = userDetails['totalGoals']
        totalAssists = userDetails['totalAssists']
        teamTrophies = userDetails['teamTrophies']

        #establishes a mysql connection
        cur = mysql.connection.cursor()
        #checks if the user enteres 'manchester city' into the playerTeam textbox
        if request.form.get('playerTeam') == 'Manchester City':
            #inserts what the user selected into the other textboxes into the table playersCity
            cur.execute("INSERT INTO playersCity(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies) VALUES(%s, %s, %s, %s, %s, %s)",(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies))
            #confirms the changes which were made to the mysql table
            mysql.connection.commit()
            #closes the mysql connection
            cur.close()
            #reroutes the user to the specific team page
            return redirect(url_for('manCity'))
        
        #checks if the user enteres 'manchester united' into the playerTeam textbox
        if request.form.get('playerTeam') == 'Manchester United':
            #inserts what the user selected into the other textboxes into the table playersUnitec
            cur.execute("INSERT INTO playersUnited(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies) VALUES(%s, %s, %s, %s, %s, %s)",(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies))
            #confirms the changes which were made to the mysql table
            mysql.connection.commit()
            #closes the mysql connection
            cur.close()
            #reroutes the user to the specific team page
            return redirect(url_for('manchesterunited'))
        
        #checks if the user enteres 'liverpool' into the playerTeam textbox
        if request.form.get('playerTeam') == 'Liverpool':
            #inserts what the user selected into the other textboxes into the table playersLiverpool
            cur.execute("INSERT INTO playersLiverpool(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies) VALUES(%s, %s, %s, %s, %s, %s)",(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies))
            #confirms the changes which were made to the mysql table
            mysql.connection.commit()
            #closes the mysql connection
            cur.close()
            #reroutes the user to the specific team page
            return redirect(url_for('liverpool'))
        
        #checks if the user enteres 'PSG' into the playerTeamtextbox
        if request.form.get('playerTeam') == 'PSG':
            #inserts what the user selected into the other textboxes into the table playersPSG
            cur.execute("INSERT INTO playersPSG(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies) VALUES(%s, %s, %s, %s, %s, %s)",(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies))
            #confirms the changes which were made to the mysql table
            mysql.connection.commit()
            #closes the mysql connection
            cur.close()
            #reroutes the user to the specific team page
            return redirect(url_for('psg'))

        #checks if the user enteres 'FC Barcelona' into the playerTeam textbox
        if request.form.get('playerTeam') == 'FC Barcelona':
            #inserts what the user selected into the other textboxes into the table playersPSG
            cur.execute("INSERT INTO playersFCB(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies) VALUES(%s, %s, %s, %s, %s, %s)",(playerName, playerTeam, playerPosition, totalGoals, totalAssists, teamTrophies))
            #confirms the changes which were made to the mysql table
            mysql.connection.commit()
            #closes the mysql connection
            cur.close()
            #reroutes the user to the specific team page
            return redirect(url_for('barcelona'))

    return render_template('postadmin.html')  
    
if __name__ == '__main__':
    app.run(debug = True)
