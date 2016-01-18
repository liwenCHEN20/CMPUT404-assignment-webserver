#  coding: utf-8 
import SocketServer
import os
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


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        new_request = self.data.split()
        req = new_request[1]
        print req
        
        if "../" in req:
            self.request.sendall("HTTP/1.1 404 Bad mimetype\n")
            return       
        #form the direct
        #find anything need
        if req[0] == '/' and req[-1] == '/': 
            file_direct = os.getcwd() + '/www'+req+'index.html'
            
            print file_direct
            # basecase
        elif req == '/':
            file_direct = os.getcwd() + '/www/index.html'
            #try to find the file
        else: 
            file_direct = os.getcwd() + '/www'+req    
            
            # open the file here
        try:
            file_content = open(os.path.normpath(file_direct),'r') 
            http_header = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/"+file_direct.split(".")[-1]+"; charset = UTF-8\r\n"
            http_body = file_content.read()
            file_content.close()
            #if cannot open means cannot find
        except:
            http_header = "HTTP/1.1 404 not found\n"
            http_body = "\r\n"
        #post thins here
        self.request.sendall(http_header)
        self.request.sendall('\r\n')
        self.request.sendall(http_body)
        self.request.sendall('content length: '+str(len(http_body))+"\n")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
