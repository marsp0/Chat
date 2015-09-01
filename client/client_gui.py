import Tkinter as tk
import tkMessageBox as mb
import datetime
import client_excep as ex
import client

class ClientGui(tk.Frame):

	def __init__(self,parent=None,*args,**kwargs):

		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.master.minsize(width=600,height=400)
		self.master.maxsize(width=600,height=400)
		self.master.config(bg='grey')
		self.config(pady=5,padx=5)
		self.pack()

		#frames
		self.login_frame = tk.Frame(self)
		self.login_frame.pack()

		self.chat_frame = tk.Frame(self)
		self.chat_frame.pack()

		self.right_frame = tk.Frame(self.chat_frame)
		self.right_frame.grid(row=1,column=2)

		self.left_frame = tk.Frame(self.chat_frame,pady=4,padx=4)
		self.left_frame.grid(row=1,column=1)

		#vars
		self.ip_var = tk.StringVar()
		self.port_var = tk.IntVar()
		self.username_var = tk.StringVar()

		self.send_var = tk.StringVar()

		self.login_view()

	def login_view(self):
		#ip
		tk.Label(self.login_frame,text='IP Address',width=20,pady=3,bd=2,relief='raised').grid(row=1,column=1)
		tk.Entry(self.login_frame,textvariable = self.ip_var).grid(row=1,column=2)

		#port
		tk.Label(self.login_frame,text='Port',width = 20,pady=3,bd=2,relief='raised').grid(row=2,column=1)
		tk.Entry(self.login_frame,text='Port',textvariable=self.port_var).grid(row=2,column=2)

		#usernmame
		tk.Label(self.login_frame,text='Username',width=20,bd=2,relief='raised',pady=3).grid(row=3,column=1)
		tk.Entry(self.login_frame,textvariable=self.username_var).grid(row=3,column=2)

		#login_buttons
		tk.Button(self.login_frame,text='Quit',command = self.quit,width=17).grid(row=4,column=1)
		tk.Button(self.login_frame,text='Enter Chat',width=17,command = self.connect).grid(row=4,column=2)


	def connect(self):
		try:
			ip_addr = self.check_ip(self.ip_var.get())
			port = self.check_port(self.port_var.get())
			username = self.check_username(self.username_var.get())
			self.client = client.Client(ip_addr,port,username)
			self.client.start()
			self.handle_receive()
			self.packer(self.login_frame,self.chat_view)
		except ex.ConnectionError as e:
			mb.showwarning('Connection Error','Could not connect to {}'.format(e.addr))
		except ex.InvalidPort as e:
			mb.showwarning('Port Error','{}\n{}'.format(e.port,e.msg))
		except ValueError:
			mb.showwarning('Port Error','The port has to be a number')
		except ex.InvalidUsername:
			mb.showwarning('Username Error','The username is invalid')
		except ex.LANError as e:
			mb.showwarning('Network Error','{}\n{}'.format(e.ip_addr,e.msg))

	def check_username(self,username):
		if username.isalnum():
			return username
		else:
			raise ex.InvalidUsername()

	def check_ip(self,ip_addr):
		if ip_addr not in ('localhost',''):
			ip_list = ip_addr.split('.')
			if len(ip_list) != 4:
				raise ex.LANError(ip_addr)
			if ip_list[:3] == ['192','168','1']:
				return ip_addr
			else:
				raise ex.LANError(ip_addr)
		return ip_addr

	def check_port(self,port):
		if port < 1024:
			raise ex.InvalidPort(port)
		return port

	def chat_view(self):
		#left frame
		self.text = tk.Text(self.left_frame,width=50,state='disabled',height=23)
		self.text.grid(row=1,column=1,columnspan=2)
		tk.Entry(self.left_frame,textvariable=self.send_var,width=38).grid(row=2,column=1)
		tk.Button(self.left_frame,text='Send',command = self.send).grid(row=2,column=2)

		#right frame
		self.user_info_frame = tk.Frame(self.right_frame)
		self.user_info_frame.pack(anchor='n')
		username, ip_addr, port = self.client.get_credentials()
		tk.Label(self.user_info_frame,text='Username',bd=2,relief='raised',width=15,pady=3).grid(row=1,column=1)
		tk.Label(self.user_info_frame,text=username,bd=2,relief='raised',width=15,pady=3).grid(row=1,column=2)
		tk.Label(self.user_info_frame,text='IP Address',bd=2,relief='raised',width=15,pady=3).grid(row=2,column=1)
		tk.Label(self.user_info_frame,text=ip_addr,bd=2,relief='raised',width=15,pady=3).grid(row=2,column=2)
		tk.Label(self.user_info_frame,text='Port',bd=2,relief='raised',width=15,pady=3).grid(row=3,column=1)
		tk.Label(self.user_info_frame,text=port,bd=2,relief='raised',width=15,pady=3).grid(row=3,column=2)

	def send(self):
		data = self.send_var.get()
		if data == '':
			pass
		else:
			self.client.send(data)
			message = 'Me: ' + self.send_var.get() + '\n'
			self.display_message(message)
			self.send_var.set('')

	def display_message(self,message):
		self.text.config(state='normal')
		self.text.insert(tk.END,message)
		self.text.config(state='disabled')

	def handle_receive(self):
		while self.client.messages:
			to_display = self.client.messages.pop(0)
			self.display_message(to_display)
		self.after(100,self.handle_receive)

	''' HELPERS '''

	def packer(self,to_unpack,to_pack):
		for child in to_unpack.winfo_children():
			child.destroy()
		to_unpack.pack_forget()
		to_pack()

	def quit(self):
		self.master.quit()

if __name__ == '__main__':
	p = ClientGui()
	p.mainloop()