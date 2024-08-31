import random
import math
import os
import numpy as np

np.random.seed(10)
random.seed(10)

absolute_path = os.path.abspath(__file__)
directory_name = os.path.dirname(absolute_path)
os.chdir(directory_name)

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

current_a_count = 0
current_b_count = 0

class Creature():
    __slots__ = ['id', 'opp_perf', 'self_perf', 'none_perf', 'food_req']
    def __init__(self, creature_id, opposing_performance, self_performance, none_performance, food_requirement):
        self.id = creature_id
        self.opp_perf = opposing_performance
        self.self_perf = self_performance
        self.none_perf = none_performance
        self.food_req = food_requirement

    def reproduce(self, matching):
        global current_b_count
        global current_a_count

        children = 0
        performance = 0
        if matching == 1:
            performance = self.self_perf
        elif matching == 0:
            performance = self.opp_perf
        else:
            performance = self.none_perf
            
        children += int(performance)
        if performance % self.food_req:
            if performance - (self.food_req * children) >= random.random() * self.food_req:
                children += 1

        if not MUTATIONS:
            if self.id == A_ID:
                current_a_count += children
            else:
                current_b_count += children

        else:
            if self.id == A_ID:
                for child in range(children):
                    if random.random() <= MUTATION_CHANCE:
                        current_b_count += 1
                    else:
                        current_a_count += 1

            else:
                for child in range(children):
                    if random.random() <= MUTATION_CHANCE:
                        current_a_count += 1
                    else:
                        current_b_count += 1


        # with open(OUTPUT_FILE, 'a') as file:
        #     print(current_a_count, current_b_count, file=file)

class FoodSource():
    __slots__ = ['visitors', 'occupancy']
    def __init__(self):
        self.visitors = []
        self.occupancy = 0

def main():
    global current_a_count
    global current_b_count
    
    current_generation = []
    next_generation = []
    food_sources = []

    frequency_over_time = []

    if EXPORT_DATA:
        file = open(OUTPUT_FILE, "w")
        file.write("")
        file.close()

    total_number_of_creatures = int(input("How many creatures should we start with? "))
    pop_a_proportion = float(input("What proportion do you want to be Creature A (in a decimal ratio)? "))

    frequency_over_time.append(pop_a_proportion)

    pop_a_start = math.ceil(total_number_of_creatures * pop_a_proportion)
    pop_b_start = total_number_of_creatures - pop_a_start

    creature_a = Creature(A_ID, A_ON_B_PERF, A_ON_A_PERF, A_ON_NONE_PERF, A_FOOD_REQ)
    creature_b = Creature(B_ID, B_ON_A_PERF, B_ON_B_PERF, B_ON_NONE_PERF, B_FOOD_REQ)

    current_generation.extend([creature_a] * pop_a_start)
    current_generation.extend([creature_b] * pop_b_start)

    number_of_food_sources = int(input("How many food sources do you want? "))

    food_sources = [FoodSource() for _ in range(number_of_food_sources)]

    num_generations = int(input("How many generations do you want? "))
    generation = 0

    print(f"Gen 0: A = {pop_a_start} B = {pop_b_start}")

    current_a_count = pop_a_start
    current_b_count = pop_b_start

    indices = [i for i in range(0, number_of_food_sources)] * 2

    while generation < num_generations:
        if STOP_ON_EXTINCTION and (current_a_count == 0 or current_b_count == 0):
            break
        current_a_count = 0
        current_b_count = 0
        np.random.shuffle(current_generation)
        np.random.shuffle(indices)

        for i in range(len(current_generation)):
            if i >= number_of_food_sources * 2:
                break
            source = food_sources[indices[i]]
            source.visitors.append(current_generation[i])
            source.occupancy += 1
        
        for food_source in food_sources:
            if food_source.occupancy == 0:
                continue
            elif food_source.occupancy == 1:
                food_source.visitors[0].reproduce(2)
            else:
                matching = food_source.visitors[1].id == food_source.visitors[0].id
                food_source.visitors[0].reproduce(matching)
                food_source.visitors[1].reproduce(matching)

        next_generation = [creature_a] * current_a_count + [creature_b] * current_b_count

        current_generation.clear()
        current_generation.extend(next_generation)
        next_generation.clear()

        generation += 1
        print(f"Gen {generation}: A = {current_a_count}, B = {current_b_count}")

        for source in food_sources:
            source.occupancy = 0
            source.visitors = list()

        if EXPORT_DATA:
            frequency = current_a_count / (current_a_count + current_b_count)
            frequency_over_time.append(frequency)


    if EXPORT_DATA:
        file = open("data.txt", 'a')
        for line in frequency_over_time:
            file.write(f"{line}\n")
        file.close()
        

if __name__ == "__main__":
    main()