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

import socket    # used for TCP/IP communication
import smtplib   # used to send email report
import time      # used to insert current date in email report
import sys
import os
import subprocess

from handlers.decorators import (login_required, category_exists, item_exists,
                                 user_created_category, user_created_item, jsonp, 
                                 testcase_exists, clear_db)
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


def keySendv2(rack,key,slot):
    TCP_IP = '10.23.223.36'
    TCP_PORT = 40000
    BUFFER_SIZE = 1024
    MESSAGE = 'MAC="' + rack + '" dataset="RC71" signal="' + key + '" output="' + slot + '" \n'
    #Open socket, send message, close scoket
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.connect((TCP_IP, TCP_PORT))
    p.send(MESSAGE)
    data = p.recv(BUFFER_SIZE)
    p.close()
    print "Return Data: " + str(data) + key
    return "keySend Output"


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
@login_required
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

@app.route('/')
@app.route('/test/<int:rack_id>/', methods=['GET', 'POST'])
@app.route('/test/<int:rack_id>/<int:slot_id>', methods=['GET', 'POST'])
@login_required
def testB(rack_id=None, slot_id="0"):
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
    print rack_macs.get(str(rack_id))
    print "slot id:"+str(slot_id)
    selectedRack = rack_macs.get(str(rack_id))
    if not selectedRack:
        print "No valid Rack Selected"
        return render_template('index.html')

    if request.method == 'POST':
        test=request.form.to_dict()
        print "POST Data:"+str(test)
        
        # Validation for slot id
        if slot_id != "0":
            print "slot id detected"
            slotVar = str(slot_id)
            print "slotVar:"+str(slotVar)
        else:
            print "no slot id detected, sending command to all stbs in rack"
            slotVar = "1-16"
        var1 = test.get('name', '')
        alphaVar = test.get('name2', '')
        if var1:
            print 'detected value in var1'
            if var1.isnumeric():
                print "numeric command detected, iterating through numbers before sending commands"
                for c in var1:
                    keySendv2(selectedRack, c, slotVar)
                return render_template('controller_main.html')
            else:
                print "command string detected, sending command directly"
                keySendv2(selectedRack, var1, slotVar)
        elif alphaVar:
            print 'name2 contents: '+ alphaVar
            t9_trans = {"a":"2", "b":"22", "c":"222", "d":"3", "e":"33",
                        "f":"333", "g":"4", "h":"44", "i":"444",
                        "j":"5", "k":"55", "l":"555", "m":"6", "n":"66",
                        "o":"666", "p":"7", "q":"77", "r":"777",
                        "s":"7777", "t":"8", "u":"88", "v":"888", 
                        "w":"9", "x":"99", "y":"999", "z":"9999"
                        }
            if alphaVar in t9_trans:
                print 'valid letter input found, translating to t9'
                for i in t9_trans.get(alphaVar):
                    keySendv2(selectedRack, i, slotVar)
                return render_template('controller_main.html') 
            else:
                message = 'invalid input detected, command was not sent'
                print message
                return render_template('controller_main.html', error=message)    
        else:
            message = 'Error with Post Data Input'
            print 'Error with Post Data Input'
            return render_template('controller_main.html', error=message)
        return render_template('controller_main.html')
    else:
        return render_template('controller_main.html')

@app.route('/postTest', methods=['GET', 'POST'])
@app.route('/postTest/', methods=['GET', 'POST'])
def postTest():
    #r = requests.post("http://localhost:5000/postTest", data={'foo': 'bar'})
    #rint (r.text)

    if request.method == 'POST':
        print request.form['name']
        newData = PostData(data=request.form['name'], green=True)
        session.add(newData)
        session.commit()
    else:
        print "Get request executed"
        print request.args.get('name', '')
        newData = PostData(data=request.args.get('name', ''), 
                           green=request.args.get('green', '')
                           )
        session.add(newData)
        session.commit()
    return render_template('postTest.html')
    

@app.route('/reporting', methods=['GET', 'POST'])
@app.route('/reporting/', methods=['GET', 'POST'])
def reporting():
    #r =requests.post("http://localhost:5000/reporting", data={'foo': 'bar'})
    #if request.method == 'POST':
    #    data = request.form['foo']
    #    print data
    #    return "Post data detected"
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
        # need function to take script_id and return test script name from DB
        # POST version:
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
        # p = subprocess.Popen("stbt run /home/e2e/e2ehost29_local/sanityAutomation/host_main_29/
        # Scoreguide/test.py")
        # p = subprocess.Popen("ls", shell=True)
        #output = p
        #print output
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
def showTestCases():  
    # grab designated command from config file
    commands = config.config['testcases_config']
    
    print commands
    print commands[0]["list_command"]

    listCommand = commands[0]["list_command"]
    p = subprocess.check_output(listCommand, shell=True)
    # print p.splitlines()
    fileArray = p.splitlines()
    for file in fileArray:
        completePath = "/home/e2e/e2ehost29_local/sanityAutomation/automation_main_28/"+file+"/test.py"
        testcase_info = TestCasesV2(name=file, path=completePath)
        session.add(testcase_info)
        session.commit()
    test_cases = session.query(TestCasesV2).all()
    return render_template("testcases.html", test_cases=test_cases)
    
@app.route('/testcases/JSON')
@jsonp
@clear_db
def testcasesJSON():
    commands = config.config['testcases_config']
    listCommand = commands[0]["list_command"]
    
    # use config file
    p = subprocess.check_output(listCommand, shell=True)
    print p.splitlines()
    fileArray = p.splitlines()
    for file in fileArray:
        completePath = "/home/e2e/e2ehost29_local/sanityAutomation/automation_main_28/"+file+"/test.py"
        testcase_info = TestCasesV2(name=file, path=completePath)
        session.add(testcase_info)
        session.commit()
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
        
        # replaces whitespace with underscore, to avoid error when creating linux directory
        editedScriptname=scriptname.replace(" ", "_")
        print editedScriptname
        
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
@app.route('/testcases/<int:testcase_id>/steps/')
def showCaseSteps(testcase_id):
    items = session.query(TestSteps).filter_by(
        testcase_id=testcase_id).all()
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
        return redirect(url_for('showCaseSteps'), testcase_id=testcase_id)
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
def deleteTestCase(testcase_id):
    # make sure db is accurate by clearing the db and repopulating it to represent the files
    # in the directory
    
    # clear the DB
    testcaseToDelete = session.query(TestCasesV2).all()
    for i in testcaseToDelete:
        session.delete(i)
        session.commit()
    
    # check what files are in the directory using 'ls' command
    listCommand = config.config['testcases_config'][0]['list_command']
    
    # prod
    p = subprocess.check_output(listCommand, shell=True)
    
    print p.splitlines()

    # take the available file names and store them in the DB
    fileArray = p.splitlines()
    for file in fileArray:
        completePath = "/home/e2e/e2ehost29_local/sanityAutomation/automation_main_28/"+file
        testcase_info = TestCasesV2(name=file, path=completePath)
        session.add(testcase_info)
        session.commit()

    # initialize object for designated testcase_id    
    testcaseToDelete = session.query(TestCasesV2).filter_by(id=testcase_id).first()
    if request.method == 'POST':
        # delete file from directory
        fileToDelete =  testcaseToDelete.name
        print fileToDelete
        
        # create command using providing configurations
        commandPath = config.config['deletetestcase_config'][0]['delete_command']
        command = commandPath + "%s" % fileToDelete 
        
        p = subprocess.check_output(command, shell=True)
        
        #delete file from DB
        session.delete(testcaseToDelete)
        session.commit()
        return redirect(url_for('showTestCases'))    
    else:
        return render_template('deleteTestCase.html')

@app.route('/tester/', methods=['GET', 'POST'])
def testerAPI():
    print os.path.dirname('testDIR/')
    #just adding some text
    #adding text for branchB
    return "tester executed"


@app.route('/testcasesv2/JSON')
@jsonp
def testcasesv2JSON():
    testcasesv2 = session.query(TestCasesV2).all()
    return jsonify(testcaseList=[i.serialize for i in testcasesv2])




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.secret_key = 'super_secret_key1'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
