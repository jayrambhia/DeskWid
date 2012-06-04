import twitter
import pygtk
pygtk.require('2.0')
import gtk

class tweetBox:
	def __init__(self, api):
		self.api = api
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_size_request(800,30)
		self.window.connect("destroy", self.close_application)
		self.window.set_title("tweetBox")
		
		self.box = gtk.HBox(False,2)
		self.window.add(self.box)
		self.box.show()
		
		self.tweet_entry = gtk.Entry()
		self.tweet_entry.set_size_request(800,30)
		self.tweet_entry.connect("activate",self.tweet)
		self.tweet_entry.set_max_length(140)
		self.box.pack_start(self.tweet_entry, False, False, 3)
		self.tweet_entry.show()
		'''
		self.button = gtk.Button('Tweet')
		self.button.set_size_request(100,30)
		self.button.connect('clicked', self.tweet)
		self.box.pack_end(self.button,False,False,2)
		self.button.show()
		'''
		self.window.show()

	def tweet(self, widget, data=None):
		text = self.tweet_entry.get_text()
		if text:
			status = self.api.PostUpdate(text)
			if status:
				self.tweet_entry.set_text('')
		return
		
	def close_application(self, widget):
		gtk.main_quit()
		
def main():
	api = twitter.Api(consumer_key="P6J5KGTWLvdArPFUg8eKBw", consumer_secret="s9QMl8EznVAfyG1AzpN0B0IiBjxZCX1uITzrjmAj6M",access_token_key="70108357-QkLkIJC6NVhrvnARuE7ofLm2Tmtcv6qOeHbVpm1By", access_token_secret="Z9adD6B0l379po2asWEwxPIKagpQfSTDmyak5zbPE",proxy ={'http':'http://f2010059:j@10.1.9.36:8080',
'https' : 'https://f2010059:j@10.1.9.36:8080' })
	tweetBox(api)
	gtk.main()
	
if __name__ == '__main__':
	main()
		
	
