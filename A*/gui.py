#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from pathfinder import *
import goocanvas
import math
import gtk
import gobject
from gtk import gdk

class Interface(goocanvas.Canvas):
	def __init__(self):
		super(Interface, self).__init__()
		self.set_flags(gtk.CAN_FOCUS)
		self.set_size_request(500, 300)
		self.set_bounds(0, 0, 1000, 1000)
		self.connect("expose_event", self.expose)
		self.connect("motion_notify_event", self.motion_notify)
		self.connect("button_press_event", self.button_press)
		self._item = goocanvas.Ellipse(parent=self.get_root_item(), center_x=100, center_y=100, radius_x=5, radius_y=5,
								 stroke_color="black",  line_width=1.0)
		self._first = None
		self._state = 0
		self._plant = {}
		self._circles = []
		self._lines = []
		self.show()
	
	def expose(self, widget, event):
		pass
		
	def motion_notify(self, widget, event):
		try:
			self._item.props.center_x = event.x
			self._item.props.center_y = event.y
		except AttributeError:
			pass
		
	def button_press(self, widget, event):
		#inserimento nodi
		if self._state == 0:
			if event.button != 3:
				self.create_node(event.x, event.y)
			#tasto destro
			elif event.button == 3:
				self._item.remove()
				del self._item
				self._state = 1
		#collegamento nodi
		elif self._state == 1:
			if event.button == 3:
				self._state = 2
				self._first = None
	
	def circle_press(self, widget, target, event):
		if self._state == 1:
			if self._first is None:
				self._first = widget
			else:
				self._second = widget
				if self._second != self._first:
					line = goocanvas.Path(parent=self.get_root_item(), 
											data="M "+str(self._first.props.center_x)+" "+str(self._first.props.center_y)+ 
											" L "+str(self._second.props.center_x)+" "+str(self._second.props.center_y), 
											line_width= 0.95)
					line.set_data("id", str(self._first.get_data("id"))+"-"+str(self._second.get_data("id")))
					self._lines.append(line)
					tmp = (self._first.get_data("id"), self._second.get_data("id"))
					self._plant[tmp] = (math.sqrt(math.pow((self._first.props.center_x - self._second.props.center_x), 2) 
									+ math.pow((self._first.props.center_y - self._second.props.center_y), 2)))
					self._first = None
				else: self._first = None
		elif self._state == 2:
			if self._first is None:
				self._first = widget.get_data("id")
				print self._first
			else:
				self._second = widget.get_data("id")
				print self._second
				if self._first == self._second:
					self._first = None
				else:
					self.find()
					self._state = 3
			
	def create_node(self, x, y):
		circle = goocanvas.Ellipse(parent=self.get_root_item(), center_x=x, center_y=y,
								 radius_x=5, radius_y=5, stroke_color="black", fill_color="black",
								  line_width=1.0, can_focus=True, stroke_pattern = None)
		circle.set_data("id", str(x)+":"+str(y))
		circle.connect("button_press_event", self.circle_press)
		self._circles.append(circle)

	def find(self):
		call = Call(self._plant, self._first, self._second)
		results = call()
		if len(results) > 0:
			for i in self._circles:
				data_i = i.get_data("id")
				for e in results:
					if data_i == e:
						i.props.fill_color="red"
			for i in self._lines:
				data_i = i.get_data("id")
				for e in range(0, len(results)-1):
					node_a = results[e]
					node_b = results[e+1]
					comb_a = node_a+"-"+node_b
					comb_b = node_b+"-"+node_a
					if data_i == comb_a or data_i == comb_b:
						i.props.stroke_color="red"

def main():
	global item, canvas, press, ok
	ok = 0
	press = 0
	interface = Interface()
	window = gtk.Window()
	window.set_title("A* pathfinder")
	window.resize(500, 300);
	window.connect("destroy", gtk.main_quit)
	window.show()	
	window.add(interface)
	gtk.main()
	
if __name__ == "__main__":
	main()
	
