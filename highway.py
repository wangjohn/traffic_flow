import math
import random

class Highway:
	def __init__(self, length, lanes=3, density=0.5, populate_type="fixed_width"):
		"""Density is the number of cars per unit length."""
		self.length = length
		self.num_lanes = lanes
        self.clear_road()
		self.reset_density(density)

    def populate_road(self, populate_type, vehicle_type="car"):
        # find out which spots to occupy
        if populate_type == "fixed_width":
            incrementer = math.ceiling(1.0/self.density)
            filled_in_spots = [i*incrementer for i in xrange(self.num_lanes*self.length/incrementer+1)]
        elif populate_type == "random":
            filled_in_spots = [i for i in xrange(self.num_lanes*self.length) if (random.random()*self.density >= 0.5)]

        # now populate those spots with vehicles
        if vehicle_type == "car":
            for spot in filled_in_spots:
                self.road[spot // self.num_lanes][spot % self.num_lanes] = Car()
        else:
            # default action is to populate the road with cars 
            for spot in filled_in_spots:
                self.road[spot // self.num_lanes][spot % self.num_lanes] = Car()

    def clear_road(self):
		self.road = [[UnoccupiedLane() for i in xrange(self.num_lanes)] for j in xrange(self.length)]

	def reset_density(self, density):
		self.density = density
        self.populate_road("fixed_width")
			

class LaneOccupier(object):
	def __init__(self, length, width, is_accident=False):
		self.length = length
		self.width = width
		self.is_accident = is_accident

	def is_accident(self):
		self.is_accident

class UnoccupiedLane(LaneOccupier):
    def __init__(self):
        super(LaneOccupier, self).__init__(1, 1, False)


class Accident(LaneOccupier):
	def __init__(self, length, width, time_left):
		super(Accident, self).__init__(length, width, True)
		self.time_left = time_left

	def decrement_time_left(self):
		self.time_left -= 1

class Vehicle(LaneOccupier):
	def __init__(self, size, speed=60):
		super(Vehicle, self).__init__(size, 1, False)
		self.size = size
        self.speed = speed

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

