'''
Author : Jay Rambhia
email : jayrambhia777@gmail.com
Git : https://github.com/jayrambhia
gist : https://gist.github.com/jayrambhia
=============================================
Name : deskwid
Repo : DeskWid
Git : https://github.com/jayrambhia/DeskWid
version 0.1
'''
import pygtk
import gtk
from threading import Thread
import gobject
import os
import twitter
import imdb
import time
import deskwidutils
gtk.gdk.threads_init()

class DeskwidWindow:
    def __init__(self, api):
        self.api = api
        self.timeline_flag = False
        self.timeline_interval = 2
        self.window = gtk.Window()
        self.window.set_title("DeskWid")
        self.window.set_size_request(1000,700)
        self.window.connect("destroy", self.close_application)
        
        self.box = gtk.VBox(False, 2)
        self.window.add(self.box)
        self.box.show()
        
        self.statusbox = gtk.HBox(False, 2)
        self.statusbox.set_size_request(1000,30)
        self.box.pack_start(self.statusbox)
        self.statusbox.show()
        
        self.statusentry = gtk.Entry()
        self.statusentry.set_size_request(900,30)
        self.statusentry.connect("activate", self.getcommand)
        self.statusbox.pack_start(self.statusentry, False, False, 5)
        self.statusentry.show()
        
        self.button = gtk.Button("command")
        self.button.set_size_request(80,30)
        self.button.connect('clicked', self.getcommand)
        self.statusbox.pack_start(self.button, False, False, 3)
        self.button.show()
        
        self.box1 = gtk.HBox(False, 2)
        self.box.pack_start(self.box1, False, False, 3)
        self.box1.show()
        
        self.genbox = gtk.VBox(False, 2)
        self.genbox.set_size_request(680, 650)
        self.box1.pack_start(self.genbox, False, False, 2)
        self.genbox.show()
        
        if self.api is None:
            self.genlabel = gtk.Label("DeskWid 0.1 -- Some of your Twitter API keys might be incorrect")
        else:
            self.genlabel = gtk.Label("DeskWid 0.1")
        self.genlabel.set_size_request(680,30)
        self.genbox.pack_start(self.genlabel)
        self.genlabel.show()
        
        self.sw1 = gtk.ScrolledWindow()
        self.sw1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw1.show()
        self.genbox.pack_start(self.sw1, False, False, 2)
        
        self.genview = gtk.TextView()
        self.genview.set_size_request(680,610)
        self.genview.set_editable(False)
        self.genview.set_wrap_mode(gtk.WRAP_WORD)
        self.genbuffer = self.genview.get_buffer()
        self.sw1.add(self.genview)
        self.genview.show()
        
        self.notebox = gtk.EventBox()
        self.notebox.set_size_request(300, 650)
        self.notebox.connect('leave_notify_event',self.savenote)
        self.box1.pack_start(self.notebox, False, False, 2)
        self.notebox.show()
        
        self.sw2 = gtk.ScrolledWindow()
        self.sw2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw2.show()
        self.notebox.add(self.sw2)
        
        self.notebook = gtk.TextView()
        self.notebook.set_size_request(300, 580)
        self.notebook.set_wrap_mode(gtk.WRAP_WORD)
        self.notebuffer = self.notebook.get_buffer()
        if os.path.isfile(os.path.join(os.getcwd(),'stickynote.txt')):
             infile = open('stickynote.txt','r')
             if infile:
                 text = infile.read()
                 infile.close()
                 self.notebuffer.set_text(text)
                 
        self.sw2.add(self.notebook)
        self.notebook.show()
        
        self.window.show()
        
    def close_application(self, widget=None, data=None):
        self.savenote()
        self.timeline_flag = False
        #self.timeline_thread.exit()
        gtk.main_quit()

    def savenote(self, widget=None, data=None):
        file = open('stickynote.txt','w')
        startiter = self.notebuffer.get_start_iter()
        enditer = self.notebuffer.get_end_iter()
        text = self.notebuffer.get_text(startiter, enditer)
        file.write(text)
        file.close()
        
    def getcommand(self, widget, data=None):
        command = self.statusentry.get_text()
        if command.startswith("\\t "):
            status = "\\t ".join(command.split("\\t ")[1:])
            if len(status) > 140:
                text = "Should not be more than 140 characters"
                gobject.idle_add(self.change_genlabel, text)
            else:
                gobject.idle_add(self.change_genlabel, "tweeting..")
                self.set_status_thread(status)
        
        elif command.startswith("\imdb "):
            gobject.idle_add(self.change_genlabel, "Fetching movie details from IMDb")
            self.fetch_movie_thread()
            
        elif command.startswith("\\timeline"):
            subcom = command.split("\\timeline ")[-1]
            if subcom.isdigit():
                self.timeline_interval = int(subcom)
                
                if self.timeline_interval < 1:
                    self.timeline_interval = 1

                if self.timeline_flag is False:
                    self.timeline_flag = True
                    self.get_timeline_thread()
            
            elif "stop" in subcom:
                self.timeline_flag = False
            
            else:
                subcom = 2 
                if self.timeline_flag is False:
                    self.timeline_flag = True
                    self.get_timeline_thread()
                    
        elif command.startswith("--proxy"):
            #print command
            self.setproxy(command)
        
        elif command.startswith("--consumer_key"):
            #print command
            deskwidutils.setconsumerkey(command.split()[-1])
        
        elif command.startswith("--consumer_secret"):
            #print command
            deskwidutils.setconsumersecret(command.split()[-1])
            #print command.strip("--consumer_secret ")
            
        elif command.startswith("--access_token_key"):
            deskwidutils.setaccesstokenkey(command.split()[-1])
            print command.split()[-1]
            
        elif command.startswith("--access_token_secret"):
            deskwidutils.setaccesstokensecret(command.split()[-1])
        
        #elif command.startswith("quit") or command.startswith("exit"):
         #   self.close_application()
                    
        self.statusentry.set_text("")
        
    def get_timeline_thread(self):
        self.timeline_thread = Thread(target=self.get_timeline).start()
     
    def get_timeline(self):
        since_id = None
        while self.timeline_flag:
            timeline=''
            tweet_list=[]
            tweet_str=''
            try:
                timeline = self.api.GetFriendsTimeline(since_id = since_id)
                if timeline:
                    for i in range(len(timeline)-1,-1,-1):
                        screen_name = '@'+timeline[i].user.screen_name
                        user_name = timeline[i].user.name
                        text = timeline[i].text
                        tweet = screen_name+' ('+user_name+') '+':\n\t'+text
                        tweet_list.append(tweet)
                        tweet_str = tweet_str + tweet + '\n'
                        gobject.idle_add(self.set_genview, tweet)
                    gobject.idle_add(self.change_genlabel, 'timeline')
                    since_id = timeline[0].id
          #          print since_id
            except :
        #        print 'Got some error'
                gobject.idle_add(self.change_genlabel, 'Unable to fetch timeline')
            
            #gobject.idle_add(self.set_genview, tweet_str)
            time.sleep(self.timeline_interval*60)
        
    def set_status_thread(self, status):
        Thread(target=self.set_status, args=(status,)).start()
        
    def set_status(self, status):
        try:
            status_ob = self.api.PostUpdate(status)
            #print "tweeted"
            gobject.idle_add(self.change_genlabel, 'Tweeted')
            self.statusentry.set_text('')
        except:
            gobject.idle_add(self.change_genlabel, 'Got some error')
            #print "Error"
            
    def fetch_movie_thread(self):
        Thread(target=self.fetch_movie).start()
        
    def fetch_movie(self):
        query = self.statusentry.get_text().split("\imdb ")[-1]
        print query
        self.movie = imdb.Movie(query)
        text = self.get_movie_detail()
        gobject.idle_add(self.set_genview, text)
        gobject.idle_add(self.change_genlabel, self.movie.title)
        self.statusentry.set_text("")
        return
        
    def get_movie_detail(self):
        m = self.movie
        if not m.title:
            return "Not Found"
        genre = " ".join(["Genre:",(", ").join(m.genre)])
        actors = " ".join(["Actors:",(", ").join(m.actors)])
        title = " ".join(["Title:",m.title])
        release_date = " ".join(["Release Date:"," ".join(m.release_date.split("\n"))])
        rating = " ".join(["Rating:",m.rating])
        rated = " ".join(["Rated:",m.rated])
        des = "\n".join(["Description:",m.description])
        text = ("\n\n").join([title, release_date, rated, rating, genre, actors, des])
        return text
        
    def change_genlabel(self, text):
        self.genlabel.set_text(text)
        
    def set_genview(self, text):
        startiter = self.genbuffer.get_start_iter()
        enditer = self.genbuffer.get_end_iter()
        pretext = self.genbuffer.get_text(startiter, enditer)
        line = "\n"+180*"-"+"\n"
        text = line.join([text, pretext])
        self.genbuffer.set_text(text)
        
    def setproxy(self, command):
        deskwidutils.setproxy(command)
        
if __name__ == "__main__":
    proxy = deskwidutils.getproxy()
    consumer_key = deskwidutils.getconsumerkey()
    consumer_secret = deskwidutils.getconsumersecret()
    access_token_key = deskwidutils.getaccesstokenkey()
    access_token_secret = deskwidutils.getaccesstokensecret()
    try:
        api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,access_token_key=access_token_key, access_token_secret=access_token_secret,proxy = proxy)
    except twitter.TwitterError:
        api = None
        print "Some keys are incorrect"
    DeskwidWindow(api)
    gtk.main()
