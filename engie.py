#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import math
import gtk
import gobject
from gtk import gdk
sys.path.append("pinako")
from pinako import *
from datetime import datetime


## Creo l'interfaccia con le librerie cairo e gtk
class hakuFace(gtk.DrawingArea):
	def __init__(self):
		super(hakuFace, self).__init__()
		self.connect("expose_event", self.expose)
		self.connect("button_press_event", self.button_press_event)
 		self.set_events(gtk.gdk.EXPOSURE_MASK
	        	         | gtk.gdk.LEAVE_NOTIFY_MASK
	                         | gtk.gdk.BUTTON_PRESS_MASK
	                         | gtk.gdk.POINTER_MOTION_MASK
	                         | gtk.gdk.POINTER_MOTION_HINT_MASK)
		self._time = None
		self.update()
		self.cont = 0
		gobject.timeout_add(100, self.update)
	
	def expose(self, widget, event):
		self.context = widget.window.cairo_create()
        	self.context.rectangle(event.area.x, event.area.y,
                		       event.area.width, event.area.height)
		self.context.clip()
		self.draw(self.context)
		
		return False
	
	def muovi(self, x, y):
		modell.addAnchor(Anchor(modell.particles[modell.findNearest(x, y)], x, y))
	
	def button_press_event(self, widget, event):
		self.muovi(event.x, event.y)
		return True
	
	def draw(self, context):
		self.cont += 1
		for i in range(0, len(modell.particles)):
			context.arc(modell.particles[i].position[0], modell.particles[i].position[1],
				2, 0, 2.0*math.pi)
			context.set_source_rgb(1, 1, 1)
			context.fill_preserve()
			context.set_source_rgb(0, 0, 0)
			context.stroke()
		for i in range(0, len(modell.polygons[0].points)):
			context.line_to(modell.polygons[0].points[i][0], modell.polygons[0].points[i][1])
		context.fill()
		modell.step()
		#if(self.cont == 8):
			#modell.particles[5].position.x = 1500
		
	def redraw_canvas(self):
		if self.window:
			alloc = self.get_allocation()
			rect = gdk.Rectangle(alloc.x, alloc.y, alloc.width, alloc.height)
			self.window.invalidate_rect(rect, True)
			self.window.process_updates(True)
	
	def update(self):
		self.time = datetime.now()
		return True
		
	def _get_time(self):
		return self._time
	def _set_time(self, datetime):
		self._time = datetime
	    	self.redraw_canvas()
	time = property(_get_time, _set_time)

def main():
	window = gtk.Window()
	interface = hakuFace()
	
	window.set_title("Pinako")
	window.add(interface)
	window.resize(1000, 700)
	window.connect("destroy", gtk.main_quit)
	window.show_all()
	rect = gdk.Rectangle()
	rect = window.window.get_frame_extents()
	print "-x %i -y %i -w %i -h %i" % (rect.x, rect.y, rect.width, rect.height)
	
	gtk.main()

modell = Modell()
cont = 0
for i in range(1,20):
	modell.addParticle(Particle(x = 330, y = 20+i*10))
#modell.addAnchor(Anchor(modell.particles[0], 380, 200))
modell.addPolygon(Polygon([[300, 320], [300, 350], [400, 350], [400, 320]]))
main()
	
