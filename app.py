from __future__ import print_function

import time
import gspread
import re
import datetime
import random
import codecs
import sys
import json

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
	MessageEvent, TextMessage, TextSendMessage, ImageSendMessage , 
	StickerSendMessage , ImageSendMessage , VideoSendMessage , TemplateSendMessage,
	SourceUser, SourceGroup, SourceRoom,
	TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
	ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
	PostbackTemplateAction, DatetimePickerTemplateAction,
	CarouselTemplate, CarouselColumn, PostbackEvent,
	StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
	ImageMessage, VideoMessage, AudioMessage, FileMessage,
	UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)


score_sheet_ID = '1F0aMMBcADRSXm07IT2Bxb_h22cIjNXlsCfBYRk53PHA'
my_database_sheet_ID = '1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk'
april_ID='Udf8f28a8b752786fa7a6be7d8c808ec6'

app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('LSZQfsnkkA1ODzqj3bPbe8lkiyW9aD22BLKsiw0B1o+yE5KS717frBcTy4Rb785oXnBlASYnpdyopKzaMhj2XkD4CEEUk3O88gxiMeRYcymrMg7irDdVuMJYWmJbIfZDJ79z925dwdXLMT6BANbGGwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('2bd5cc6f366fd9c567693ab4e18a6ea2')
# user_id = "Udf8f28a8b752786fa7a6be7d8c808ec6"
auth_json_path = "./auth.json"

now = datetime.datetime.now()
today = time.strftime("%c")
mode = 1

def get_value_from_google_sheet(SPREADSHEET_ID,RANGE_NAME):
	# Setup the Sheets API
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	# Call the Sheets API
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
												 range=RANGE_NAME).execute()
	return result.get('values', [])


def get_score_sheet(list_top,list_name,list_target,target):
	global score_sheet_ID
	values = get_value_from_google_sheet(score_sheet_ID,'A2:M11')
	if not values:
		print('No data found.')
	else:
		for row in values:	
			list_top.append(row[0])
			list_name.append(row[1])
			list_target.append(row[target])

def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path,scopes)
    return gspread.authorize(credentials)

gss_scopes = ['https://spreadsheets.google.com/feeds']
gss_client = auth_gss_client(auth_json_path, gss_scopes)

def leaderboard(key):
	list_top = []
	list_name = []
	list_score = []
	get_score_sheet(list_top,list_name,list_score,key)
	# print (list_top,list_name,list_score)
	score_str = ""
	for i in range(0,10):
		score_str += (str(list_top[i])+" --- "+list_score[i]+"\n【"+list_name[i]+"】\n")
	# print(score_str)
	score_str += str((datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S"))
	# score_str += str(time.strftime("%c"))
	return score_str

def event_progress():
	# Setup the Sheets API
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	# Call the Sheets API
	SPREADSHEET_ID = '1F0aMMBcADRSXm07IT2Bxb_h22cIjNXlsCfBYRk53PHA'
	RANGE_NAME = 'E15'
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
												 range=RANGE_NAME).execute()
	values = result.get('values', [])
	if not values:
		print('No data found.')
	else:
		for row in values:	
			return row[0]

def event_remain_time():
	global score_sheet_ID
	values = get_value_from_google_sheet(score_sheet_ID,'E17')
	if not values:
		print('No data found.')
	else:
		for row in values:	
			return row[0]
			
def switch_still_on():
	global mode	
	mode = 1
	return '我已經正在說話囉，歡迎來跟我互動 ^_^ '

def switch_off():
	global mode	
	mode = 0
	return '好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「!說話」 > <'

def readme():
	with open('readme.txt', 'r') as f:
		content = f.read()
	return content

def room_get():
	global my_database_sheet_ID
	list_room = []
	values = get_value_from_google_sheet(my_database_sheet_ID,'room!A1:A')
	if not values:
		print('No data found.')
	else:
		for row in values:	
			list_room.append(row[0])
		return "當前房號1為： "+list_room[0]+"\n當前房號2為： "+list_room[1]

def room_update(user_message):
	global my_database_sheet_ID
	try:
		room_number = user_message.split(" ",1)
		print("get new number : "+room_number[1])
	except:
		return "【請依照範例輸入：】\nroom1 12345"

	try:
		wks = gss_client.open_by_key(my_database_sheet_ID)
		sheet = wks.worksheet('room')
		sheet.update_acell('A1', room_number[1])
		return "當前房號1已更新為："+room_number[1]	
	except:
		line_bot_api.push_message(april_ID, TextSendMessage(text='智乃壞掉囉~~~'))
		return "看來是google又壞掉了QQ，我已經幫忙通知四月拔拔了! 請稍等~~"

def room_update2(user_message):
	global my_database_sheet_ID
	try:
		room_number = user_message.split(" ",1)
		print("get new number : "+room_number[1])
	except:
		return "【請依照範例輸入：】\nroom2 12345"

	try:
		wks = gss_client.open_by_key(my_database_sheet_ID)
		sheet = wks.worksheet('room')
		sheet.update_acell('A2', room_number[1])
		return "當前房號1已更新為："+room_number[1]	
	except:
		line_bot_api.push_message(april_ID, TextSendMessage(text='智乃壞掉囉~~~'))
		return "看來是google又壞掉了QQ，我已經幫忙通知四月拔拔了! 請稍等~~"
			
def slient_mode(user_message,event):
	global mode
	if(user_message == "!說話"):
		mode = 1 
		message = TextSendMessage(text='沒問題 ^_^，我來陪大家聊天惹，但如果覺得我太吵的話，請跟我說 「!閉嘴」 > <')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["!閉嘴"]):
		mode = 0
		message = TextSendMessage(text='我已經閉嘴了 > <  (小聲)')
		line_bot_api.reply_message(event.reply_token,message)

def active_mode(user_message,event):
	global mode
	print ("start seraching key in cmd box ...")
	message = "default"
	if(user_message in ["!閉嘴"]):
		message = switch_off()
	elif(user_message in ["!說話"]):
		message = switch_still_on()
	elif(user_message in ["!使用說明書","!help","!說明書"]):
		message = readme()
	elif(user_message in ["即時排名","即時戰況",'排名','分數','戰況','score']):
		message = leaderboard(2)
	elif(user_message in ["%數","%"]):
		message = leaderboard(3)
	elif(user_message in ['一位差']):
		message = leaderboard(4)
	elif(user_message in ['分數差']):
		message = leaderboard(5)
	elif(user_message in ['場數差']):
		message = leaderboard(6)
	elif(user_message in ["追擊時間","脫褲子"]):
		message = leaderboard(7)
	elif(user_message in ['時速']):
		message = leaderboard(8)
	elif(user_message in ['場速']):
		message = leaderboard(9)
	elif(user_message in ["活動進度",'進度']):
		message = event_progress()
	elif(user_message in ["剩餘時間"]):
		message = event_remain_time()
	elif(user_message in ["房號","room"]):
		message = room_get()
	elif(user_message.find("room1") == 0):
		message = room_update(user_message)
	elif(user_message.find("room2") == 0):
		message = room_update2(user_message)
	
	if message != "default" :
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
		return
	print ("key not found in cmd box !")
	

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
	global timezone
	global mode 
	print("now: "+str((datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S")))
	print(event)		
	user_message = event.message.text
	
	if(user_message== "test"):
		message = TextSendMessage(text='Hello World !!!')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message== "state"):
		message = TextSendMessage(
			text="(silent mode)" if mode == 0 else "(active mode)"
		)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["!壞掉啦","呼叫工程師","呼叫四月"]):
		line_bot_api.push_message(april_ID, TextSendMessage(text='智乃壞掉囉~~~'))
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經幫您通知四月拔拔了! 請稍等~~"))
	elif(mode == 0):
		slient_mode(user_message,event) 
	elif(mode == 1):
		active_mode(user_message,event)
		
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
