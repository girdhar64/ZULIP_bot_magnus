import pprint
import zulip
import sys
import re
import json
import httplib2
import os

from chatterbot import ChatBot
from translate import Translate
from hackernews import Hackernews
from movie import Movie
from lyrics import Lyrics
from holiday import Holiday
from currency import Currency
from cricket import Cricket
from crypto import Crypto
from giphy import Giphy
from wiki import WikiPedia
# from motivate import Motivate
from shorturl import Urlshortener
from geocode import Geocode
from weather import Weather
from dict_ import Dictionary
from joke import Joke
from pnr import Pnr
from mustread import Mustread
from screenshot import Ss
from poll import Poll
from cricket import Cricket
p = pprint.PrettyPrinter()
BOT_MAIL = "magnus-bot@zulipchat.com"

class ZulipBot(object):
	def __init__(self):
		self.client = zulip.Client(site="https://fazeup.zulipchat.com/api/")
		self.subscribe_all()
		self.hacknews = Hackernews()
		self.trans = Translate()
		self.movie= Movie()
		self.lyrics = Lyrics()
		self.holiday = Holiday()
		self.currency = Currency()
		self.cricket = Cricket()
		# self.chatbot.train("chatterbot.corpus.english")
		self.crypto = Crypto()
		self.trans = Translate()
		self.g = Giphy()
		self.w = WikiPedia()
		# self.tw = Twimega()
		# self.motivate = Motivate()
		self.shortenedurl = Urlshortener()
		self.geo = Geocode()
		self.weather = Weather()
		self.dict_ = Dictionary()
		self.joke = Joke()
		self.pnr = Pnr()
		self.mustread = Mustread()
		self.ss = Ss()
		self.cricket = Cricket()
		self.poll = Poll()
		print("done init")
		self.subkeys = ["crypto", "translate", "define", "joke", "weather",
				"giphy", "pnr", "mustread", "poll", "hackernews", "hn", "HN", "motivate",
				"twitter", "screenshot", "memo", "cricnews", "help", "shorturl","movie", "currency", "holiday", "lyrics"]

	def subscribe_all(self):
		json = self.client.get_streams()["streams"]
		streams = [{"name": stream["name"]} for stream in json]
		self.client.add_subscriptions(streams)

	def process(self, msg):
		content = msg["content"].split()
		sender_email = msg["sender_email"]
		ttype = msg["type"]
		stream_name = msg['display_recipient']
		stream_topic = msg['subject']

		print(content)

		if sender_email == BOT_MAIL:
			return

		print("Sucessfully heard.")

		if content[0].lower() == "magnus" or content[0] == "@**magnus**":
			if content[1].lower() == "translate":
				ip = content[2:]
				ip = " ".join(ip)
				message = self.trans.translate(ip)
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": message
					})
			if content[1].lower() == "movie":
				ip = content[2:]
				ip = " +".join(ip)
				message = self.movie.about(ip)
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": message
					})

			if content[1].lower() == "lyrics":
				author = content[2]
				title = content[3:]
				title = " ".join(title)
				message = self.lyrics.about(author, title)
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": message
					})
			if content[1].lower() == 'holiday':
				quote_data = self.holiday.holiday()
				self.client.send_message({
					"type": "stream",
					"to": stream_name,
					"subject": stream_topic,
					"content": quote_data
					})

			if content[1].lower() == 'currency':
				x = content[2]
				y = content[3]

				quote_data = self.currency.currency(x,y)
				self.client.send_message({
					"type": "stream",
					"to": stream_name,
					"subject": stream_topic,
					"content": quote_data
					})

			if content[1].lower() == "cricnews":
				news = self.cricket.news()
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": news
					})


			if content[1].lower() == 'hackernews' or content[1].lower() == 'hn' or content[1].lower() == 'HN':
				news = self.hacknews.get_hackernews()
				self.client.send_message({
					"type": "stream",
					"to": stream_name,
					"subject": stream_topic,
					"content": news
					})

			if content[1].lower() == "crypto":
				if len(content) > 3 and content[3].lower() == "in":
					message = self.crypto.get_price(content[2], content[4])
				else:
					message = self.crypto.get_price(content[2])
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
						"to": msg["display_recipient"],
					"content": message
					})

			if content[1].lower() == "joke":
				text = self.joke.tellJoke()
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": text
					})

			# if content[1].lower() == 'motivate':
			# 	quote_data = self.motivate.get_quote()
			# 	self.client.send_message({
			# 		"type": "stream",
			# 		"to": stream_name,
			# 		"subject": stream_topic,
			# 		"content": quote_data
			# 		})
			if content[1].lower() == "mustread":
				email = self.mustread.get_email(self.client.get_members(),msg["content"])
				senderusername = self.mustread.get_username(self.client.get_members(),msg["sender_email"])
				print(email)
				self.client.send_message({
					"type": "private",
					"to": email,
					"content": "**"+senderusername+"** mentioned you in must read ! \nThe message says : "+" ".join(content[2:])
					})

			if content[1].lower() == "pnr":
				message = self.pnr.get_pnr(content[2])
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": message
					})
			if content[1].lower() == "screenshot":
				result = self.ss.get_ss(content[2])
				print(result)
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": "Screenshot taken :wink:\n[Screenshot Link]("+result+")"
					})

			if content[1].lower() == "poll":
				if content[2].lower() == "create":
					print(",".join(content[4:]))
					idno = self.poll.create_poll(content[3],content[4:])
					self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": "Poll Successfully Created and id is : **"+str(idno)+"**"
					})
				elif content[2].lower() == "show":
					if content[3].lower() == "all":
						polldetails = self.poll.show_allpoll()
						self.client.send_message({
						"type": "stream",
						"subject": msg["subject"],
						"to": msg["display_recipient"],
						"content": polldetails
						})
					else:
						polldetails = self.poll.show_poll(content[3])
						self.client.send_message({
						"type": "stream",
						"subject": msg["subject"],
						"to": msg["display_recipient"],
						"content": "Poll ID: **"+polldetails["id"]+"**\n Question : **"+polldetails["pollname"]+"**\nOption : **"+polldetails["options"]+"**\n Votes : **"+polldetails["votes"]+"**"
						})
				elif content[2].lower() == "vote":
					vote = self.poll.vote_poll(content[3],content[4])
					self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": "Your Vote Has Been Recorded!"
					})
				elif content[2].lower() == "delete":
					if content[3].lower() == "all":
						deleted = self.poll.delete_allpoll()
						self.client.send_message({
						"type": "stream",
						"subject": msg["subject"],
						"to": msg["display_recipient"],
						"content": "all polls has been removed from database"
						})
					else:
						deleted = self.poll.delete_poll(content[3])
						self.client.send_message({
						"type": "stream",
						"subject": msg["subject"],
						"to": msg["display_recipient"],
						"content": "The given poll has been removed from database"
						})

			if content[1].lower() == "shorturl":
				short_url = self.shortenedurl.get_shorturl(content)
				self.client.send_message({
					"type": "stream",
					"to": stream_name,
					"subject": stream_topic,
					"content": short_url
					})

			if content[1] not in self.subkeys:
				ip = content[1:]
				ip = " ".join(ip)
				message = self.Chatbot.get_response(ip).text
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": message
					})


		elif "magnus" in content and content[0] != "magnus":
			self.client.send_message({
				"type": "stream",
				"subject": msg["subject"],
				"to": msg["display_recipient"],
				"content": "Hey there! :blush:"
				})
		else:
			return

def main():
	bot = ZulipBot()
	bot.client.call_on_each_message(bot.process)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Magnus Served You Well")
		sys.exit(0)
