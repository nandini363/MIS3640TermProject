import requests
import time
from twilio.rest import Client


def isAvailible(url):
	"""checks if shoe is availible"""
	inStock = '''"availability": "https://schema.org/InStock"'''
	outOfStock = '''"availability": "https://schema.org/OutOfStock"'''
	r = requests.get(url)
	if inStock in r.text:
		return True
	return False


def sendtext(inStock,number, url):
	"""sends text if in stock"""
	if inStock:
		account_sid = "AC503e3d79fa5deb5654e06699f3e1b525" # Change this to your own Twilio account SID
		auth_token = '89cf9211d801ac1b7705bbdbbfc306e0' # Change this to your own Twilio authorization token
		client = Client(account_sid, auth_token)

		message = client.messages \
		                .create(
		                     body="Shoe is now in stock, here is the link: %s" % url,
		                     from_='+13237451834', #Change this to your own Twilio number
		                     to=number
		                 )

		print(message.sid)
		return True
	return False

def stripNumber(number):
	"""removes any extra symbols from user entered phone number"""
	#removes any characters that arent actual numbers
	num = ""
	charsToRemove = ["-","(",")", " ",]
	for x in number:
		if x not in charsToRemove:
			num = num + x
	return num

def numberVerify(number):
	"""Verifies phone number"""
	if len(number) != 10:
		return False 
	return True

def urlVerify(url):
	"""Verifies if url is a Nike shoe url"""
	if "https://www.nike.com/t/" not in url:
		return False
	return True


def getUrl():
	"""User inputs Url"""
	urlCheck = False
	while not urlCheck:
		url = input("Enter Nike URL:")
		urlCheck = urlVerify(url)
		if not urlCheck:
			print("Please enter a correct Nike URL")
	return url

	
	
def getNumber():
	"""User inputs phone number"""
	numCheck = False
	while not numCheck:
		number = input("Enter phone number:")
		number = stripNumber(number)
		numCheck = numberVerify(number)
		if not numCheck:
			print("Please enter a correct phone number")
	#Need +1 for twilio api
	number = "+1" + number
	return number


def shoeBot():
	"""if not in stock it rechecks every minute until shoe is in stock"""
	url = getUrl()
	number = getNumber()
	sent = False
	#checks if in stock every minute
	while not sent:
		inStock = isAvailible(url)
		sent = sendtext(inStock,number,url)
		if not sent:
			print("shoe not in stock will check again in 1 minute")
			time.sleep(60)
	return True





if __name__ == "__main__":
    done = shoeBot()
    if done:
    	print("Text has been sent. Please restart bot if you want to check for another Nike shoe")

