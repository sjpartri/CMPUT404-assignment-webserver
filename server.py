#  coding: utf-8 


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

import os
import SocketServer



class MyWebServer(SocketServer.BaseRequestHandler):
    
    
    response = ""
  
   
    def handle(self):

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
	http_request = self.data.splitlines()[0].split()
	

	#Check to see if the first line of the request contains the valid GET type
	if self.valid_request(http_request):
		requestData = http_request[1];
		path = os.path.abspath("www" + requestData)


	#1.Check to see if the path ends at a file and if the Content-Type of that file is valid and the file exists
		if self.valid_file(path):
			content_type = path.split(".")[-1].lower()
			if(content_type == "css" or content_type == "html"):
				content_extension = "text/"+content_type
				self.OK_200(content_extension,path)
			else:
				self.ERROR_404(self.response)

	#2.Check to see if the path ends at directory and checks if that directory contains a valid index
		elif self.valid_dir(path):
			path = path + "/index.html"
			if self.valid_file(path):
				content_type = "text/html\n\n"
				self.OK_200(content_type,path)

	#We can not conclude that path is not a valid directory nor a valid file
		else:	
			self.ERROR_404(self.response)
	
	#The request contained something other then the GET type		
	else:	
		self.ERROR_501(self.response)

	#send back a response with the valid file content
	print self.response
        self.request.sendall(self.response)

    def OK_200(self,content_type,path):
	print path
	self.response +=("HTTP/1.1 200 OK\n"+
                    "Content-Type: "+content_type+"\n\n"+
                    open(path).read())
	return

    
    def ERROR_501(self,response):
	self.response += ("HTTP/1.1 501 Not Implemented\n"+
                        "Content-Type text/html\n\n"+
                        "<!DOCTYPE html>\n"+
                        "<html><body>HTTP/1.1 501 Not Implemented\n\n"+
                        "Server only supports GET.</body></html>")
	return

    def ERROR_404(self,response):
	self.response += ("HTTP/1.1 404 Not Found\r\n"
                          "Connection: close\r\n"
                          "Content-Type: text/html\n\n"
                          "<!DOCTYPE html>\n"
                          "<html><body><h1>Oops! The page you are looking for seems to "
                          "be missing.</h1></body></html>")
	return
	

    def valid_request(self,http_request):
	if len(http_request) == 3:
		print http_request[0]
		if http_request[0] == "GET":
			return True
		else:
			return False	

    def valid_file(self,path):
	if (os.path.isfile(path)):
		return True
	else:
	 	return False

    def valid_dir(self,path):
	if (os.path.isdir(path)):
	       return True
	else:
		return False
		

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
