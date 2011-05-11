import logging, email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.urlfetch import fetch
import urllib
from BeautifulSoup import BeautifulSoup
    
def dbg():
    """ Enter pdb in App Engine
    
    Renable system streams for it.
    """
    import pdb
    import sys
    pdb.Pdb(stdin=getattr(sys,'__stdin__'),stdout=getattr(sys,'__stderr__')).set_trace(sys._getframe().f_back)

def send_via_kapow(number, message):
    url = 'http://www.kapow.co.uk/scripts/sendsms.php?username=neontribe&password=b191wkm&mobile=%s&sms=%s'
    url = url % (number, urllib.quote_plus(message))
    response = fetch(url)
    return response

def scrape_ncc(number, street):
    #dbg()
    payload = "__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUJOTQwMTczNDE4D2QWAmYPZBYCAgIPZBYCAgEPZBYGAgEPZBYEAgEPZBYCAgUPEGRkFgBkAgIPZBYCAgEPEGRkFgBkAgMPFgIeB1Zpc2libGVoZAIFDxYCHwBoZBgBBSpjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJGNvbnRlbnRNdWx0aVZpZXcPD2RmZNInlWuoj%2B1qIemQ54M0YaiTyKRa&__EVENTVALIDATION=%2FwEWBAKF%2BrexCwKDh6m8BwLwxu3%2FAQLw2PTaBr%2BMsxUUHGL1U%2BoJyGcNzAk0PBpJ&ctl00%24ContentPlaceHolder1%24streetNameTextBox="
    payload += urllib.quote_plus(str(street)) 
    payload += "&ctl00%24ContentPlaceHolder1%24houseNoTextBox="
    payload += urllib.quote_plus(str(number))
    payload += "&ctl00%24ContentPlaceHolder1%24welcomeSearchButton=Search"


    response = fetch('http://www.norwich.gov.uk/webapps/awc/bincollectiondayfinder.aspx', payload, 'POST')
    dom = BeautifulSoup(response.content)
    logging.info(dom.find(id="content"))
    theskinny = dom.find(id='ctl00_ContentPlaceHolder1_output').findNextSiblings('p')[:3]
    text = ' '.join([tag.text for tag in theskinny])
    return text

class IncomingSMSHandler(InboundMailHandler):
    def receive(self, mail_message):
        #dbg()
        plaintext_bodies = mail_message.bodies('text/plain')
        msg = ' '.join([x[1].decode() for x in plaintext_bodies])
        logging.info("Received a message from: " + mail_message.sender)
        logging.info(msg)
        
        #parse message
        # Is it a bin message?
        if 'binposse ' in msg.lower():
            items = msg.split(' ')
            house_number = items[1]
            street = items[2]
            
            #scrape ncc
            info = scrape_ncc(house_number, street)
            
            if 'remind' in msg.lower():
                info += " We'll send you a reminder the evening before :-)"
            #save result
            #TODO :-(
            
            # get a phone number
            #dbg()
            phone = '0' + mail_message.subject.split('+44')[1].split(' ')[0]
            
            #send response
            status = send_via_kapow(phone, info)
        
        
        
#application = webapp.WSGIApplication([('/_ah/mail/sms@binman-norwich.appspotmail.com', LogSenderHandler)], debug=True)
application = webapp.WSGIApplication([IncomingSMSHandler.mapping()], debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
