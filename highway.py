import math
import random

class Highway:
	def __init__(self, length, lanes=3, density=0.5, populate_type="fixed_width"):
		"""Density is the number of cars per unit length."""
		self.length = length
		self.num_lanes = lanes
        self.time = 0
        self.clear_road()
		self.reset_density(density)

    def populate_road(self, populate_type, vehicle_type="car"):
        # find out which spots to occupy
        if populate_type == "fixed_width":
            incrementer = math.ceiling(1.0/self.density)
            filled_in_spots = [i*incrementer for i in xrange(self.num_lanes*self.length/incrementer+1)]
        elif populate_type == "random":
            filled_in_spots = [i for i in xrange(self.num_lanes*self.length) if (random.random()*self.density >= 0.5)]

        # set the spots to the desired vehicle type
        self.set_vehicles(filled_in_spots, vehicle_type)

    def set_vehicles(self, filled_in_spots, vehicle_type="car"):
        obj_type = Car
        if vehicle_type == "car":
            obj_type = Car
        elif vehicle_type == "pickup_truck":
            obj_type = PickupTruck 
        elif vehicle_type == "semi_truck":
            obj_type = SemiTruck 
        elif vehicle_type == "suv":
            obj_type = SUV 

        for spot in filled_in_spots:
            new_vehicle = obj_type()
            i = spot // self.num_lanes
            j = spot % self.num_lanes
            self.road[i][j] = new_vehicle
            self.vehicles[(i,j)] = new_vehicle

    def clear_road(self):
		self.road = [[UnoccupiedLane() for i in xrange(self.num_lanes)] for j in xrange(self.length)]
        self.vehicles = {}

	def reset_density(self, density):
		self.density = density
        self.populate_road("fixed_width")

    def get_next_vehicle_position(self, start_place, lane, forward=True):
        """Gets the position of the next vehicle in the specified lane, returns none if there are no vehicles in front."""
        if forward:
            start = start_place+1
            end = self.length
            increment = 1
        else:
            start = start_place-1
            end = -1
            increment = -1
        for i in xrange(start, end, increment):
            if self.vehicles[(i,lane)]:
                return (i, lane) 
        return None


    def next_time_step(self):
        self.time += 1
        # check if anyone needs to switch lanes
        for x in xrange(len(self.road)):
            for spot_num in xrange(self.num_lanes):
                # check how far up the car can move 
                current_vehicle = self.road[x][spot_num] 
                if current_vehicle.is_vehicle:
                    next_vehicle_position = self.get_next_vehicle_position(x, spot_num)
                    if next_vehicle_position and current_vehicle.should_switch_lanes(x, next_vehicle_position[0]):
                        # if there is a vehicle in front, we move up to the follow distance of the vehicle, or change lanes probabilistically
                        self.switch_lanes((x, spot_num))

        # move all of the cars up by their respective speeds, making sure to slow them down so they are slower than the guy ahead
        # we start at the back to simulate speed pileups
        for x in xrange(len(self.road)):
            for y in xrange(self.num_lanes):
                current_vehicle = self.road[x][y]
                if current_vehicle.is_vehicle:
                    next_vehicle_position = self.get_next_vehicle_position(x, y)
                    # move the vehicle up, making sure that we keep follow distance in place
                    if (next_vehicle_position[0] - x) < current_vehicle.follow_distance + current_vehicle.speed:
                        new_x = next_vehicle_position[0] - current_vehicle.follow_distance
                        # slow down the car if necessary
                        if next_vehicle.speed > current_vehicle.speed:
                            current_vehicle.speed = next_vehicle.speed
                    else:
                        new_x = x + current_vehicle.speed

                    # move the position of the vehicle
                    self.make_position_switch((x,y),(new_x,y))


    def switch_lanes(self, vehicle_position):
        (x, y) = vehicle_position
        follow_distance = self.vehicles[vehicle_position].follow_distance
        # try switching to the left lane, make sure we don't run into a car ahead of us
        if y+1 < self.num_lanes and (self.get_next_vehicle_position(x,y+1)[0] - x) > follow_distance:
            # check if there is someone behind
            previous_vehicle_position = self.get_next_vehicle_position(x, y+1, False)
            self.make_lane_switch(vehicle_position, previous_vehicle_position, y+1)
        # now try switching into the right lane
        elif y-1 >= 0 and (self.get_next_vehicle_position(x,y-1)[0] - x) > follow_distance:
            previous_vehicle_position = self.get_next_vehicle_position(x, y-1, False)
            self.make_lane_switch(vehicle_position, previous_vehicle_position, y-1)

    def make_lane_switch(self, switching_vehicle_position, incoming_vehicle_position, new_lane):
        switching_vehicle = self.vehicles[switching_vehicle_position]
        if incoming_vehicle_position:
            incoming_vehicle = self.vehicles[incoming_vehicle_position]
            distance = switching_vehicle_position[0] - incoming_vehicle_position[0]

            if incoming_vehicle.speed <= switching_vehicle.speed:
                # if the incoming vehicle is slower than the switching vehicle, we only care to do anything when the distance is too close
                if distance < incoming_vehicle.follow_distance:
                    # incoming vehicle needs to slow down to allow appropriate follow distance
                    incoming_vehicle.speed -= (incoming_vehicle.follow_distance - distance)
            elif distance - incoming_vehicle.follow_distance < incoming_vehicle.speed - switching_vehicle.speed:
                # going to crash, definitely need to try to slow down and switch
                incoming_vehicle.speed -= (incoming_vehicle.speed - switching_vehicle.speed - (distance - incoming_vehicle.follow_distance))

        # switch the lane
        self.make_position_switch(switching_vehicle_position, (switching_vehicle_position[0], new_lane))

    def make_position_switch(self, old_position, new_position):
        vehicle = self.vehicles[old_position]
        unoccupied_lane = UnoccupiedLane()

        # move the vehicle in the vehicles hash
        self.vehicles[new_position] = vehicle
        self.vehicles[old_position] = unoccupied_lane

        # move the vehicle in the road list of lists
        self.road[old_position[0]][old_position[1]] = unoccupied_lane
        self.road[new_position[0]][new_position[1]] = vehicle



class LaneOccupier(object):
	def __init__(self, length, width, is_accident=False, is_vehicle=True):
		self.length = length
		self.width = width
		self.is_accident = is_accident
        self.is_vehicle = is_vehicle

	def is_accident(self):
		self.is_accident

class UnoccupiedLane(LaneOccupier):
    def __init__(self):
        super(LaneOccupier, self).__init__(1, 1, False, False)


class Accident(LaneOccupier):
	def __init__(self, length, width, time_left):
		super(Accident, self).__init__(length, width, True, False)
		self.time_left = time_left

	def decrement_time_left(self):
		self.time_left -= 1

class Vehicle(LaneOccupier):
	def __init__(self, size, speed, follow_distance = 10):
		super(Vehicle, self).__init__(size, 1, False, True)
		self.size = size
        self.speed = speed
        self.follow_distance = follow_distance

    def should_switch_lanes(self, start_position, next_vehicle_position):
        distance = next_vehicle_position - start_position
        if distance - self.follow_distance < self.speed:
            return True

class Car(Vehicle):
	def __init__(self):
		super(Car, self).__init__(1, 70)

class PickupTruck(Vehicle):
	def __init__(self):
		super(Car, self).__init__(2, 65)

class SemiTruck(Vehicle):
	def __init__(self):
		super(Car, self).__init__(5, 55)

class SUV(Vehicle):
	def __init__(self):
		super(Car, self).__init__(2, 65)

if __name__ == '__main__':
	a = Car()
	print a.get_speed()

