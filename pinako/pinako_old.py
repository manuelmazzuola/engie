#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
from math import sqrt

class Vector(object):
	"""
	Contiene 2 valori x e y 
	La classe accetta 2 valori
	"""
	def __init__(self, a=0, b=0):
		self.x, self.y = a, b
class Particle(object):
	"""
	Contiene i dati per definire la particella
	Accetta x, y, la massa e un valore booleano 
	per sapere se è connessa con altre particelle
	"""
	def __init__(self, _x=0, _y=0, m=1, c=True):
		 self.force = Vector()
		 self.position = Vector(_x, _y)
		 self.prev_position = Vector(_x, _y)
		 self.mass = m
		 self.connected = c
class Modell(object):
	"""
	Contiene il modello
	Accetta k, friction, elasticity, constrain_iterations 
	e la gravità x e y
	"""
	def __init__(self, kappa=10, f=10, e=0.7, loop=20, _x=0, _y=80):
		self.k = kappa
		self.friction = f
		self.elasticity = e
		self.length = 10
		self.constrain_iterations = loop
		self.gravity = Vector(_x, _y)
		self.particles = []
		self.theta = 0

def estDistance(dx, dy, r):
	return sqrt(dx * dx + dy * dy)

def addParticle(m, p, c=True):
	"""
	Aggiunge a un modello una particella
	Accetta il modello, la particella e un valore booleano
	per definire se la particella influenza ed è influenzata dalle altre
	"""
	p.connected = c
	m.particles.append(p)
	
def accumulateModell(m):
	"""
	Accumula la forza per ogni particella di un modello
	Accetta il modello
	"""
	v = Vector()
	for i in range(0, len(m.particles)):
		m.particles[i].force.x = m.gravity.x * m.particles[i].mass
		m.particles[i].force.y = m.gravity.y * m.particles[i].mass
		v.x = m.particles[i].position.x - m.particles[i].prev_position.x
		v.y = m.particles[i].position.y - m.particles[i].prev_position.y
		m.particles[i].force.x -= v.x * m.friction
		m.particles[i].force.y -= v.y * m.friction
		
def integrateModell(m):
	"""
	Integra le particelle di un modello
	Accetta il modello
	"""
	for i in range(0, len(m.particles)):
		x = m.particles[i].position.x
		y = m.particles[i].position.y
		m.particles[i].position.x = x + (x - m.particles[i].prev_position.x) + m.particles[i].force.x * 0.2 * 0.2
		m.particles[i].position.y = y + (y - m.particles[i].prev_position.y) + m.particles[i].force.y * 0.2 * 0.2
		m.particles[i].prev_position.x = x
		m.particles[i].prev_position.y = y

def constrainModell(m):
	"""
	Calcola l aposizione delle particelle che sono influenzate dalle altre
	Accetta il modello
	"""
	if len(m.particles) > 1:
		for q in range(0, m.constrain_iterations):
			for i in range(0, (len(m.particles))-1):
				if m.particles[i].connected == True and m.particles[i+1].connected == True:
					x = m.particles[i].position.x
					y = m.particles[i].position.y
					dx = m.particles[i+1].position.x - x
					dy = m.particles[i+1].position.y - y
					
					distance = estDistance(dx, dy, m.length)
					
					fraction = (distance - m.length) / distance / 2
					m.particles[i].position.x = x + dx * fraction
					m.particles[i].position.y = y + dy * fraction
					m.particles[i+1].position.x = x + dx * (1 - fraction)
					m.particles[i+1].position.y = y + dy * (1 - fraction)
	## Se la particella nn è influenzata salta il ciclo
					
def stepModell(m):
	"""
	Calcola ogni volta il tutto
	Accetta il modello
	"""
	accumulateModell(m)
	integrateModell(m)
	constrainModell(m)
	print "=================="
	for i in range(0, len(m.particles)):
		print "Particella: ", i
		print m.particles[i].position.x, m.particles[i].position.y
	
if __name__ == "__main__":
	modell = Modell()
	for i in range(1,4):
		addParticle(modell, Particle(_x = 100, _y = 20+i*10), True)
	for i in range(0, 3):
		stepModell(modell)

## addParticle(prova, Particle(_x = 400, _y = (40+(o*10)), c = True))
	

		
	
	
	





	
	
	
