import xml.sax
from TextProcessing import processText,processTitle
from collections import defaultdict
import sys
import timeit

pageList = []

class WikiPage():
    def __init__(self):
        self.title = ""
        self.ns = ""
        self.id = ""
        self.redirect = ""
        self.revision = {'id':"",'parentid':"",'timestamp':"",'contributor':{'username':"",'id':""},'minor':"",'comment':"",'text':"",'shal':"",'model':"",'format':""}

    def refresh(self):
        self.title = ""
        self.ns = ""
        self.id = ""
        self.redirect = ""
        self.revision = {'id':"",'parentid':"",'timestamp':"",'contributor':{'username':"",'id':""},'minor':"",'comment':"",'text':"",'sha1':"",'model':"",'format':""}

class WikiContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.stack = []
        self.title = ""
        self.ns = ""
        self.id = ""
        self.redirect = ""
        self.revision = {'id':"",'parentid':"",'timestamp':"",'contributor':{'username':"",'id':""},'minor':"",'comment':"",'text':"",'sha1':"",'model':"",'format':""}
        self.pageObject = WikiPage()
        self.textWords = None
        self.infoBoxWords = None
        self.categoryWords = None
        self.externalLinkWords = None

    def startElement(self, name, attrs):
        #print(("startElement '" + name + "'"))
        self.stack.append(name)
        if name=="page":
            self.refresh()
            self.pageObject.refresh()
        #print(self.stack)

    def endElement(self, name):
        #print(("endElement '" + name + "'"))
        self.stack.pop()
        global pageList
        #print(self.stack)
        if name=="page":
            self.pageObject.title=self.title
            self.pageObject.ns=self.ns
            self.pageObject.id=self.id
            self.pageObject.redirect=self.redirect
            self.pageObject.revision['id']=self.revision['id']
            self.pageObject.revision['parentid']=self.revision['parentid']
            self.pageObject.revision['timestamp']=self.revision['timestamp']
            self.pageObject.revision['contributor']['id']=self.revision['contributor']['id']
            self.pageObject.revision['contributor']['username']=self.revision['contributor']['username']
            self.pageObject.revision['minor']=self.revision['minor']
            self.pageObject.revision['comment']=self.revision['comment']
            self.pageObject.revision['text']=self.revision['text']
            self.pageObject.revision['sha1']=self.revision['sha1']
            self.pageObject.revision['model']=self.revision['model']
            self.pageObject.revision['format']=self.revision['format']
            pageList.append(self.pageObject)
        elif name == "title":                                               #End Tag: Title
            self.titleWords=processTitle(self.title)           #Parse Title
            print(self.titleWords)
        elif name == "text":                                              #End Tag: Body Text
            self.textWords, self.infoBoxWords, self.categoryWords, self.externalLinkWords = processText(self.revision['text'])
            print(self.textWords)            #Parse Body Text
            #WikiHandler.createIndex(self, WikiHandler.titleWords, WikiHandler.textWords, WikiHandler.infoBoxWords, WikiHandler.categoryWords, WikiHandler.externalLinkWords)

    def characters(self, content):
        content = str(content)
        if self.stack[len(self.stack)-1]=="title":
            self.title+= content
        elif self.stack[len(self.stack)-1]=="ns":
            self.ns+= content
        elif self.stack[len(self.stack)-1]=="redirect":
            self.redirect+= content
        elif self.stack[len(self.stack)-1]=="parentid":
            self.revision['parentid']+= content
        elif self.stack[len(self.stack)-1]=="timestamp":
            self.revision['timestamp']+= content
        elif self.stack[len(self.stack)-1]=="minor":
            self.revision['minor']+= content
        elif self.stack[len(self.stack)-1]=="comment":
            self.revision['comment']+= content
        elif self.stack[len(self.stack)-1]=="text":
            self.revision['text']+= content
        elif self.stack[len(self.stack)-1]=="sha1":
            self.revision['sha1']+= content
        elif self.stack[len(self.stack)-1]=="model":
            self.revision['model']+= content
        elif self.stack[len(self.stack)-1]=="format":
            self.revision['format']+= content
        elif self.stack[len(self.stack)-1]=="username":
            self.revision['contributor']['username']+= content
        elif self.stack[len(self.stack)-1]=="id":
            if self.stack[len(self.stack)-2]=="page":
                self.id+=content
            elif self.stack[len(self.stack)-2]=="revision":
                self.revision['id']+=content
            elif self.stack[len(self.stack)-2]=="contributor":
                self.revision['contributor']['id']+=content

        #print(("characters '" + content + "'"))

    def refresh(self):
        self.title = ""
        self.ns = ""
        self.id = ""
        self.redirect = ""
        self.revision = {'id':"",'parentid':"",'timestamp':"",'contributor':{'username':"",'id':""},'minor':"",'comment':"",'text':"",'sha1':"",'model':"",'format':""}
        self.textWords = None
        self.infoBoxWords = None
        self.categoryWords = None
        self.externalLinkWords = None


def main(sourceFileName):
    source = open(sourceFileName,encoding="utf8")
    parser = xml.sax.make_parser()
    parser.setContentHandler(WikiContentHandler())
    parser.parse(source)

if __name__ == "__main__":
    main("addressbook2.xml")
