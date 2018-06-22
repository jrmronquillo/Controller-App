from flask import (Flask, render_template, request, redirect, jsonify, url_for,
                   flash)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, CategoryItem, User, PostData, TestCases, TestSteps, TestCasesV2

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

import datetime
import pytz
import tzlocal

import socket    # used for TCP/IP communication
import smtplib   # used to send email report
import time      # used to insert current date in email report
import sys
import os
import subprocess

from handlers.decorators import (login_required, category_exists, item_exists,
                                 user_created_category, user_created_item, jsonp, 
                                 testcase_exists, clear_db, update_DB_with_files)
# separate config file to distinguish between test and production configurations
import testConfig
import prodConfig

config = testConfig


app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"


engine = create_engine('sqlite:///catalogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


import telnetlib
import socket

def setVideo(config):
    # config variable designed be a dictionary of video routes
    print config

    # map am integer from 1-16 to desginated router channel
    channel = {"1":"128", "2":"129", "3":"130", "4":"131",
           "5":"132", "6":"133", "7":"134", "8":"135",
                   "9":"136", "10":"137", "11":"138", "12":"139",
                   "13":"140", "14":"141", "15":"142", "16":"143"}
    rs = []
    racks = []
    slots = []
    # generate rack representation in a list
    for i in range (12):
        racks.append("r"+str(i+1))
    print racks
    for j in range(16):
        slots.append("s"+str(j+1))
    print slots
    for k in racks:
        for l in slots:
            rs.append(k+l)
    print rs

    # generate message to to send to video router
    routerInputs = []   
    for key, value in config.items():
        print key
        print value
        routerPort = str(channel[key])
        sourcePosition = str(rs.index(value))
        print routerPort + " " + sourcePosition
        routerInputs.append(routerPort + " " + sourcePosition)
    print routerInputs

    # connect to video router and send generated message
    tn = telnetlib.Telnet("10.23.223.202", "9990")
    tn.write("VIDEO OUTPUT ROUTING:\n")
    for route in routerInputs:  
        print route     
        tn.write(route)
        tn.write("\n")
    tn.write("\n")
    tn.read_until("ACK", 2)
    tn.close()

    return "routeVideo function executed!"
# customConfig = {"1":"r2s10", "2":"r2s11"}
# setVideo(customConfig)

def configMultiviewer(mode):
    tn = telnetlib.Telnet("10.23.223.93", "9990")
    tn.write("CONFIGURATION:\n")
    if mode == "true":
        tn.write("Solo enabled: true\n")
    elif mode == "false":
        tn.write("Solo enabled: false\n")
    else:
        return "error"
    tn.write("\n")
    tn.read_until("ACK", 2)
    tn.close()
    return "config multiviewer!"

def setSolo(position):
    print position 
    tn = telnetlib.Telnet("10.23.223.93", "9990")
    tn.write("VIDEO OUTPUT ROUTING:\n")
    # 16 position
    msg = "16 "+str(position)+"\n"
    tn.write(msg)
    tn.write("\n")
    # auto set solo to on
    tn.write("CONFIGURATION:\n")
    tn.write("Solo enabled: true\n")
    tn.write("\n")
    tn.close()
    return "set solo executed"

def keySendv2(rack,key,slot):
    TCP_IP = '10.23.223.36'
    TCP_PORT = 40000
    BUFFER_SIZE = 1024
    MESSAGE = 'MAC="' + rack + '" dataset="RC71" signal="' + key + '" output="' + slot + '" \n'
    # Open socket, send message, close scoket
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.settimeout(5)
    p.connect((TCP_IP, TCP_PORT))
    p.send(MESSAGE)
    data = p.recv(BUFFER_SIZE)
    p.close()
    print "Return Data: " + str(data) + key
    return "keySend Output"

def keySendv3(commandParams):
    for i in commandParams:
        print i
        # keySendv2(rack,key, slot)
 

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)
    # return "The current session state is %s" % login_session['state']


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is '
                                            'already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doens't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;"'
    output += '"-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    # print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/'
    url += 'revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        response = make_response(json.dumps('Failed to revoke token for '
                                            'given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Test to see if socket is reachable
@app.route('/check', methods=['GET', 'POST'])
def check():
    conn = httplib2.Http('www.google.com')  # I used here HTTP not HTTPS for simplify
    conn.request('HEAD', '/')  # Just send a HTTP HEAD request 
    res = conn.getresponse()

    if res.status == 200:
        print "ok"
    else:
        print "problem : the query returned %s because %s" % (res.status, res.reason) 

# Test page for development
@app.route('/test', methods=['GET', 'POST'])
@app.route('/test/', methods=['GET', 'POST'])
# @login_required
def test():
    if request.method == 'POST':
        print 'test'
        print request.form
        test=request.form.to_dict()
        print test
        print "test:"+test['name']
        if 'rack' in request.form:
            rack=request.form['rack']
            print "Rack was in request form"
        else:
            print "Rack was not found in request form"
            error = "Rack was not selected, please select rack to continue."
        return render_template('controller_main.html', error=error)
    else:
        return render_template('controller_main.html')

@app.route('/testingPage', methods=['GET', 'POST'])
def testingPage():
    return render_template('testingPage.html')

@app.route('/testingPage2', methods=['GET', 'POST'])
def testingPage2():
    return render_template('testingPage2.html')


@app.route('/setVideo/', methods=['GET', 'POST'])
def configVideo():
    defaultConf = {
                    "1":"r3s1", "2":"r3s2", "3":"r3s3", "4":"r3s4",
                    "5":"r3s5","6":"r4s6", "7":"r3s7", "8":"r3s8",
                    "9":"r1s1", "10":"r1s2", "11":"r1s3", "12":"r1s4",
                    "13":"r1s5", "14":"r1s6", "15":"r1s7", "16":"r1s8"
                }
    allclientsConf = {
                    "1":"r2s1", "2":"r2s2", "3":"r2s3", "4":"r2s4",
                    "5":"r2s5", "6":"r2s6", "7":"r2s7", "8":"r2s8",
                    "9":"r2s9", "10":"r2s10", "11":"r2s11", "12":"r2s12",
                    "13":"r2s13", "14":"r2s14", "15":"r2s15", "16":"r2s16"
    }

    allserversConf = {
                    "1":"r3s1", "2":"r3s2", "3":"r3s3", "4":"r3s4",
                    "5":"r3s5", "6":"r3s6", "7":"r3s7", "8":"r3s8",
                    "9":"r3s9", "10":"r3s10", "11":"r3s11", "12":"r3s12",
                    "13":"r3s13", "14":"r3s14", "15":"r3s15", "16":"r3s16"   
    }

    quadConf = {
                    "1":"r3s8", "2":"r2s15", "3":"r3s5", "4":"r2s10",
                    "5":"r2s14", "6":"r2s16", "7":"r2s9", "8":"r2s11",
                    "9":"r3s1", "10":"r2s2", "11":"r3s2", "12":"r2s5",
                    "13":"r2s1", "14":"r2s3", "15":"r2s4", "16":"r2s6"   
    }

    b12 = {
        "1":"r3s8", "2":"r2s15", "3":"r3s5", "4":"r2s10",
                    "5":"r2s14", "6":"r2s16", "7":"r2s9", "8":"r2s11",
                    "9":"r3s1", "10":"r2s2", "11":"r3s2", "12":"r2s5",
                    "13":"r2s1", "14":"r2s3", "15":"r2s4", "16":"r2s6"  
    }

    if request.method == 'POST':
        postData =  request.form.get('multiviewerProfile')
        print postData
        soloConfig = request.form.get('soloConfig')
        if postData == "defaultConf":
            setVideo(defaultConf)
            print "default conf"
        elif postData == "allserversConf":
            setVideo(allserversConf)
            print "all servers conf"
        elif postData == "allclientsConf":
            setVideo(allclientsConf)
            print "all clients conf"
        elif postData == "quadConf":
            setVideo(quadConf)
            print "quad conf"
        elif postData == "solo":
            configMultiviewer("true")
            print "configMultiviewer attempted!"
        elif postData == "nosolo":
            configMultiviewer("false")
            print "configMutliviewer attempted!"
        else:
            print "error with multiviewerProfile"
        
        print "solo config:"
        print soloConfig
        acceptedInput = [
                         "0","1", "2", "3", "4", "5", "6", "7", "8",
                         "9", "10", "11", "12", "13", "14", "15"
                        ]
        if soloConfig in acceptedInput:
            setSolo(soloConfig)
        else:
            print "Error with input to for Solo Route Change"
        print "attempted to set video configs"
        return render_template('set_video.html')
    else:
        return render_template('set_video.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/controller/')
@app.route('/controller/<string:button_set>/', methods=['GET', 'POST'])
@app.route('/controller/<string:button_set>/<string:quad>/', methods=['GET', 'POST'])
@app.route('/controller/<string:button_set>/<string:quad>/<int:rack_id>/', methods=['GET', 'POST'])
@app.route('/controller/<string:button_set>/<string:quad>/<int:rack_id>/<string:slot_id>/', methods=['GET', 'POST'])
@app.route('/controller/<string:button_set>/<string:quad>/<int:rack_id>/<string:slot_id>/', methods=['GET', 'POST'])
# login_required
def testB(button_set="main", rack_id="0", slot_id="0", quad='noQuad'):
    # if not rack_id:
    #    return "rack_id was undefined"
    print "button_set:"
    print button_set
    print "quad:"
    print quad 
    rack_macs = {"0":"00-80-A3-A2-D9-13", "1":"00-80-A3-A9-E3-68", 
                 "2":"00-80-A3-A9-E3-6A", "3":"00-80-A3-A9-E3-7A", 
                 "4":"00-80-A3-A9-DA-67", "5":"00-80-A3-A9-E3-79", 
                 "6":"00-80-A3-A9-E3-78", "7":"00-80-A3-9E-67-37", 
                 "8":"00-80-A3-9D-86-D5", "9":"00-80-A3-9E-67-34",
                 "10":"00-80-A3-9E-67-27", "11":"00-80-A3-9D-86-CF",
                 "12":"00-80-A3-9E-67-35", "13":"00-20-4A-BD-C5-1D",
                 "14":"00-80-A3-9D-86-D2", "15":"00-80-A3-9E-67-3B",
                 "16":"00-80-A3-9E-67-36", "17":"00-80-A3-9E-67-32",
                 "18":"00-80-A3-9D-86-D6", "19":"00-80-A3-9D-86-D3",
                 "20":"00-80-A3-9D-86-D1", "21":"00-80-A3-9D-86-D0",
                 "22":"00-20-4A-DF-64-55", "23":"00-80-A3-A1-7C-3C",
                 "24":"00-80-A3-A2-48-5C", "25":"00-20-4A-DF-65-A0",
                 "26":"00-80-A3-9E-67-3A"}

    t9_trans = {"a":"2", "b":"22", "c":"222", "d":"3", "e":"33",
                        "f":"333", "g":"4", "h":"44", "i":"444",
                        "j":"5", "k":"55", "l":"555", "m":"6", "n":"66",
                        "o":"666", "p":"7", "q":"77", "r":"777",
                        "s":"7777", "t":"8", "u":"88", "v":"888", 
                        "w":"9", "x":"99", "y":"999", "z":"9999"
                        }
    
    #if button_set == "letters":
    #    return render_template("controller_main_letters.html", button_set=button_set, quad=quad)
    #elif button_set == "numbers":
    #    return render_template('controller_numbers.html', button_set=button_set, quad=quad)
    #else:
    #    return render_template('controller_main.html', button_set=button_set, quad=quad)


    print rack_macs.get(str(rack_id))
    print "slot id:"+str(slot_id)
    selectedRack = rack_macs.get(str(rack_id))
    if not selectedRack:
        print "checking quad"
        if quad != "true":
            print "No valid Rack Selected"
            flash("Please select Rack" )
            return render_template('controller_main.html', button_set=button_set, quad=quad)


    

    if request.method == 'POST':
        if not selectedRack:
            if quad != "true":
                print "No valid Rack Selected"
                flash("Please select Rack")
                return render_template('controller_main.html', button=button_set, quad=quad)  

        test=request.form.to_dict()
        print "POST Data:"+str(test)
        
        # function for implementing sending to two racks at once
        #ke
        #ksTest = request.form.get('keySendTest')
        #print ksTest
        #if ksTest == "qwerty":
        #    testList = {
        #                "rack":"rack1",
        ##                "command":"menu",
        #                "slot":"1"
        #                }
                        
        #    keySendv3(testList)
        #    return "kstest executed"



        # Validation for slot id
        if slot_id != "0":
            print "slot id detected"
            slotVar = str(slot_id)
            print "slotVar:"+str(slotVar)
        else:
            print "no slot id detected, sending command to all stbs in rack"
            slotVar = "1-16"
        var1 = test.get('name', '')
        print "var1:"
        print var1
        alphaVar = test.get('name2', '')
        
        keyword = test.get('keyword', '')
        print keyword
        #------
        print "quad mode:" + str(quad)
      
        # check for keyword flag
        if keyword:
            print keyword
            check=""
            for letter in keyword:
                    print "letter:"+letter
                    digitVer = t9_trans.get(letter)
                    print "digitVer:"+digitVer
                    testArray = []
                    for char in digitVer:
                        print "Char:" + char
                        testArray.append(char)
                        #keySendv2(selectedRack, k, slotVar)
                    print testArray
                    print "char after loop:" +char
                    if check == char:
                        print "comparision passed!"
                        #time.sleep(5)
                        keySendv2(selectedRack, "rightArrow", slotVar)
                    # sENd ir command
                    for testArrayItem in testArray:
                        print "testArrayItem:"+testArrayItem
                        keySendv2(selectedRack, testArrayItem, slotVar)
                    print "last number command sent:"+testArrayItem
                    check = testArrayItem
            pass
        

        if var1:
            print 'detected value in var1'
            if var1.isnumeric():
                print "numeric command detected, iterating through numbers before sending commands"
                print "quad mode:" + str(quad)
                if quad == 'true':
                    print rack_macs["3"]
                    for c in var1:
                        keySendv2(rack_macs["3"], c, '1,2,9,8')
                        keySendv2(rack_macs["2"], c, '1,2,3,4,5,6,9,10,11,14,15,16')
                    return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id)
                else:
                    for c in var1:
                        keySendv2(selectedRack, c, slotVar)
                    return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id)
            else:
                print "command string detected, sending command directly"
                if quad == 'true':
                    keySendv2(rack_macs["3"], var1, '1,2,9,8')
                    keySendv2(rack_macs["2"], var1, '1,2,3,4,5,6,9,10,11,14,15,16')
                    #return render_template('controller_main.html')
                else:
                    print "slot var:"
                    print slotVar
                    keySendv2(selectedRack, var1, slotVar)
        elif alphaVar:
            print 'name2 contents: '+ alphaVar
          
            if alphaVar in t9_trans:
                print 'valid letter input found, translating to t9'
                for i in t9_trans.get(alphaVar):
                    keySendv2(selectedRack, i, slotVar)
                return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id) 
            else:
                message = 'invalid input detected, command was not sent'
                print message
                return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id, error=message)    
        else:
            message = 'Error with Post Data Input'
            print 'Error with Post Data Input'
            return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id, error=message)
        return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id)
    else:
        print "request was not POST"
        return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id)


@app.route('/dev')
def dev():
    return render_template('dev.html')

@app.route('/keySendTest')
@app.route('/keysendTest/', methods=['GET', 'POST'])
def keySendTest():
    rack_macs = {"0":"00-80-A3-A2-D9-13", "1":"00-80-A3-A9-E3-68", 
                 "2":"00-80-A3-A9-E3-6A", "3":"00-80-A3-A9-E3-7A", 
                 "4":"00-80-A3-A9-DA-67", "5":"00-80-A3-A9-E3-79", 
                 "6":"00-80-A3-A9-E3-78", "7":"00-80-A3-9E-67-37", 
                 "8":"00-80-A3-9D-86-D5", "9":"00-80-A3-9E-67-34",
                 "10":"00-80-A3-9E-67-27", "11":"00-80-A3-9D-86-CF",
                 "12":"00-80-A3-9E-67-35", "13":"00-20-4A-BD-C5-1D",
                 "14":"00-80-A3-9D-86-D2", "15":"00-80-A3-9E-67-3B",
                 "16":"00-80-A3-9E-67-36", "17":"00-80-A3-9E-67-32",
                 "18":"00-80-A3-9D-86-D6", "19":"00-80-A3-9D-86-D3",
                 "20":"00-80-A3-9D-86-D1", "21":"00-80-A3-9D-86-D0",
                 "22":"00-20-4A-DF-64-55", "23":"00-80-A3-A1-7C-3C",
                 "24":"00-80-A3-A2-48-5C", "25":"00-20-4A-DF-65-A0"}
    print "key Send Test!"
    rack = rack_macs["3"]
    slotVar = "1,2,8,9"
    print rack, slotVar
    keySendv2(rack, "menu", slotVar)
    return "keysend Test!"

@app.route('/shef', methods=['GET', 'POST'])
@app.route('/shef/', methods=['GET', 'POST'])
def shefCommands():
    return render_template('shef.html')

@app.route('/sampleApp', methods=['GET', 'POST'])
@app.route('/sampleApp', methods=['GET', 'POST'])
def sampleApp():
    return render_template('sampleApp.html')

@app.route('/postTest', methods=['GET', 'POST'])
@app.route('/postTest/', methods=['GET', 'POST'])
def postTest():
    #r = requests.post("http://localhost:5000/postTest", data={'foo': 'bar'})
    #rint (r.text)

    if request.method == 'POST':
        print request.form['name']

        d = datetime.datetime.now()
        d_utc = datetime.datetime.utcnow()
        localTZ = tzlocal.get_localzone()
        tt = d_utc.replace(tzinfo=pytz.utc).astimezone(localTZ).strftime("%b %-d %H:%M:%S")
        print tt

        newData = PostData(data=request.form['name'], green=True, formatted_date=tt)
        session.add(newData)
        session.commit()
    else:
        print "Get request executed"
        timeVar = time.strftime('%b %-d %H:%M:%S', time.gmtime())
        print timeVar  
        print request.args.get('name', '')
        newData = PostData(data=request.args.get('name', ''), 
                           green=request.args.get('green', ''),
                           formatted_date=timeVar
                           )
        session.add(newData)
        session.commit()
    return render_template('postTest.html')
    

@app.route('/reporting', methods=['GET', 'POST'])
@app.route('/reporting/', methods=['GET', 'POST'])
def reporting():
    data = session.query(PostData).all()
    print "data:"+str(data) 
    for item in data:
        print item.id
        print item.data
    return render_template('reporting.html', data=data)

@app.route('/reporting/JSON')
@jsonp
def reportingJSON():
    data = session.query(PostData).all()

    return jsonify(dataList=[i.serialize for i in data])

@app.route('/pythonTest')
def pythonTest():
    var = datetime.datetime.now().time()
    var2 = datetime.datetime.now().strftime("%-m/%-d/%y")
    return "python test executed: " + str(var)+ " " + str(var2)

@app.route('/scriptStart/', methods=['GET','POST'])
def scriptStart():
    if request.method == 'POST':
        script_id = request.form['script_id']
        if script_id:
            test_cases = session.query(TestCasesV2).filter_by(id=script_id).all()
            if test_cases:
                for i in test_cases:
                    name = i.name
                    path = i.path
                    commandString = "stbt run "+path
                    print commandString
                    p = subprocess.Popen(commandString, shell=True)
            else:
                message = "Did not find any matching test cases with that id, did not run script"
                print message
                return message
        else:
            message = "script_id needed to start script"
            print message
            return message
        return render_template('scriptStart.html', output=p)
    else:
        return render_template('scriptStart.html')

@app.route('/screenshot/', methods=['GET','POST'])
def screenshot():
    commands = config.config['screenshot_config']
    command =  commands[0]['command']
    defaultCommand = commands[0]['defaultCommand']
    if request.method == 'POST':
        data=request.form.to_dict()
        if data:
            screenshotName = data['name']
            completeCommand = str(command) + "%s%s"  % (screenshotName, ".png")
            print completeCommand
            
            # with configs:
            p = subprocess.Popen(completeCommand, shell=True)
        else:
            p = subprocess.Popen(defaultCommand, shell=True)
            
        output = p
        print output
        return render_template('screenshot.html', output=output)
    else:
        return render_template('screenshot.html')

@app.route('/testcases/', methods=['GET', 'POST'])
@clear_db
@update_DB_with_files
def showTestCases():  
    test_cases = session.query(TestCasesV2).all()
    return render_template("testcases.html", test_cases=test_cases)
    
@app.route('/testcases/JSON')
@jsonp
@clear_db
@update_DB_with_files
def testcasesJSON():
    testcases = session.query(TestCasesV2).all()
    return jsonify(testcaseList=[i.serialize for i in testcases])

@app.route('/testcase/new/', methods=['GET', 'POST'])
def createTestCase():
    if request.method == 'POST':
        if 'name' in request.form:
            print "found name"
        else:
            print "request.form was null"
            return "request.form was null"
        
        scriptname=str(request.form['name'])
        
        # replaces whitespace with underscore, to avoid error with any modifications of linux directory
        editedScriptname=scriptname.replace(" ", "_")
        # print editedScriptname
        
        path = config.config['createtestcase_config'][0]['dir_path']
        complete_path = str(path) + editedScriptname  
        command = "mkdir %s" % complete_path
        
        #print command
        p = subprocess.check_output(command, shell=True)

        # below is deprecated, no longer necessary to store name in DB manually. 
        # /testcases/JSON will instead check available files in
        # main directory and store representation in DB automatically.
        #
        # testcase_info = TestCases(name=request.form['name'], path=completePath)
        # session.add(testcase_info)
        # session.commit()
        return redirect(url_for('showTestCases'))
    else:
        return render_template('newtestcase.html')

@app.route('/testcases/<int:testcase_id>/')
@app.route('/testcases/<int:testcase_id>/steps/', methods=['GET', 'POST'])
def showCaseSteps(testcase_id):
    items = session.query(TestSteps).filter_by(
        testcase_id=testcase_id).all()

    if request.method == 'POST':
        stepData = request.form['keypress']
        newStep = TestSteps(testcase_id=testcase_id,
                           step=stepData
                           )
        session.add(newStep)
        session.commit()
        return redirect(url_for('showCaseSteps', testcase_id=testcase_id))
    return render_template('steps.html', testcase_id=testcase_id, items=items)

@app.route('/testcases/<int:testcase_id>/steps/new/', methods=['GET', 'POST'])
def newStep(testcase_id):
    if request.method == 'POST':
        stepData = request.form['stepData']
        newStep = TestSteps(testcase_id=testcase_id,
                           step=stepData
                           )
        session.add(newStep)
        session.commit()
        return redirect(url_for('showCaseSteps', testcase_id=testcase_id))
    else: 
        return render_template('newStep.html')

@app.route('/testcases/<int:testcase_id>/steps/JSON')
@jsonp
def stepsJSON(testcase_id):
    items = session.query(TestSteps).filter_by(
        testcase_id=testcase_id).all()
    return jsonify(teststeps=[i.serialize for i in items])

@app.route('/testcases/<int:testcase_id>/delete/', methods=['GET', 'POST'])
@testcase_exists
@clear_db
@update_DB_with_files
def deleteTestCase(testcase_id):
    # initialize object for designated testcase_id    
    testcaseToDelete = session.query(TestCasesV2).filter_by(id=testcase_id).first()
    if request.method == 'POST':
        # delete file from directory

        fileToDelete =  str(testcaseToDelete.name).replace(" ", "\ ")
        print fileToDelete
        print "sss"
        # create command using providing configurations
        fileToDelete =  str(testcaseToDelete.name).replace(" ","\ ")
        print fileToDelete
        
        # create command using provided configurations
        commandPath = config.config['deletetestcase_config'][0]['delete_command']
        command = commandPath + "%s" % fileToDelete 
        print command
        p = subprocess.check_output(command, shell=True)
        
        #delete file from DB
        session.delete(testcaseToDelete)
        session.commit()
        return redirect(url_for('showTestCases'))    
    else:
        return render_template('deleteTestCase.html')

@app.route('/tester/', methods=['GET', 'POST'])
def testerAPI():
    #if request.method == 'POST':
    d = datetime.datetime.now()
    d_utc = datetime.datetime.utcnow()
    localTZ = tzlocal.get_localzone()
    tt = d_utc.replace(tzinfo=pytz.utc).astimezone(localTZ).strftime("%b %-d %H:%M:%S")
    print tt
    return tt



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.secret_key = 'super_secret_key1'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
