#include <cstdlib>
#include <iostream>
#include <cmath>
#include <vector>
#include <algorithm>
#include <random>

using namespace std;

const bool EXPORT_DATA = true;
const char* OUTPUT_FILE = "data.txt";

const int A_ID = 1;
const double A_ON_B_PERF = 0.5;
const double A_ON_A_PERF = 1.75;
const double A_ON_NONE_PERF = 2;
const double A_FOOD_REQ = 1;

const int B_ID = 2;
const double B_ON_A_PERF = 1.5;
const double B_ON_B_PERF = 0.75;
const double B_ON_NONE_PERF = 2;
const double B_FOOD_REQ = 1;

const bool STOP_ON_EXTINCTION = true;

const bool MUTATIONS = false;
const double MUTATION_CHANCE = 0.01;

class Creature {
public:
    int id;
    double opp_perf;
    double self_perf;
    double none_perf;
    double food_req;

    Creature() {}

    Creature(int creature_id, double opposing_performance, double self_performance, double none_performance, double food_requirement) {
        id = creature_id;
        opp_perf = opposing_performance;
        self_perf = self_performance;
        none_perf = none_performance;
        food_req = food_requirement;
    }

    void reproduce(int matching, int *current_a_count, int *current_b_count) {
        int children = 0;
        double performance = 0;
        if (matching == 0) {
            performance = opp_perf;
        }
        else if (matching == 1) {
            performance = self_perf;
        }
        else {
            performance = none_perf;
        }

        children += int(performance);
        if (fmod(performance, food_req) != 0) {
            if (performance - (food_req * children) >= ((double)rand() / (double)RAND_MAX) * food_req) {
                children++;
            }
        }

        if (!(MUTATIONS)) {
            if (id == A_ID) {
                (*current_a_count) += children;
            }
            else {
                (*current_b_count) += children;
            }
        }
        else {
            if (id == A_ID) {
                for (int i = 0; i < children; i++) {
                    if (((double)rand() / (double)RAND_MAX) <= MUTATION_CHANCE) {
                        (*current_b_count)++;
                    }
                    else {
                        (*current_a_count)++;
                    }
                }
            }
            else {
                for (int i = 0; i < children; i++) {
                    if (((double)rand() / (double)RAND_MAX) <= MUTATION_CHANCE) {
                        (*current_a_count)++;
                    }
                    else {
                        (*current_b_count)++;
                    }
                }
            }
        }
    }
};

class FoodSource {
    public:
        Creature visitors[2];
        int occupancy = 0;

        FoodSource() {}
        
};

int main() {
    mt19937 mt(time(0));
    std::mt19937 rng(std::random_device{}());
    srand(static_cast <unsigned> (time(0)));

    int num_creatures;
    float pop_a_proportion;
    int num_food_sources;
    int num_generations;
    int generation = 0;

    std::cout << "How many creatures should we start with? ";
    cin >> num_creatures;
    std::cout << "\nWhat proportion do you want to be Creature A (in a decimal ratio)? ";
    cin >> pop_a_proportion;
    std::cout << "\nHow many food sources do you want? ";
    cin >> num_food_sources;
    std::cout << "\nHow many generations do you want? ";
    cin >> num_generations;

    int pop_a_start = ceil(num_creatures * pop_a_proportion);
    int pop_b_start = num_creatures - pop_a_start;
    int total_creature_count = pop_a_start + pop_b_start;
    int current_a_count = pop_a_start;
    int current_b_count = pop_b_start;

    Creature creature_a = Creature(A_ID, A_ON_B_PERF, A_ON_A_PERF, A_ON_NONE_PERF, A_FOOD_REQ);
    Creature creature_b = Creature(B_ID, B_ON_A_PERF, B_ON_B_PERF, B_ON_NONE_PERF, B_FOOD_REQ);

    int max_children = ceil(max({A_ON_B_PERF, A_ON_A_PERF, A_ON_NONE_PERF, B_ON_A_PERF, B_ON_B_PERF, B_ON_NONE_PERF}));

    int max_generation_size = max_children * num_food_sources * 2;
    
    vector<Creature> current_generation(max_generation_size);
    vector<int> creature_indices(max_generation_size);

    for (int i = 0; i < current_a_count; i++) {
        current_generation[i] = creature_a;
    }

    for (int i = 0; i < current_b_count; i++) {
        current_generation[i + current_a_count] = creature_b;
    }

    vector<int> food_indices(num_food_sources * 2);

    for (int i = 0; i < num_food_sources * 2; i += 2) {
        food_indices[i] = floor(i / 2);
        food_indices[i + 1] = floor(i / 2);
    }

    vector<FoodSource> food_sources(num_food_sources);

    for (int i = 0; i < num_food_sources; i++) {
        food_sources[i] = FoodSource();
    }

    std::cout << "Gen " << generation << ": A = " << current_a_count << ", B = " << current_b_count << "\n";

    while (generation < num_generations) {
        if (STOP_ON_EXTINCTION && (current_a_count == 0 || current_b_count == 0)) {
            break;
        }
        total_creature_count = current_a_count + current_b_count;
        current_a_count = 0;
        current_b_count = 0;

        creature_indices.clear();
        for (int i = 0; i < total_creature_count; ++i) {
            creature_indices.push_back(i);
        }

        shuffle(creature_indices.begin(), creature_indices.end(), rng);
        shuffle(food_indices.begin(), food_indices.end(), rng);

        int loop_length = min(total_creature_count, num_food_sources * 2);

        for (int i = 0; i < loop_length; i++) {
            food_sources[food_indices[i]].visitors[food_sources[food_indices[i]].occupancy] = current_generation[creature_indices[i]];
            food_sources[food_indices[i]].occupancy++;
        }

        for (int i = 0; i < num_food_sources; i++) {
            if (food_sources[i].occupancy == 0) {
                continue;
            }
            else if (food_sources[i].occupancy == 1) {
                food_sources[i].visitors[0].reproduce(2, &current_a_count, &current_b_count);
            }
            else {
                int matching = food_sources[i].visitors[0].id == food_sources[i].visitors[1].id;
                food_sources[i].visitors[0].reproduce(matching, &current_a_count, &current_b_count);
                food_sources[i].visitors[1].reproduce(matching, &current_a_count, &current_b_count);
            }
            food_sources[i].occupancy = 0;
        }

        current_generation.clear();

        for (int i = 0; i < current_a_count; i++) {
            current_generation[i] = creature_a;
        }

        for (int i = 0; i < current_b_count; i++) {
            current_generation[i + current_a_count] = creature_b;
        }

        generation++;
        std::cout << "Gen " << generation << ": A = " << current_a_count << ", B = " << current_b_count << "\n";
    }
    return 0;
}