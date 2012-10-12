import math

class Highway:
	def __init__(self, length, lanes=3, density=1):
		"""Density is the number of cars per unit length."""
		self.length = length
		self.num_lanes = lanes
		self.road = [[CarObject(None) for i in xrange(self.num_lanes)] for j in xrange(self.length)]
		self.reset_density(density)

	def reset_density(self, density):
		self.density = density
		for stretch in self.road:
			cars_appropriated = 0
			for i in xrange(len(stretch)):
				if stretch[i] == 0:
					print 'blah'
			


class LaneOccupier(object):
	def __init__(self, length, width, is_accident=False):
		self.length = length
		self.width = width
		self.is_accident = is_accident

	def is_accident(self):
		self.is_accident

class Accident(LaneOccupier):
	def __init__(self, length, width, time_left):
		super(Accident, self).__init__(length, width, True)
		self.time_left = time_left

	def decrement_time_left(self):
		self.time_left -= 1

class Vehicle(LaneOccupier):
	def __init__(self, size):
		super(Vehicle, self).__init__(size, 1, False)
		self.size = size

	def get_speed(self):
		return (1.0/math.log(self.size+1))

class Car(Vehicle):
	def __init__(self):
		super(Car, self).__init__(1)

class PickupTruck(Vehicle):
	def __init__(self):
		super(Car, self).__init__(2)

class SemiTruck(Vehicle):
	def __init__(self):
		super(Car, self).__init__(5)

class SUV(Vehicle):
	def __init__(self):
		super(Car, self).__init__(2)

if __name__ == '__main__':
	a = Car()
	print a.get_speed()

