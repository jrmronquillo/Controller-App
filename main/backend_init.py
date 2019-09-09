
from flask import (Flask, render_template, request, redirect, jsonify, url_for,
                   flash)
from flask import session as login_session
import random
import string
import urllib2


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

@app.route('/')
def main():
	return 'backend is running!'


@app.route('/rssTest')
@support_jsonp 
def rssTest():
    print rssFeedConverter()
    fullData= rssFeedConverter()
    testArr = []
    for item in fullData:
        print item.title
        testArr.append(item.title)
    # testArr = ['test', 'test2']
    
    return jsonify(title=testArr)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.secret_key = 'super_secret_key1'
    app.debug = True
    app.run(host='0.0.0.0', port=5001)