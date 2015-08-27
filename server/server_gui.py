import Tkinter as tk
import tkMessageBox as mb

class ServerGui(tk.Frame):

	def __init__(self,parent=None,*args,**kwargs):

		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.master.minsize(width=600,height=400)
		self.master.maxsize(width=600,height=400)
		self.config(padx=5,pady=5)
		self.pack()

		#frames
		self.config_frame = tk.Frame(self)
		self.config_frame.grid(row=1,column=1)
		self.rest_frame = tk.Frame(self)
		self.rest_frame.grid(row=2,column=1)


		#ip 
		self.ip_var = tk.StringVar()
		self.ip_label = tk.Label(self.config_frame,text='IP Address',width=20,relief='raised',bd=2,pady=3)
		self.ip_label.grid(row=1,column=1)
		self.ip_entry = tk.Entry(self.config_frame,textvariable = self.ip_var)
		self.ip_entry.grid(row=1,column=2)

		#port
		self.port_var = tk.IntVar()
		self.port_label = tk.Label(self.config_frame,text='Port Number',width=20,bd=2,relief='raised',pady=3)
		self.port_label.grid(row=2,column=1)
		self.port_entry = tk.Entry(self.config_frame,textvariable=self.port_var)
		self.port_entry.grid(row=2,column=2)

		#config buttons
		self.quit = tk.Button(self.config_frame,text='Quit',width=17)
		self.quit.grid(row=3,column=1)

		self.server_button = tk.Button(self.config_frame,text='Start Server',width=17,command = self.start_server)
		self.server_button.grid(row=3,column=2)

	def start_server(self):
		ip_addr = self.ip_var.get()
		port = self.port_var.get()
		if self.check_ip(ip_addr):
			print 'server started'
		else:
			mb.showwarning('Error','The IP address you entered is invalid')

	def check_ip(self,ip_addr):
		ip_list = ip_addr.split('.')
		if len(ip_list) != 4:
			return False
		elif not (all(x.isdigit() for x in ip_list)):
 			return False
 		return True


if __name__ == '__main__':
	p = ServerGui()
	p.mainloop()