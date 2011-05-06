import logging, email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app

def set_trace():
    import pdb, sys
    debugger = pdb.Pdb(stdin=sys.__stdin__, 
        stdout=sys.__stdout__)
    debugger.set_trace(sys._getframe().f_back)

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        plaintext_bodies = mail_message.bodies('text/plain')
        logging.info("Received a message from: " + mail_message.sender)
        
#application = webapp.WSGIApplication([('/_ah/mail/sms@binman-norwich.appspotmail.com', LogSenderHandler)], debug=True)
application = webapp.WSGIApplication([LogSenderHandler.mapping()], debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
