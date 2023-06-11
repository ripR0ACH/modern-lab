import numpy as np
import matplotlib.pyplot as plt

data = "SampleData_Summer2023.dat"

class Position:
		def __init__(self, time = 0, x_position = 0, y_position = 0, z_position = 0) -> None:
			self.t = time
			self.x = x_position
			self.y = y_position
			self.z = z_position
		def __str__(self) -> str:
			return "(" + ', '.join(str(v) for v in vars(self).values()) + ")"
class Particle:
	def __init__(self) -> None:
		self.pos = []
	def add_pos(self, position) -> None:
		self.pos.append(position)

with open(data, "r") as f:
	objs = [Particle() for i in range(6)]
	for line in f:
		line = [float(i) for i in line.split()]
		for i in range(6):
			objs[i].add_pos(Position(line[0], line[(3 * i) + 1], line[(3 * i) + 2], line[(3 * i) + 3]))
	fig, ax = plt.subplots(1, 1)
	for obj in objs[:3]:
		t = []
		x = []
		y = []
		z = []
		for i in obj.pos:
			t.append(i.t)
			x.append(i.x)
			y.append(i.y)
			z.append(i.z)
		ax.plot(t, x)
		ax.set_xlabel("time")
		ax.set_ylabel("x position")
		ax.set_title("Particle x position vs. time")
	plt.show()