'''
Author : Jay Rambhia
email : jayrambhia777@gmail.com
Git : https://github.com/jayrambhia
gist : https://gist.github.com/jayrambhia
=============================================
Name : deskwidutils
Repo : DeskWid
Git : https://github.com/jayrambhia/DeskWid
version 0.1
'''
#            Copyright (c) 2012 Jay Rambhia

# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import gdbm

def setproxy(command):
    proxystr = command.strip("--proxy ")
    #print proxystr
    if proxystr.startswith("http:"):
        f = gdbm.open("proxyfile","c")
        f["http"] = proxystr
        f.close()
    elif proxystr.startswith("https:"):
        f = gdbm.open("proxyfile","c")
        f["https"] = proxystr
        f.close()
    elif proxystr is "None" or proxystr is "none":
        f = gdbm.open("proxyfile","c")
        f["https"] = ""
        f["http"] = ""
        f.close()

def getproxy():
    f = gdbm.open("proxyfile","c")
    keys = f.keys()
    proxy = {}
    if "http" in keys:
        proxy["http"] = f["http"]
    if "https" in keys:
        proxy["https"] = f["https"]
    return proxy

def getconsumerkey():
    f = gdbm.open("accesskeys","c")
    consumer_key = None
    if "consumer_key" in f.keys():
        consumer_key = f["consumer_key"]
    f.close()
    return consumer_key
    
def getconsumersecret():
    f = gdbm.open("accesskeys","c")
    consumer_secret = None
    if "consumer_secret" in f.keys():
        consumer_secret = f["consumer_secret"]
    f.close()
    return consumer_secret
    
def getaccesstokenkey():
    f = gdbm.open("accesskeys","c")
    access_token_key = None
    if "access_token_key" in f.keys():
        access_token_key = f["access_token_key"]
    f.close()
    return access_token_key
    
def getaccesstokensecret():
    f = gdbm.open("accesskeys","c")
    access_token_secret = None
    if "access_token_secret" in f.keys():
        access_token_secret = f["access_token_secret"]
    f.close()
    return access_token_secret


def setconsumerkey(consumer_key):
    f = gdbm.open("accesskeys","c")
    f["consumer_key"] = consumer_key
    f.close()
    
def setconsumersecret(consumer_secret):
    f = gdbm.open("accesskeys","c")
    f["consumer_secret"] = consumer_secret
    f.close()
    
def setaccesstokenkey(access_token_key):
    f = gdbm.open("accesskeys","c")
    f["access_token_key"] = access_token_key
    f.close()
    
def setaccesstokensecret(access_token_secret):
    f = gdbm.open("accesskeys","c")
    f["access_token_secret"] = access_token_secret
    f.close()

def filterunicode(text):
    
    text = text.replace('&#39;',"'")
    text = text.replace('&quot;','"')
    text = text.replace('&nbsp;',' ')
    text = text.replace('&gt;','>')
    text = text.replace('&lt;','<')
    
    return text
