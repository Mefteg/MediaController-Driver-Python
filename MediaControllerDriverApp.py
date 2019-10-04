from tkinter import *
from tkinter.ttk import *

from MediaControllerDriver import MediaControllerDriver

default_baudrate = 9600

class MediaControllerDriverApp:
	def __init__(self, root):
		self.root = root
		self.driver = MediaControllerDriver()
		self.ports = []

		self.create_ports_frame(root)
		self.update_ports_treeview()

		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

	def create_ports_frame(self, root):
		ports_frame = Frame(root)

		## Create vertical scrollbar.
		vertical_scrollbar = Scrollbar(ports_frame)
		vertical_scrollbar.pack(side=RIGHT, fill=Y)

		## Create changelists tree view.
		self.ports_treeview = Treeview(ports_frame, yscrollcommand=vertical_scrollbar.set, height=17, columns=('port', 'state'))
		self.ports_treeview.bind("<Double-1>", self.on_double_click)
		self.ports_treeview.heading("#0", text="#")
		self.ports_treeview.column("#0", minwidth=40, width=40, stretch=False)
		self.ports_treeview.heading('port', text="Port")
		self.ports_treeview.column('port', stretch=False)
		self.ports_treeview.heading('state', text="State")
		self.ports_treeview.column('state', stretch=False)

		self.ports_treeview.pack(fill=X)

		vertical_scrollbar.config(command=self.ports_treeview.yview)

		ports_frame.pack(fill=X)

		return ports_frame

	def update_ports_treeview(self):
		## Clear all.
		for child in self.ports_treeview.get_children():
			self.ports_treeview.delete(child)

		self.ports = self.driver.list_ports()
		## Set new changelists.
		i = 0
		for port in self.ports:
			self.ports_treeview.insert('', END, text=str(i), values=(port.device, 'Available'))
			++i

	def on_double_click(self, event):
		## Get the selected serial port.
		selected_item_name = self.ports_treeview.selection()[0]
		selected_item_index = int(self.ports_treeview.item(selected_item_name, "text"))
		selected_port = self.ports[selected_item_index]
		## Open the serial port.
		self.driver.open_port(selected_port, default_baudrate)

	def on_closing(self):
		self.driver.close()
		self.root.destroy()

if __name__ == "__main__":

	root = Tk()
	root.title("Media Controller App")
	root.geometry("400x600")

	app = MediaControllerDriverApp(root)

	root.mainloop()
	try:
		root.destroy()
	except Exception:
		print("Error: Destroy the app isn't necessary here.")