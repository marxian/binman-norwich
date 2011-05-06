import logging, email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.urlfetch import fetch
import urllib

    
def dbg():
    """ Enter pdb in App Engine
    
    Renable system streams for it.
    """
    import pdb
    import sys
    pdb.Pdb(stdin=getattr(sys,'__stdin__'),stdout=getattr(sys,'__stderr__')).set_trace(sys._getframe().f_back)

def send_via_kapow():
    pass

def scrape_ncc(number, street):
    
    payload = "__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUJOTQwMTczNDE4D2QWAmYPZBYCAgIPZBYCAgEPZBYGAgEPZBYEAgEPZBYCAgUPEGRkFgBkAgIPZBYCAgEPEGRkFgBkAgMPFgIeB1Zpc2libGVoZAIFDxYCHwBoZBgBBSpjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJGNvbnRlbnRNdWx0aVZpZXcPD2RmZNInlWuoj%2B1qIemQ54M0YaiTyKRa&__EVENTVALIDATION=%2FwEWBAKF%2BrexCwKDh6m8BwLwxu3%2FAQLw2PTaBr%2BMsxUUHGL1U%2BoJyGcNzAk0PBpJ&ctl00%24ContentPlaceHolder1%24streetNameTextBox="
    payload += urllib.quote_plus(street) 
    payload += "&ctl00%24ContentPlaceHolder1%24houseNoTextBox="
    payload += urllib.quote_plus(number)
    payload += "&ctl00%24ContentPlaceHolder1%24welcomeSearchButton=Search"


    response = fetch('http://www.norwich.gov.uk/webapps/awc/bincollectiondayfinder.aspx', payload, 'POST')
    
    return response

class IncomingSMSHandler(InboundMailHandler):
    def receive(self, mail_message):
        dbg()
        plaintext_bodies = mail_message.bodies('text/plain')
        msg = ' '.join([x[1].decode() for x in plaintext_bodies])
        logging.info("Received a message from: " + mail_message.sender)
        
        #parse message
        number = '106'
        street = 'lincoln'
        
        #scrape ncc
        info = scrape_ncc(number, street)
        
        #save result
        
        
        #send response
        
        
        
#application = webapp.WSGIApplication([('/_ah/mail/sms@binman-norwich.appspotmail.com', LogSenderHandler)], debug=True)
application = webapp.WSGIApplication([IncomingSMSHandler.mapping()], debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
