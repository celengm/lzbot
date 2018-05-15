from __future__ import print_function

import time
import gspread
import re
import datetime
import random

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from flask import Flask, request, abort
from urllib.request import urlopen
from oauth2client.service_account import ServiceAccountCredentials

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage , StickerSendMessage
)

def get_sheet(list_time,list_name,list_content):
	# Setup the Sheets API
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	# Call the Sheets API
	SPREADSHEET_ID = '1Txkvi53ANaFl8Qqug4EsaKTwTGDIgDEarhrewEe2Ruk'
	RANGE_NAME = 'A2:D'
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
												 range=RANGE_NAME).execute()
	values = result.get('values', [])
	if not values:
		print('No data found.')
	else:
		sheet_result = "hello world!"
		for row in values:
			# Print columns A and E, which correspond to indices 0 and 4.		
			list_time.append(row[0])
			# list_name.append(row[1])
			list_content.append(row[3])
			# print('time:%s content:%s' % (row[0], row[1] , row[2]))
		

# def post_content():
	
			
def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path,scopes)
    return gspread.authorize(credentials)

 
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('+wjG+A6ltvlFVrmQmxyBaXcfljMtYaCTMXnVBoTxhWwMcSRX9+1mMObUO6oVongrp2y7parq1a1/bbbwvOhn/iO26lASkwoWX1u0HBisf7ZRr4cfMzcXFYM/8eFwpeQkdcXYz2obPYl1sE6+kWyC4QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4c154ea12f7a284b5edd99087d760143')
user_id = "Udf8f28a8b752786fa7a6be7d8c808ec6"

auth_json_path = "./auth.json"

gss_scopes = ['https://spreadsheets.google.com/feeds']



gss_client = auth_gss_client(auth_json_path, gss_scopes)

def update_sheet(gss_client, key, today,messageid,messagetype,text):
    wks = gss_client.open_by_key(key)
    sheet = wks.sheet1
    sheet.insert_row([today,messageid,messagetype,text], 2)



# update.py
		
#push message to one user
# line_bot_api.push_message(user_id, 
    # TextSendMessage(text='Hello World!'))
# push message to multiple users
# line_bot_api.multicast(['user_id1', 'user_id2'], 
    # TextSendMessage(text='Hello World!'))	
	
	
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	print (event)
	# print (event.source.userId)

	if(event.message.text== "test"):
		message = TextSendMessage(text='Hello World !!!')
		line_bot_api.reply_message(event.reply_token,message)
	elif(event.message.text== "歷史訊息"):
		line_bot_api.push_message(user_id,TextSendMessage(text="以下僅列出前10筆歷史訊息"))
		list_time = []
		list_name = []
		list_content = []
		get_sheet(list_time,list_name,list_content)
		print (list_time,list_name,list_content)
		score_str = ""
		for i in range(0,10):
			score_str += (str(list_content[i])+"	("+list_time[i]+")\n")
		print(score_str)
		line_bot_api.push_message(user_id,TextSendMessage(text=score_str))
	elif(event.message.text== "貼圖辣"):
		randsticker = random.randint(140,180)
		message = StickerSendMessage(package_id='2',sticker_id=str(randsticker))
		line_bot_api.reply_message(event.reply_token,message)
	
	# lineuserid = event.source.userId
	messageid = event.message.id
	# lineuserid = "howard"
	messagetype = event.message.type
	text = event.message.text
	# message = TextSendMessage(text)
	spreadsheet_key = "1Txkvi53ANaFl8Qqug4EsaKTwTGDIgDEarhrewEe2Ruk"	
	# spreadsheet_key_path = 'spreadsheet_key'
	now = datetime.datetime.now()

	# if cheapest_price is not None:
	today = time.strftime("%c")
	# with open(spreadsheet_key_path) as f:
	#    spreadsheet_key = f.read().strip()
	update_sheet(gss_client, spreadsheet_key, today, messageid,messagetype,text)
	# push message to one user
	# line_bot_api.push_message(user_id, 
	# TextSendMessage(text='Hello World!'))
		
	# line_bot_api.reply_message(
		# event.reply_token,
		# message)
		

		
		
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
