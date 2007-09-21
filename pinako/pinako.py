# -*- coding: UTF-8 -*-
from form import *
import sys


class Particle(object):
	def __init__(self, x=0, y=0, m=1):
		 self.force = [0, 0]
		 self.position = [x, y]
		 self.prev_position = [x, y]
		 self.mass = m


class Polygon(object):
	def __init__(self, p):
		self.points = p
		self.normals = []
		for i in range(0, len(self.points)):
			j = (i+1) % len(self.points)
			dx = self.points[j][0] - self.points[i][0]
			dy = self.points[j][1] - self.points[i][1]
			length = sqrt(dx*dx + dy*dy)
			vect = [-dy/length, dx/length]
			self.normals.append(vect)


class Anchor(object):
	def __init__(self, p, x, y):
		self.position = [x, y]
		self.particle = p

		
class Modell(object):
	def __init__(self, k=10, f=10, e=0.5, loop=10, x=0, y=80):
		self.kappa = k
		self.friction = f
		self.elasticity = e
		self.length = 10
		self.constrain_iterations = loop
		self.gravity = [x, y]
		self.particles = []
		self.anchors = []
		self.polygons = []
		# ?? che roba è theta ?? perché ce la misi ??
		self.theta = 0
		
	def addParticle(self, p):
		self.particles.append(p)
	
	def addAnchor(self, a):
		self.anchors.append(a)
	
	def addPolygon(self, p):
		self.polygons.append(p)
	
	def findNearest(self, x, y):
		rel = 1000000
		o = 0
		for i in range(0, len(self.particles)):
			dx = self.particles[i].position[0] - x
			dy = self.particles[i].position[1] - y
			distance = sqrt(dx*dx + dy*dy)
			if distance < rel:
				rel = distance
				o = i
		return i
	
	def accumulate(self):
		v = [0, 0]
		for i in range(0, len(self.particles)):
			self.particles[i].force[0] = self.gravity[0] * self.particles[i].mass
			self.particles[i].force[1] = self.gravity[1] * self.particles[i].mass
			v[0] = self.particles[i].position[0] - self.particles[i].prev_position[0]
			v[1] = self.particles[i].position[1] - self.particles[i].prev_position[1]
			self.particles[i].force[0] -= v[0] * self.friction
			self.particles[i].force[1] -= v[1] * self.friction

	def integrate(self):
		for i in range(0, len(self.particles)):
			x = self.particles[i].position[0]
			y = self.particles[i].position[1]
			self.particles[i].position[0] = x + (x - self.particles[i].prev_position[0]) + \
												   self.particles[i].force[0] * 0.2 * 0.2 
			self.particles[i].position[1] = y + (y - self.particles[i].prev_position[1]) + \
												   self.particles[i].force[1] * 0.2 * 0.2
			self.particles[i].prev_position[0] = x
			self.particles[i].prev_position[1] = y

	def constrainAnchors(self):
		for i in range(0, len(self.anchors)): #Constrain anchors
			self.anchors[i].particle.position[0], self.anchors[i].particle.position[1] = self.anchors[i].position[0], self.anchors[i].position[1]	
	
	def constrainParticles(self):
		if len(self.particles) > 1: #Constrain particles
			for q in range(0, self.constrain_iterations):
				for i in range(0, (len(self.particles))-1):
					x = self.particles[i].position[0]
					y = self.particles[i].position[1]
					dx = self.particles[i+1].position[0] - x
					dy = self.particles[i+1].position[1] - y
					
					distance = estimate(dx, dy, self.length)
					
					fraction = (distance - self.length) / distance / 2
					self.particles[i].position[0] = x + dx * fraction
					self.particles[i].position[1] = y + dy * fraction
					self.particles[i+1].position[0] = x + dx * (1 - fraction)
					self.particles[i+1].position[1] = y + dy * (1 - fraction)
	
	def reflectParticle(self, i, e):
		distance = -1000
		for k in range(0, len(self.polygons[i].points)):
			d = self.polygons[i].normals[k][0] * (self.particles[e].position[0] - self.polygons[i].points[k][0]) + \
				self.polygons[i].normals[k][1] * (self.particles[e].position[1] - self.polygons[i].points[k][1])
			if d > distance:
				distance = d
				edge = k
				n = self.polygons[i].normals[k]
		self.particles[e].position[0] -= (1 + self.elasticity) * distance * n[0]
		self.particles[e].position[1] -= (1 + self.elasticity) * distance * n[1]
		distance = n[0] * (self.particles[e].prev_position[1] - self.polygons[i].points[edge][1]) + n[1] * \
		 (self.particles[e].prev_position[0] - self.polygons[i].points[edge][0])
		self.particles[e].prev_position[0] -= (1 + self.elasticity) * distance * n[0]
		self.particles[e].prev_position[1] -= (1 + self.elasticity) * distance * n[1]
	
	def containsParticle(self, i, e):
		for a in range(0, len(self.polygons[i].points)):
			dx = self.particles[e].position[0] - self.polygons[i].points[a][0]
			dy = self.particles[e].position[1] - self.polygons[i].points[a][1]
			control = (self.polygons[i].normals[a][0] * dx) + (self.polygons[i].normals[a][1] * dy)
			if control >= 0:
				return False
		return True
	
	def constrainPolygons(self, i, e):
		if self.containsParticle(i, e):
			self.reflectParticle(i, e)
	
	def constrain(self):
		self.constrainAnchors()
		self.constrainParticles()
		for i in range(0, len(self.polygons)):
			for e in range(0, len(self.particles)):
				self.constrainPolygons(i, e)
	
	def step(self):
		self.accumulate()
		self.integrate()
		self.constrain()
		#print "=================="
		#for i in range(0, len(self.particles)):
		#	print "Particella: ", i
		#	print self.particles[i].position[0], self.particles[i].position[1]
			
			
if __name__ == "__main__":
	modell = Modell()
	for i in range(1,4):
		modell.addParticle(Particle(x = 300, y = 20+i*10))
	#modell.addAnchor(Anchor(modell.particles[0], 0, 0))
	modell.addPolygon(Polygon([[900, 900], [910, 900], [900, 910], [910, 910]]))
	for i in range(0, 20):
		modell.step()
	

	
	
	





	
	
	
