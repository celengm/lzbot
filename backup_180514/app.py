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
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage , StickerSendMessage , ImageSendMessage , VideoSendMessage
)

# video_list = ["https://i.imgur.com/Upmorh0.mp4"]
# image_list = ['https://i.imgur.com/N48r8cd.gif','https://i.imgur.com/iSAnJd4.gif','https://i.imgur.com/8H72aoG.gif','https://i.imgur.com/BTNb7zf.gif','https://i.imgur.com/XO7YFi5.gif','https://i.imgur.com/x0qYhR7.gif']

BGD_namelist = ['牛込りみ','山吹沙綾','戸山香澄','市ヶ谷有咲','花園たえ','上原ひまり','羽沢つぐみ','美竹蘭','宇田川巴','青葉モカ','白鷺千聖','若宮イヴ','丸山彩','大和麻弥','氷川日菜','氷川紗夜','宇田川あこ','湊友希那','白金燐子','今井リサ','北沢はぐみ','奥沢美咲','弦巻こころ','瀬田薫','松原花音']

app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('+wjG+A6ltvlFVrmQmxyBaXcfljMtYaCTMXnVBoTxhWwMcSRX9+1mMObUO6oVongrp2y7parq1a1/bbbwvOhn/iO26lASkwoWX1u0HBisf7ZRr4cfMzcXFYM/8eFwpeQkdcXYz2obPYl1sE6+kWyC4QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4c154ea12f7a284b5edd99087d760143')
# user_id = "Udf8f28a8b752786fa7a6be7d8c808ec6"
auth_json_path = "./auth.json"

now = datetime.datetime.now()
today = time.strftime("%c")
mode = 1

def get_score_sheet(list_top,list_name,list_target,target):
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
	RANGE_NAME = 'A2:G11'
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
												 range=RANGE_NAME).execute()
	values = result.get('values', [])
	if not values:
		print('No data found.')
	else:
		sheet_result = "hello world!"
		for row in values:	
			list_top.append(row[0])
			list_name.append(row[1])
			list_target.append(row[target])
		
def get_key_response(key):
	# Setup the Sheets API
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	# Call the Sheets API
	SPREADSHEET_ID = '1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk'
	RANGE_NAME = 'Sheet1!A2:B800'
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
												 range=RANGE_NAME).execute()
	values = result.get('values', [])
	if not values:
		print('No data found.')
	else:
		list_key = []
		list_response = []
		for row in values:	
			list_key.append(row[0])
			list_response.append(row[1])
		if key in list_key:
			# list_response = list_key.index(key)
			list_response_index = [i for i,v in enumerate(list_key) if v==key]
			print (list_response_index)
			random_reply = random.randint(0,len(list_response_index)-1)
			return list_response[list_response_index[random_reply]]
		else:
			return 0
		
def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path,scopes)
    return gspread.authorize(credentials)

gss_scopes = ['https://spreadsheets.google.com/feeds']
gss_client = auth_gss_client(auth_json_path, gss_scopes)

def update_sheet(gss_client, key, today,messageid,messagetype,text):
    wks = gss_client.open_by_key(key)
    sheet = wks.sheet1
    sheet.insert_row([today,messageid,messagetype,text], 2)
	
def update_sheet_key(gss_client, key, input , output):
    wks = gss_client.open_by_key(key)
    sheet = wks.sheet1
    sheet.insert_row([input , output], 2)
	
def get_food_sheet(key):
	# Setup the Sheets API
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	# Call the Sheets API
	SPREADSHEET_ID = '1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk'
	if key == 1:
		RANGE_NAME = 'food!A2:A'
	elif key == 2:
		RANGE_NAME = 'food!B2:B'
	result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
												 range=RANGE_NAME).execute()
	values = result.get('values', [])
	if not values:
		print('No data found.')
	else:
		list_food = []
		for row in values:	
			list_food.append(row[0])
			
		random_food_index = random.randint(0,len(list_food)-1)
		return list_food[random_food_index]

def gacha_BGD():
	random_number = random.randint(0,999)
	if random_number <= 30-1:
		return "4★ "+random.choice(BGD_namelist)
	elif random_number <= 30+85-1:
		return "3★ "+random.choice(BGD_namelist)
	elif random_number <= 30+85+885-1:
		return "2★ "+random.choice(BGD_namelist)
	
def gacha_last_BGD():
	random_number = random.randint(0,99)
	if random_number <= 3-1:
		return "4★ "+random.choice(BGD_namelist)
	elif random_number <= 3+97-1:
		return "3★ "+random.choice(BGD_namelist)
	
def ten_gacha_BGD():
	ten_gacha_BGD_result=""
	for i in range(9):
		ten_gacha_BGD_result += str(gacha_BGD())
		ten_gacha_BGD_result += "\n"
	ten_gacha_BGD_result += str(gacha_last_BGD())
	return ten_gacha_BGD_result
	
def gacha_CGSS():
	random_number = random.randint(0,99)
	if random_number <= 3-1:
		return "SSR"
	elif random_number <= 3+12-1:
		return "SR"
	elif random_number <= 3+12+85-1:
		return "R"
	
def gacha_last_CGSS():
	random_number = random.randint(0,99)
	if random_number <= 3-1:
		return "SSR"
	elif random_number <= 3+97-1:
		return "SR"
	
def ten_gacha_CGSS():	
	ten_gacha_CGSS_result=""
	for i in range(9):
		ten_gacha_CGSS_result += str(gacha_CGSS())
		if i == 4:
			ten_gacha_CGSS_result += "\n"
		else:
			ten_gacha_CGSS_result += " , "
	ten_gacha_CGSS_result += str(gacha_last_CGSS())
	return ten_gacha_CGSS_result

def teach(user_message):
	reply_message = user_message.lstrip("!教育 ")
	split_result = reply_message.split(' ', 1 )
	if(len(split_result) <= 1):
		return "學習字詞失敗 > <"
	else:
		spreadsheet_key = "1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk"
		update_sheet_key(gss_client,spreadsheet_key,split_result[0],split_result[1])
		success_learn ="已學習字詞 「"+split_result[0]+"」 !!!"
		return success_learn

def leaderboard():
	list_top = []
	list_name = []
	list_score = []
	get_score_sheet(list_top,list_name,list_score,2)
	# print (list_top,list_name,list_score)
	score_str = ""
	for i in range(0,10):
		score_str += (str(list_top[i])+"\t"+list_name[i]+"\t"+list_score[i]+"\n")
	# print(score_str)
	return score_str

def your_pants():
	list_top = []
	list_name = []
	list_time = []
	get_score_sheet(list_top,list_name,list_time,6)
	# print (list_top,list_name,list_score)
	score_str = ""
	score_str += ("目前" + str(list_top[0])+"為\t"+list_name[0]+"\t\n")
	for i in range(1,10):
		score_str += (list_name[i]+"\t還需要 "+list_time[i]+" 才能脫 "+list_name[i-1]+" 的褲子\n")
	return score_str
			
def slient_mode(user_message,event):
	global mode
	if(user_message== "!說話"):
		mode = 1
		message = TextSendMessage(text='沒問題 ^_^，我來陪大家聊天惹，但如果覺得我太吵的話，請跟我說 「!閉嘴」 > <')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message== "!閉嘴"):
		mode = 0
		message = TextSendMessage(text='我已經閉嘴了 > <  (小聲)')
		line_bot_api.reply_message(event.reply_token,message)

def	active_mode(user_message,event):
	global mode
	if(user_message in ["!閉嘴","!安靜","!你閉嘴","!你安靜"]):
		mode = 0
		message = TextSendMessage(text='好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「!說話」 > <')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message == "!說話"):
		mode = 1
		message = TextSendMessage(text='我已經正在說話囉，歡迎來跟我互動 ^_^ ')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["即時排名","即時戰況"]):
		score_str = leaderboard()
		message = TextSendMessage(text=score_str)
		line_bot_api.reply_message(event.reply_token,message)
		# line_bot_api.push_message(user_id,TextSendMessage(text=score_str))
	elif(user_message in ["脫褲子","脫內褲"]):
		score_str = your_pants()
		message = TextSendMessage(text=score_str)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["貼圖辣","貼圖啦","貼圖","貼圖喇"]):
		randsticker = random.randint(140,180)
		message = StickerSendMessage(package_id='2',sticker_id=str(randsticker))
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message == "母湯電影版"):		
		message = VideoSendMessage(
		original_content_url='https://i.imgur.com/Upmorh0.mp4',
		preview_image_url='https://i.imgur.com/Upmorh0.gif'
		)
		line_bot_api.reply_message(event.reply_token, message)
	elif(user_message == "!抽食物"):
		food = get_food_sheet(1)
		message = TextSendMessage(text=food)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message == "!抽飲料"):
		food = get_food_sheet(2)
		message = TextSendMessage(text=food)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message == "!CGSS單抽"):
		result = "【您抽到的是：】\n"
		result += gacha_CGSS()
		message = TextSendMessage(text=result)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["!CGSS十連","!CGSS十抽","!CGSS10連","!CGSS10抽"]):
		result = "【您抽到的是：】\n"
		result += ten_gacha_CGSS()
		message = TextSendMessage(text=result)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["!BGD單抽","!bgd單抽"]):
		result = "【您抽到的是：】\n"
		result += gacha_BGD()
		message = TextSendMessage(text=result)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message in ["!BGD十連","!BGD十抽","!BGD10連","!BGD10抽","!bgd十連","!bgd十抽","!bgd10連","!bgd10抽"]):
		result = "【您抽到的是：】\n"
		result += ten_gacha_BGD()
		message = TextSendMessage(text=result)
		line_bot_api.reply_message(event.reply_token,message)	
		
	# ------ below are find function ------	 
	elif(user_message.find("母湯") == 0):
		message = ImageSendMessage(
		original_content_url= "https://i.imgur.com/rUZ4AdD.jpg",
		preview_image_url= "https://i.imgur.com/rUZ4AdD.jpg"
		)
		line_bot_api.reply_message(event.reply_token, message)	
	elif(user_message.find("!機率") == 0):
		probability = random.randint(0,101)
		reply_message = user_message.lstrip("!機率 ")
		reply_message = "嗯... 我覺得 "+reply_message + " 的機率是 "+ str(probability) + " % !!!"
		message = TextSendMessage(text=reply_message)
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message.find("!抽數字") == 0):
		reply_message = user_message.lstrip("!抽數字 ")
		random_number = random.randint(1,int(reply_message))
		message = TextSendMessage(text=random_number)
		line_bot_api.reply_message(event.reply_token,message)		
	elif(user_message.find("!教育") == 0):
		teach_result = teach(user_message)
		message = TextSendMessage(text=teach_result)
		line_bot_api.reply_message(event.reply_token,message)
	else:
		key_message = get_key_response(user_message)
		if key_message != 0:
			message = TextSendMessage(text=key_message)
			line_bot_api.reply_message(event.reply_token,message)
	
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
	global mode 
	print(today)
	print(event)		
	user_message = event.message.text
	
	if(user_message== "test"):
		message = TextSendMessage(text='Hello World !!!')
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message== "state"):
		if mode == 0:
			message = TextSendMessage(text="(silent mode)")
		elif mode == 1:
			message = TextSendMessage(text="(active mode)")
		line_bot_api.reply_message(event.reply_token,message)
	elif(user_message== "!重新開機"):
		quit()
	elif(mode == 0):
		slient_mode(user_message,event)
	elif(mode == 1):
		active_mode(user_message,event)
		
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
	
# notes 
	
#push message to one user
# line_bot_api.push_message(user_id, 
    # TextSendMessage(text='Hello World!'))
# push message to multiple users
# line_bot_api.multicast(['user_id1', 'user_id2'], 
    # TextSendMessage(text='Hello World!'))	

# lineuserid = event.source.userId
# messageid = event.message.id
# lineuserid = "howard"
# messagetype = event.message.type
# text = event.message.text
# message = TextSendMessage(text)

# spreadsheet_key_path = 'spreadsheet_key'
# if cheapest_price is not None:

# with open(spreadsheet_key_path) as f:
#    spreadsheet_key = f.read().strip()
# update_sheet(gss_client, spreadsheet_key, today, messageid,messagetype,text)
# push message to one user
# line_bot_api.push_message(user_id, 
# TextSendMessage(text='Hello World!'))

# line_bot_api.reply_message(
# event.reply_token,
# message)
		