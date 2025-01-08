# ABM Traffic Simulation

## 📖 Introduction
The ABM Traffic Simulation is a Python-based project built using the Mesa framework for Agent-Based Modeling. It simulates cars navigating a circular road, adjusting their speed and direction based on their position and proximity to other cars. The simulation is designed to demonstrate traffic flow dynamics and road navigation behavior in a controlled environment.
This project is ideal for experimenting with traffic modeling, agent interactions, and understanding the challenges of dynamic speed and direction control in constrained road systems.

## ✨ Features
1. Circular Road Model
* The road is represented as a MultiGrid with a wraparound layout, forming a continuous circular track.
* Road cells are defined by CellAgent objects, ensuring proper navigation paths for cars.
2. Dynamic Car Behavior
* Speed Control: Cars adjust their speed (either 1 or 2) based on the distance to the car ahead.
* Direction Control: Cars change their direction dynamically at corners to navigate the road layout.
* Proximity Awareness: Cars slow down when approaching another car to avoid collisions, mimicking real-world traffic behavior.
3. Traffic Density Visualization
* The simulation tracks road usage and highlights areas of traffic density using a heatmap, enabling users to visualize congestion patterns.
4. Flexible Parameters
* Number of Cars: The simulation supports a customizable number of car agents.
* Grid Size: The size of the road grid can be modified for larger or smaller tracks.
* Car Speed: Cars can move at one of two speeds, which can be adjusted in the configuration.

## 🚀 Installation
To run the simulation, you will need Python 3.8 or later and the required dependencies.

Prerequisites
Install the necessary Python libraries:
pip install mesa matplotlib numpy

Usage
Clone this repository:
git clone <repository-url>
cd circular-road-simulation

Run the simulation: 
python run.py

## 🎮 How It Works
CarAgent
The primary agent in the simulation represents a car. Each car has:
* Position: A tuple representing the grid coordinates.
* Speed: Determines how many cells it moves per step.
* Direction: Indicates whether the car is moving up, down, left, or right.
Cars dynamically adjust their speed and direction as they navigate the circular track, responding to the environment and other agents.

CellAgent
Grid cells that represent the road or non-road areas. Each cell tracks whether it is part of the road and contributes to visualizing traffic density.

RoadModel
The overarching model manages the simulation environment, including:
* Placement of cars and road cells.
* Traffic density tracking.
* Updating car behaviors each step.

## 📂 Key Components
* CarAgent: Represents individual cars on the road.
* CellAgent: Represents road segments and tracks traffic.
* RoadModel: Governs the simulation logic and agent interactions.
* server.py: Handles the visualization of the simulation in a web-based interface.

## 📸 Visualization
* Cars are displayed as agents moving along the grid.
* Traffic density is visualized as a heatmap, with higher density areas appearing more intense.

## 🖊️ Customization
To modify the simulation parameters, edit the configuration in run.py:
* Number of Cars: Change the value of N_CARS.
* Grid Size: Adjust GRID_WIDTH and GRID_HEIGHT.
* Car Speed: Modify the CarAgent initialization logic for custom speed ranges.

## Future Enhancements
* Collision Handling: Add collision detection and response mechanisms.
* Variable Speeds: Introduce a range of speeds to simulate diverse vehicle behavior.
* Advanced Road Layouts: Extend beyond circular roads to simulate intersections or highways.

## Acknowledgments
* Built using the Mesa agent-based modeling framework.
* Inspired by real-world traffic flow studies and dynamics.

