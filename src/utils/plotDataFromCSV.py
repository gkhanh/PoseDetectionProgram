import matplotlib.pyplot as plt
import csv

x1 = []
x2 = []
y1 = []
y2 = []


with open('D:/MoveLabStudio/Assignment/PoseDetectionPrototype/output/output.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')

    for row in lines:
        if row[1] == "RIGHT_HIP":
            x1.append(row[0])
            y1.append(float(row[3]))
        if row[1] == "RIGHT_KNEE":
            x2.append(row[0])
            y2.append(float(row[3]))

count = 0
min_red = min(y2)
print(round(min_red, 4))
# Iterate over the red data
for i in range(len(y1)):
    # Check if this point is a minimum
    if min_red <= y2[i] <= 0.3:
        count += 1
        # If the sum of the red and green data is less than 0.3, increment the counter
        # if y1[i] + y2[i] <= 0.3:
        #     count += 1

print(count)

ax1 = plt.axes()
ax1.set_xticklabels([])
plt.plot(x1, y1, color='g', linewidth=0.2)
plt.plot(x1, y2, color='r', linewidth=0.2)

plt.xticks(rotation=90)
plt.xlabel('Amplitude')
plt.ylabel('Time')

plt.title('Sample Data', fontsize=20)

plt.show()
