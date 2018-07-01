#!usr/bin/env python

##################################################################
# setup.py                                                       #
# description: for running the web server honeypot               #
# author: @shipcod3                                              #
# greetz: ROOTCON goons and baby jim trevor                      #
##################################################################

import sys, http.server, socketserver, cgi, logging, time

currenttime = time.strftime("%Y-%m-%d.%H-%M-%S.%Z", time.localtime())
logging.basicConfig(filename='http_' + currenttime + '.log',level=logging.DEBUG)
sys.stderr = open('shttph_' + currenttime + '.log', 'w', buffer)

print("""
  _  _                   ___
 | || |___ _ _  ___ _  _| _ \_  _
 | __ / _ \ ' \/ -_) || |  _/ || |
 |_||_\___/_||_\___|\_, |_|  \_, |
                    |__/     |__/  by @shipcod3
""")
class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.info(self.client_address[0]) 
        logging.info(self.headers)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.info(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        for item in form.list:
            logging.info(item)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

def usage():
    print("USAGE: python setup.py <port>")

def main(argv):
    if len(argv) < 2:
        return usage()

    PORT = int(sys.argv[1])
    Handler = ServerHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("\n [***] Honeypot Web Server is running at port", PORT)
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        main(sys.argv)
        
    except KeyboardInterrupt:
        print("\n HoneyPy has been stopped :(")
        pass
