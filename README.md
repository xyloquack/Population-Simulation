NOTE: For use of the C++ version of the program, you need to install the header file from here from either a package manager or directly in order to compile it: https://github.com/nlohmann/json                                      
      If you do choose to download it directly, simply place the json.hpp file into the same directory as the C++ file and change " #include <nlohmann/json.hpp> " to " #include "json.hpp" "

After watching a lot of Primer videos over the years, I decided to try and do what they did in their simulations.

After mapping out the way that I thought that it would work in my head it did not seem particularly hard, especially after jotting down notes of how I would accomplish the task in my notes when my laptop was dead.
This is not necessarily the best code, but it runs decently quick for what I need it to do, and there is no reason I could not rewrite the program to work with C, which I may do at some point.

To change the way that the program's conditions work, you have several constants you can change at the top of the file, and I will walk through the naming scheme now:

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

When you see "BLANK on BLANK PERF" in a name, it means that the first creature in the population is competing with the second creature, and this is the label of the performance. 
So you can think of it as "FIRST on SECOND PERF". This property is given to the first creature so that it can store how much food it will gain from the interaction with the second creature, or how performant it will be.

This second creature may sometimes be labelled as "none", and all that means is that the creature is alone at the food source, and thus can consume the food at the food source uncontested.

The FOOD_REQ constant is for either population A or for population B, and that number dictates how much food is required for that creature to reproduce.

A_ID and B_ID I don't forsee needing to be changed by anyone using this program, as it just indicates how the simulation will identify the competition at the food source, but
this could possibly be expanded upon with more creatures given a few tweaks to the code, particularly the class where it compares against different ids where it would then need to do additional
comparisons, and the area where the starting population would be generated.
