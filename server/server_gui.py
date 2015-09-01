import Tkinter as tk
import tkMessageBox as mb
import server_excep as ex
import server 


class ServerGui(tk.Frame):

	def __init__(self,parent=None,*args,**kwargs):

		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.master.minsize(width=600,height=400)
		self.master.maxsize(width=600,height=400)
		self.config(padx=5,pady=5)
		self.master.config()
		self.pack()

		#frames
		self.config_frame = tk.Frame(self)
		self.config_frame.grid(row=1,column=1)
		self.log_frame = tk.Frame(self,pady=7,padx=5)
		self.log_frame.grid(row=2,column=1)

		#port
		self.port_var = tk.IntVar()
		self.port_label = tk.Label(self.config_frame,text='Port Number',width=20,bd=2,relief='raised',pady=3)
		self.port_label.grid(row=1,column=1)
		self.port_entry = tk.Entry(self.config_frame,textvariable=self.port_var)
		self.port_entry.grid(row=1,column=2)

		#config buttons
		self.quit_button = tk.Button(self.config_frame,text='Quit',width = 17,command = self.quit)
		self.quit_button.grid(row=2,column=1)

		self.server_button = tk.Button(self.config_frame,text='Start Server',width=17,command = self.start_server)
		self.server_button.grid(row=2,column=2)

		#log stuff
		self.scroll = tk.Scrollbar(self.log_frame)
		self.scroll.grid(row=1,column=2)

		self.text = tk.Text(self.log_frame,state = 'disabled',height = 19,width=75,yscrollcommand=self.scroll.set)
		self.text.grid(row=1,column=1)

		self.scroll.config(command = self.text.yview)


	def start_server(self):
		try:
			port = self.check_port(self.port_var.get())
			self.server = server.ChatServer(port)
			self.server.start_server()
			self.text.config(state='normal')
 			self.text.insert(tk.END,'Server Started\n','a')
 			self.text.config(state='disabled')
			self.server_status()
		except ValueError:
			mb.showwarning('Error','The port should be a number')
		except ex.InvalidPort as e:
			mb.showwarning('Error','{}\n{}'.format(e.msg,e.port))
		except ex.ConnectionError:
			mb.showwarning('Connection Error','Make sure that the port is not already occupied')

 	def check_port(self,port):
 		if port < 1024:
 			raise ex.InvalidPort(port)
 		return port

 	def server_status(self):
 		while self.server.events:
 			event = self.server.get_event()
 			self.text.config(state='normal')
 			self.text.insert(tk.END,event,'a')
 			self.text.config(state='disabled')
		self.after(1000,self.server_status)

 	def quit(self):
 		try:
 			self.server.stop_server()
 		except AttributeError:
 			pass
 		finally:
 			self.master.quit()

if __name__ == '__main__':
	p = ServerGui()
	p.mainloop()