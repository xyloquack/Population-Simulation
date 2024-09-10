import random
import math
import os
import numpy as np

# This is used to tell the os where the current directory of the file is located, 
# so that it places the data file in the same location
absolute_path = os.path.abspath(__file__)
directory_name = os.path.dirname(absolute_path)
os.chdir(directory_name)

# These are the constants of the simulation that act as settings
EXPORT_DATA = True
OUTPUT_FILE = "data.txt"

A_ID = 1
A_ON_B_PERF = 0.5
A_ON_A_PERF = 1.75
A_ON_NONE_PERF = 2
A_FOOD_REQ = 1

B_ID = 2
B_ON_A_PERF = 1.5
B_ON_B_PERF = 0.75
B_ON_NONE_PERF = 2
B_FOOD_REQ = 1

STOP_ON_EXTINCTION = True

MUTATIONS = True
MUTATION_CHANCE = 0.01

# This is the creature class that stores all of the information about that particular type of creature, it serves as simply
# a prototype in the current implementation that is duplicated along an array.
class Creature():
    __slots__ = ['id', 'opp_perf', 'self_perf', 'none_perf', 'food_req']
    def __init__(self, creature_id, opposing_performance, self_performance, none_performance, food_requirement):
        self.id = creature_id
        self.opp_perf = opposing_performance
        self.self_perf = self_performance
        self.none_perf = none_performance
        self.food_req = food_requirement

# This reproduction function is one of the two fundamental pieces of the generation, where it is given information on whether
# it is facing an opposing species or an identical species, and then updates and returns the current counts to be used later
    def reproduce(self, matching, current_a_count, current_b_count):

        # Initialize variables and figure out what performance will be used.
        children = 0
        performance = 0
        if matching == 1:
            performance = self.self_perf
        elif matching == 0:
            performance = self.opp_perf
        else:
            performance = self.none_perf
        
        # Calcualate the number of children the creature ended up having
        children += int(performance)
        if performance % self.food_req:
            if performance - (self.food_req * children) >= random.random() * self.food_req:
                children += 1

        # If mutations are switched to off, simply increment the count of the appropriate type of creature
        if not MUTATIONS:
            if self.id == A_ID:
                current_a_count += children
            else:
                current_b_count += children

        # But if it is on
        else:
            # Figure out it it is creature A or B
            if self.id == A_ID:
                # Then figure out if each child mutated or not
                for child in range(children):
                    # By seeing if the mutation chance was greater than the random number
                    if random.random() <= MUTATION_CHANCE:
                        # And then either assign it to a mutated creature count
                        current_b_count += 1
                    else:
                        # Or the same creature count
                        current_a_count += 1

            # This one is creature B, same logic as A
            else:
                for child in range(children):
                    if random.random() <= MUTATION_CHANCE:
                        current_a_count += 1
                    else:
                        current_b_count += 1

        # Return the current running total
        return current_a_count, current_b_count

# This is the food source class that simply stores what creatures are visiting, and the amount. A nominal speed increase
# might be possible if this were simply replaced with an array, but it would likely be so small it makes no difference,
# when there are other operations in this program that take much longer to perform. So this will probably be kept for readability.
class FoodSource():
    __slots__ = ['visitors', 'occupancy']
    def __init__(self):
        self.visitors = []
        self.occupancy = 0

# MAIN FUNCTION, nothing else to really say about this, it does a few things.
def main():
    
    # This is simply establishing variables that will be used to keep track of the state of the simulation
    current_generation = []
    food_sources = []
    frequency_over_time = []

    # Prompts for the user to answer about how they want the initial starting conditions to be. These could
    # be changed into constants at the top, but I prefer this approach since it is probably something that 
    # will be changed often and this requires less code editing between tests.
    while True:
        total_number_of_creatures = input("How many creatures should we start with? ")
        try:
            total_number_of_creatures = int(total_number_of_creatures)
            break
        except:
            print("Not a valid input. Try again: ")
    while True:
        pop_a_proportion = input("What proportion do you want to be Creature A (in a decimal ratio)? ")
        try:
            pop_a_proportion = float(pop_a_proportion)
            break
        except:
            print("Not a valid input. Try again: ")
    while True:
        number_of_food_sources = input("How many food sources do you want? ")
        try:
            number_of_food_sources = int(number_of_food_sources)
            break
        except:
            print("Not a valid input. Try again: ")
    while True:
        num_generations = input("How many generations do you want? ")
        try:
            num_generations = int(num_generations)
            break
        except:
            print("Not a valid input. Try again: ")

    # The initial relative frequency is just the initial condition set by the user, nothing special
    frequency_over_time.append(pop_a_proportion)

    # This will actually calculate how many creatures the starting count and relative frequency describes
    pop_a_start = math.ceil(total_number_of_creatures * pop_a_proportion)
    pop_b_start = total_number_of_creatures - pop_a_start

    # Sets up the creature prototypes for creature A and creature B, since no data of these creatures
    # is ever actually modified, but instead only accessed throughout the population
    creature_a = Creature(A_ID, A_ON_B_PERF, A_ON_A_PERF, A_ON_NONE_PERF, A_FOOD_REQ)
    creature_b = Creature(B_ID, B_ON_A_PERF, B_ON_B_PERF, B_ON_NONE_PERF, B_FOOD_REQ)

    # Puts the appropriate amount of prototypes into the current_generation array.
    current_generation = [creature_a] * pop_a_start + [creature_b] * pop_b_start

    # Food sources have to be uniquely created because that data actually is modified throughout the simulation.
    food_sources = [FoodSource() for _ in range(number_of_food_sources)]

    generation = 0

    print(f"Gen 0: A = {pop_a_start} B = {pop_b_start}")

    current_a_count = pop_a_start
    current_b_count = pop_b_start

    # This array was actually really important for optimization, since it removed the step of randomly selecting
    # an available index for a food source, and then checking if that food source has an available slot. This
    # array allows for one shuffle and then simple iteration. Since every available index is in there twice, the
    # food sources will never be overallocated, and that removes a condition check for if the food source can
    # be allocated to.
    indices = [i for i in range(0, number_of_food_sources)] * 2

    # Generation loop!!!!
    while generation < num_generations:
        # I don't know if it would be more efficient to just put this in the while check, but I like this implementation
        # because it is easier to read and will only be done once per generation anyways, which is definitely not the
        # current bottleneck of the simulation
        if STOP_ON_EXTINCTION and (current_a_count == 0 or current_b_count == 0):
            break
        current_a_count = 0
        current_b_count = 0

        # This will shuffle the current_generation and the indices array so that they can be iterated through and
        # assignemnts can be made.
        np.random.shuffle(current_generation)
        np.random.shuffle(indices)

        # Loops through either each creature or each food source essentially, and uses the index i of both to make
        # the assignment
        for i in range(min(len(current_generation), len(indices))):
            source = food_sources[indices[i]]
            source.visitors.append(current_generation[i])
            source.occupancy += 1
        
        # Once all assignments are all made, this will loop through every food source and activate the reproduce
        # function of each creature, tallying the count along the way.
        for food_source in food_sources:
            if food_source.occupancy == 0:
                continue
            elif food_source.occupancy == 1:
                current_a_count, current_b_count = food_source.visitors[0].reproduce(2, current_a_count, current_b_count)
            else:
                matching = food_source.visitors[1].id == food_source.visitors[0].id
                current_a_count, current_b_count = food_source.visitors[0].reproduce(matching, current_a_count, current_b_count)
                current_a_count, current_b_count = food_source.visitors[1].reproduce(matching, current_a_count, current_b_count)
            # Clears the data of the food source so that it is freed up next generation
            food_source.occupancy = 0
            food_source.visitors = list()

        # Sets up the next generation inside the current generation array.
        current_generation = [creature_a] * current_a_count + [creature_b] * current_b_count

        generation += 1
        print(f"Gen {generation}: A = {current_a_count}, B = {current_b_count}")

        if EXPORT_DATA:
            frequency = current_a_count / (current_a_count + current_b_count)
            frequency_over_time.append(frequency)

    # After the simulation has ended, this will write all the data to a file, if EXPORT_DATA is True, and that can then be
    # immediately run through the sister program, data_plotter.py, to visualize the population over time.
    if EXPORT_DATA:
        file = open("data.txt", 'w')
        for line in frequency_over_time:
            file.write(f"{line}\n")
        file.close()
        

if __name__ == "__main__":
    main()