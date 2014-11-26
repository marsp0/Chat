from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
from tkColorChooser import *
from tkSimpleDialog import *
import time
import sys
import requests
import json
import shelve
import os.path
import smtplib
import socket
import thread



class ChatApp(Frame):

    def __init__(self, parent=None, **kwargs):
        Frame.__init__(self,parent,**kwargs)
        self.pack()
        #make app not resizable
        self.master.resizable(width='false',height='false')


        #Frame for received text
        self.textFrame = Frame(self)
        self.textFrame.grid(row=0,column=0)
        self.textFrame.config(width=400,height=400)

        #Text widget for the self.textFrame
        self.text = Text(self.textFrame,state='disabled')
        self.text.pack()

        #frame for the friends and the setting up
        self.setupFrame = Frame(self)
        self.setupFrame.grid(row=0,column=1,sticky='n')

        #IP FRAME
        self.ipFrame = Frame(self.setupFrame)
        self.ipFrame.pack(side='top')

        #IP ADDRESS FIELDS
        self.serverAddressVar = StringVar()
        self.serverAddressField = Entry(self.ipFrame,width=20,textvariable=self.serverAddressVar)
        self.serverAddressLabel = Label(self.ipFrame,text='IP Address')
        self.serverAddressVar.set('127.0.0.1')
        #packing of ip setups
        self.serverAddressLabel.grid(row=0,column=0)
        self.serverAddressField.grid(row=0,column=1)

        #PORT FIELDS
        self.serverPortVar = IntVar()
        self.serverPortLabel = Label(self.ipFrame,text='Port')
        self.serverPortField = Entry(self.ipFrame,textvariable=self.serverPortVar)
        self.serverPortVar.set('5000')
        #packing port fields
        self.serverPortLabel.grid(row=1,column=0)
        self.serverPortField.grid(row=1,column=1)

        #Button for server setup
        Button(self.ipFrame,text='Set Server',command = self.setServer).grid(row=2,column = 1)

        self.clientAddressVar = StringVar()
        self.clientAddressField = Entry(self.ipFrame, textvariable=self.clientAddressVar)
        self.clientAddressLabel = Label(self.ipFrame, text='IP Address')
        #packing them
        self.clientAddressField.grid(row=3,column=1)
        self.clientAddressLabel.grid(row=3,column=0)

        self.clientPortVar = IntVar()
        self.clientPortField = Entry(self.ipFrame,textvariable=self.clientPortVar)
        self.clientPortLabel = Label(self.ipFrame,text = 'Port')
        #packing
        self.clientPortLabel.grid(row=4,column=0)
        self.clientPortField.grid(row=4,column=1)

        #button for client
        Button(self.ipFrame, text='Add Friend',command = self.addFriend).grid(row=5,column=1)


        #SENDING FRAME
        self.sendFrame = Frame(self)
        self.sendFrame.grid(row=1,column=0)

        #sendfield
        self.sendTextVar = StringVar()
        self.sendText = Entry(self.sendFrame,textvariable = self.sendTextVar,width = 60)
        self.sendText.grid(row=0,column=0)
        Button(self.sendFrame,text='Send',command=self.send).grid(row=0,column=1)

        #server vars
        self.serverStatus = 0

        #all contacts 
        self.users = {}
        self.counter = 0

        #friend list
        self.list = Listbox(self.setupFrame)
        self.list.pack()

        #file var
        self.to_send = None

        #quit/remove/selectfile
        self.configButtons = Frame(self.setupFrame)
        self.configButtons.pack()

        Button(self.configButtons,text='Attach File',command = self.handleFile).grid(row=0,column=0)
        Button(self.configButtons,text='Quit',command=self.quit).grid(row=0,column=1)

    def handleFile(self):
        filename = askopenfilename()
        self.to_send = open(filename,'r').read()
        nameToDisplay = filename.split('/')[-1]
        self.ext = nameToDisplay.split('.')[-1]
        self.sendTextVar.set('SENDING: %s'%nameToDisplay)

    def send(self):
        dataToSend = self.sendTextVar.get()
        if dataToSend.startswith('SENDING: '):
            for connection in self.users.keys():
                self.users[connection].send('RECEIVING %s: %s'%(len(self.to_send),self.to_send))
        else:
            for connection in self.users.keys():
                self.users[connection].send(dataToSend)
        self.displayMessages(dataToSend,'Me')
        self.sendTextVar.set('')
        

    def addFriend(self):
        if self.serverStatus == 1:
            address = (self.clientAddressVar.get(),self.clientPortVar.get())
            conn = socket.socket()
            conn.connect(address)
            self.addClient(conn,address)
            thread.start_new_thread(self.handleMessages,(conn,address))
        else:
            print 'Set server first!'

    def addClient(self,connection,addr):
        self.users[self.counter] = connection
        self.list.insert((self.counter),addr)
        self.counter += 1

    def handleMessages(self,connection,address):
        while 1:
            try:
                data= connection.recv(1024)
                if not data:
                    continue
                elif data.startswith('RECEIVING'):
                    index_colon = data.find(':')
                    lengthOfFile = int(data[:index_colon].split()[-1])
                    current = 0
                    filee = data[index_colon+2:]
                    probe = len(filee)
                    while current < lengthOfFile-probe:
                        part_data =  connection.recv(1024)
                        filee += part_data
                        current += len(part_data)
                    print self.ext
                    name = asksaveasfile(mode='w',defaultextension = '.'+self.ext)
                    name.write(filee)
                    name.close()
                self.displayMessages(data,address)
            except AttributeError:
                self.displayMessages('You declined the transfer', 'Me')

    def displayMessages(self,data,address):
        if not(data.startswith('RECEIVING')):
            self.text.config(state='normal')
            self.text.insert('end','%s: %s\n'%(address,data))
            self.text.config(state='disabled')
        else:
            self.text.config(state='normal')
            self.text.insert('end','File received!')
            self.text.config(state='disabled')

    def setServer(self):
        self.server = socket.socket()
        self.server.bind((self.serverAddressVar.get(),self.serverPortVar.get()))
        self.server.listen(5)
        self.serverStatus = 1
        thread.start_new_thread(self.listenClients, ())

    def listenClients(self):
        while 1:
            conn , addr = self.server.accept()
            self.addClient(conn,addr)
            thread.start_new_thread(self.handleMessages,(conn,addr))



if __name__=='__main__':
    ChatApp().mainloop()
