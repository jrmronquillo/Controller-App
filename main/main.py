from flask import (Flask, render_template, request, redirect, jsonify, url_for,
                   flash)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, CategoryItem, User

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

from handlers.decorators import (login_required, category_exists, item_exists,
                                 user_created_category, user_created_item)

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"


engine = create_engine('sqlite:///catalogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def keySendv2(rack,key,slot):
    #rack = "00-80-A3-A9-E3-7A"
    #key = 'menu'
    #slot = "1-16"
    #def jKeyPress(rack, key, slot):
    #Prepare 3-byte control message for transmission
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
    #jKeyPress("00-80-A3-A9-C3-7A", "menu", "1-16")
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


# API endpoint for All Categories
@app.route('/categories/JSON')
def showCategoriesJSON():
    categories = session.query(Categories).all()

    return jsonify(categorylist=[i.serialize for i in categories])


# Making an API endpoint (GET request)
@app.route('/categories/<int:category_id>/item/JSON')
def showItemsJSON(category_id):
    category = session.query(Categories).filter_by(id=category_id).first()
    if category is not None:
        items = session.query(CategoryItem).filter_by(
         category_id=category_id).all()
        return jsonify(categoryItems=[i.serialize for i in items])
    else:
        return ''


# show all categories
@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Categories).all()
    if 'username' not in login_session:
        tme = datetime.datetime.utcnow()
        return render_template('publiccategories.html',
                               categories=categories,
                               tme=tme)
    else:
        return render_template('categories.html', categories=categories)


# create new category
@app.route('/categories/new/', methods=['GET', 'POST'])
@login_required
def newCategory():
    if request.method == 'POST':
        newCategory = Categories(name=request.form['name'],
                                 user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


# edit category
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
@category_exists
@user_created_category
def editCategory(category_id):
    editedCategory = session.query(
        Categories).filter_by(id=category_id).first()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            return redirect(url_for('showCategories'))
    else:
        return render_template(
            'editCategory.html', category=editedCategory)


# delete category
@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
@category_exists
@user_created_category
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Categories).filter_by(id=category_id).first()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template(
                'deleteCategory.html', category=categoryToDelete)

#Show User Dates
@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/dates/')
def showDates(category_id):
    return render_template('dates.html')


# Show a category item
@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/')
@category_exists
def showItems(category_id):
    category = session.query(Categories).filter_by(id=category_id).first()
    creator = getUserInfo(category.user_id)
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()
    if ('username' not in login_session):
        return render_template('publicitem.html',
                               items=items,
                               category=category,
                               creator=creator)
    else:
        return render_template('item.html',
                               items=items,
                               category=category,
                               creator=creator)


# Create a category item
@app.route('/categories/<int:category_id>/item/new/', methods=['GET', 'POST'])
@login_required
def newItem(category_id):
    if request.method == 'POST':
        newCategoryItem = CategoryItem(name=request.form['name'],
                                       description=request.form['description'],
                                       user_id=login_session['user_id'],
                                       category_id=category_id)
        session.add(newCategoryItem)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newCategoryItem.html', category_id=category_id)


# Edit a category item
@app.route('/categories/<int:category_id>/item/<int:categoryitem_id>/edit/',
           methods=['GET', 'POST'])
@login_required
@item_exists
@user_created_item
def editItem(category_id, categoryitem_id):
    editedCategoryItem = session.query(
            CategoryItem).filter_by(
            id=categoryitem_id).filter_by(category_id=category_id).first()
    if request.method == 'POST':
        if request.form['name']:
            editedCategoryItem.name = request.form['name']
        if request.form['description']:
            editedCategoryItem.description = request.form['description']
            return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template(
                'editCategoryItem.html',
                category_id=category_id,
                item=editedCategoryItem
                )


# Delete a category item
@app.route('/categories/<int:category_id>/item/<int:categoryitem_id>/delete/',
           methods=['GET', 'POST'])
@login_required
@item_exists
@user_created_item
def deleteItem(category_id, categoryitem_id):
    categoryitemToDelete = session.query(
        CategoryItem).filter_by(
        id=categoryitem_id).filter_by(category_id=category_id).first()
    if request.method == 'POST':
        session.delete(categoryitemToDelete)
        session.commit()
        return redirect(
            url_for('showItems', category_id=category_id))
    else:
        return render_template(
                    'deleteItem.html',
                    category_id=category_id,
                    categoryitem=categoryitemToDelete
                            )


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
        #rack=request.form['rack']
        #name=request.form['name']
        #name2=request.form['name2']
        #print name
        #print name2
        #print rack
        #print request.method
        #num=request.form['num']
        #print rack
        #print rack
        #print "num=" + num
        #print request.form['value']
        ##keySendv2("00-80-A3-A9-E3-7A", name, "1-16")
        return render_template('test.html')
    else:
        return render_template('test.html')

@app.route('/test/<int:rack_id>/', methods=['GET', 'POST'])
@app.route('/test/<int:rack_id>/<int:slot_id>', methods=['GET', 'POST'])
def testB(rack_id, slot_id="0"):
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
        return "Error: No valid Rack Selected"

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
                return render_template('test.html')
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
                return render_template('test.html') 
            else:
                message = 'invalid input detected, command was not sent'
                print message
                return render_template('test.html', error=message)    
        else:
            message = 'Error with Post Data Input'
            print 'Error with Post Data Input'
            return render_template('test.html', error=message)
        #command = test['name']
        #if command.isnumeric():
        #    for c in command:
        #        keySendv2(selectedRack, c, slotVar)
        #    return render_template('test.html')
        #else:
        #    print 'case2'
        #    keySendv2(selectedRack, command, slotVar)

        #print "command:"+command
        return render_template('test.html')
    else:
        return render_template('test.html')




    



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.secret_key = 'super_secret_key1'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
