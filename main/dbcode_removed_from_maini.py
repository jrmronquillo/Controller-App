# Test page for development
@app.route('/test', methods=['GET', 'POST'])
@app.route('/test/', methods=['GET', 'POST'])
# @login_required
def test():
    if request.method == 'POST':
        print('test')
        print(request.form)
        test=request.form.to_dict()
        print(test)
        print("test:"+test['name'])
        if 'rack' in request.form:
            rack=request.form['rack']
            # print "Rack was in request form"
        else:
            # print "Rack was not found in request form"
            error = "Rack was not selected, please select rack to continue."
        return render_template('controller_main.html', error=error)
    else:
        return render_template('controller_main.html')

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    print( 'In gdisconnect access token is %s', access_token)
    print('User name is: ')
    # print login_session['username']
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/'
    url += 'revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
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

@app.route('/postTest', methods=['GET', 'POST'])
@app.route('/postTest/', methods=['GET', 'POST'])
def postTest():
    #r = requests.post("http://localhost:5000/postTest", data={'foo': 'bar'})
    #rint (r.text)

    if request.method == 'POST':
        # print request.form['name']

        d = datetime.datetime.now()
        d_utc = datetime.datetime.utcnow()
        localTZ = tzlocal.get_localzone()
        tt = d_utc.replace(tzinfo=pytz.utc).astimezone(localTZ).strftime("%b %-d %H:%M:%S")
        # print tt

        newData = PostData(data=request.form['name'], green=True, formatted_date=tt)
        session.add(newData)
        session.commit()
    else:
        # print "Get request executed"
        timeVar = time.strftime('%b %-d %H:%M:%S', time.gmtime())
        # print timeVar  
        # print request.args.get('name', '')
        newData = PostData(data=request.args.get('name', ''), 
                           green=request.args.get('green', ''),
                           formatted_date=timeVar
                           )
        session.add(newData)
        session.commit()
    return render_template('postTest.html')

@app.route('/reporting/JSON')
@jsonp
def reportingJSON():
    data = session.query(PostData).all()

    return jsonify(dataList=[i.serialize for i in data])

@app.route('/testcases/', methods=['GET', 'POST'])
@clear_db
@update_DB_with_files
def showTestCases():  
    if request.method == 'POST':
        script_id = request.form['script_id']
        rack = request.form['rack']
        slot = request.form['slot']
        if script_id:
            test_cases = session.query(TestCasesV2).filter_by(id=script_id).all()
            if test_cases:
                for i in test_cases:
                    name = i.name
                    path = i.path
                    commandString = "stbt run "+path+" "+rack+" "+slot
                    # print commandString
                    p = subprocess.Popen(commandString, shell=True)
                    return redirect(url_for('reporting'))
            else:
                message = "Did not find any matching test cases with that id, did not run script"
                # print message
                return message
        else:
            message = "script_id needed to start script"
            # print message
            return message
        return render_template('testcases.html', output=p)
    else:
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
            print("found name")
        else:
            # print "request.form was null"
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
        # print fileToDelete
        # print "sss"
        # create command using providing configurations
        fileToDelete =  str(testcaseToDelete.name).replace(" ","\ ")
        # print fileToDelete
        
        # create command using provided configurations
        commandPath = config.config['deletetestcase_config'][0]['delete_command']
        command = commandPath + "%s" % fileToDelete 
        # print command
        p = subprocess.check_output(command, shell=True)
        
        #delete file from DB
        session.delete(testcaseToDelete)
        session.commit()
        return redirect(url_for('showTestCases'))    
    else:
        return render_template('deleteTestCase.html')
    
    @app.route('/blog/', methods=['GET', 'POST'])
def blog():
    blogposts = session.query(BlogPosts).all()
    # print blogposts
    for post in blogposts:
        print(post.id)
        print(post.title)
        print(post.created_date)

    if request.method == 'POST':
        # print 'blog post created!'
        blog_title = request.form.get('blog_title')
        content = request.form.get('content')
        # print blog_title
        # print content
        newPost = BlogPosts(title=blog_title, content=content
                           )
        session.add(newPost)
        session.commit()
        return render_template('blog.html', posts=blogposts)
    else:
        return render_template('blog.html', posts=blogposts)

@app.route('/blog/newPost', methods=['GET', 'POST'])
def newPost():
    if request.method == 'POST':
        post_title = request.form['blog_title']
        post_content = request.form['content']
        post_author = request.form['blog_author']
        newPost = BlogPosts(title=post_title,
                            content=post_content,
                            author=post_author
                           )
        session.add(newPost)
        session.commit()
        return redirect(url_for('blog'))
    else:
        return render_template('newPost.html')


@app.route('/blog/<int:post_id>/deletePost/', methods=['GET', 'POST'])
def deletePost(post_id):
    # print post_id
    if request.method == 'POST':   
        postToDelete = session.query(BlogPosts).filter_by(id=post_id).first()
        #delete file from DB
        session.delete(postToDelete)
        session.commit()
        return redirect(url_for('blog')) 
    else:
        return render_template('deletePost.html')

@app.route('/stbPosition/<int:id>/edit/<string:rsPosition>/', methods=['GET', 'POST'])
def editStbPosition(id, rsPosition):
    editedStb = session.query(
        Stb).filter_by(id=id).first()
    editedStb.rackslot_id = rsPosition
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            return redirect(url_for('showCategories'))
    else:
        return 'stb position edit executed'
 
@app.route('/stbs/JSON')
def showStbsJSON(): 
    rackInfo = session.query(RackSlot).all()
    return jsonify(stbInfoData=[i.serialize for i in rackInfo])
#
#@app.route('/stbs/', methods=['GET', 'POST'])
#def showStbs():
#    stbInfo = session.query(Stb).all()
#   rackInfo = session.query(RackSlot).all()
#    if request.method == 'POST':
#        rackSlotObject = RackSlot(
#                                rackNumber=request.form['rackNumber'],
#                               irnetboxMac=request.form['irnetboxMac'],
#                                slot=request.form['slot'],
#                                videoRoute=request.form['videoRoute'],
#                                stbModel=request.form['stbModel'])
#        session.add(rackSlotObject)
#        session.commit()
        #print 'stbInfo:'
        #print stbInfo
        #print 'showStb api executed'
#    return render_template('stbInfo.html', stbinfo=stbInfo, rackInfo=rackInfo)

#@app.route('/stbs/new/')
#def newStb():
#    stbs = {'1': {'mac':'001', 'slot': '2'}
#            }
#    
#    if request.method =='POST':
#        
#        newStb = Stb(mac='0000', slot='1', model='hr44-800', rackslot_id='r3s1')
#        session.add(newSTB)
#        session.commit()
#        return render_template('stbInfo.html', stbinfo='')
#    else:
        # print stbs
#        newStb = RackSlot(rackNumber='A03', irnetboxMac='00-00-01',
#                            slot='1', videoRoute='r3s1',
#                            stbModel='hr44-500')
#        session.add(newStb)
#        session.commit()
#        return render_template('stbInfo     .html', stbinfo='')


#@app.route('/editRackSlots/<string:rack_id>/', methods=['GET', 'POST'])
#def editRackSlots(rack_id):
#    rackSlotToEdit = session.query(
#        RackSlot).filter_by(id=rack_id).first()
#    print rackSlotToEdit
#    if rackSlotToEdit == None:
#        print 'Error: db entry not found'
#        return redirect(url_for('showStbs'))
#
#    if request.method == 'POST':
#        rackSlotToEdit.rackNumber = request.form['rackNumber']
#        rackSlotToEdit.irnetboxMac = request.form['irnetboxMac']
#        rackSlotToEdit.slot = request.form['slot']
#        rackSlotToEdit.videoRoute = request.form['videoRoute']
#        rackSlotToEdit.stbModel = request.form['stbModel']
#        return redirect(url_for('showStbs'))

#    return render_template('editRackSlots.html', rackSlotToEdit=rackSlotToEdit)

#@app.route('/deleteRackSlot/<string:rackslot_id>/', methods=["GET", "POST"])
#def deleteRackSlot(rackslot_id):
#    rackSlotToDelete = session.query(RackSlot).filter_by(id=rackslot_id).first()
#    #delete file from DB
#    if request.method == 'POST':
#        session.delete(rackSlotToDelete)
#        session.commit()
#        return redirect(url_for('showStbs'))
#    return render_template('deleteRackSlot.html', rackSlotToDelete=rackSlotToDelete)
# Create anti-forgery state token
#@app.route('/login')
#def showLogin():
#    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
#                    for x in xrange(32))
#    login_session['state'] = state
#    return render_template('login.html', STATE=state)
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
        print ("Token's client ID does not match app's.")
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
    print("done!")
    return output


def createStbObject():
    newSTB = Stb(mac='00-00', slot='1', model='hr44', rackslot_id='1' )
    session.add(Stb);
    return 'test'

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


