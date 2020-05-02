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





@app.route('/jsonTest/<string:configNum>/')
def jsonTest(configNum):
    configArr = [
        {
            '1': {'macAddr': '00-80-A3-9D-86-D6', 'slot': '1', 'model': 'H21-100', 'vidRouteMoniker': 'r14s1'},
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
           '1': {'macAddr': '00-80-A3-A9-E3-7A', 'slot': '1', 'model': 'H44-100', 'vidRouteMoniker':'r3s1'}, 
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
           '9': {'macAddr': '00-80-A3-9E-67-34', 'slot': '9', 'model': 'HR44-700', 'vidRouteMoniker': 'r9s9'},
           '10': {'macAddr': '00-80-A3-9E-67-34', 'slot': '10', 'model': 'client', 'vidRouteMoniker': 'r9s10'},
           '11': {'macAddr': '00-80-A3-9E-67-34', 'slot': '11', 'model': 'client', 'vidRouteMoniker': 'r9s11'},
           '12': {'macAddr': '00-80-A3-9E-67-34', 'slot': '12', 'model': 'client', 'vidRouteMoniker': 'r9s12'},
           '13': {'macAddr': '00-80-A3-9E-67-34', 'slot': '13', 'model': 'null', 'vidRouteMoniker': 'r9s12'},
           '14': {'macAddr': '00-80-A3-9E-67-34', 'slot': '14', 'model': 'null', 'vidRouteMoniker': 'r9s12'},
           '15': {'macAddr': '00-80-A3-9E-67-34', 'slot': '15', 'model': 'null', 'vidRouteMoniker': 'r9s12'},
           '16': {'macAddr': '00-80-A3-9E-67-34', 'slot': '16', 'model': 'null', 'vidRouteMoniker': 'r9s12'}, 
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
           '1': {'macAddr': '00-80-A3-9D-86-D6', 'slot': '1', 'model': 'new', 'vidRouteMoniker':'r9s1'}, 
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
        {
           '1': {'macAddr': '00-80-A3-9D-86-D6', 'slot': '1', 'model': 'hs17', 'vidRouteMoniker':'r9s1'}, 
           '2': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '2', 'model': 'hs17', 'vidRouteMoniker':'r9s2'},
           '3': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '3', 'model': 'hs17', 'vidRouteMoniker': 'r9s3'},
           '4': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '4', 'model': 'hs17', 'vidRouteMoniker': 'r9s4'},
           '5': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '5', 'model': 'hs17', 'vidRouteMoniker': 'r9s5'},
           '6': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '6', 'model': 'hs17', 'vidRouteMoniker': 'r9s6'},
           '7': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '7', 'model': 'hs17', 'vidRouteMoniker': 'r9s7'},
           '8': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '8', 'model': 'hs17', 'vidRouteMoniker': 'r9s8'},
           '9': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '9', 'model': 'hs17', 'vidRouteMoniker': 'r9s9'},
           '10': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '10', 'model': 'hs17', 'vidRouteMoniker': 'r9s10'},
           '11': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '11', 'model': 'hs17', 'vidRouteMoniker': 'r9s11'},
           '12': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '12', 'model': 'hs17', 'vidRouteMoniker': 'r9s12'},
           '13': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '13', 'model': 'hs17', 'vidRouteMoniker': 'r9s12'},
           '14': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '14', 'model': 'hs17', 'vidRouteMoniker': 'r9s12'},
           '15': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '15', 'model': 'hs17', 'vidRouteMoniker': 'r9s12'},
           '16': {'macAddr': '00-80-A3-9E-67-3A', 'slot': '16', 'model': 'hs17', 'vidRouteMoniker': 'r9s12'},
        },

        #


    ]
    # return jsonify(fakeData={'1':{'macAddr': '00-80-A3-9D-86-D0', 'slot': '1', 'model': 'H24-100', 'vidRouteMoniker':'r13s1'}})
    return jsonify(fakeData=configArr[int(configNum)-1])

@app.route('/setCookie/', methods = ['POST', 'GET'])
def setCookie():
    resp = make_response(render_template('redesign.html'))
    resp.set_cookie('myCookie', 'testUSER')
    return resp

@app.route('/getCookie/', methods = ['POST', 'GET'])
def getCookie():
    cookieContents = request.cookies.get('myCookie')
    print( cookieContents)
    return cookieContents


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

@app.route('/stbs/', methods=['GET', 'POST'])
def showStbs():
    stbInfo = session.query(Stb).all()
    rackInfo = session.query(RackSlot).all()
    if request.method == 'POST':
        rackSlotObject = RackSlot(
                                rackNumber=request.form['rackNumber'],
                                irnetboxMac=request.form['irnetboxMac'],
                                slot=request.form['slot'],
                                videoRoute=request.form['videoRoute'],
                                stbModel=request.form['stbModel'])
        session.add(rackSlotObject)
        session.commit()
        #print 'stbInfo:'
        #print stbInfo
        #print 'showStb api executed'
    return render_template('stbInfo.html', stbinfo=stbInfo, rackInfo=rackInfo)

stbs = {
    '1': {'mac':'00:00:00:00', 'slot': '1', 'model': 'testModel'}
}
@app.route('/stbs/new/')
def newStb():
    stbs = {'1': {'mac':'001', 'slot': '2'}
            }
    
    if request.method =='POST':
        
        newStb = Stb(mac='0000', slot='1', model='hr44-800', rackslot_id='r3s1')
        session.add(newSTB)
        session.commit()
        return render_template('stbInfo.html', stbinfo='')
    else:
        # print stbs
        newStb = RackSlot(rackNumber='A03', irnetboxMac='00-00-01',
                            slot='1', videoRoute='r3s1',
                            stbModel='hr44-500')
        session.add(newStb)
        session.commit()
        return render_template('stbInfo     .html', stbinfo='')


@app.route('/editRackSlots/<string:rack_id>/', methods=['GET', 'POST'])
def editRackSlots(rack_id):
    rackSlotToEdit = session.query(
        RackSlot).filter_by(id=rack_id).first()
    print rackSlotToEdit
    if rackSlotToEdit == None:
        print 'Error: db entry not found'
        return redirect(url_for('showStbs'))

    if request.method == 'POST':
        rackSlotToEdit.rackNumber = request.form['rackNumber']
        rackSlotToEdit.irnetboxMac = request.form['irnetboxMac']
        rackSlotToEdit.slot = request.form['slot']
        rackSlotToEdit.videoRoute = request.form['videoRoute']
        rackSlotToEdit.stbModel = request.form['stbModel']
        return redirect(url_for('showStbs'))

    return render_template('editRackSlots.html', rackSlotToEdit=rackSlotToEdit)

@app.route('/deleteRackSlot/<string:rackslot_id>/', methods=["GET", "POST"])
def deleteRackSlot(rackslot_id):
    rackSlotToDelete = session.query(RackSlot).filter_by(id=rackslot_id).first()
    #delete file from DB
    if request.method == 'POST':
        session.delete(rackSlotToDelete)
        session.commit()
        return redirect(url_for('showStbs'))
    return render_template('deleteRackSlot.html', rackSlotToDelete=rackSlotToDelete)
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
# @app.route('/setVideo/redesign/<int:configNum>/', methods=['GET', 'POST'])
def configVideo2(cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8,
                 cell9, cell10, cell11, cell12, cell13, cell14, cell15, cell16):
    # sanitize inputs

    #
    vidPositionArr = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8,
                      cell9, cell10, cell11, cell12, cell13, cell14, cell15, cell16]
    vidPositionDict = {}
    for i in vidPositionArr:
        vidPositionDict[str(vidPositionArr.index(i)+1)] = i
    # print "vidPositionDict:"
    # print vidPositionDict  

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

@app.route('/redesign/multiview/setGrid/<string:gridConfig>/')
def multiviewAPI(gridConfig):
    status = setGrid(gridConfig)
    print('status:'+status)
    return "multiviewAPI return "+status+gridConfig

@app.route('/redesign/setSolo/<string:mode>')
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

@app.route('/redesign/setSoloPosition/<string:position>')
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

@app.route('/redesign/labelsMode/<string:mode>')
def labelsMode(mode):
    labelsDisplay(mode)
    return 'labels mode executed'

@app.route('/redesign/audioMeters/<string:mode>')
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
    

@app.route('/reporting', methods=['GET', 'POST'])
@app.route('/reporting/', methods=['GET', 'POST'])
def reporting():
    data = session.query(PostData).all()
    # print "data:"+str(data)
    # using current time to pass into jinja template, so that it can be used to append
    # img url to make it unique and therefore avoid the img-caching issue
    # print datetime.datetime.now().time()  
    for item in data:
        print(item.id)
        print(item.data)
    return render_template('reporting.html', data=data, tme=datetime.datetime.now().time())

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
                    # print commandString
                    p = subprocess.Popen(commandString, shell=True)
            else:
                message = "Did not find any matching test cases with that id, did not run script"
                # print message
                return message
        else:
            message = "script_id needed to start script"
            # print message
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

@app.route('/redesign/', methods=['GET', 'POST'])
def redesign():
    # print 'get request made???'

    if request.method == 'POST':
        # print 'post request made!'
        postData =  request.form.get('name')
        # print 'post data:' + postData

    return render_template('redesign.html')

@app.route('/redesign/command/<string:irnetboxMac>/<string:slot>/<string:action>/', methods=['GET', 'POST'])
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
                    'chandown', '0','1','2','3','4','5','6','7','8','9', 'back']

    slot_list = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16', '1-16']

    if(irnetboxMac in mac_list and slot in slot_list and action in command_list): 
        # print 'valid command/slotNumber/mac'
        keySendv2(irnetboxMac, action, slot)
        # keySendv2(viewerPositions[viewerPosition][0], action, viewerPositions[viewerPosition][1])
        # keySendv2("00-80-A3-A9-E3-6A", action, '1-16')
        # keySendv2("00-80-A3-A9-E3-7A", val, '1-16')
        return render_template('redesign.html', errorMessage='')
    else:
        print( "invalid mac, slot, or action was used")
        print(irnetboxMac)
        print(action)
        print(slot)

        return render_template('redesign.html', errorMessage='Invalid MAC, command or slot number used')

    

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

@app.route('/redesign-mock')
def redesign_mock():
    return render_template('redesign-mock.html')


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
