from flask import (Flask, render_template, request, redirect, jsonify, url_for,
                   flash)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Stb, RackSlot
from flask import session as login_session
import random
import string
# import urllib2 

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

import feedparser

import datetime
import pytz
import tzlocal

import socket    # used for TCP/IP communication
import smtplib   # used to send email report
import time      # used to insert current date in email report
import sys
import os
import subprocess
import re       # regex library

# used for setting cors headers
from flask_cors import CORS 

from handlers.decorators import (support_jsonp, login_required, category_exists, item_exists,
                                 user_created_category, user_created_item, jsonp, 
                                 testcase_exists, clear_db, update_DB_with_files)
# separate config file to distinguish between test and production configurations
import testConfig
import prodConfig

config = testConfig

# test text to see if this shows up in the testBranch

app = Flask(__name__)
cors = CORS(app, resources={r"/rssTest": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"


engine = create_engine('sqlite:///stbInfo.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


import telnetlib
import socket


def takeScreenshot(scriptName = 'test', imageName = 'test'):
    print ("screenshot function executed")
    localtime = time.localtime(time.time())
    command = "stbt screenshot "
    path = "/home/e2e/e2ehost_local/sanityAutomation/automation_main_28/"+scriptName+"/"
    screenshotName = imageName
    completeCommand = str(command) + "%s%s%s%s"  % (path, screenshotName, localtime, ".png")
    #print completeCommand
    
    # with configs:
    p = subprocess.Popen(completeCommand, shell=True)
    


            
        

def setVideo(config):
    # config variable designed be a dictionary of video routes
    # sample: "1":"r3s1", "2":"r3s2", "3":"r3s3", "4":"r3s4",
    #                "5":"r3s5","6":"r3s6", "7":"r3s7", "8":"r3s8",
    #                "9":"r2s1", "10":"r2s2", "11":"r2s3", "12":"r2s4",
    #                "13":"r2s5", "14":"r2s6", "15":"r2s7", "16":"r2s8"
    print ('config passed in to setVideo:')
    print(config)
    for key, value in config.items():
        #print key
        #print value
    # map an integer from 1-16 to designated router channel
        channel = {"1":"128", "2":"129", "3":"130", "4":"131",
           "5":"132", "6":"133", "7":"134", "8":"135",
                   "9":"136", "10":"137", "11":"138", "12":"139",
                   "13":"140", "14":"141", "15":"142", "16":"143"}
    
    

    rs = []
    racks = []
    slots = []
    # generate rack representation in a list
    for i in range (24):
        racks.append("r"+str(i+1))
    #print racks
    #print 'number of items?'+str(len(racks))
    for j in range(16):
        slots.append("s"+str(j+1))
    #print slots
    for k in racks:
        for l in slots:
            rs.append(k+l)
    #print rs
    
    # generate message to to send to video router
    routerInputs = []   
    for key, value in config.items():
        #print key
        #print value
        
        #----
        # issue was found with value data info on racks 14+ are not matching the proper video routes using the rack
        # representation logic from above
        # added logic below to check if data is using rack greater than 13
        # and if so, map the video routes from racks 14/15 to the proper hard coded video routes
        #-----
        rackNum = value.split('r')
        rackNum2 = rackNum[1].split('s')
        #print rackNum
        #print rackNum2[0]
        #print rackNum2[1]
        if int(rackNum2[0]) >= 14:
            updatedConfig = {
                'r14s1':'200', 'r14s2':'201', 'r14s3':'202', 'r14s4':'203',
                'r14s5':'204', 'r14s6':'205', 'r14s7':'206', 'r14s8':'207',
                'r15s1':'208', 'r15s2':'209', 'r15s3':'210', 'r15s4':'211',
                'r15s5':'212', 'r15s6':'213', 'r15s7':'214', 'r15s8':'215',
                'r16s1':'216', 'r16s2':'217', 'r16s3':'218', 'r16s4':'219',
                'r16s5':'220', 'r16s6':'221', 'r16s7':'222', 'r16s8':'223',
                'r17s1':'224', 'r17s2':'225', 'r17s3':'226', 'r17s4':'227',
                'r17s5':'228', 'r17s6':'229', 'r17s7':'230', 'r17s8':'231',
                'r18s1':'232', 'r18s2':'233', 'r18s3':'234', 'r18s4':'235',
                'r18s5':'236', 'r18s6':'237', 'r18s7':'238', 'r18s8':'239',
                'r19s1':'240', 'r19s2':'241', 'r19s3':'242', 'r19s4':'243',
                'r19s5':'244', 'r19s6':'245', 'r19s7':'246', 'r19s8':'247',
                'r20s1':'248', 'r20s2':'249', 'r20s3':'250', 'r20s4':'251',
                'r20s5':'252', 'r20s6':'253', 'r20s7':'254', 'r20s8':'255',
                'r21s1':'256', 'r21s2':'257', 'r21s3':'258', 'r21s4':'259',
                'r21s5':'260', 'r21s6':'261', 'r21s7':'262', 'r21s8':'263',

            }
            #print 'updatedConfig:'
            #print updatedConfig[value]

            sourcePosition = str(updatedConfig[value])
            #print 'initial sourcePosition:'
            #print sourcePosition
        else:
            sourcePosition = str(rs.index(value))
            #print 'default sourcePosition'
            #print sourcePosition



        routerPort = str(channel[key])
        #print routerPort + " " + sourcePosition



        routerInputs.append(routerPort + " " + sourcePosition)
    #print 'router inputs:'
    #print routerInputs

    # connect to video route and multiviewer
    # video route
    
    #-----
    tn = telnetlib.Telnet("10.23.223.202", "9990")
    


    # send generated message to video router
    
    # tn.write("VIDEO OUTPUT ROUTING:\n")
    tn.write(("VIDEO OUTPUT ROUTING:\n").encode('ascii'))
    for index,route in enumerate(routerInputs):       
        print(type(route))
        print(route)
        tn.write(route.encode('ascii'))
        tn.write(("\n").encode('ascii'))
    tn.write(("\n").encode('ascii'))
    tn.read_until(("ACK").encode('ascii'), 2)
    tn.close()
    #----

    return "routeVideo function executed!"

# customConfig = {"1":"r2s10", "2":"r2s11"}
# setVideo(customConfig)
def setLabels(labelArr):
    #print'setLabels backend function:'
    #print labelArr
    stbModels = {"r3s1":"H44-500", "r3s2":"HR54-700", "r3s3":"HR54-500",
                 "r3s4":"HR54-200", "r3s5":"HR44-700", 
                 "r3s6":"HR44-500", "r3s7":"HR44-200",
                 "r3s8":"HR34-700", "r2s1":"C51-100",
                 "r2s2":"C41-500", "r2s3":"C41-700",
                 "r2s4":"C51-500", "r2s5":"C51-700",
                 "r2s6":"C61W-700", "r2s7":"C51-500",
                 "r2s8":"C41-700", "r2s9":"C51-100",
                 "r2s10":"C41-500", "r2s11":"C41w-100",
                 "r2s12":"C41-500", "r2s13":"C41-700",
                 "r2s14":"C31-700", "r2s15":"C41-700",
                 "r2s16":"C41-700", "r1s1":"Rack1 - STB1",
                 "r1s2":"Rack1 - STB2", "r1s3":"Rack1 - STB3",
                 "r1s4":"Rack1 - STB4", "r1s5":"Rack1 - STB5",
                 "r1s6":"Rack1 - STB6", "r1s7":"Rack1 - STB6",
                 "r1s8":"Rack1 - STB 8"}
    tnMV = telnetlib.Telnet("10.23.223.93", "9990")
    # tnMV.write("INPUT LABELS:\n")
    tnMV.write(("INPUT LABELS:\n").encode('ascii'))
    for key,value in labelArr.items():
        #print 'key:'
        #print key
        multiviewerPos = int(key)-1
        #print value
        # labelName = stbModels.get(value,"default")
        labelName = value
        commandStr = str(multiviewerPos) + " " + labelName
        #print 'command String:'
        #print commandStr
        tnMV.write((commandStr).encode('ascii'))
        tnMV.write(("\n").encode('ascii'))
    tnMV.write(("\n").encode('ascii'))
    # multiviewer
    

    return "set labels executed!!"

def labelsDisplay(labelsMode):
    tn = telnetlib.Telnet("10.23.223.93", "9990")
    print(labelsMode)
    validModes = ['true', 'false']
    labelsModeStr = str(labelsMode)
    if labelsModeStr in validModes:
        # set labels config
        print(labelsModeStr) 
        tn.write("CONFIGURATION:\n")
        # tn.write("Display labels: "+ labelsModeStr +"\n")
        tn.write("Display labels: "+labelsModeStr+"\n")
        tn.write("\n") 
        tn.close()
        print("labelsDisplay executed")
        return "labels display executed"
    else:
        print "invalid mode"
        return "invalid mode"

def audioMeters(audioMode):
    tn = telnetlib.Telnet("10.23.223.93", "9990")
    print(audioMode)
    validModes = ['true', 'false']
    audioModeStr = str(audioMode)
    if audioModeStr in validModes:
        # set labels config
        print(audioModeStr) 
        tn.write("CONFIGURATION:\n")
        # tn.write("Display labels: "+ labelsModeStr +"\n")
        tn.write("Display audio meters: "+audioModeStr+"\n")
        tn.write("\n") 
        tn.close()
        print("audioMeters executed")
        return "audioMeters executed"

def setGrid(gridConfig):
    validVals = ["2x2", "3x3","4x4"]
    strVal = str(gridConfig)
    print('[setGrid]-strVal:'+strVal)
    if (strVal in validVals):
        #print "valid value found!"
        tnMV = telnetlib.Telnet("10.23.223.93", "9990")
        tnMV.write("CONFIGURATION:\n")
        tnMV.write("Layout: "+strVal+"\n")
        tnMV.write("\n")
        return 'multviewAPI executed!'
    else:
        return "invalid input - multiviewerAPI did not execute"

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
    #print position 
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
    
    # telnet needs bytes and not string, so using line below to convert MESSAGE str to bytes
    # bytesMessage = bytes(MESSAGE, 'utf-8')
    bytesMessage = bytes(MESSAGE);
    
    # MESSAGE = MAC = A03 dataset="RC71" signal="menu" output = "1-16" \n
    # Open socket, send message, close scoket
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.settimeout(5)
    p.connect((TCP_IP, TCP_PORT))
    # p.send(MESSAGE)

    # send bytesMessages instead of str MESSAGE 
    p.send(bytesMessage)
    data = p.recv(BUFFER_SIZE)
    p.close()
    #print "Return Data: " + str(data) + key
    return "keySend Output"

def keySendv3(commandParams):
    for i in commandParams:
        print(i)
        # keySendv2(rack,key, slot)
        #return "keySendv3 executed"
# server-side handling of rss feeds
def rssFeedConverter():
    url="https://news.google.com/news/rss"
    data = feedparser.parse(url)
    # print data['feed']['title']
    # print len(data['entries'])
    for article in data['entries']:
        article.title + ":" + article.link
    
    return data['entries']
     
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/controller_beta')
def controller_beta():
    return render_template('controller_beta.html')



@app.route('/rssTest')
@support_jsonp 
def rssTest():
    #print rssFeedConverter()
    fullData= rssFeedConverter()
    testArr = []
    for item in fullData:
        #print item.title
        testArr.append(item.title)
    # testArr = ['test', 'test2']
    
    return jsonify(title=testArr)
    
    # return jsonify(fakeData=configArr[int(configNum)-1])


@app.route('/deviceInfo/')
def deviceInfo():
    # return hardcoded stb info below
    #"0":"00-80-A3-A2-D9-13", "1":"00-80-A3-A9-E3-68", 
    #             "2":"00-80-A3-A9-E3-6A", "3":"00-80-A3-A9-E3-7A", 
    #             "4":"00-80-A3-A9-DA-67", "5":"00-80-A3-A9-E3-79", 
    #             "6":"00-80-A3-A9-E3-78", "7":"00-80-A3-9E-67-37", 
    #             "8":"00-80-A3-9D-86-D5", "9":"00-80-A3-9E-67-34",
    #             "10":"00-80-A3-9E-67-27", "11":"00-80-A3-9D-86-CF",
    #             "12":"00-80-A3-9E-67-35", "13":"00-20-4A-BD-C5-1D",
    #             "14":"00-80-A3-9D-86-D2", "15":"00-80-A3-9E-67-3B",
    #             "16":"00-80-A3-9E-67-36", "17":"00-80-A3-9E-67-32",
    #             "18":"00-80-A3-9D-86-D6", "19":"00-80-A3-9D-86-D3",
    #             "20":"00-80-A3-9D-86-D1", "21":"00-80-A3-9D-86-D0",
    #             "22":"00-20-4A-DF-64-55", "23":"00-80-A3-A1-7C-3C",
    #             "24":"00-80-A3-A2-48-5C", "25":"00-20-4A-DF-65-A0",
    #             "26":"00-80-A3-9E-67-3A"
    deviceInfo = {
        'A00' : {
                'macAddr':'00-80-A3-A2-D9-13',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    }, 
                },
        'A01': {
                'macAddr': '00-80-A3-A9-E3-68',
                '1':{
                        'model':'hr-test1',
                        'vidRouteMoniker':'r1s1',
                        'port':'8011',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r1s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r1s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r1s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r1s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r1s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r1s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r1s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'r1s9',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'r1s10',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'r1s11',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'r1s12',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'r1s13',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'r1s14',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'r1s15',
                        'port':'',
                    },
                '16':{
                        'model':'hrtest-16',
                        'vidRouteMoniker':'r1s16',
                        'port':'',
                    },
                },
        'A02': {
                'macAddr': '00-80-A3-A9-E3-6A',
                '1':{
                        'model':'client1',
                        'vidRouteMoniker':'r2s1',
                        'port':'',
                    },
                '2':{
                        'model':'client2',
                        'vidRouteMoniker':'r2s2',
                        'port':'',
                    },
                '3':{
                        'model':'client3',
                        'vidRouteMoniker':'r2s3',
                        'port':'',
                    },
                '4':{
                        'model':'client4',
                        'vidRouteMoniker':'r2s4',
                        'port':'',
                    },
                '5':{
                        'model':'client5',
                        'vidRouteMoniker':'r2s5',
                        'port':'',
                    },
                '6':{
                        'model':'client6',
                        'vidRouteMoniker':'r2s6',
                        'port':'',
                    },
                '7':{
                        'model':'client7',
                        'vidRouteMoniker':'r2s7',
                        'port':'',
                    },
                '8':{
                        'model':'client8',
                        'vidRouteMoniker':'r2s8',
                        'port':'',
                    },
                '9':{
                        'model':'client9',
                        'vidRouteMoniker':'r2s9',
                        'port':'',
                    },
                '10':{
                        'model':'client10',
                        'vidRouteMoniker':'r2s10',
                        'port':'',
                    },
                '11':{
                        'model':'client11',
                        'vidRouteMoniker':'r2s11',
                        'port':'',
                    },
                '12':{
                        'model':'client12',
                        'vidRouteMoniker':'r2s12',
                        'port':'',
                    },
                '13':{
                        'model':'client13',
                        'vidRouteMoniker':'r2s13',
                        'port':'',
                    },
                '14':{
                        'model':'client14',
                        'vidRouteMoniker':'r2s14',
                        'port':'',
                    },
                '15':{
                        'model':'client15',
                        'vidRouteMoniker':'r2s15',
                        'port':'',
                    },
                '16':{
                        'model':'client16',
                        'vidRouteMoniker':'r2s16',
                        'port':'',
                    },
                },
        'A03': {
                'macAddr': '00-80-A3-A9-E3-7A',
                '1':{
                        'model':'H44',
                        'vidRouteMoniker':'r3s1',
                        'port':'',
                    },
                '2':{
                        'model':'HR54-700',
                        'vidRouteMoniker':'r3s2',
                        'port':'',
                    },
                '3':{
                        'model':'HR54-500',
                        'vidRouteMoniker':'r3s3',
                        'port':'',
                    },
                '4':{
                        'model':'HR54-200',
                        'vidRouteMoniker':'r3s4',
                        'port':'',
                    },
                '5':{
                        'model':'HR44-700',
                        'vidRouteMoniker':'r3s5',
                        'port':'',
                    },
                '6':{
                        'model':'HR44-500',
                        'vidRouteMoniker':'r3s6',
                        'port':'',
                    },
                '7':{
                        'model':'HR44-200',
                        'vidRouteMoniker':'r3s7',
                        'port':'',
                    },
                '8':{
                        'model':'HR34-700',
                        'vidRouteMoniker':'r3s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'r3s9',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'r3s10',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'r3s11',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'r3s12',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'r3s13',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'r3s14',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'r3s15',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'r3s16',
                        'port':'',
                    },   
            },
        'A04':{
                'macAddr': '00-80-A3-A9-DA-67',
                '1':{
                        'model':'r4s1',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r4s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r4s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r4s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r4s4',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r4s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r4s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r4s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'r4s9',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'r4s10',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'r4s11',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'r4s12',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'r4s13',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'r4s14',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'r4s15',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'r4s16',
                        'port':'',
                    },
            },
        'A05':{
                'macAddr':'00-80-A3-A9-E3-79',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r5s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r5s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r5s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r5s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r5s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r5s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r5s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r5s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'r5s9',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'r5s10',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'r5s11',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'r5s12',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'r5s13',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'r5s14',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'r5s15',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'r5s16',
                        'port':'',
                    },
            },
        'A06':{
                'macAddr':'00-80-A3-A9-E3-78',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r6s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r6s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r6s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r6s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r6s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r6s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r6s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r6s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'r6s9',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'r6s10',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'r6s11',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'r6s12',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'r6s13',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'r6s14',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'r6s15',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'r6s16',
                        'port':'',
                    },
            },
        'A07':{
            'macAddr':'00-80-A3-9E-67-37',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r7s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r7s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r7s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r7s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r7s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r7s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r7s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r7s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'r7s9',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'r7s10',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'r7s11',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'r7s12',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'r7s13',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'r7s14',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'r7s15',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'r7s16',
                        'port':'',
                    },
            },
        'A08':{
                'macAddr':'00-80-A3-9D-86-D5',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r8s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r8s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r8s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r8s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r8s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r8s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r8s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r8s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'r8s9',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'r8s10',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'r8s11',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'r8s12',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'r8s13',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'r8s14',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'r8s15',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'r8s16',
                        'port':'',
                    },
                },
            'A09':{
                    'macAddr':'00-80-A3-9E-67-34',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r9s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r9s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r9s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r9s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r9s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r9s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r9s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r9s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'r9s9',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'r9s10',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'r9s11',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'r9s12',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'r9s13',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'r9s14',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'r9s15',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'r9s16',
                        'port':'',
                    },
                },
            'A10':{
                'macAddr':'00-80-A3-9E-67-27',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r10s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r10s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r10s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r10s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r10s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r10s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r10s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r10s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'r10s9',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'r10s10',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'r10s11',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'r10s12',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'r10s13',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'r10s14',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'r10s15',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'r10s16',
                        'port':'',
                    },
            },
        'A11':{
                'macAddr':'00-80-A3-9D-86-CF',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r11s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r11s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r11s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r11s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r11s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r11s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r11s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r11s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'r11s9',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'r11s10',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'r11s11',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'r11s12',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'r11s13',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'r11s14',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'r11s15',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'r11s16',
                        'port':'',
                    },
                },
            'B04':{
                    'macAddr':'00-20-4A-BD-C5-1D',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r21s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r21s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r21s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r21s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r21s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r21s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r21s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r21s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                },
            'B05':{
                    'macAddr':'00-80-A3-9D-86-D2',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r20s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r20s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r20s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r20s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r20s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r20s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r20s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r20s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                },
            'B06':{
                    'macAddr':'00-80-A3-9E-67-3B',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r19s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r19s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r19s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r19s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r19s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r19s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r19s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r19s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                },
            'B07':{
                    'macAddr':'00-80-A3-9E-67-36',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r18s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r18s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r18s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r18s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r18s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r18s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r18s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r18s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                },
            'B08':{
                    'macAddr':'00-80-A3-9E-67-32',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r17s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r17s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r17s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r17s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r17s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r17s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r17s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r17s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                },
            'B09': {
                    'macAddr':'00-80-A3-9D-86-D6',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r16s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r16s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r16s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r16s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r16s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r16s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r16s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r16s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                },
            'B10': {
                    'macAddr':'00-80-A3-9D-86-D3',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r15s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r15s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r15s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r15s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r15s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r15s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r15s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r15s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                },
            'B11':{
                    'macAddr':'00-80-A3-9D-86-D1',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r14s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r14s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r14s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r14s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r14s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r14s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r14s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r14s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                },
            'B12':{
                    'macAddr':'00-80-A3-9D-86-D0',
                '1':{
                        'model':'',
                        'vidRouteMoniker':'r13s1',
                        'port':'',
                    },
                '2':{
                        'model':'',
                        'vidRouteMoniker':'r12s2',
                        'port':'',
                    },
                '3':{
                        'model':'',
                        'vidRouteMoniker':'r13s3',
                        'port':'',
                    },
                '4':{
                        'model':'',
                        'vidRouteMoniker':'r13s4',
                        'port':'',
                    },
                '5':{
                        'model':'',
                        'vidRouteMoniker':'r13s5',
                        'port':'',
                    },
                '6':{
                        'model':'',
                        'vidRouteMoniker':'r13s6',
                        'port':'',
                    },
                '7':{
                        'model':'',
                        'vidRouteMoniker':'r13s7',
                        'port':'',
                    },
                '8':{
                        'model':'',
                        'vidRouteMoniker':'r13s8',
                        'port':'',
                    },
                '9':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '10':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '11':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '12':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '13':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '14':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '15':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                '16':{
                        'model':'',
                        'vidRouteMoniker':'',
                        'port':'',
                    },
                },
    }
    return jsonify(deviceInfo)

@app.route('/jsonTest/<string:configNum>/')
def jsonTest(configNum):
    configArr = [
        {
            '1': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '1', 'model': 'H21-100', 'vidRouteMoniker': 'r14s1'},
            '2': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '2', 'model': 'H21-200', 'vidRouteMoniker': 'r14s2'},
            '3': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '3', 'model': 'H23-600', 'vidRouteMoniker': 'r14s3'},
            '4': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '4', 'model': 'HR20-100', 'vidRouteMoniker': 'r14s4'},
            '5': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '5', 'model': 'HR20-700', 'vidRouteMoniker': 'r14s5'},
            '6': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '6', 'model': 'HR21-100', 'vidRouteMoniker': 'r14s6'},
            '7': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '7', 'model': 'HR22-100', 'vidRouteMoniker': 'r14s7'},
            '8': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '8', 'model': 'HR24-500', 'vidRouteMoniker': 'r14s8'},
            '9': {'macAddr': '00-80-A3-9D-86-D3', 'slot': '1', 'model': 'THR22-100', 'vidRouteMoniker': 'r15s1'},
            '10': {'macAddr': '00-80-A3-9D-86-D3', 'slot': '2', 'model': 'HR21-200', 'vidRouteMoniker': 'r15s2'},
            '11': {'macAddr': '00-80-A3-9D-86-D3', 'slot': '3', 'model': 'HR21P-200', 'vidRouteMoniker': 'r15s3'},
            '12': {'macAddr': '00-80-A3-9D-86-D3', 'slot': '4', 'model': 'R22-100', 'vidRouteMoniker': 'r15s4'},
            '13': {'macAddr': '00-80-A3-9D-86-D3', 'slot': '5', 'model': 'HR24-200', 'vidRouteMoniker': 'r15s5'},
            '14': {'macAddr': '00-80-A3-9D-86-D3', 'slot': '6', 'model': 'HR21-700', 'vidRouteMoniker': 'r15s6'},
            '15': {'macAddr': '00-80-A3-9D-86-D3', 'slot': '7', 'model': 'HR23-700', 'vidRouteMoniker': 'r15s7'},
            '16': {'macAddr': '00-80-A3-9D-86-D3', 'slot': '8', 'model': 'HR24-500', 'vidRouteMoniker': 'r15s8'},
        },

        {
           '1': {'macAddr': '00-80-A3-9E-67-34', 'slot': '5', 'model': 'H44-100', 'vidRouteMoniker':'r3s1'}, 
           '2': {'macAddr': '00-80-A3-A9-E3-7A', 'slot': '2', 'model': 'HR54-700', 'vidRouteMoniker':'r3s2'},
           '3': {'macAddr': '00-80-A3-A9-E3-7A', 'slot': '3', 'model': 'HR54-500', 'vidRouteMoniker': 'r3s3'},
           '4': {'macAddr': '00-80-A3-A9-E3-7A', 'slot': '4', 'model': 'HR54-200', 'vidRouteMoniker': 'r3s4'},
           '5': {'macAddr': '00-80-A3-A9-E3-7A', 'slot': '5', 'model': 'HR44-700', 'vidRouteMoniker': 'r3s5'},
           '6': {'macAddr': '00-80-A3-A9-E3-7A', 'slot': '6', 'model': 'HR44-500', 'vidRouteMoniker': 'r3s6'},
           '7': {'macAddr': '00-80-A3-A9-E3-7A', 'slot': '7', 'model': 'HR44-200', 'vidRouteMoniker': 'r3s7'},
           '8': {'macAddr': '00-80-A3-A9-E3-7A', 'slot': '8', 'model': 'HR34-700', 'vidRouteMoniker': 'r3s8'},
           '9': {'macAddr': '00-80-A3-A9-E3-6A', 'slot': '1', 'model': 'C51-100(H44-500)', 'vidRouteMoniker': 'r2s1'},
           '10': {'macAddr': '00-80-A3-A9-E3-6A', 'slot': '2', 'model': 'C41-700(H44-500)', 'vidRouteMoniker': 'r2s2'},
           '11': {'macAddr': '00-80-A3-A9-E3-6A', 'slot': '3', 'model': 'C41-700(H44-500)', 'vidRouteMoniker': 'r2s3'},
           '12': {'macAddr': '00-80-A3-A9-E3-6A', 'slot': '4', 'model': 'C51-500(HR54R1-700)', 'vidRouteMoniker': 'r2s4'},
           '13': {'macAddr': '00-80-A3-A9-E3-6A', 'slot': '5', 'model': 'C61-700(HR54R1-700)', 'vidRouteMoniker': 'r2s5'},
           '14': {'macAddr': '00-80-A3-A9-E3-6A', 'slot': '6', 'model': 'C61w-700(HR54R1-700)', 'vidRouteMoniker': 'r2s6'},
           '15': {'macAddr': '00-80-A3-A9-E3-6A', 'slot': '7', 'model': 'C51-500(HR54-500)', 'vidRouteMoniker': 'r2s7'},
           '16': {'macAddr': '00-80-A3-A9-E3-6A', 'slot': '8', 'model': 'C41-700(HR54-200)', 'vidRouteMoniker': 'r2s8'},   
        },

        #rack A09
        {
            '1': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '1', 'model': 'HR44-200', 'vidRouteMoniker':'r6s1'}, 
           '2': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '2', 'model': 'Client', 'vidRouteMoniker':'r6s2'},
           '3': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '3', 'model': 'client', 'vidRouteMoniker': 'r6s3'},
           '4': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '4', 'model': 'client', 'vidRouteMoniker': 'r6s4'},
           '5': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '5', 'model': 'HR44-500', 'vidRouteMoniker': 'r6s5'},
           '6': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '6', 'model': 'client', 'vidRouteMoniker': 'r6s6'},
           '7': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '7', 'model': 'client', 'vidRouteMoniker': 'r6s7'},
           '8': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '8', 'model': 'client', 'vidRouteMoniker': 'r6s8'},
           '9': {'macAddr': '00-80-A3-9E-67-37', 'slot': '1', 'model': 'HR44-700', 'vidRouteMoniker': 'r7s1'},
           '10': {'macAddr': '00-80-A3-9E-67-37', 'slot': '2', 'model': 'client', 'vidRouteMoniker': 'r7s2'},
           '11': {'macAddr': '00-80-A3-9E-67-37', 'slot': '3', 'model': 'client', 'vidRouteMoniker': 'r7s3'},
           '12': {'macAddr': '00-80-A3-9E-67-37', 'slot': '4', 'model': 'client', 'vidRouteMoniker': 'r7s4'},
           '13': {'macAddr': '00-80-A3-9E-67-37', 'slot': '5', 'model': 'null', 'vidRouteMoniker': 'r7s5'},
           '14': {'macAddr': '00-80-A3-9E-67-37', 'slot': '6', 'model': 'null', 'vidRouteMoniker': 'r7s6'},
           '15': {'macAddr': '00-80-A3-9E-67-37', 'slot': '7', 'model': 'null', 'vidRouteMoniker': 'r7s7'},
           '16': {'macAddr': '00-80-A3-9E-67-37', 'slot': '8', 'model': 'null', 'vidRouteMoniker': 'r7s8'}, 
        },

        {
           '1': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '1', 'model': 'HR54-200', 'vidRouteMoniker':'r9s1'}, 
           '2': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '2', 'model': 'Client', 'vidRouteMoniker':'r9s2'},
           '3': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '3', 'model': 'client', 'vidRouteMoniker': 'r9s3'},
           '4': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '4', 'model': 'client', 'vidRouteMoniker': 'r9s4'},
           '5': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '5', 'model': 'HR54-500', 'vidRouteMoniker': 'r9s5'},
           '6': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '6', 'model': 'client', 'vidRouteMoniker': 'r9s6'},
           '7': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '7', 'model': 'client', 'vidRouteMoniker': 'r9s7'},
           '8': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '8', 'model': 'client', 'vidRouteMoniker': 'r9s8'},
           '9': {'macAddr': '00-80-A3-9D-86-D5', 'slot': '9', 'model': 'HR54-700', 'vidRouteMoniker': 'r9s9'},
           '10': {'macAddr': '00-80-A3-9D-86-D5', 'slot': '10', 'model': 'client', 'vidRouteMoniker': 'r9s10'},
           '11': {'macAddr': '00-80-A3-9D-86-D5', 'slot': '11', 'model': 'client', 'vidRouteMoniker': 'r9s11'},
           '12': {'macAddr': '00-80-A3-9D-86-D5', 'slot': '12', 'model': 'client', 'vidRouteMoniker': 'r9s12'},
           '13': {'macAddr': '00-80-A3-9D-86-D5', 'slot': '13', 'model': 'null', 'vidRouteMoniker': 'r9s12'},
           '14': {'macAddr': '00-80-A3-9D-86-D5', 'slot': '14', 'model': 'null', 'vidRouteMoniker': 'r9s12'},
           '15': {'macAddr': '00-80-A3-9D-86-D5', 'slot': '15', 'model': 'null', 'vidRouteMoniker': 'r9s12'},
           '16': {'macAddr': '00-80-A3-9D-86-D5', 'slot': '16', 'model': 'null', 'vidRouteMoniker': 'r9s12'}, 
        },

        {
           '1': {'macAddr': '00-80-A3-9D-86-D6', 'slot': '1', 'model': 'new', 'vidRouteMoniker':'r6s1'}, 
           '2': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '2', 'model': 'new', 'vidRouteMoniker':'r9s2'},
           '3': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '3', 'model': 'new', 'vidRouteMoniker': 'r9s3'},
           '4': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '4', 'model': 'new', 'vidRouteMoniker': 'r9s4'},
           '5': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '5', 'model': 'new', 'vidRouteMoniker': 'r9s5'},
           '6': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '6', 'model': 'new', 'vidRouteMoniker': 'r9s6'},
           '7': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '7', 'model': 'new', 'vidRouteMoniker': 'r9s7'},
           '8': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '8', 'model': 'new', 'vidRouteMoniker': 'r9s8'},
           '9': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '9', 'model': 'new', 'vidRouteMoniker': 'r9s9'},
           '10': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '10', 'model': 'new', 'vidRouteMoniker': 'r9s10'},
           '11': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '11', 'model': 'new', 'vidRouteMoniker': 'r9s11'},
           '12': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '12', 'model': 'new', 'vidRouteMoniker': 'r9s12'},
           '13': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '13', 'model': 'new', 'vidRouteMoniker': 'r9s12'},
           '14': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '14', 'model': 'new', 'vidRouteMoniker': 'r9s12'},
           '15': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '15', 'model': 'new', 'vidRouteMoniker': 'r9s12'},
           '16': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '16', 'model': 'new', 'vidRouteMoniker': 'r9s12'}, 
        },
        # config 6
        {
           '1': {'macAddr': '00-80-A3-A9-DA-67', 'slot': '1', 'model': 'r4s1', 'vidRouteMoniker':'r4s1'}, 
           '2': {'macAddr': '00-80-A3-A9-DA-67', 'slot': '2', 'model': 'r4s2', 'vidRouteMoniker':'r4s2'},
           '3': {'macAddr': '00-80-A3-A9-DA-67', 'slot': '3', 'model': 'r4s3', 'vidRouteMoniker': 'r4s3'},
           '4': {'macAddr': '00-80-A3-A9-DA-67', 'slot': '4', 'model': 'r4s4', 'vidRouteMoniker': 'r4s4'},
           '5': {'macAddr': '00-80-A3-A9-DA-67', 'slot': '5', 'model': 'r4s5', 'vidRouteMoniker': 'r4s5'},
           '6': {'macAddr': '00-80-A3-A9-DA-67', 'slot': '6', 'model': 'r4s6', 'vidRouteMoniker': 'r4s6'},
           '7': {'macAddr': '00-80-A3-A9-DA-67', 'slot': '7', 'model': 'r4s7', 'vidRouteMoniker': 'r4s7'},
           '8': {'macAddr': '00-80-A3-A9-DA-67', 'slot': '8', 'model': 'r4s8', 'vidRouteMoniker': 'r4s8'},
           '9': {'macAddr': '00-80-A3-A9-E3-78', 'slot': '9', 'model': 'rack5-1', 'vidRouteMoniker': 'r5s1'},
           '10': {'macAddr': '00-80-A3-A9-E3-79', 'slot': '10', 'model': 'rack5-2', 'vidRouteMoniker': 'r5s2'},
           '11': {'macAddr': '00-80-A3-A9-E3-79', 'slot': '11', 'model': 'rack5-3', 'vidRouteMoniker': 'r5s3'},
           '12': {'macAddr': '00-80-A3-A9-E3-79', 'slot': '12', 'model': 'rack5-4', 'vidRouteMoniker': 'r5s4'},
           '13': {'macAddr': '00-80-A3-A9-E3-79', 'slot': '13', 'model': 'rack5-5', 'vidRouteMoniker': 'r5s5'},
           '14': {'macAddr': '00-80-A3-A9-E3-79', 'slot': '14', 'model': 'rack5-6', 'vidRouteMoniker': 'r5s6'},
           '15': {'macAddr': '00-80-A3-A9-E3-79', 'slot': '15', 'model': 'rack5-7', 'vidRouteMoniker': 'r5s7'},
           '16': {'macAddr': '00-80-A3-A9-E3-79', 'slot': '16', 'model': 'rack5-8', 'vidRouteMoniker': 'r5s8'},
        },
        # config 7 - rack b12; rack b11
        {
           '1': {'macAddr': '00-80-A3-9D-86-D0', 'slot': '1', 'model': 'h25-100', 'vidRouteMoniker':'r13s1'}, 
           '2': {'macAddr': '00-80-A3-9D-86-D0', 'slot': '2', 'model': 'h25-500', 'vidRouteMoniker':'r13s2'},
           '3': {'macAddr': '00-80-A3-9D-86-D0', 'slot': '3', 'model': 'h25-700', 'vidRouteMoniker': 'r13s3'},
           '4': {'macAddr': '00-80-A3-9D-86-D0', 'slot': '4', 'model': 'empty', 'vidRouteMoniker': 'r13s4'},
           '5': {'macAddr': '00-80-A3-9D-86-D0', 'slot': '5', 'model': 'hr34-700', 'vidRouteMoniker': 'r13s5'},
           '6': {'macAddr': '00-80-A3-9D-86-D0', 'slot': '6', 'model': 'C31-700', 'vidRouteMoniker': 'r13s6'},
           '7': {'macAddr': '00-80-A3-9D-86-D0', 'slot': '7', 'model': 'empty', 'vidRouteMoniker': 'r13s7'},
           '8': {'macAddr': '00-80-A3-9D-86-D0', 'slot': '8', 'model': 'empty', 'vidRouteMoniker': 'r13s8'},
           '9': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '1', 'model': 'H21-100', 'vidRouteMoniker': 'r14s1'},
           '10': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '2', 'model': 'H21-200', 'vidRouteMoniker': 'r14s2'},
           '11': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '3', 'model': 'H23-600', 'vidRouteMoniker': 'r14s3'},
           '12': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '4', 'model': 'HR20-100', 'vidRouteMoniker': 'r14s4'},
           '13': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '5', 'model': 'HR20-700', 'vidRouteMoniker': 'r14s5'},
           '14': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '6', 'model': 'HR21-100', 'vidRouteMoniker': 'r14s6'},
           '15': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '7', 'model': 'HR22-100', 'vidRouteMoniker': 'r14s7'},
           '16': {'macAddr': '00-80-A3-9D-86-D1', 'slot': '8', 'model': 'HR24-500', 'vidRouteMoniker': 'r14s8'},
        }


    ]
    # return jsonify(fakeData={'1':{'macAddr': '00-80-A3-9D-86-D0', 'slot': '1', 'model': 'H24-100', 'vidRouteMoniker':'r13s1'}})
    return jsonify(fakeData=configArr[int(configNum)-1])

@app.route('/setCookie/', methods = ['POST', 'GET'])
def setCookie():
    resp = make_response(render_template('celeste.html'))
    resp.set_cookie('myCookie', 'testUSER')
    return resp

@app.route('/getCookie/', methods = ['POST', 'GET'])
def getCookie():
    cookieContents = request.cookies.get('myCookie')
    print( cookieContents)
    return cookieContents






# Test to see if socket is reachable
@app.route('/check', methods=['GET', 'POST'])
def check():
    conn = httplib2.Http('www.google.com')  # I used here HTTP not HTTPS for simplify
    conn.request('HEAD', '/')  # Just send a HTTP HEAD request 
    res = conn.getresponse()

    if res.status == 200:
        print("ok")
    else:
        print("problem : the query returned %s because %s" % (res.status, res.reason) )



@app.route('/testingPage', methods=['GET', 'POST'])
def testingPage():
    return render_template('testingPage.html')

@app.route('/testingPage2', methods=['GET', 'POST'])
def testingPage2():
    return render_template('testingPage2.html')


@app.route('/setVideo/<string:cell1>/<string:cell2>/<string:cell3>/<string:cell4>'
             '/<string:cell5>/<string:cell6>/<string:cell7>/<string:cell8>'
             '/<string:cell9>/<string:cell10>/<string:cell11>/<string:cell12>'
             '/<string:cell13>/<string:cell14>/<string:cell15>/<string:cell16>/', methods=['GET', 'POST'])
# @app.route('/setVideo/celeste/<int:configNum>/', methods=['GET', 'POST'])
def configVideo2(cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8,
                 cell9, cell10, cell11, cell12, cell13, cell14, cell15, cell16):
    # todo: sanitize inputs

    #
    vidPositionArr = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8,
                      cell9, cell10, cell11, cell12, cell13, cell14, cell15, cell16]
    print "vidPositionArr: "
    print vidPositionArr
    vidPositionDict = {}
    for i in vidPositionArr:
        if i != 'null':
            vidPositionDict[str(vidPositionArr.index(i)+1)] = i
    print "vidPositionDict:"
    print vidPositionDict  

    physicalPosition = {
                            'r3s1':'H44-500',
                            'r3s2':'HR54-700',
                            'r3s3':'HR54-500',
                            'r3s4':'HR54-200',
                            'r3s5':'HR44-700',
                            'r3s6':'HR44-500',
                            'r3s7':'HR44-200',
                            'r3s8':'HR34-700'
                        }

    defaultConf = {
                    "1":"r3s1", "2":"r3s2", "3":"r3s3", "4":"r3s4",
                    "5":"r3s5","6":"r3s6", "7":"r3s7", "8":"r3s8",
                    "9":"r2s1", "10":"r2s2", "11":"r2s3", "12":"r2s4",
                    "13":"r2s5", "14":"r2s6", "15":"r2s7", "16":"r2s8"
                }
    allclientsConf = {
                    "1":"r2s1", "2":"r2s2", "3":"r2s3", "4":"r2s4",
                    "5":"r2s5", "6":"r2s6", "7":"r2s7", "8":"r2s8",
                    "9":"r2s9", "10":"r2s10", "11":"r2s11", "12":"r2s12",
                    "13":"r2s13", "14":"r2s14", "15":"r2s15", "16":"r2s16"
    }
    # print configNum
    #r12 = A12, r13 = B12, r14 = B11
    dictionary1 = {
        '1':{
                    "1":"r3s1", "2":"r3s2", "3":"r3s3", "4":"r3s4",
                    "5":"r3s5","6":"r3s6", "7":"r3s7", "8":"r3s8",
                    "9":"r2s1", "10":"r2s2", "11":"r2s3", "12":"r2s4",
                    "13":"r2s5", "14":"r2s6", "15":"r2s7", "16":"r2s8"
                },
        '2':{
                    "1":"r2s1", "2":"r2s2", "3":"r2s3", "4":"r2s4",
                    "5":"r2s5", "6":"r2s6", "7":"r2s7", "8":"r2s8",
                    "9":"r2s9", "10":"r2s10", "11":"r2s11", "12":"r2s12",
                    "13":"r2s13", "14":"r2s14", "15":"r2s15", "16":"r2s16"
    },
        '3': {
                    "1":"r3s8", "2":"r2s15", "3":"r3s5", "4":"r2s10",
                    "5":"r2s14", "6":"r2s16", "7":"r2s9", "8":"r2s11",
                    "9":"r3s1", "10":"r2s2", "11":"r3s2", "12":"r2s5",
                    "13":"r2s1", "14":"r2s3", "15":"r2s4", "16":"r2s6"   
            },

        '4': {   
                    "1":"r13s1", "2":"r13s2", "3":"r13s3", "4":"r13s4",
                    "5":"r13s5", "6":"r13s6", "7":"r13s7", "8":"r13s8",
                    "9":"r14s1", "10":"r14s2", "11":"r14s3", "12":"r14s4",
                    "13":"r14s5", "14":"r14s6", "15":"r14s7", "16":"r14s8"
            },
        '5': {
                    "1":"r15s1", "2":"r15s2", "3":"r15s3", "4":"r15s4",
                    "5":"r15s5", "6":"r15s6", "7":"r15s7", "8":"r15s8",
                    "9":"r16s1", "10":"r16s2", "11":"r16s3", "12":"r16s4",
                    "13":"r16s5", "14":"r16s6", "15":"r16s7", "16":"r16s8"
            }, 
    }
    

    if str(1) in dictionary1:
        # print dictionary1[str(configNum)]
        # setVideo(dictionary1[str(1)])
        setVideo(vidPositionDict)
        return 'configVideo2 initiated'
    else:
        # print 'invalid multiviwer configuration key used'
        return 'invalid multiviwer configuration key used'

@app.route('/setLabels/<string:stb1>/<string:stb2>/<string:stb3>/<string:stb4>'
           '/<string:stb5>/<string:stb6>/<string:stb7>/<string:stb8>'
           '/<string:stb9>/<string:stb10>/<string:stb11>/<string:stb12>'
           '/<string:stb13>/<string:stb14>/<string:stb15>/<string:stb16>/', methods=['GET', 'POST'])
def configLabels(stb1='', stb2='', stb3='', stb4='', stb5='', stb6='', stb7='', stb8='',
                 stb9='',stb10='', stb11='', stb12='', stb13='', stb14='', stb15='', stb16=''):
    # sanititize inputs - only go to next step if stb input contains digits/letters with a total less
    # than 10 characters
    sanitizerArr = [stb1, stb2, stb3, stb4, stb5, stb6, stb7, stb8,
                    stb9, stb10, stb11, stb12, stb13, stb14, stb15, stb16]
    for stb in sanitizerArr:
        regexStatus = re.findall("^[0-9A-Za-z]{10,}",stb)
        if (regexStatus):
            # print 'fail:'
            # print stb
            # print regexStatus
            return 'one of the stb inputs failed regex! (digit or character less than 10 characters)'
        else:
            # print 'stb input qualified!'
            # print stb
            print(regexStatus)
    

    # store url input strings into an array/list
    # store parameters in a dictionary because that is what the setLabels() functions uses.
    # Note: The stb variables are by default 'unicode', so they were converted invidually
    # to string to accomodate setLabels()
    labelArr = {'1': str(stb1), '2': str(stb2), '3':str(stb3), '4':str(stb4),
                '5': str(stb5), '6': str(stb6), '7':str(stb7), '8':str(stb8),
                '9': str(stb9), '10': str(stb10), '11': str(stb11), '12': str(stb12),
                '13': str(stb13), '14': str(stb14), '15': str(stb15), '16': str(stb16)}
    # print "0o000labelArr values: "
    # print labelArr

    labelConfigs = {
            '1':{
                '1': 'HR34-700', '2': 'C41-700', '3': 'hr44-700', '4': 'test'
                },
            '2':{},
            '3':{},
            '4':{'1':'H24-100', '2': 'H24-200', '3': 'H24-700', '4': 'H25-100',
                 '5':'HR24-100', '6':'H25-700', '7':'H25-500', '8': 'HR24-200', 
                 '9': 'H21-100F', '10':'H21-200', '11':'H23-600', '12': 'HR20-100',
                 '13': 'HR20-700', '14': 'HR21-100', '15': 'HR22-100F', '16':'HR24-500'},
            '5': {}
    }

    #if str(configNum2) in labelConfigs:
    #    print labelConfigs[str(configNum2)]
    #    setLabels(labelConfigs[str(configNum2)])
    #    return 'configLabels initiated'
    #else:
    #    return 'error with configLabels'
    
    setLabels(labelArr)
    return 'config labels executed'

@app.route('/celeste/multiview/setGrid/<string:gridConfig>/')
def multiviewAPI(gridConfig):
    status = setGrid(gridConfig)
    print('status:'+status)
    return "multiviewAPI return "+status+gridConfig

@app.route('/celeste/setSolo/<string:mode>')
def setSoloConfig(mode):
    # true or false
    # only run if input is valid
    valVars = ['true', 'false']
    if mode in valVars:
        Message = 'valid input detected! - '+mode
        configMultiviewer(mode);
    else:
        print('invalid input!')
        Message = 'invalid input'
    # configMultiviewer(mode)
    return Message

@app.route('/celeste/setSoloPosition/<string:position>')
def setSoloPosition(position):
    offsetPos = int(position)-1
    validPos = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9',
                '10', '11','12', '13', '14', '15']

    if str(offsetPos) in validPos:
        print('valid position, offsetPos is: '+str(offsetPos))
        setSolo(offsetPos)
        return 'setSoloPosition executed with valid position: '+position
    else:
        return 'setSoloPosition executed - invalid position entered: '+position

@app.route('/celeste/labelsMode/<string:mode>')
def labelsMode(mode):
    labelsDisplay(mode)
    return 'labels mode executed'

@app.route('/celeste/audioMeters/<string:mode>')
def audioMetersDisplay(mode):
    audioMeters(mode)
    return 'audioMeters executed'




@app.route('/setVideov1/', methods=['GET', 'POST'])
def configVideo():
    defaultConf = {
                    "1":"r3s1", "2":"r3s2", "3":"r3s3", "4":"r3s4",
                    "5":"r3s5","6":"r3s6", "7":"r3s7", "8":"r3s8",
                    "9":"r2s1", "10":"r2s2", "11":"r2s3", "12":"r2s4",
                    "13":"r2s5", "14":"r2s6", "15":"r2s7", "16":"r2s8"
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
                    "9":"r1s1", "10":"r1s2", "11":"r1s3", "12":"r1s4",
                    "13":"r1s5", "14":"r1s6", "15":"r1s7", "16":"r1s8"   
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
        # print postData
        soloConfig = request.form.get('soloConfig')
        if postData == "defaultConf":
            setVideo(defaultConf)
            setLabels(defaultConf)
            # print "default conf"
        elif postData == "allserversConf":
            setVideo(allserversConf)
            setLabels(allserversConf)
            # print "all servers conf"
        elif postData == "allclientsConf":
            setVideo(allclientsConf)
            setLabels(allclientsConf)
            # print "all clients conf"
        elif postData == "quadConf":
            setVideo(quadConf)
            setLabels(quadConf)
            # print "quad conf"
        elif postData == "solo":
            configMultiviewer("true")
            # print "configMultiviewer attempted!"
        elif postData == "nosolo":
            configMultiviewer("false")
            # print "configMutliviewer attempted!"
        else:
            print("error with multiviewerProfile")
        
        #print "solo config:"
        #print soloConfig
        acceptedInput = [
                         "0","1", "2", "3", "4", "5", "6", "7", "8",
                         "9", "10", "11", "12", "13", "14", "15"
                        ]
        if soloConfig in acceptedInput:
            setSolo(soloConfig)
        else:
            print( "Error with input to for Solo Route Change")
        # print "attempted to set video configs"
        return render_template('set_video.html')
    else:
        return render_template('set_video.html')

# simulated data for video router and multiviewer configs,
# in the future will move to a database or some external API  
def defaultConf():
    return {
                    "1":"r3s1", "2":"r3s2", "3":"r3s3", "4":"r3s4",
                    "5":"r3s5","6":"r3s6", "7":"r3s7", "8":"r3s8",
                    "9":"r2s1", "10":"r2s2", "11":"r2s3", "12":"r2s4",
                    "13":"r2s5", "14":"r2s6", "15":"r2s7", "16":"r2s8"
                }
def allclientsConf():
    return {
                    "1":"r2s1", "2":"r2s2", "3":"r2s3", "4":"r2s4",
                    "5":"r2s5", "6":"r2s6", "7":"r2s7", "8":"r2s8",
                    "9":"r2s9", "10":"r2s10", "11":"r2s11", "12":"r2s12",
                    "13":"r2s13", "14":"r2s14", "15":"r2s15", "16":"r2s16"
    }

def allserversConf():
    return {
                    "1":"r3s1", "2":"r3s2", "3":"r3s3", "4":"r3s4",
                    "5":"r3s5", "6":"r3s6", "7":"r3s7", "8":"r3s8",
                    "9":"r1s1", "10":"r1s2", "11":"r1s3", "12":"r1s4",
                    "13":"r1s5", "14":"r1s6", "15":"r1s7", "16":"r1s8"   
    }

def quadConf():
    return {
                    "1":"r3s8", "2":"r2s15", "3":"r3s5", "4":"r2s10",
                    "5":"r2s14", "6":"r2s16", "7":"r2s9", "8":"r2s11",
                    "9":"r3s1", "10":"r2s2", "11":"r3s2", "12":"r2s5",
                    "13":"r2s1", "14":"r2s3", "15":"r2s4", "16":"r2s6"   
    }

def b12():
    return {
        "1":"r3s8", "2":"r2s15", "3":"r3s5", "4":"r2s10",
                    "5":"r2s14", "6":"r2s16", "7":"r2s9", "8":"r2s11",
                    "9":"r3s1", "10":"r2s2", "11":"r3s2", "12":"r2s5",
                    "13":"r2s1", "14":"r2s3", "15":"r2s4", "16":"r2s6"  
    }

def stbModels():
    return {"r3s1":"H44-500", "r3s2":"HR54-700", "r3s3":"HR54-500",
                 "r3s4":"HR54-200", "r3s5":"HR44-700", 
                 "r3s6":"HR44-500", "r3s7":"HR44-200",
                 "r3s8":"HR34-700", "r2s1":"C51-100",
                 "r2s2":"C41-500", "r2s3":"C41-700",
                 "r2s4":"C51-500", "r2s5":"C51-700",
                 "r2s6":"C61W-700", "r2s7":"C51-500",
                 "r2s8":"C41-700", "r2s9":"C51-100",
                 "r2s10":"C41-500", "r2s11":"C41w-100",
                 "r2s12":"C41-500", "r2s13":"C41-700",
                 "r2s14":"C31-700", "r2s15":"C41-700",
                 "r2s16":"C41-700", "r1s1":"Rack1 - STB1",
                 "r1s2":"Rack1 - STB2", "r1s3":"Rack1 - STB3",
                 "r1s4":"Rack1 - STB4", "r1s5":"Rack1 - STB5",
                 "r1s6":"Rack1 - STB6", "r1s7":"Rack1 - STB6",
                 "r1s8":"Rack1 - STB 8"}





@app.route('/controller', methods=['GET', 'POST'])
@app.route('/controller/<string:viewConfigMode>')
@app.route('/controller/<string:viewConfigMode>/<string:button_set>/', methods=['GET', 'POST'])
@app.route('/controller/<string:viewConfigMode>/<string:button_set>/<string:quad>/', methods=['GET', 'POST'])
@app.route('/controller/<string:viewConfigMode>/<string:button_set>/<string:quad>/<int:rack_id>/', methods=['GET', 'POST'])
@app.route('/controller/<string:viewConfigMode>/<string:button_set>/<string:quad>/<int:rack_id>/<string:slot_id>/', methods=['GET', 'POST'])
@app.route('/controller/<string:viewConfigMode>/<string:button_set>/<string:quad>/<int:rack_id>/<string:slot_id>/<string:scriptMode>/', methods=['GET', 'POST'])
# login_required
def testB(button_set="main", rack_id="0", slot_id="0", quad='noQuad', scriptMode = '', viewConfigMode='quadConf'):
    #print 'fetch executed'
    viewRackDict = {}
    viewSlotDict = {}
    configList = {'defaultConf': defaultConf(), 'allserversConf': allserversConf(), 'quadConf': quadConf()}
    viewConfig = configList[viewConfigMode]
    for key, value in viewConfig.items():
        viewRackDict[key] = int(value.split('s')[0].split('r')[1])
    #print "viewRackDict"
    #print viewRackDict
    for key, value in viewConfig.items():
        viewSlotDict[key] = value.split('s')[1]
    #print "viewSlotDict"
    #print viewSlotDict
    # if not rack_id:
    #    return "rack_id was undefined"
    #print "button_set:"
    #print button_set
    #print "quad:"
    #print quad 
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


    #print rack_macs.get(str(rack_id))
    #print "slot id:"+str(slot_id)
    selectedRack = rack_macs.get(str(rack_id))
    if not selectedRack:
        #print "checking quad"
        if quad != "true":
            #print "No valid Rack Selected"
            flash("Please select Rack" )
            return render_template('controller_main.html', button_set=button_set, quad=quad, viewConfigMode=viewConfigMode)


    

    if request.method == 'POST':
        #print viewConfigMode
        # handle multiviewer API
        # initialize post data to designated variabiles
        postData =  request.form.get('multiviewerProfile')
        soloConfig = request.form.get('soloConfig')

        # change video routes
        if postData == "defaultConf":
            setVideo(defaultConf())
            setLabels(defaultConf())
            viewConfig = defaultConf()
            # print "default conf"
        elif postData == "allserversConf":
            setVideo(allserversConf())
            setLabels(allserversConf())
            viewConfig = allserversConf()
            #print "all servers conf"
        elif postData == "allclientsConf":
            setVideo(allclientsConf())
            setLabels(allclientsConf())
            viewConfig = allclientsConf()
            # print "all clients conf"
        elif postData == "quadConf":
            setVideo(quadConf())
            setLabels(quadConf())
            viewConfig = quadConf()
            # print "quad conf"
        elif postData == "solo":
            configMultiviewer("true")
            # print "configMultiviewer attempted!"
        elif postData == "nosolo":
            configMultiviewer("false")
            # print "configMutliviewer attempted!"
        else:
            viewDict = {'defaultConf': defaultConf(), 'allserversConf': allserversConf(), 'allclientsConf': allclientsConf(), 'b12': b12(), 'quadConf':quadConf()}
            viewConfig = viewDict[viewConfigMode]
            # print "viewConfig"
            # print viewConfig

            #print "error with multiviewerProfile"

        for key, value in viewConfig.items():
            viewRackDict[key] = int(value.split('s')[0].split('r')[1])
            #print "viewRackDict"
            #print viewRackDict
        for key, value in viewConfig.items():
            viewSlotDict[key] = value.split('s')[1]
            #print "viewSlotDict"
            #print viewSlotDict

        # set view with rack slot info

        
        
        # change multiviewer configuration
        acceptedInput = [
                         "0","1", "2", "3", "4", "5", "6", "7", "8",
                         "9", "10", "11", "12", "13", "14", "15"
                        ]
        if soloConfig in acceptedInput:
            setSolo(soloConfig)
        else:
            print( "Error with input to for Solo Route Change")
        # print "attempted to set video configs"
        #return render_template('controller_main.html', button=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id)

        # end of multiviewer API




        if not selectedRack:
            if quad != "true":
                print("No valid Rack Selected")
                flash("Please select Rack")
                return render_template('controller_main.html', button=button_set, quad=quad, viewConfigMode=viewConfigMode, viewRacks=viewRackDict, viewSlots=viewSlotDict)  

        test=request.form.to_dict()
        

        # Validation for slot id
        if slot_id != "0":
            # print "slot id detected"
            slotVar = str(slot_id)
            #print "slotVar:"+str(slotVar)
        else:
            # print "no slot id detected, sending command to all stbs in rack"
            slotVar = "1-16"
        var1 = test.get('name', '')
        # print "var1:"
        # print var1
        alphaVar = test.get('name2', '')
        
        keyword = test.get('keyword', '')
        # print keyword
        #------
        # print "quad mode:" + str(quad)
      
        # check for keyword flag 
        if keyword:
            # print keyword
            check=""
            for letter in keyword:
                    # print "letter:"+letter
                    digitVer = t9_trans.get(letter)
                    # print "digitVer:"+digitVer
                    testArray = []
                    for char in digitVer:
                        # print "Char:" + char
                        testArray.append(char)
                        #keySendv2(selectedRack, k, slotVar)
                    #print testArray
                    # print "char after loop:" +char
                    if check == char:
                        # print "comparision passed!"
                        #time.sleep(5)
                        keySendv2(selectedRack, "rightArrow", slotVar)
                    # sENd ir command
                    for testArrayItem in testArray:
                        # print "testArrayItem:"+testArrayItem
                        keySendv2(selectedRack, testArrayItem, slotVar)
                    # print "last number command sent:"+testArrayItem
                    check = testArrayItem
            pass
        

        if var1:
            # print 'detected value in var1'
            if var1.isnumeric():
                # print "numeric command detected, iterating through numbers before sending commands"
                # print "quad mode:" + str(quad)
                if quad == 'true':
                    # print rack_macs["3"]
                    for c in var1:
                        keySendv2(rack_macs["3"], c, '1,2,5,8')
                        keySendv2(rack_macs["2"], c, '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16')
                    return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id, viewConfigMode=viewConfigMode, viewRacks=viewRackDict, viewSlots=viewSlotDict)
                else:
                    for c in var1:
                        keySendv2(selectedRack, c, slotVar)
                    return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id, viewConfigMode=viewConfigMode, viewRacks=viewRackDict, viewSlots=viewSlotDict)
            else:
                # print "command string detected, sending command directly"
                if quad == 'true':
                    keySendv2(rack_macs["3"], var1, '1,2,9,8')
                    keySendv2(rack_macs["2"], var1, '1,2,3,4,5,6,9,10,11,14,15,16')
                    #return render_template('controller_main.html')
                else:
                    # print "slot var:"
                    # print slotVar
                    keySendv2(selectedRack, var1, slotVar)
                    takeScreenshot()
        elif alphaVar:
            # print 'name2 contents: '+ alphaVar
          
            if alphaVar in t9_trans:
                # print 'valid letter input found, translating to t9'
                for i in t9_trans.get(alphaVar):
                    keySendv2(selectedRack, i, slotVar)
                return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id, viewConfigMode=viewConfigMode, viewRacks=viewRackDict, viewSlots=viewSlotDict) 
            else:
                message = 'invalid input detected, command was not sent'
                # print message
                return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id, error=message, viewConfigMode=viewConfigMode, viewRacks=viewRackDict, viewSlots=viewSlotDict)    
        else:
            message = 'Error with Post Data Input'
            # print 'Error with Post Data Input'
            return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id, error=message, viewConfigMode=viewConfigMode, viewRacks=viewRackDict, viewSlots=viewSlotDict)
        return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id, viewConfigMode=viewConfigMode, viewRacks=viewRackDict, viewSlots=viewSlotDict)
    else:
        # print "request was not POST"
        return render_template('controller_main.html', button_set=button_set, quad=quad, rack_id=rack_id, slot_id=slot_id, viewConfigMode=viewConfigMode, viewRacks=viewRackDict, viewSlots=viewSlotDict)


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
    # print "key Send Test!"
    rack = rack_macs["3"]
    slotVar = "1,2,8,9"
    # print rack, slotVar
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

@app.route('/sampleApp2', methods=['GET', 'POST'])
@app.route('/sampleApp2', methods=['GET', 'POST'])
def sampleApp2():
    return render_template('sampleApp2.html')

@app.route('/sampleApp2/page1')
@app.route('/sampleApp2/page1/')
def page2():
    return render_template('page1.html')



@app.route('/reporting', methods=['GET', 'POST'])
@app.route('/reporting/', methods=['GET', 'POST'])
def reporting():
    # data = session.query(PostData).all()
    # print "data:"+str(data)
    # using current time to pass into jinja template, so that it can be used to append
    # img url to make it unique and therefore avoid the img-caching issue
    # print datetime.datetime.now().time()  
    for item in data:
        print(item.id)
        print(item.data)
    return render_template('reporting.html', data=data, tme=datetime.datetime.now().time())



@app.route('/pythonTest')
def pythonTest():
    var = datetime.datetime.now().time()
    var2 = datetime.datetime.now().strftime("%-m/%-d/%y")
    return "python test executed: " + str(var)+ " " + str(var2)

#@app.route('/scriptStart/', methods=['GET','POST'])
#def scriptStart():
#    if request.method == 'POST':
#        script_id = request.form['script_id']
#        if script_id:
#            test_cases = session.query(TestCasesV2).filter_by(id=script_id).all()
#            if test_cases:
#                for i in test_cases:
#                    name = i.name
#                    path = i.path
#                    commandString = "stbt run "+path
#                    # print commandString
#                    p = subprocess.Popen(commandString, shell=True)
#            else:
#                message = "Did not find any matching test cases with that id, did not run script"
#                # print message
#                return message
#        else:
#            message = "script_id needed to start script"
#            # print message
#            return message
#        return render_template('scriptStart.html', output=p)
#    else:
#        return render_template('scriptStart.html')

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
            # print completeCommand
            
            # with configs:
            p = subprocess.Popen(completeCommand, shell=True)
        else:
            p = subprocess.Popen(defaultCommand, shell=True)
            
        output = p
        # print output
        return render_template('screenshot.html', output=output)
    else:
        return render_template('screenshot.html')




    




@app.route('/tester/', methods=['GET', 'POST'])
def testerAPI():
    #if request.method == 'POST':
    d = datetime.datetime.now()
    d_utc = datetime.datetime.utcnow()
    localTZ = tzlocal.get_localzone()
    tt = d_utc.replace(tzinfo=pytz.utc).astimezone(localTZ).strftime("%b %-d %H:%M:%S")
    # print tt
    return tt

@app.route('/automation/', methods=['GET', 'POST'])
def automation():
    return render_template('automation.html')

@app.route('/reactTest/')
def reactTest():
    return render_template('reactTest.html')

@app.route('/celeste/', methods=['GET', 'POST'])
def celeste():
    # print 'get request made???'

    if request.method == 'POST':
        # print 'post request made!'
        postData =  request.form.get('name')
        # print 'post data:' + postData

    return render_template('celeste.html')

@app.route('/celeste/command/<string:irnetboxMac>/<string:slot>/<string:action>/', methods=['GET', 'POST'])
def command(irnetboxMac, slot, action):
    print('command script executed!')
    # print irnetboxMac
    # TEST TEST TEST
    # information needed:
    # STB selected - Rack and Slot
    # a) Solo - Rack and Slot
    # b) All Clients
    # Command to Send
    mac_list = ['00-80-A3-A9-E3-7A', "00-80-A3-A2-D9-13", "00-80-A3-A9-E3-68", 
                 "00-80-A3-A9-E3-6A", "00-80-A3-A9-E3-7A", 
                 "00-80-A3-A9-DA-67", "00-80-A3-A9-E3-79", 
                 "00-80-A3-A9-E3-78", "00-80-A3-9E-67-37", 
                 "00-80-A3-9D-86-D5", "00-80-A3-9E-67-34",
                 "00-80-A3-9E-67-27", "00-80-A3-9D-86-CF",
                 "00-80-A3-9E-67-35", "00-20-4A-BD-C5-1D",
                 "00-80-A3-9D-86-D2", "00-80-A3-9E-67-3B",
                 "00-80-A3-9E-67-36", "00-80-A3-9E-67-32",
                 "00-80-A3-9D-86-D6", "00-80-A3-9D-86-D3",
                 "00-80-A3-9D-86-D1", "00-80-A3-9D-86-D0",
                 "00-20-4A-DF-64-55", "00-80-A3-A1-7C-3C",
                 "00-80-A3-A2-48-5C", "00-20-4A-DF-65-A0",
                 "00-80-A3-9E-67-3A"]
    
    command_list = ['menu', 'guide', 'info', 'exit', 'select', 'leftArrow', 
                    'rightArrow', 'upArrow', 'downArrow', 'red', 'prev', 
                    'dash','rewind', 'play', 'fastforward', 'chanup', 'record',
                    'chandown', '0','1','2','3','4','5','6','7','8','9', 'back', 'pause', 'enter', 'blue']

    slot_list = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16', '1-16']

    if(irnetboxMac in mac_list and slot in slot_list and action in command_list): 
        # print 'valid command/slotNumber/mac'
        keySendv2(irnetboxMac, action, slot)
        # keySendv2(viewerPositions[viewerPosition][0], action, viewerPositions[viewerPosition][1])
        # keySendv2("00-80-A3-A9-E3-6A", action, '1-16')
        # keySendv2("00-80-A3-A9-E3-7A", val, '1-16')
        return render_template('celeste.html', errorMessage='')
    else:
        print( "invalid mac, slot, or action was used")
        print(irnetboxMac)
        print(action)
        print(slot)

        return render_template('celeste.html', errorMessage='Invalid MAC, command or slot number used')

    

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

    viewerPositions = {
                    "1": [rack_macs["3"], "8"],
                    "2": [rack_macs["2"], "15"],
                    "3": [rack_macs["3"], "5"],
                    "4": [rack_macs["2"], "10"],
                    "5": [rack_macs["2"], "14"],
                    "6": [rack_macs["2"], "16"],
                    "7": [rack_macs["2"], "9"],
                    "8": [rack_macs["2"], "11"],
                    "9": [rack_macs["3"], "1"],
                    "10": [rack_macs["2"], "2"],
                    "11": [rack_macs["3"], "2"],
                    "12": [rack_macs["2"], "5"],
                    "13": [rack_macs["2"], "1"],
                    "14": [rack_macs["2"], "3"],
                    "15": [rack_macs["2"], "4"],
                    "16": [rack_macs["2"], "6"]
                    }
    # print viewerPositions[viewerPosition][0]
  
        


@app.route('/celeste-mock')
def celeste_mock():
    return render_template('celeste-mock.html')


@app.route('/sampleWebkitApp')
def sampleWebkitApp():
    return render_template('sampleWebkitApp.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.secret_key = 'super_secret_key1'
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
