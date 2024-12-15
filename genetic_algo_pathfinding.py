import matplotlib.pyplot as plt
import math
import random as rd
from matplotlib.animation import FuncAnimation

# Used to create a solution
class Solution:
    
    is_destination_found = False
    path = [(0, 0)] # A list of positions that form a path
    steps = [] # The actions taken to create a path
    radius = 3
    fitness = 0 # How close the path got to the destination

    def __init__(self, steps):
        
        self.steps = steps

# Used to create obstacles and destination
class SearchSpaceObject:

    def __init__(self, position, radius):
        
        self.position = position
        self.radius = radius

class SearchSpace:
    
    solutions = [] # The population of solutions
    generations = 1000 # Amount of iterations
    destination = SearchSpaceObject((600, 500), 3) # Goal state
    
    obstacles = (
        SearchSpaceObject((300, 150), 70),
        SearchSpaceObject((150, 300), 70),
        # SearchSpaceObject((285, 250), 75),
        SearchSpaceObject((550, 150), 110),
        SearchSpaceObject((450, 400), 100),
        SearchSpaceObject((225, 485), 85),
        # SearchSpaceObject((450, 500), 70)
    )

    def __init__(self):

        # Initialize a hundred initial solutions
        for i in range(0, 100, 1):
            steps = []
            
            # Give each solution ten random steps to perform
            for i in range(17):
                steps.append((rd.uniform(-50, 50), rd.uniform(-50, 50)))
            
            new_solution = Solution(steps) # Create new Solution
            self.solutions.append(new_solution) # Append new solution to solution list

    # Used for checking if position will collide with obstacle or destination
    def collision_check(self, obstacle, solution, position):

        # Get euclidean distance
        d = math.dist(position, obstacle.position)
        
        # Check if solution is inside obstacle
        if d <= obstacle.radius - solution.radius:
            return True # collision detected

        # Check if solution intersects obstacle
        elif d < obstacle.radius + solution.radius:
            return True # collision detected

        # Check if solution touches obstacle
        elif d == obstacle.radius + solution.radius:
            return True # collision detected

        # Particle does not collide with this obstacle
        else:
            return False # no collision
                
    # Used to generate new position for solution by adding step to last position
    def change_position(self, solution, step):
        
        new_position = (solution.path[-1][0] + step[0]),(solution.path[-1][1] + step[1]) # Get new position
        
        for obstacle in self.obstacles:

            # If new position collides with an obstacle, reject it and instead return the last position
            if self.collision_check(obstacle, solution, new_position) == True:
                return solution.path[-1]
        
        # If the new position collides with the destination, set is_destination_found to True
        if self.collision_check(self.destination, solution, new_position) == True:
            solution.is_destination_found = True
        return new_position
    
    # Find distance of each solution's last position to the destination
    def fitness_func(self, solution):
        
        return math.dist(self.destination.position, solution.path[-1])
    
    # Sort solution by the closest to the destination
    # Keep the top 50% and discard the rest
    def selection(self):
        
        self.solutions.sort(key=self.fitness_func, reverse = False)
        self.solutions = self.solutions[:(int(len(self.solutions)/2))]

    # Form two child step lists by combining the steps of two parents
    def crossover(self, parent_1, parent_2):
        child_1_steps = parent_1.steps[:(int(len(parent_1.steps)/2))] + parent_2.steps[(int(len(parent_2.steps)/2)):]
        child_2_steps = parent_2.steps[:(int(len(parent_2.steps)/2))] + parent_1.steps[(int(len(parent_1.steps)/2)):]

        return child_1_steps, child_2_steps

    # Randomize one step from a child solution's steps
    def mutation(self, child_steps):
        mutate = rd.randint(0, 16)
        child_steps[mutate]=((rd.uniform(-50, 50), (rd.uniform(-50, 50))))
        return child_steps

    def generate_new_solutions(self):
        
        # List of children solutions
        children = []
        
        # Get parent pairs
        for i in range(0, len(self.solutions), 2):
            
            # Combine steps of parent pair to form steps for children
            child_1_steps, child_2_steps = self.crossover(self.solutions[i], self.solutions[i + 1])
            
            # Perform mutation on steps
            child_1_steps = self.mutation(child_1_steps)
            child_2_steps = self.mutation(child_2_steps)
            
            # Add children to list of children
            children.append(Solution(child_1_steps))
            children.append(Solution(child_2_steps))
        
        # Add list of children to solution list
        self.solutions = self.solutions + children

    def genetic_algorithm(self, frame):
        
        for solution in self.solutions:
            
            # If destination is already found, append last position to path
            if solution.is_destination_found == True:
                solution.path.append(solution.path[-1])
                continue
            
            else:
                for step in solution.steps:

                    # Perform step to get new position
                    next_position = self.change_position(solution, step)
                    solution.path.append(next_position)
        
        # Sort solutions by best fitness and purge underperformers
        self.selection()
        
        # Get new solutions
        self.generate_new_solutions()
        
        # Path of best performer. For FuncAnimation
        path_x = []
        path_y = []
        for position in self.solutions[0].path:
            path_x.append(position[0])
            path_y.append(position[1])
        
        # Reset paths of solutions
        for solution in self.solutions:
            solution.path = [(0, 0)]

        #Set data of path to be animated
        animated_solution_positions.set_data(path_x, path_y)

        # Print generation number
        print(f'Generation: {frame + 1}')

        # For animating best performer
        return animated_solution_positions,

# Generate search space
search_space = SearchSpace()
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect(1)

# Used for animation
animated_solution_positions, = ax.plot(0, 0, linestyle = 'dashed', color = 'blue', marker = 'o', markersize = 6)

# Plot destination
ax.plot(search_space.destination.position[0], 
        search_space.destination.position[1], 
        color = 'red', 
        marker = 'o', 
        markersize = search_space.destination.radius * 2)

# PLot starting position
ax.plot(0, 0, color='black', marker='o', markersize = 6)

# Draw obstacles
for obstacle in search_space.obstacles:
    ax.add_patch(plt.Circle((obstacle.position[0], 
                             obstacle.position[1]), 
                             obstacle.radius, 
                             fill = True, 
                             color = 'green'))

animation = FuncAnimation(
    fig = fig,
    func = search_space.genetic_algorithm,
    frames = search_space.generations,
    interval = 41,
    repeat = False
)

plt.show()
