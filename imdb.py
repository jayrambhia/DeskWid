'''
Author : Jay Rambhia
email : jayrambhia777@gmail.com
Git : https://github.com/jayrambhia
gist : https://gist.github.com/jayrambhia
=============================================
Name : imdb
Repo : DeskWid
Git : https://github.com/jayrambhia/DeskWid
version 0.1
'''
from BeautifulSoup import BeautifulSoup
from mechanize import Browser
from mechanize._mechanize import LinkNotFoundError
import re
from urllib2 import URLError
import deskwidutils
def getunicode(soup):
	body=''
	if isinstance(soup, unicode):
		soup = soup.replace('&#39;',"'")
		soup = soup.replace('&quot;','"')
		soup = soup.replace('&nbsp;',' ')
		body = body + soup
	else:
		if not soup.contents:
			return ''
		con_list = soup.contents
		for con in con_list:
			body = body + getunicode(con)
	return body

class Movie:
    def __init__(self, query):
        self.query = query
        self.title = ""
        self.rating = ""
        self.rated = ""
        self.actors = ""
        self.genre = ""
        self.description = ""
        self.release_date = ""
        if self.query:
            self.fetchmovie()
        
    def fetchmovie(self):
        movie_detail = getmoviedetails(self.query)
        self.setattributes(movie_detail)
        
    def setattributes(self, movie_detail):
        if movie_detail is not None:
            self.title = movie_detail["title"]
            self.rating = movie_detail['rating']
            self.rated = movie_detail['rated']
            self.actors = movie_detail['actors']
            self.genre = movie_detail['genre']
            self.description = movie_detail['description']
            self.release_date = movie_detail['release_date']
        

def getmoviedetails(query):
    movie_detail = None
    URL = getURL(query)
    proxy = deskwidutils.getproxy()
    #proxy = None
    soup = getsoup(URL, proxy)
    if soup is not None:
        movie_detail = fetchmoviedetails(soup)
    return movie_detail
        
def fetchmoviedetails(soup):
    detail_dict={'title':'',
                'rating':'',
                'rated':'',
                'actors':'',
                'genre':'',
                'description':'',
                'release_date':''}
    try:
        movie_title = getunicode(soup.find('title'))
        rate = soup.find('span',itemprop='ratingValue')
        rating = getunicode(rate)
    
        actors=[]
        actors_soup = soup.findAll('a',itemprop='actors')
        for i in range(len(actors_soup)):
            actors.append(getunicode(actors_soup[i]))
    
        des = soup.find('meta',{'name':'description'})['content']

        genre=[]
        infobar = soup.find('div',{'class':'infobar'})
        r = infobar.find('',{'title':True})['title']
        genrelist = infobar.findAll('a',{'href':True})
	
        for i in range(len(genrelist)-1):
            genre.append(getunicode(genrelist[i]))
        release_date = getunicode(genrelist[-1])
    
        detail_dict={'title':movie_title,
                    'rating':rating,
                    'rated':r,
                    'actors':actors,
                    'genre':genre,
                    'description':des,
                    'release_date':release_date}
    except TypeError,e:
        print e
    return detail_dict
    
def getURL(search_query):
    base_URL = "http://www.imdb.com/find?q="
    search_query = '+'.join(search_query.split())
    URL = base_URL + search_query + "&s=all"
    return URL
    
def getsoup(URL, proxy = None):
    br = Browser()
    if proxy is not None:
        br.set_proxies(proxy)
    br.open(URL)
    try:
        title_URL = br.find_link(url_regex = re.compile(r'/title/tt.*'))
    except LinkNotFoundError:
        return None
    try:
        res = br.follow_link(title_URL)
    except URLError:
        return None
    
    soup = BeautifulSoup(res.read())
    return soup

def getproxy():
    proxy = {'http':'http://f2010059:j@10.1.9.36:8080',
             'https':'https://f2010059:j@10.1.9.36:8080'}
    return proxy

