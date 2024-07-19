# so, the thing that c&c generals did well with planes
# and the thing that doesn't work well in sup com

import random
import time
import math

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame

from direct.distributed.ClockDelta import ClockDelta

from vector import vector


class SupTime:
	def __init__(self, base):

		self.b = base

		# my_cube = self.b.loader.loadModel("cube.obj")
		# my_cube.setColor(1,0,0)
		# my_cube.reparentTo(self.b.render)

		# my_cube.setPos(0, 0, 0)
		# self.cube = my_cube

		self.camera_setup()
		self.cubes = {}
		self.t = 0

		# self.cam.lookAt(self.cube)
		self.cube_offsets = {}
		self.xlen = 10
		self.ylen = 10
		self.cube_series_length = 3
		self.cloud_cover = 4/8

		self.init_cubes()

		self.swirl_center = (5.5, 5.5, 0)

	def init_cubes(self):
		x = 0
		while x < self.xlen:
			y = 0
			while y < self.ylen:
				c = 0
				cube_list = []
				offsets = []
				while c < self.cube_series_length:
					r = random.random()
					if r < self.cloud_cover:
						a = 1
					else:
						c += 1
						continue

					my_cube = self.b.loader.loadModel("cube.obj")
					my_cube.reparentTo(self.b.render)
					my_cube.setScale(random.random())
					cube_list.append(my_cube)

					offsets.append(random.random()*0.3)
					# offsets.append(0)

					c += 1
				self.cubes[(x, y)] = cube_list
				# self.cubes_offset[(x,y)] = random.random()
				self.cube_offsets[(x, y)] = offsets
				y += 1
			x += 1

	def camera_setup(self):
		# should be fine, don't move yet.
		print("init")
		self.b.disableMouse()
		self.cam = self.b.camera
		# like focal point
		self.anchor_point = (0, 0, 0)
		self.anchor_object = None
		self.notmovedfor = 0
		self.lastanchorpos = (0, 0, 0)
		self.cam.setPos(5, 5, 25)
		self.cam.setHpr(0, -90, 0)

	def main(self, delta_t):
		self.t += delta_t/5
		x = 0
		my_range = 3
		M = vector.RotationMatrix(math.pi/2, vector.Vector(0, 0, 1))

		while x < self.xlen:
			y = 0
			while y < self.ylen:
				# if x==y and x==5:
					# y+=1
					# continue
				cubes = self.cubes[(x, y)]
				offsets = self.cube_offsets[(x, y)]
				c = 0
				for cube in cubes:
					offset = offsets[c]
					my_t = self.t + offset*my_range + c/self.cube_series_length*my_range
					x_off = (my_t % 1 - 1 / 2) * my_range

					rel = 1 - (x_off / my_range)
					# print(rel)
					# sine scaling

					rel = (math.cos(2*rel*math.pi)+1)/2

					cube.setScale(rel/2)
					# cube.setScale(1,0.1,0.1)

					x_diff = self.swirl_center[0] - x
					y_diff = self.swirl_center[1] - y
					v=vector.Vector(x_diff,y_diff,0)
					v=v.normalize()
					v2 = M*v
					#if x == 7 and y ==7:
						#print(x_diff,y_diff)
					#m=(y_diff**2+x_diff**2)**0.5
					#alt_v = (y_diff/m,x_diff/m,0)
					#if x == 7 and y ==7:
						#print(alt_v)
					cube.setPos(x+v2[0]*x_off,y+v2[1]*x_off,0)
					
					c+=1
				y+=1
			x+=1
		
class Wrapper:
	def __init__(self):

		# this is required for this demo
		self.b = ShowBase()

		# this is sort of optional allows for easily building and deleting
		# elements
		
		self.SupTime = SupTime(self.b)

def old():
	W=Wrapper()
	while True:
		#delta_t=ClockDelta.getDelta()
		delta_t = globalClock.dt
		W.b.taskMgr.step()
		W.SupTime.main(delta_t)

if __name__=="__main__":
	old()
