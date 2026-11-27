
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

# Data
x = [48,37.5,62.5,25]
y = [320,300,200,340]

# Create scatter plot
plt.scatter(x, y)

# Labels
plt.xlabel("Load (N)")
plt.ylabel("Pedal Rate(rev/min)")
plt.title("Scatter Plot of Load vs Pedal Rate")

result = linregress(x, y)

x_line = np.linspace(min(x), max(x), 100)
y_line = result.intercept + result.slope * x_line

plt.plot(x_line, y_line, color="red")
plt.savefig("scatter_plot.png", dpi=300, bbox_inches="tight")
# Display graph
plt.show()