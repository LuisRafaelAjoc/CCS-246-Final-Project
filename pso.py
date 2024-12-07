import matplotlib.pyplot as plt
import numpy as np
import math

import matplotlib.animation as animation

class Particle:
    def __init__(self, position, radius, velocity):
        self.position = position
        self.radius = radius
        self.velocity = velocity
        self.pbest = self.position

class Obstacle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

class PSO:
    def __init__(self):
        self.gbest = [0.0, 0.0]
        self.best_score = 0.0

    def collision_check(self, obstacles, particle):
        for obstacle in obstacles:
            d = math.sqrt((particle.position[0] - obstacle.center[0]) * (particle.position[0] - obstacle.center[0]) + (particle.position[1] - obstacle.center[1]) * (particle.position[1] - obstacle.center[1]))
            
            # Check if particle is inside obstacle
            if d <= obstacle.radius - particle.radius:
                pass # return collision

            # Check if particle intersects obstacle
            elif d < obstacle.radius + particle.radius:
                pass # return collision

            # Check if particle touches obstacle
            elif d == obstacle.radius + particle.radius:
                pass # return collision

            # Particle does not collide with this obstacle
            else:
                
    
    def fitness():
        pass

    def optimization():
        pass

def main():
    pass
