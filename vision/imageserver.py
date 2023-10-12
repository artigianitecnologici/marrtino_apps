import os, sys, time, socket
import threading

import numpy as np
import json
import cv2

class ImageServer(threading.Thread):

    def __init__(self, port):
        threading.Thread.__init__(self)

        self.predict_cb = None
        
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(3) # timeout when listening (exit with CTRL+C)

        # Bind the socket to the port
        server_address = ('', port)
        self.sock.bind(server_address)
        self.sock.listen(1)

        print("Image Server running on port ", port, " ...")
        
        self.dorun = True # server running
        self.connection = None  # connection object


    def stop(self):
        self.dorun = False

    def connect(self):
        connected = False
        while (self.dorun and not connected):
            try:
                # print 'Waiting for a connection ...'
                # Wait for a connection
                self.connection, client_address = self.sock.accept()
                self.connection.settimeout(3)
                connected = True
                print('MobileNet Server: Connection from ', client_address)
            except:
                pass #print("Listen again ...")   


    # buf may contain a first chunk of data
    def recvall(self, count, chunk):
        buf = chunk
        count -= len(buf)
        while count>0:
            newbuf = self.connection.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf
        

    def set_predict_cb_fn(self, fn):
        self.predict_cb = fn

    def predict(self, img):
        if self.predict_cb is None:
            return "ImageServer Error: undefined callback function"
        else:
            return self.predict_cb(img)


    def run(self):
        
        res = "N/A"
        while (self.dorun):
            self.connect()  # wait for connection
            try:
                # Receive data
                while (self.dorun):
                    try:
                        data = self.connection.recv(2048)
                        data = data.strip()
                    except socket.timeout:
                        data = "***"
                    except:
                        data = None

                    # utf-8 decoding
                    buf = b''
                    if (type(data)!=str):
                        k = data.find(b'\n')
                        if (k<0):
                            data = data.decode('utf-8')
                        elif (len(data)>k+1):
                            buf = data[k+2:]
                            data = data[0:k].decode('utf-8')
                    
                    if (data!=None and data !="" and data!="***"):
                        self.received = data
                        print("Received: %r" %data)
                        v = data.split(' ')
                        if v[0]=='REQ':
                            self.connection.send('ACK\n\r')
                        elif v[0]=='FILE' and len(v)>1:
                            print('Eval image [%s]' %v[1])
                            res = self.predict(v[1])
                            ressend = (res+'\n\r').encode('UTF-8')
                            self.connection.send(res)
                        elif v[0]=='RGB' and len(v)>=3:
                            imgwidth = int(v[1])
                            imgheight = int(v[2])
                            imgsize = imgwidth*imgheight*3
                            print("RGB image size: %d" %imgsize)
                            buf = self.recvall(imgsize, buf)
                            if buf is not None:
                                print("Image received size: %d " %(len(buf)))
                                # convert to image
                                a = np.fromstring(buf, dtype='uint8')
                                a = a.reshape((imgheight,imgwidth,3))
                                #a = a / 255.0 # mobilenet
                                # img = np.array([a])  # mobilenet
                                img = np.array(a)
                                res = self.predict(img)                                
                                ressend = (res+'\n\r').encode('UTF-8')
                                self.connection.send(ressend)
                        elif v[0]=='GETRESULT':
                            ressend = (res+'\n\r').encode('UTF-8')
                            self.connection.send(ressend)


                    elif (data == None or data==""):
                        break
            finally:
                print('Image Server Connection closed.')
                # Clean up the connection
                if (self.connection != None):
                    self.connection.close()
                    self.connection = None





