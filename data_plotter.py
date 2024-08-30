import os
import matplotlib.pyplot as plt
import numpy as np

absolute_path = os.path.abspath(__file__)
directory_name = os.path.dirname(absolute_path)
os.chdir(directory_name)

DATA = "data.txt"

def main():
    y = []
    with open(DATA, "r") as file:
        for line in file.readlines():
            y.append(float(line))
    print(y)

    x = range(0, len(y))

    x_np = np.array(x)
    y_np = np.array(y)

    plt.plot(x_np, y_np, linewidth=2, color='black')
    plt.fill_between(x_np, y_np, 1, color='red', alpha=0.5)
    plt.fill_between(x_np, y_np, 0, color='blue', alpha=0.5)
    plt.ylim((0, 1))
    plt.xlim((x_np[0], x_np[-1]))
    plt.xlabel = "Generation"
    plt.ylabel = "Relative Population Frequency"
    plt.title("Realtive Frequency of Population A Over Time")
    plt.show()

if __name__ == "__main__":
    main()