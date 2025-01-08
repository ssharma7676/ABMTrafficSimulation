from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa import DataCollector
from mesa.time import RandomActivation
from car import CarAgent
import numpy as np
import random


def compute_average_speed(model):
    agent_speeds = [agent.speed for agent in model.schedule.agents]
    average_speed = sum(agent_speeds) / model.num_agents

    agent_speeds_bottomcells = [agent.speed for agent in model.schedule.agents if agent.current_position[1] == model.nWaterCells]
    if (len(agent_speeds_bottomcells)==0):
        average_speed_bottomcells = None
    else:
        average_speed_bottomcells = sum(agent_speeds_bottomcells) / len(agent_speeds_bottomcells)

    return average_speed


class CellAgent(Agent):
    """This class represents the cells in the grid that form the circular road.
          Cells will have a constant color and location."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class RoadModel(Model):
    """This class represents a road model with different agents (CellAgents and CarAgents)."""

    def __init__(self, N, width, height):
        self.width = width
        self.height = height
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.heatmap_data = np.zeros((self.height, self.width))
        self.grid = MultiGrid(self.width, self.height, True)
        self.carColors = []
        self.nWaterCells = 2

        self.background_cells = []

        # Create car color list
        r = lambda: random.randint(0, 255)
        for i in range(100):
            newColor = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
            self.carColors.append(newColor)

        # CREATE CELL AGENT AND SET ITS ATTRIBUTE
        count = 0  # for unique_id
        for x in range(self.width):
            for y in range(self.height):
                # Create cell agent
                cell_object = CellAgent(count, self)
                # Place this agent to the correct location of the model's grid
                self.grid.place_agent(cell_object, (x, y))
                cell_object.init_position = (x, y)
                # Set attribute for each cell
                self.set_attribute_cell(cell_object, x, y)

                # Append to the list containing all background cells
                self.background_cells.append(cell_object)

                count += 1

        # FIND ALL ROAD CELLS' POSITION AS POSSIBLE CAR'S INITIAL POSITION
        self.roads = [
            cell.pos for cell in self.background_cells if cell.type == "road"]

        self.posRoadCells = []
        self.posRoadCells = self.posRoadCells + [(self.nWaterCells, y) for y in
                                                 range(self.nWaterCells, self.height - self.nWaterCells)]
        self.posRoadCells = self.posRoadCells + [(x, self.height - self.nWaterCells - 1) for x in
                                                 range(self.nWaterCells + 1, self.width - self.nWaterCells)]
        self.posRoadCells = self.posRoadCells + [(self.width - self.nWaterCells - 1, y) for y in
                                                 range(self.height - self.nWaterCells - 2, self.nWaterCells - 1, -1)]
        self.posRoadCells = self.posRoadCells + [(x, self.nWaterCells) for x in
                                                 range(self.width - self.nWaterCells - 2, self.nWaterCells, -1)]

        # Create car agents
        self.agent_objects = []
        for i in range(self.num_agents):
            car = CarAgent(i, self)

            print("Initial position of car " + str(car.unique_id) + ": ", car.init_position)

            self.grid.place_agent(car, car.init_position)
            self.schedule.add(car)
            self.agent_objects.append(car)

            # Update heatmap data
            x, y = car.init_position
            self.heatmap_data[self.height - 1 - y][x] += 1

        self.datacollector = DataCollector(model_reporters={"AverageSpeed": compute_average_speed}, agent_reporters={"Speed": "speed"})

        # Attribute running for visualization
        self.running = True

    def step(self):
        self.datacollector.collect(self)
        """Activate the step for all car agents at once."""
        self.schedule.step()

    def set_attribute_cell(self, cell_object, x, y):
        # Attribute "ROAD" for cells
        if 2 <= x <= (self.width - 3) and y == 2:
            cell_object.type = "road"
        elif 2 <= x <= (self.width - 3) and y == (self.height - 3):
            cell_object.type = "road"
        elif x == 2 and 2 <= y <= (self.height - 3):
            cell_object.type = "road"
        elif x == (self.width - 3) and 2 <= y <= (self.height - 3):
            cell_object.type = "road"

        elif x <= (self.width - 1) and y < 2:
            cell_object.type = "water"
        elif x <= (self.width - 1) and y > (self.height - 3):
            cell_object.type = "water"
        elif x < 2 and y <= (self.height - 1):
            cell_object.type = "water"
        elif x > (self.width - 3) and y <= (self.height - 3):
            cell_object.type = "water"

        else:
            cell_object.type = "grass"