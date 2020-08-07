import hashlib
import json
import sys
import os
import time
from http.client import HTTPException

from flask import Flask, render_template, request, flash, url_for, jsonify, session, redirect
import pymysql
from datetime import datetime, date

from requests import HTTPError
from werkzeug.utils import secure_filename

import pytz
from pytz import timezone

UPLOAD_FOLDER = 'static/UPLOADS/'
ALLOWED_EXTENSIONS = { 'png', 'jpg'}  # {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'SECRETKEYXIAN'


# Lambda Function
current_milli_time = lambda: int(round(time.time() * 1000))

####################### DATABASE ###############################
class DatabaseByPyMySQL:
    def __init__(self):
        host = "localhost"
        user = "root" # pigemkwh_PI
        password = "" #  QT^SiM(9]#gJ
        db = "flask_pigeon_infinity" # pigemkwh_pigeon_infinity

        self.conection = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
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

        sql_all = 'SELECT * FROM user WHERE email = "{0}" OR phone = "{0}";'.format(email)
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



    def addAuctionEvent(self, auctionName, pigeon, details, auctionStart, auctionEnd, filename):

        try:
            # Adding
            sql1 = 'INSERT INTO AuctionEvent(AuctionName, AuctionDetails, TotalPigeon, AuctionStart, AuctionEnd, MainPicture, Currency)' \
                   ' VALUES("{0}","{1}",{2},"{3}","{4}","{5}","BDT");'.format(auctionName, details, pigeon,
                                                                              auctionStart, auctionEnd, filename)
            print(sql1, flush=True)
            self.cursor.execute(sql1)
            self.conection.commit()
            return True

        except:
            print('Error on addAnimal()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    def addPigeon(self, AuctionID, PigeonRing, PigeonName, StartingPrice, PigeonGender, PigeonColor, BreedBy, OfferBy, PigeonDetails, AuctionStart, AuctionEnd, filename, otherPics):
        print(otherPics)
        try:
            # Adding
            sql1 = 'INSERT INTO Pigeon(AuctionID, PigeonRing, PigeonName, Price, MainPic, AllPic, PigeonGender, PigeonColor, BreedBy, OfferBy, PigeonDetails, StartTime, EndTime)' \
                   ' VALUES({0},"{1}","{2}",{3},"{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}");'\
                .format(AuctionID, PigeonRing, PigeonName, StartingPrice, filename, otherPics, PigeonGender, PigeonColor, BreedBy, OfferBy, PigeonDetails, AuctionStart, AuctionEnd)
            print(sql1, flush=True)
            self.cursor.execute(sql1)
            self.conection.commit()
            return True

        except:
            print('Error on addPigeon()', flush=True)
            print('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    def getLastAuction(self):
        sql_qry = 'SELECT * FROM auctionevent ORDER BY AuctionID DESC LIMIT 1;'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getLastAuction : ', str(data), flush=True)

        if len(data)>0:
            return data[0], True
        else:
            return data, False

    def getAllAuctions(self):
        sql_qry = 'SELECT * FROM auctionevent;'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()


        if len(data)>0:
            data2 = []
            for d in data:
                total, pigeons = self.getTotalAmountByAuctionID(d['AuctionID'])
                if total is not None:
                    d['TotalAmount'] = int(total)
                else:
                    d['TotalAmount'] = 0
                d['Pigeons'] = pigeons
                bids = self.getTotalBidsByAuctionID(d['AuctionID'])
                d['Bids'] = bids
                data2.append(d)

            return data2, True
        else:
            return data, False

    def getTotalAmountByAuctionID(self, ID):
        sql_qry = 'SELECT SUM(price) as Total , COUNT(PigeonID)as Pigeons FROM Pigeon WHERE AuctionID = {0};'.format(ID)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()


        if len(data)>0:
            return data[0]['Total'], data[0]['Pigeons']
        else:
            return data

    def getTotalBidsByAuctionID(self, ID):
        sql_qry = 'SELECT COUNT(BidID)as Bids FROM Bid WHERE AuctionID = {0};'.format(ID)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        if len(data)>0:
            return data[0]['Bids']
        else:
            return data

    def getAuctionByID(self, id):
        sql_qry = 'SELECT * FROM auctionevent WHERE AuctionID = {0};'.format(id)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getAuctionByID : ', str(data[0]), flush=True)

        if len(data) > 0:
            return data[0], True
        else:
            return data, False

    def getPigeonsByAuctionID(self, id):
        sql_qry = 'SELECT * FROM pigeon WHERE AuctionID = {0};'.format(id)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getPigeonsByAuctionID : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    def getPigeonByID(self, id):
        sql_qry = 'SELECT * FROM pigeon WHERE PigeonID = {0};'.format(id)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        print('getPigeonsByAuctionID : ', str(data), flush=True)

        if len(data) > 0:
            return data[0], True
        else:
            return data, False
###############################################################

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Login', methods=['POST', 'GET'])
def login():

    if session.get('user_id') is not None:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['user_email']
        pw = request.form['user_pass']

        DB = DatabaseByPyMySQL()
        user, sts = DB.getUserByEmail(email)

        if sts:
            pwd = computeMD5hash(pw)
            if pwd == user['password']:

                session['user_id'] = user['user_id']
                session['name'] = user['name']
                session['phone'] = user['phone']
                session['email'] = user['email']
                session['address'] = user['address']

                return redirect(url_for('home'))
            else:
                return render_template('login.html', error='Wrong password')
        else:
            return render_template('login.html', error='Not registered')

    return render_template('login.html')

@app.route('/Logout')
def logout():
    session.pop('user_id', None)
    session.pop('name', None)
    session.pop('phone', None)
    session.pop('email', None)
    session.pop('address', None)

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/Auction')
def auction():
    DB = DatabaseByPyMySQL()
    data, sts = DB.getAllAuctions()

    runningAuc = []
    upcommingAuc = []
    pastAuc = []

    for d in data:
        curTime = time.strftime('%Y %m %d %H:%M:%S')

        dt_obj = datetime.strptime(curTime,
                                   '%Y %m %d %H:%M:%S')
        curMilliSec = dt_obj.timestamp() * 1000

        dt_obj = datetime.strptime(d['AuctionStart'],
                                   '%Y-%m-%d %H:%M')
        aucMilliSecStart = dt_obj.timestamp() * 1000

        #print(str(curTime)+' :: '+str(d['AuctionStart']))
        #print(str(curMilliSec)+' :: '+str(aucMilliSecStart))

        if(curMilliSec>=aucMilliSecStart):
            #print('Running or past')
            dt_obj = datetime.strptime(d['AuctionEnd'],
                                       '%Y-%m-%d %H:%M')
            aucMilliSecEnd = dt_obj.timestamp() * 1000

            #print(str(curTime) + ' :: ' + str(d['AuctionEnd']))
            #print(str(curMilliSec) + ' :: ' + str(aucMilliSecEnd))

            if(curMilliSec<aucMilliSecEnd):
                runningAuc.append(d)
                #print('Running')
            else:
                pastAuc.append(d)
                #print('Past')

        elif(curMilliSec<aucMilliSecStart):
            upcommingAuc.append(d)
            #print('Upcomming')

    return render_template('auction.html', runningAuc=runningAuc, upcommingAuc=upcommingAuc, pastAuc=pastAuc)


@app.route('/Auction/<auction_no>')
def single_auction(auction_no):

    DB = DatabaseByPyMySQL()
    auc,sts = DB.getAuctionByID(auction_no)
    pgs, sts = DB.getPigeonsByAuctionID(auction_no)

    curTime = time.strftime('%Y %m %d %H:%M:%S')

    dt_obj = datetime.strptime(curTime,
                               '%Y %m %d %H:%M:%S')
    curMilliSec = dt_obj.timestamp() * 1000

    dt_obj = datetime.strptime(auc['AuctionEnd'],
                               '%Y-%m-%d %H:%M')
    aucMilliSecEnd = dt_obj.timestamp() * 1000

    dt_obj = datetime.strptime(auc['AuctionStart'],
                               '%Y-%m-%d %H:%M')
    aucMilliSecStart = dt_obj.timestamp() * 1000

    if curMilliSec > aucMilliSecStart:
        if (curMilliSec < aucMilliSecEnd):
            running = 'Running'
        else:
            running = 'Ended'
    else:
        running = 'Upcoming'

    return render_template('single_auction.html', auc=auc, pgs=pgs, running=running)

@app.route("/getTime", methods=['GET'])
def getTime():
    print("browser time: ", request.args.get("time"))
    print("server time : ", time.strftime('%A %B, %d %Y %H:%M:%S'))
    return "Done"

@app.route('/Profile')
def profile():
    return render_template('profile.html', userData={})

@app.route('/Articles')
def article():
    return render_template('article.html', userData={})



@app.route('/Auction/Pigeon/<pigeon>')
def pigeon(pigeon):
    DB = DatabaseByPyMySQL()
    pg, sts = DB.getPigeonByID(pigeon)


    curTime = time.strftime('%Y %m %d %H:%M:%S')

    dt_obj = datetime.strptime(curTime,
                               '%Y %m %d %H:%M:%S')
    curMilliSec = dt_obj.timestamp() * 1000

    dt_obj = datetime.strptime(pg['EndTime'],
                               '%Y-%m-%d %H:%M')
    pigeonMilliSecEnd = dt_obj.timestamp() * 1000

    dt_obj = datetime.strptime(pg['StartTime'],
                               '%Y-%m-%d %H:%M')
    pigeonMilliSecStart = dt_obj.timestamp() * 1000

    if curMilliSec > pigeonMilliSecStart:
        if (curMilliSec < pigeonMilliSecEnd):
            running = 'Running'
        else:
            running = 'Ended'
    else:
        running = 'Upcoming'

    #x = u'[ "A","B","C" , " D"]'
    x = pg['AllPic']
    lst = x.strip('[]').replace("'", '').replace(' ', '').split(',')
    pg['AllPic'] = lst

    return render_template('pigeon.html', pigeon=pg, running=running)

@app.route('/Privacy')
def privacy():
    return render_template('profile.html', userData={})

@app.route('/Rules')
def rules():
    return render_template('rules.html', userData={})

@app.route('/Contact')
def contact():
    return render_template('contact.html', userData={})

@app.route('/Clubs')
def club():
    return render_template('contact.html', userData={})

@app.route('/Buy')
def buy():
    return render_template('contact.html', userData={})

@app.route('/About')
def about():
    return render_template('contact.html', userData={})


@app.route('/Admin')
def admin():
    return 'admin'


@app.route('/Admin/Auction')
def admin_auction():
    DB = DatabaseByPyMySQL()
    data, sts = DB.getAllAuctions()
    return render_template('admin_auction.html', auctions = data)

@app.route('/Admin/Auction/Add', methods=['GET', 'POST'])
def admin_add_auction():
    if request.method == 'POST':
        try:
            if 'auction_image' not in request.files:
                print('No file part', flush=True)
                return render_template('admin_add_auction.html', error='No picture selected')
            file = request.files['auction_image']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                print('No selected file', flush=True)
                return render_template('admin_add_auction.html', error='Only allow png, jpg formats')

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = str(current_milli_time()) + filename[-4:]
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                print(filename, flush=True)

                try:
                    auctionName = request.form['auctionName']
                    pigeon = request.form['pigeon']
                    details = request.form['details']
                    pigeon = request.form['pigeon']
                    startDate = request.form['startDate']
                    startTime = request.form['startTime']
                    endDate = request.form['endDate']
                    endTime = request.form['endTime']

                    print('TIMES = ', startDate, startTime, endDate, endTime)
                except:
                    return render_template('admin_add_auction.html', error='Missing information')
                    print('Error = ', str(sys.exc_info()[0]), flush=True)

                auctionStart = startDate + ' '+ startTime
                auctionEnd = endDate + ' '+ endTime
                db = DatabaseByPyMySQL()
                status = db.addAuctionEvent(auctionName, pigeon, details, auctionStart, auctionEnd, filename)

                print(str(status), flush=True)

                if status:
                    auc,sts = db.getLastAuction()
                    session['totalPigeon'] = pigeon
                    session['AuctionID'] = auc['AuctionID']
                    session['AuctionName'] = auc['AuctionName']
                    session['AuctionStart'] = auc['AuctionStart']
                    session['AuctionEnd'] = auc['AuctionEnd']
                    return redirect(url_for('admin_add_auction_pigeons'))
                else:
                    return render_template('admin_add_auction.html', error='Something went wrong')

        except HTTPError:
            print('Exception : ' + str(HTTPException), flush=True)
            return render_template('admin_add_auction.html', error='PLEASE FILL UP CORRECTLY', userData=userData)

    return render_template('admin_add_auction.html')

@app.route('/Admin/Auction/Add/Pigeons', methods=['POST','GET'])
def admin_add_auction_pigeons():

    data = {
        'pigeonCount': int(session['totalPigeon']),
        'AuctionID' : session['AuctionID'],
        'AuctionStart' : session['AuctionStart'],
        'AuctionEnd' : session['AuctionEnd'],
        'AuctionName' : session['AuctionName']
    }
    #totalPigeons = int(session['totalPigeon'])

    if request.method == 'POST':
        for i in range(int(session['totalPigeon'])):
            try:
                if 'PigeonMainPic'+str(i+1) not in request.files:
                    print('No file part PigeonMainPic'+str(i+1), flush=True)
                    for d in request.files:
                        print(d)
                    return render_template('admin_add_auction_pigeons.html', error='No picture selected', data = data)
                file = request.files['PigeonMainPic'+str(i+1)]
                # if user does not select file, browser also
                # submit an empty part without filename
                if file.filename == '':
                    print('No selected file', flush=True)
                    return render_template('admin_add_auction_pigeons.html', error='Only allow png, jpg formats', data = data)

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    cur_mili = str(current_milli_time())
                    filename =  cur_mili + filename[-4:]
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    print('PigeonOthersPics'+str(i+1)+' :: '+filename, flush=True)

                    files = request.files.getlist('PigeonOthersPics'+str(i+1))
                    imNo = 0
                    otherPics = []
                    for fi in files:
                        finame = secure_filename(fi.filename)
                        finame = cur_mili +str(imNo)+ finame[-4:]
                        imNo += 1
                        fi.save(os.path.join(app.config['UPLOAD_FOLDER'], finame))
                        print('PigeonMainPic' + str(i+1) + ' :: ' + finame, flush=True)
                        otherPics.append(finame)
                    try:
                        PigeonRing = request.form['PigeonRing'+str(i+1)]
                        PigeonName = request.form['PigeonName'+str(i+1)]
                        StartingPrice = request.form['StartingPrice'+str(i+1)]
                        PigeonGender = request.form['PigeonGender'+str(i+1)]
                        PigeonColor = request.form['PigeonColor'+str(i+1)]
                        BreedBy = request.form['BreedBy'+str(i+1)]
                        OfferBy = request.form['OfferBy'+str(i+1)]
                        PigeonDetails = request.form['PigeonDetails'+str(i+1)]

                    except:
                        return render_template('admin_add_auction_pigeons.html', error='Missing information', data = data)
                        print('Error = ', str(sys.exc_info()[0]), flush=True)

                    db = DatabaseByPyMySQL()
                    status = db.addPigeon(session['AuctionID'], PigeonRing, PigeonName, StartingPrice, PigeonGender, PigeonColor, BreedBy, OfferBy, PigeonDetails, session['AuctionStart'], session['AuctionEnd'], filename, otherPics)
                    print(str(status), flush=True)

            except HTTPError:
                print('Exception : ' + str(HTTPException), flush=True)
                return render_template('admin_add_auction_pigeons.html', error='SOMETHING WENT WRONG', data = data)

        return redirect(url_for('admin_auction'))

    return render_template('admin_add_auction_pigeons.html', data = data)

@app.route('/Admin/Member')
def admin_member():
    return render_template('admin_member.html', userData={})

@app.route('/Admin/Article')
def admin_article():
    return render_template('admin_article.html', userData={})

@app.route('/Admin/Club')
def admin_club():
    return render_template('admin_club.html', userData={})


def computeMD5hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
