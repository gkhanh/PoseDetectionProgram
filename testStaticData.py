import numpy as np
import matplotlib.pyplot as plt


threshold = 1e-10
# Create x values as a sine wave from 0.25 to 0.75
Range = np.linspace(0, 6, 10000)
f = 4
w = 2 * np.pi * f
y = np.full_like(Range, 0.4)  # y is a horizontal line at 0.3
Amplitude = 0.15
x = Amplitude * np.sin(w * Range + np.pi/2) + 0.45

count = 0
for i in range(1, len(Range)):
    if ((x[i] - y[i]) * (x[i-1] - y[i-1])) <= threshold:
        count += 1

print("Number of points where x and y meet:", count)

# Plot the lines
plt.plot(Range, y, label='y = 0.3')
plt.plot(Range, x, label='Sine wave')

plt.ylim(0, 1)
plt.show()

