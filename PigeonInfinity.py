import hashlib
import sys
from http.client import HTTPException

from flask import Flask, render_template, request, flash, url_for, jsonify, session, redirect
import pymysql
from datetime import datetime

from requests import HTTPError

app = Flask(__name__)
app.secret_key = 'SECRETKEYXIAN'

####################### DATABASE ###############################
class DatabaseByPyMySQL:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = ""
        db = "flask_pigeon_infinity"

        self.conection = pymysql.connect(host=host, user=user, password=password, db=db,
                                         cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conection.cursor()

    '''def addSome(self):
      self.cursor.execute("INSERT INTO demo VALUES(" + str(32154) + "," + str(85746) + ");")
      self.conection.commit()
      print("DATA ADDED")

       def getSome(self):
          self.cursor.execute("SELECT * from demo;")
          data = self.cursor.fetchall()
          print(data)'''



    def getAllAnimals(self):
        sql_qry = 'SELECT * FROM animal;'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAllAnimals : ', str(data), flush=True)

        if len(data)>0:
            return data, True
        else:
            return data, False

    def getAnimalByID(self, id):
        sql_qry = 'SELECT * FROM animal WHERE AnimalID = {0};'.format(id)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAnimalByID : ', str(data[0]), flush=True)

        if len(data) > 0:
            return data[0], True
        else:
            return data, False

    def SearchAnimal(self,searchText):
        sql_qry = 'SELECT * FROM animal WHERE AnimalCategory LIKE "%{0}%" OR AnimalTAG LIKE "%{0}%" OR AnimalOwner LIKE "%{0}%" OR AnimalBreed LIKE "%{0}%";'.format(searchText)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('SearchAnimal : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    def addAnimal(self, AnimalCategory, AnimalBreed, AnimalSex, AnimalOwner, AnimalAge,
                  AnimalFather, AnimalMother, AnimalPictureName):

        try:
            last_id, sts = self.getAnimalLastID()
            print('last ID = ' + str(last_id), flush=True)
            animal_id = int(last_id) + 1
            animal_tag = AnimalCategory[0:2]+'-'+AnimalBreed[0:3]+'-'+str(animal_id)


            # current date and time
            now = datetime.now()

            addedDate = str(now.strftime("%d-%m-%Y"))

            # Adding
            sql1 = 'INSERT INTO animal(AnimalID, AnimalTag, AnimalCategory, AnimalBreed, AnimalSex, AnimalOwner, AnimalAge, AnimalFather, AnimalMother, AnimalStatus, AddedDate, UpdatedDate, AnimalPictureName)' \
                   ' VALUES({0},"{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","ALIVE","{9}","{9}","{10}");'.format(animal_id, animal_tag, AnimalCategory, AnimalBreed, AnimalSex,
                                                                                                                    AnimalOwner, AnimalAge, AnimalFather, AnimalMother, addedDate, AnimalPictureName)
            print(sql1, flush=True)
            self.cursor.execute(sql1)
            self.conection.commit()

            self.updateCommonData(AnimalCategory, 'ADD')

            return True

        except:
            print('Error on addAnimal()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

#####################

    def isEmailExist(self, email, phone):
        self.cursor.execute('SELECT * FROM user WHERE email = "{0}" OR phone = "{1}";'.format(email, phone))
        data = self.cursor.fetchall()
        if len(data) > 0:
            print('EMAIL EXIST', flush=True)
            return True
        else:
            print('EMAIL DO NOT EXIST', flush=True)
            return False


    def getUserByEmail(self, email):

        sql_all = 'SELECT * FROM user WHERE UserEmail = "{0}"'.format(email)
        self.cursor.execute(sql_all)
        data = self.cursor.fetchall()

        if len(data)>0:
            return data[0], True
        else:
            return data, False

    def Login(self, Email, Pass):
        print(Email, Pass, flush=True)
        if self.isEmailExist(Email):
            user, sts = self.getUserByEmail(Email)
            if user['UserPass'] == Pass:
                return user['Type'], user['UserName'], True
            else:
                return 'NULL','NULL', False
        else:
            return 'NULL','NULL', False

    def Register(self, Name, Address, DOB, NID, Email, Phone, Pass):

        print(Name, Address, DOB, NID, Email, Phone, Pass)

        if not self.isEmailExist(Email, Phone):
            # current date and time
            now = datetime.now()

            nowDate = str(now.strftime("%d-%m-%Y"))

            # Adding
            sql = 'INSERT INTO user (name, phone, email, password, address, register_date, dob, nid)' \
                   ' VALUES("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}");'\
                    .format(Name, Phone, Email, Pass, Address, nowDate, DOB, NID)
            print(sql)
            self.cursor.execute(sql)
            self.conection.commit()
            return 'REGISTRATION COMPLETE, PLEASE LOGIN'
        else:
            return 'USER EXISTED, TRY LOGIN'
###############################################################

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Login')
def login():
    '''if session.get('UserID') is not None:
        return redirect(url_for('home'))'''

    '''session['UserID'] = user_id
    session['UserName'] = details['name']
    session['idToken'] = idToken
    session['UserEmail'] = details['email']
    session['UserPhone'] = details['phone']
    session['UserAddress'] = details['address']
    
    return redirect(url_for('home'))
    '''
    '''
    try:
    # Log the user in
    
    except HTTPError:
    print('Exception : '+str(HTTPException), flush=True)
    return render_template('login.html', error='TRUE')
    '''
    if request.method == 'POST':
        email = request.form['Email']
        pw = request.form['Pass']

    return render_template('login.html', methods=['POST', 'GET'])

@app.route('/Logout')
def logout():
    session.pop('UserID', None)
    session.pop('UserName', None)
    session.pop('idToken', None)
    session.pop('UserEmail', None)
    session.pop('UserPhone', None)
    session.pop('UserAddress', None)

    return redirect(url_for('home'))


@app.route('/Registration', methods=['GET', 'POST'])
def registration():

    if request.method == 'POST':
        try:
            userData = {}
            user_name = request.form['user_name']
            userData.update({'user_name':user_name})

            user_address = request.form['user_address']
            userData.update({'user_address':user_address})

            user_dob = request.form['user_dob']
            userData.update({'user_dob':user_dob})

            user_nid = request.form['user_nid']
            userData.update({'user_nid':user_nid})

            user_email = request.form['user_email']
            userData.update({'user_email':user_email})

            user_phone = request.form['user_phone']
            userData.update({'user_phone':user_phone})

            user_pass1 = request.form['user_pass1']
            user_pass2 = request.form['user_pass2']

            if user_pass1 == user_pass2:
                DB = DatabaseByPyMySQL()
                msg = DB.Register(user_name, user_address, user_dob, user_nid, user_email, user_phone, computeMD5hash(user_pass1))

                return render_template('register.html', error=msg, userData={})
            else:
                return render_template('register.html', error='PASSWORD NOT MATCH', userData=userData)
        except HTTPError:
            print('Exception : ' + str(HTTPException), flush=True)
            return render_template('register.html', error='PLEASE FILL UP CORRECTLY', userData=userData)


    return render_template('register.html', userData={})

def computeMD5hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()

if __name__ == '__main__':
    app.debug = True
    app.run()
