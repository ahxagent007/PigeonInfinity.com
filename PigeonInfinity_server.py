import hashlib
import os
import time

from flask import Flask, render_template, request, flash, url_for, jsonify, session, redirect
import pymysql
from datetime import datetime

from requests import HTTPError
from werkzeug.utils import secure_filename

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
        host = "104.219.248.46"
        user = "pigemkwh_PI"
        password = "!;KgfeFDnFKX"
        db = "pigemkwh_pigeon_infinity"

        self.conection = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conection.cursor()


    def isEmailExist(self, email, phone):
        self.cursor.execute('SELECT * FROM user WHERE email = "{0}" OR phone = "{1}";'.format(email, phone))
        data = self.cursor.fetchall()
        if len(data) > 0:
            return True
        else:
            return False

    def getUserByEmail(self, email):

        sql_all = 'SELECT * FROM user WHERE email = "{0}" OR phone = "{0}";'.format(email)
        self.cursor.execute(sql_all)
        data = self.cursor.fetchall()

        if len(data)>0:
            return data[0], True
        else:
            return data, False

    def getUserByID(self, id):

        sql_all = 'SELECT * FROM user WHERE user_id = {0};'.format(id)
        self.cursor.execute(sql_all)
        data = self.cursor.fetchall()

        if len(data)>0:
            return data[0], True
        else:
            return data, False

    def getAdminByEmail(self, email):

        sql_all = 'SELECT * FROM admin WHERE email = "{0}";'.format(email)
        self.cursor.execute(sql_all)
        data = self.cursor.fetchall()

        if len(data) > 0:
            return data[0], True
        else:
            return data, False

    def Login(self, Email, Pass):
        if self.isEmailExist(Email):
            user, sts = self.getUserByEmail(Email)
            if user['UserPass'] == Pass:
                return user['Type'], user['UserName'], True
            else:
                return 'NULL','NULL', False
        else:
            return 'NULL','NULL', False

    def LoginAdmin(self, Email, Pass):

        user, sts = self.getAdminByEmail(Email)

        if user['pass'] == Pass:
            return user['name'], True
        else:
            return 'NULL', False

    def Register(self, Name, Address, DOB, NID, Email, Phone, Pass, ref):

        if not self.isEmailExist(Email, Phone):
            # current date and time
            now = datetime.now()

            nowDate = str(now.strftime("%Y-%m-%d %H:%M:%S"))

            # Adding
            sql = 'INSERT INTO user (name, phone, email, password, address, register_date, dob, nid, reference)' \
                   ' VALUES("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}", "{8}");'\
                    .format(Name, Phone, Email, Pass, Address, nowDate, DOB, NID, ref)
            self.cursor.execute(sql)
            self.conection.commit()
            return 'REGISTRATION COMPLETE, PLEASE LOGIN'
        else:
            return 'USER EXISTED, TRY LOGIN'

    def addAuctionEvent(self, auctionName, pigeon, details, auctionStart, auctionEnd, filename):

        try:
            # Adding
            sql1 = 'INSERT INTO auctionevent(AuctionName, AuctionDetails, TotalPigeon, AuctionStart, AuctionEnd, MainPicture, Currency)' \
                   ' VALUES("{0}","{1}",{2},"{3}","{4}","{5}","BDT");'.format(auctionName, details, pigeon,
                                                                              auctionStart, auctionEnd, filename)
            self.cursor.execute(sql1)
            self.conection.commit()
            return True

        except:
            return False

    def addPigeon(self, AuctionID, PigeonRing, PigeonName, StartingPrice, PigeonGender, PigeonColor, BreedBy, OfferBy, PigeonDetails, AuctionStart, AuctionEnd, filename, otherPics, vdo):
        ##(otherPics)
        try:
            # Adding
            sql1 = 'INSERT INTO pigeon(AuctionID, PigeonRing, PigeonName, Price, MainPic, AllPic, PigeonGender, PigeonColor, BreedBy, OfferBy, PigeonDetails, StartTime, EndTime, vdoLink)' \
                   ' VALUES({0},"{1}","{2}",{3},"{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}", "{13}");'\
                .format(AuctionID, PigeonRing, PigeonName, StartingPrice, filename, otherPics, PigeonGender, PigeonColor, BreedBy, OfferBy, PigeonDetails, AuctionStart, AuctionEnd, vdo)
            #(sql1, flush=True)
            self.cursor.execute(sql1)
            self.conection.commit()
            return True

        except:
            #('Error on addPigeon()', flush=True)
            #('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    def getLastAuction(self):
        sql_qry = 'SELECT * FROM auctionevent ORDER BY AuctionID DESC LIMIT 1;'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        #('getLastAuction : ', str(data), flush=True)

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
        sql_qry = 'SELECT SUM(price) as Total , COUNT(PigeonID)as Pigeons FROM pigeon WHERE AuctionID = {0};'.format(ID)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()


        if len(data)>0:
            return data[0]['Total'], data[0]['Pigeons']
        else:
            return data

    def getTotalBidsByAuctionID(self, ID):
        sql_qry = 'SELECT COUNT(BidID)as Bids FROM bid WHERE AuctionID = {0};'.format(ID)
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

        #('getAuctionByID : ', str(data[0]), flush=True)

        if len(data) > 0:
            return data[0], True
        else:
            return data, False

    def getPigeonsByAuctionID(self, id):
        sql_qry = 'SELECT * FROM pigeon WHERE AuctionID = {0};'.format(id)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        #('getPigeonsByAuctionID : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    def getPigeonByID(self, id):
        sql_qry = 'SELECT * FROM pigeon WHERE PigeonID = {0};'.format(id)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        #('getPigeonsByAuctionID : ', str(data), flush=True)

        if len(data) > 0:
            return data[0], True
        else:
            return data, False

    def getBids(self, id):
        sql_qry = 'SELECT user.name, user.user_id, bid.BidAmount, bid.BidTimeDate, pigeon.PigeonName, pigeon.PigeonRing, pigeon.AuctionID, pigeon.EndTime FROM bid ' \
                    'JOIN user ON bid.UserID = user.user_id '\
                    'JOIN pigeon ON pigeon.PigeonID = bid.PigeonID '\
                    'WHERE bid.PigeonID = {0} ' \
                    'ORDER BY bid.BidID DESC;'.format(id)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        #('getBids : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    def getLastBid(self, id):
        sql_qry = 'SELECT * FROM bid WHERE PigeonID = {0} ORDER BY BidID DESC;'.format(id)
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        #('getPigeonsByAuctionID : ', str(data), flush=True)

        if len(data) > 0:
            return data[0], True
        else:
            return data, False

    def getLatestBids(self):

        sql_qry = 'SELECT bid.BidAmount, bid.BidTimeDate, user.name, user.user_id, pigeon.PigeonName, pigeon.PigeonRing, pigeon.PigeonID FROM bid ' \
                  'JOIN user ON user.user_id = bid.UserID ' \
                  'JOIN pigeon ON pigeon.PigeonID = bid.PigeonID '  \
                  'ORDER BY BidID DESC LIMIT 100;'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        #('getLatestBids : ', str(data), flush=True)

        if len(data) > 0:
            return data, True
        else:
            return data, False

    def placeBid(self, pigeonID, userID, auctionID, amount, bidTime, name):
        try:
            # Adding
            sql = 'INSERT INTO bid(UserID, PigeonID, AuctionID, BidAmount, BidTimeDate)' \
                   ' VALUES({0},{1},{2},{3},"{4}");'.format(userID, pigeonID, auctionID, amount, bidTime)
            #(sql, flush=True)
            self.cursor.execute(sql)
            self.conection.commit()

            sql2 = 'UPDATE pigeon ' \
                   'SET Price = {0}, LastBidderID = {1}, LastBidderName = "{2}" ' \
                   'WHERE PigeonID = {3}'.format(amount, userID, name, pigeonID)
            #(sql2, flush=True)
            self.cursor.execute(sql2)
            self.conection.commit()
            return True

        except:
            #('Error on placeBid()', flush=True)
            #('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    def updatePigeonTime(self, pigeonID, auc_ID, Time):
        try:
            # Adding
            sql = 'UPDATE pigeon ' \
                   'SET EndTime = "{0}" ' \
                   'WHERE PigeonID = {1}'.format(Time, pigeonID)
            #(sql, flush=True)
            self.cursor.execute(sql)
            self.conection.commit()

            sql2 = 'UPDATE auctionEvent ' \
                   'SET AuctionEnd = "{0}" ' \
                   'WHERE AuctionID = {1}'.format(Time, auc_ID)
            #(sql2, flush=True)
            self.cursor.execute(sql2)
            self.conection.commit()
            return True

        except:
            #('Error on updatePigeonTime()', flush=True)
            #('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    def getSetting(self, page):

        sql_all = 'SELECT * FROM setting WHERE page = "{0}" ;'.format(page)
        self.cursor.execute(sql_all)
        data = self.cursor.fetchall()

        if len(data)>0:
            return data[0], True
        else:
            return data, False

    def getArticleByID(self, id):

        sql_all = 'SELECT * FROM article WHERE id = "{0}" ;'.format(id)
        self.cursor.execute(sql_all)
        data = self.cursor.fetchall()

        if len(data)>0:
            return data[0], True
        else:
            return data, False

    def getAllArticles(self):

        sql_all = 'SELECT * FROM article;'
        self.cursor.execute(sql_all)
        data = self.cursor.fetchall()

        if len(data)>0:
            return data, True
        else:
            return data, False

    def updateUserPoint(self, userID, amount):
        try:
            sql = 'UPDATE user ' \
                   'SET bid_limit = bid_limit+{0}*.2, bid_point = bid_point+1, total_bid_amount = total_bid_amount+{1} ' \
                   'WHERE user_id = {2}'.format(amount, amount, userID)
            #(sql, flush=True)
            self.cursor.execute(sql)
            self.conection.commit()
            return True
        except:
            #('Error on updateUserPoint()', flush=True)
            #('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    def updateUserPic(self, userID, pic):
        try:
            sql = 'UPDATE user ' \
                   'SET pro_pic = "{0}" ' \
                   'WHERE user_id = {1}'.format(pic, userID)

            #(sql, flush=True)
            self.cursor.execute(sql)
            self.conection.commit()
            return True
        except:
            #('Error on updateUserPic()', flush=True)
            #('Error = ', str(sys.exc_info()[0]), flush=True)
            return False


    def getAllMembers(self):
        sql_qry = 'SELECT * FROM user;'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()


        if len(data)>0:
            return data, True
        else:
            return data, False

    def getAllHighFanciers(self):
        sql_qry = 'SELECT * FROM highfancier;'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()

        if len(data)>0:
            return data, True
        else:
            return data, False

    def getUnverifiedMembers(self):
        sql_qry = 'SELECT * FROM user WHERE status = "UNVERIFIED";'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()


        if len(data)>0:
            return data, True
        else:
            return data, False

    def getVerifiedMembers(self):
        sql_qry = 'SELECT * FROM user WHERE status = "VERIFIED";'
        self.cursor.execute(sql_qry)
        data = self.cursor.fetchall()


        if len(data)>0:
            return data, True
        else:
            return data, False

    def verifyMember(self, userID, adminName):
        try:

            sql = 'UPDATE user ' \
                   'SET status = "VERIFIED", approvedBy = "{0}" ' \
                   'WHERE user_id = {1}'.format(adminName, userID)
            #(sql, flush=True)
            self.cursor.execute(sql)
            self.conection.commit()

            return True

        except:
            #('Error on verifyMember()', flush=True)
            #('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    def unverifyMember(self, userID, adminName):
        try:

            sql = 'UPDATE user ' \
                   'SET status = "UNVERIFIED", approvedBy = "{0}" ' \
                   'WHERE user_id = {1}'.format(adminName, userID)
            #(sql, flush=True)
            self.cursor.execute(sql)
            self.conection.commit()

            return True

        except:
            #('Error on unverifyMember()', flush=True)
            #('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

    def addArticle(self, title, para1, para2, auth, filename):

        try:
            sql1 = 'INSERT INTO article (title, para1, para2, auth, picture)' \
                   ' VALUES("{0}","{1}","{2}","{3}","{4}");'.format(title, para1, para2, auth, filename)
            #(sql1, flush=True)
            self.cursor.execute(sql1)
            self.conection.commit()
            return True

        except:
            #('Error on addArticle()', flush=True)
            #('Error = ', str(sys.exc_info()[0]), flush=True)
            return False

###############################################################

@app.route('/')
def home():
    DB = DatabaseByPyMySQL()
    auc, sts = DB.getLastAuction()
    setting, sts1 = DB.getSetting('home')
    bids, sts2 = DB.getLatestBids()
    fanciers, sts3 = DB.getAllHighFanciers()

    return render_template('index.html', auc=auc, setting=setting, bids=bids, fanciers = fanciers)

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

            reference = request.form['reference']

            if user_pass1 == user_pass2:
                DB = DatabaseByPyMySQL()
                msg = DB.Register(user_name, user_address, user_dob, user_nid, user_email, user_phone, computeMD5hash(user_pass1), reference)

                return render_template('register.html', error=msg, userData={})
            else:
                return render_template('register.html', error='PASSWORD NOT MATCH', userData=userData)
        except HTTPError:
            #('Exception : ' + str(HTTPException), flush=True)
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
        curTime = time.strftime('%Y-%m-%d %H:%M:%S')

        dt_obj = datetime.strptime(curTime,
                                   '%Y-%m-%d %H:%M:%S')
        curMilliSec = dt_obj.timestamp() * 1000

        dt_obj = datetime.strptime(d['AuctionStart'],
                                   '%Y-%m-%d %H:%M:%S')
        aucMilliSecStart = dt_obj.timestamp() * 1000

        if(curMilliSec>=aucMilliSecStart):

            dt_obj = datetime.strptime(d['AuctionEnd'],
                                       '%Y-%m-%d %H:%M:%S')
            aucMilliSecEnd = dt_obj.timestamp() * 1000

            if(curMilliSec<aucMilliSecEnd):
                runningAuc.append(d)

            else:
                pastAuc.append(d)

        elif(curMilliSec<aucMilliSecStart):
            upcommingAuc.append(d)

    runningAuc = runningAuc[::-1]
    upcommingAuc = upcommingAuc[::-1]
    pastAuc = pastAuc[::-1]

    return render_template('auction.html', runningAuc=runningAuc, upcommingAuc=upcommingAuc, pastAuc=pastAuc)


@app.route('/Auction/<auction_no>')
def single_auction(auction_no):

    DB = DatabaseByPyMySQL()
    auc,sts = DB.getAuctionByID(auction_no)
    pgs, sts = DB.getPigeonsByAuctionID(auction_no)

    curTime = time.strftime('%Y-%m-%d %H:%M:%S')

    dt_obj = datetime.strptime(curTime, '%Y-%m-%d %H:%M:%S')
    curMilliSec = dt_obj.timestamp() * 1000

    dt_obj = datetime.strptime(auc['AuctionEnd'], '%Y-%m-%d %H:%M:%S')
    aucMilliSecEnd = dt_obj.timestamp() * 1000

    dt_obj = datetime.strptime(auc['AuctionStart'], '%Y-%m-%d %H:%M:%S')
    aucMilliSecStart = dt_obj.timestamp() * 1000

    if curMilliSec > aucMilliSecStart:
        if (curMilliSec < aucMilliSecEnd):
            running = 'Running'
        else:
            running = 'Ended'
    else:
        running = 'Upcoming'

    #auc['AuctionStart'] = datetime.strptime(auc['AuctionStart'], '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    #auc['AuctionEnd'] = datetime.strptime(auc['AuctionEnd'], '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

    return render_template('single_auction.html', auc=auc, pgs=pgs, running=running)

@app.route('/Auction/Pigeon/<pigeon>')
def pigeon(pigeon):
    DB = DatabaseByPyMySQL()
    pg, sts = DB.getPigeonByID(pigeon)
    auc_pgs, stss = DB.getPigeonsByAuctionID(pg['AuctionID'])
    bid_list, stsss = DB.getBids(pigeon)


    curTime = time.strftime('%Y-%m-%d %H:%M:%S')

    dt_obj = datetime.strptime(curTime,
                               '%Y-%m-%d %H:%M:%S')
    curMilliSec = dt_obj.timestamp() * 1000

    dt_obj = datetime.strptime(pg['EndTime'],
                               '%Y-%m-%d %H:%M:%S')
    pigeonMilliSecEnd = dt_obj.timestamp() * 1000

    dt_obj = datetime.strptime(pg['StartTime'],
                               '%Y-%m-%d %H:%M:%S')
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

    return render_template('pigeon.html', pigeon=pg, running=running, auc_pgs=auc_pgs, bid_list=bid_list)

@app.route('/Auction/Pigeon/Bids', methods=['POST'])
def getBid():
    pigeonID = request.form.get('pigeonID')

    DB = DatabaseByPyMySQL()
    bids, sts = DB.getBids(pigeonID)

    return jsonify(bids)

@app.route('/Auction/Pigeon/Bid', methods=['POST'])
def Bid():
    pigeonID = request.form.get('pigeonID')
    amount = request.form.get('amount')
    userID = request.form.get('userID')
    auctionID = request.form.get('auctionID')
    name = request.form.get('userName')

    DB = DatabaseByPyMySQL()

    user, sts = DB.getUserByID(userID)

    if user['status'] == 'UNVERIFIED':
        status = 'Your account is not verified, please contact us.'
        data = {'status': status}
        return jsonify(data)

    pign, stsa = DB.getPigeonByID(pigeonID)

    curTime = time.strftime('%Y-%m-%d %H:%M:%S')
    dt_obj = datetime.strptime(curTime,
                               '%Y-%m-%d %H:%M:%S')
    curMilliSec = dt_obj.timestamp() * 1000

    aucTime_obj = datetime.strptime(pign['EndTime'],
                                    '%Y-%m-%d %H:%M:%S')
    aucMilliSec = aucTime_obj.timestamp() * 1000



    if curMilliSec < aucMilliSec:
        bid, sts = DB.getLastBid(pigeonID)
        if sts:
            if int(amount)>bid['BidAmount']:

                bidTime_obj = datetime.strptime(bid['BidTimeDate'],
                                           '%Y-%m-%d %H:%M:%S')
                bidMilliSec = bidTime_obj.timestamp() * 1000

                if curMilliSec>bidMilliSec:
                    bid_status = DB.placeBid(pigeonID, userID, auctionID, amount, curTime, name)
                    if bid_status:

                        if (aucMilliSec-curMilliSec) < 600000:
                            s = (aucMilliSec + 900000) / 1000.0
                            updatedDate = datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')
                            #('AucTime ' + pign['EndTime'] + ' Updated Time ' + updatedDate)
                            DB.updatePigeonTime(pigeonID, auctionID, updatedDate)

                            status = 'Your bid placed successfully! Time Increased!'
                        else:
                            status = 'Your bid placed successfully!'
                            DB.updateUserPoint(userID, amount)
                    else:
                        status = 'Error!'
                else:
                    status = 'Sorry, Another bid already placed!'
            else:
                status = 'Amount is lower then last bid'

        else:
            bid_status = DB.placeBid(pigeonID, userID, auctionID, amount, curTime, name)
            if bid_status:

                if (aucMilliSec - curMilliSec) < 600000:
                    s = (aucMilliSec + 900000) / 1000.0
                    updatedDate = datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')
                    #('AucTime ' + pign['EndTime'] + ' Updated Time ' + updatedDate)

                    DB.updatePigeonTime(pigeonID, auctionID, updatedDate)
                    status = 'Your bid placed successfully! Time Increased!'
                else:
                    status = 'Your bid placed successfully!'
                    DB.updateUserPoint(userID,amount)
            else:
                status = 'Error!'
    else:
        status = 'Sorry, Auction Ended'

    #(status)
    data = {'status':status}

    return jsonify(data)

@app.route("/getTime", methods=['GET'])
def getTime():
    #("browser time: ", request.args.get("time"))
    #("server time : ", time.strftime('%A %B, %d %Y %H:%M:%S'))
    return "Done"

@app.route('/Profile')
def profile():
    if session.get('user_id') is None:
        return redirect(url_for('login'))

    DB = DatabaseByPyMySQL()
    pro, sts = DB.getUserByID(session['user_id'])

    return render_template('profile.html', user=pro)

@app.route('/Profile/Edit', methods=['GET', 'POST'])
def profile_edit():
    if session.get('user_id') is None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            if 'pro_pic' not in request.files:
                return render_template('profile_edit.html', error='No picture selected')
            file = request.files['pro_pic']

            if file.filename == '':
                #('No selected file', flush=True)
                return render_template('profile_edit.html', error='Only allow png, jpg formats')

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = str(session['user_id']) + filename[-4:]
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                #(filename, flush=True)

                db = DatabaseByPyMySQL()
                status = db.updateUserPic(session['user_id'], filename)

                #(str(status), flush=True)
                return redirect(url_for('profile'))

        except HTTPError:
            #('Exception : ' + str(HTTPException), flush=True)
            return render_template('profile_edit.html', error='SOMETHING NOT RIGHT')

    return render_template('profile_edit.html')

@app.route('/Profile/<id>')
def public_profile(id):

    DB = DatabaseByPyMySQL()
    pro, sts = DB.getUserByID(id)

    return render_template('public_profile.html', user=pro)

@app.route('/Articles')
def article():
    DB = DatabaseByPyMySQL()
    articles, sts = DB.getAllArticles()
    articles.reverse()

    return render_template('article.html', articles=articles)

@app.route('/Articles/<no>')
def single_article(no):
    DB = DatabaseByPyMySQL()
    atricle,sts = DB.getArticleByID(no)

    return render_template('single_article.html', article=atricle)



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
    return render_template('clubs.html', userData={})

@app.route('/Buy')
def buy():
    return render_template('buy.html', userData={})

@app.route('/About')
def about():
    return render_template('about.html', userData={})


@app.route('/Admin/Login', methods=['POST', 'GET'])
def admin_login():

    if session.get('admin') is not None:
        return redirect(url_for('admin'))

    if request.method == 'POST':
        email = request.form['user_email']
        pw = request.form['user_pass']

        DB = DatabaseByPyMySQL()
        user, sts = DB.getAdminByEmail(email)

        if sts:
            pwd = computeMD5hash(pw)
            if pwd == user['pass']:

                session['admin'] = user['name']

                return redirect(url_for('admin'))
            else:
                return render_template('admin_login.html', error='Wrong password')
        else:
            return render_template('admin_login.html', error='Not Found')

    return render_template('admin_login.html')

@app.route('/Admin/Logout')
def admin_logout():
    session.pop('admin', None)

    return redirect(url_for('home'))

@app.route('/Admin')
def admin():
    if session.get('admin') is None:
        return redirect(url_for('admin_login'))

    return render_template('admin.html')

@app.route('/Admin/Auction')
def admin_auction():
    if session.get('admin') is None:
        return redirect(url_for('admin_login'))
    DB = DatabaseByPyMySQL()
    data, sts = DB.getAllAuctions()
    return render_template('admin_auction.html', auctions = data)

@app.route('/Admin/Auction/Add', methods=['GET', 'POST'])
def admin_add_auction():
    if session.get('admin') is None:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        try:
            if 'auction_image' not in request.files:
                #('No file part', flush=True)
                return render_template('admin_add_auction.html', error='No picture selected')
            file = request.files['auction_image']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                #('No selected file', flush=True)
                return render_template('admin_add_auction.html', error='Only allow png, jpg formats')

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = str(current_milli_time()) + filename[-4:]
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                #(filename, flush=True)

                try:
                    auctionName = request.form['auctionName']
                    pigeon = request.form['pigeon']
                    details = request.form['details']
                    pigeon = request.form['pigeon']
                    startDate = request.form['startDate']
                    startTime = request.form['startTime']
                    endDate = request.form['endDate']
                    endTime = request.form['endTime']


                    #('TIMES = ', startDate, startTime, endDate, endTime)
                except:
                    return render_template('admin_add_auction.html', error='Missing information')
                    #('Error = ', str(sys.exc_info()[0]), flush=True)

                auctionStart = startDate + ' '+ startTime
                auctionEnd = endDate + ' '+ endTime

                auctionStart = datetime.strptime(auctionStart, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M:%S')
                auctionEnd = datetime.strptime(auctionEnd, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M:%S')

                db = DatabaseByPyMySQL()
                status = db.addAuctionEvent(auctionName, pigeon, details, auctionStart, auctionEnd, filename)

                #(str(status), flush=True)

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
            #('Exception : ' + str(HTTPException), flush=True)
            return render_template('admin_add_auction.html', error='PLEASE FILL UP CORRECTLY')

    return render_template('admin_add_auction.html')

@app.route('/Admin/Auction/Add/Pigeons', methods=['POST','GET'])
def admin_add_auction_pigeons():
    if session.get('admin') is None:
        return redirect(url_for('admin_login'))

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
                    #('No file part PigeonMainPic'+str(i+1), flush=True)
                    return render_template('admin_add_auction_pigeons.html', error='No picture selected', data = data)
                file = request.files['PigeonMainPic'+str(i+1)]
                # if user does not select file, browser also
                # submit an empty part without filename
                if file.filename == '':
                    #('No selected file', flush=True)
                    return render_template('admin_add_auction_pigeons.html', error='Only allow png, jpg formats', data = data)

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    cur_mili = str(current_milli_time())
                    filename =  cur_mili + filename[-4:]
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    #('PigeonOthersPics'+str(i+1)+' :: '+filename, flush=True)

                    files = request.files.getlist('PigeonOthersPics'+str(i+1))
                    imNo = 0
                    otherPics = []
                    for fi in files:
                        finame = secure_filename(fi.filename)
                        finame = cur_mili +str(imNo)+ finame[-4:]
                        imNo += 1
                        fi.save(os.path.join(app.config['UPLOAD_FOLDER'], finame))
                        #('PigeonMainPic' + str(i+1) + ' :: ' + finame, flush=True)
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
                        vdo = request.form['vdo'+str(i+1)]

                    except:
                        return render_template('admin_add_auction_pigeons.html', error='Missing information', data = data)
                        #('Error = ', str(sys.exc_info()[0]), flush=True)

                    db = DatabaseByPyMySQL()
                    status = db.addPigeon(session['AuctionID'], PigeonRing, PigeonName, StartingPrice, PigeonGender, PigeonColor, BreedBy, OfferBy, PigeonDetails, session['AuctionStart'], session['AuctionEnd'], filename, otherPics, vdo)
                    #(str(status), flush=True)

            except HTTPError:
                #('Exception : ' + str(HTTPException), flush=True)
                return render_template('admin_add_auction_pigeons.html', error='SOMETHING WENT WRONG', data = data)

        return redirect(url_for('admin_auction'))

    return render_template('admin_add_auction_pigeons.html', data = data)

@app.route('/Admin/Member')
def admin_member():
    if session.get('admin') is None:
        return redirect(url_for('admin_login'))

    DB = DatabaseByPyMySQL()
    members, sts = DB.getAllMembers()

    return render_template('admin_member.html', members=members)

@app.route('/Admin/Member/Unverified', methods=['GET', 'POST'])
def admin_member_unverified():
    if session.get('admin') is None:
        return redirect(url_for('admin_login'))

    DB = DatabaseByPyMySQL()
    members, sts = DB.getUnverifiedMembers()

    if request.method == 'POST':
        try:
            user_id = request.form['verify']
            #(user_id)
            DB.verifyMember(user_id, session['admin'])
            return redirect(url_for('admin_member_unverified'))

        except HTTPError:
            #('Exception : ' + str(HTTPException), flush=True)
            return redirect(url_for('admin_member_unverified'))


    return render_template('admin_member_unverified.html', members=members)

@app.route('/Admin/Member/Verified', methods=['GET','POST'])
def admin_member_verified():
    if session.get('admin') is None:
        return redirect(url_for('admin_login'))

    DB = DatabaseByPyMySQL()
    members, sts = DB.getVerifiedMembers()

    if request.method == 'POST':
        try:
            user_id = request.form['unverify']
            #(user_id)
            DB.unverifyMember(user_id, session['admin'])
            return redirect(url_for('admin_member_verified'))

        except HTTPError:
            #('Exception : ' + str(HTTPException), flush=True)
            return redirect(url_for('admin_member_verified'))

    return render_template('admin_member_verified.html', members=members)


@app.route('/Admin/Article', methods=['GET', 'POST'])
def admin_article():
    if session.get('admin') is None:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        try:
            if 'pic' not in request.files:
                #('No file part', flush=True)
                return render_template('admin_article.html', error='No picture selected')
            file = request.files['pic']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                #('No selected file', flush=True)
                return render_template('admin_article.html', error='Only allow png, jpg formats')

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = str(current_milli_time()) + filename[-4:]
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                #(filename, flush=True)

                try:
                    title = request.form['title']
                    para1 = request.form['para1']
                    para2 = request.form['para2']

                except:
                    return render_template('admin_article.html', error='Missing information')
                    #('Error = ', str(sys.exc_info()[0]), flush=True)


                db = DatabaseByPyMySQL()
                status = db.addArticle(title, para1, para2, session['admin'], filename)

                #(str(status), flush=True)
            return render_template('admin_article.html', error='Article added')

        except HTTPError:
            #('Exception : ' + str(HTTPException), flush=True)
            return render_template('admin_article.html', error='PLEASE FILL UP CORRECTLY')


    return render_template('admin_article.html', userData={})

@app.route('/Admin/Club')
def admin_club():
    if session.get('admin') is None:
        return redirect(url_for('admin_login'))

    return render_template('admin_club.html', userData={})


def computeMD5hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


if __name__ == '__main__':
    app.debug = True
    app.run()
