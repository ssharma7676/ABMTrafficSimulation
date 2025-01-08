from mesa import Agent, Model
from random import randint


class CarAgent(Agent):
    """This class represents the cars in the model."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = "car"
        self.init_position = self.model.posRoadCells[unique_id]
        self.current_position = self.init_position
        self.direction = self.get_direction()
        self.count = 0
        self.state = "continue_forward"
        self.speed = randint(1, 2)
        self.color = self.model.carColors[unique_id]

    def get_direction(self):
        # default position directions
        if self.current_position[0] == self.model.nWaterCells:
            direction = "down"
        elif self.current_position[1] == self.model.nWaterCells:
            direction = "right"
        elif self.current_position[0] == self.model.width - self.model.nWaterCells - 1:
            direction = "up"
        elif self.current_position[1] == self.model.height - self.model.nWaterCells - 1:
            direction = "left"
        # corner directions
        if self.current_position == (self.model.nWaterCells,self.model.nWaterCells):
            direction = "right"
        elif self.current_position == (self.model.width-self.model.nWaterCells-1,self.model.nWaterCells):
            direction = "up"
        elif self.current_position == (self.model.width-self.model.nWaterCells-1,self.model.height-self.model.nWaterCells-1):
            direction = "left"
        elif self.current_position == (self.model.nWaterCells, self.model.height-self.model.nWaterCells-1):
            direction = "down"

        return direction

    def step(self):
        self.count += 1
        self.change_speed()

    def continue_forward(self):
        """MOVING FORWARD"""
        # Already having a direction and have a road ahead
        if self.move_to_road_cell_forward():
            next_position = self.current_position
            self.set_new_direction_place_agent(next_position)
        else:
            self.corner()

    def corner(self):
        """Have to turn at the corner of the road."""
        if self.speed == 2 and self.pos == (self.model.width - 3, 3):
            self.direction = "up"
            self.continue_forward()
        elif self.speed == 2 and self.pos == (self.model.width - 4, self.model.height - 3):
            self.direction = "left"
            self.continue_forward()
        elif self.speed == 2 and self.pos == (2, self.model.height - 4):
            self.direction = "down"
            self.continue_forward()
        elif self.speed == 2 and self.pos == (3, 2):
            self.direction = "right"
            self.continue_forward()
        elif self.speed == 3 and self.pos == (self.model.width - 3, 3):
            self.direction = "up"
            self.continue_forward()
        elif self.speed == 3 and self.pos == (self.model.width - 4, self.model.height - 3):
            self.direction = "left"
            self.continue_forward()
        elif self.speed == 3 and self.pos == (2, self.model.height - 4):
            self.direction = "down"
            self.continue_forward()
        elif self.speed == 3 and self.pos == (3, 2):
            self.direction = "right"
            self.continue_forward()
        elif self.direction == "right" and self.pos == (self.model.width - 3, 2):
            self.direction = "up"
            self.continue_forward()
        elif self.direction == "up" and self.pos == (self.model.width - 3, self.model.height - 3):
            self.direction = "left"
            self.continue_forward()
        elif self.direction == "left" and self.pos == (2, self.model.height - 3):
            self.direction = "down"
            self.continue_forward()
        elif self.direction == "down" and self.pos == (2, 2):
            self.direction = "right"
            self.continue_forward()

    def set_new_direction_place_agent(self, next_position):
        # Unpack tuple position
        x, y = self.pos
        a, b = next_position

        # Update heatmap for everytime it goes to new location
        self.model.heatmap_data[self.model.height - 1 - y][x] += 1
        # Set new direction
        if a > x:
            self.direction = "right"
        elif a < x:
            self.direction = "left"
        elif b > y:
            self.direction = "up"
        elif b < y:
            self.direction = "down"
        # Place agent to new position
        self.model.grid.move_agent(self, next_position)

    # ROAD
    def road_cell_around(self):
        # List contains position of 4 bordering cells (top, bottom, left, right)
        cells_around = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False)
        # List contains position of road cells that are from those 4 cells above
        possible_roads = []
        for pos in cells_around:
            # x, y = pos
            for cell_object in self.model.background_cells:
                if cell_object.pos == pos and cell_object.type == "road":
                    possible_roads.append(pos)
        return possible_roads

    def move_to_road_cell_forward(self):
        nWaterCells = self.model.nWaterCells
        (x, y) = self.pos
        # distance = speed * time
        # time = 1
        d = self.speed * 1

        # default positions
        if self.direction == "right":
            p = x + d
            q = y
        elif self.direction == "left":
            p = x - d
            q = y
        elif self.direction == "up":
            p = x
            q = y + d
        elif self.direction == "down":
            p = x
            q = y - d

        if self.direction == "right" and p >= (self.model.width - nWaterCells):
            q = q + abs((self.model.width - nWaterCells) - p) + 1
            p = self.model.width - nWaterCells - 1
        elif self.direction == "up" and q >= (self.model.height - nWaterCells):
            p = p - abs((self.model.height - nWaterCells) - q) - 1
            q = self.model.height - nWaterCells - 1
        elif self.direction == "left" and p < nWaterCells:
            q = q - (nWaterCells - p)
            p = nWaterCells
        elif self.direction == "down" and q < nWaterCells:
            p = p + (nWaterCells - q)
            q = nWaterCells

        self.current_position = (p, q)
        return p, q

    def check_cell_is_road(self, cell_position):
        possible_roads = self.road_cell_around()
        if cell_position in possible_roads:
            return True

    def change_speed(self):
        (p, q) = self.current_position

        i = self.unique_id - 1
        if self.unique_id == 0:
            i = self.model.num_agents-1
        (w, z) = self.model.agent_objects[i].current_position

        if self.direction == "right" and self.model.agent_objects[i].direction == 'right':
            distance = abs(w - p) - 1
        elif self.direction == "left" and self.model.agent_objects[i].direction == 'left':
            distance = abs(w - p) - 1
        elif self.direction == "up" and self.model.agent_objects[i].direction == 'up':
            distance = abs(z - q) - 1
        elif self.direction == "down" and self.model.agent_objects[i].direction == 'down':
            distance = abs(z - q) - 1
        else:
            distance = abs(w - p) + abs(z - q) - 1

        if distance > 3:
            self.speed = randint(0, 3)
            self.continue_forward()
        elif distance == 0:
            self.speed = 0
            self.continue_forward()
        elif 1 <= distance <= 3:
            self.speed = 1
            self.continue_forward()