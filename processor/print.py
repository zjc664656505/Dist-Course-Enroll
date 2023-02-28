import matplotlib.pyplot as plt

x = [1,2,4,8]
y1 = [32.203, 64.731, 114.324, 212.113]
y2 = [25.159,49.217,92.926,173.78]
y3 = [32.438, 62.243, 113.693, 211.267]

plt.plot(x, y1, marker='o', label="our")
plt.plot(x, y3, marker='x', label="OCC")
plt.plot(x, y2, marker='v', label="lock")
plt.xlabel('number of shards')
# naming the y axis
plt.ylabel('trx/sec')
plt.title('throughput')
plt.legend(loc="upper left")
plt.show()

y = [16.598, 9.086, 7.705, 5.459]
y1 = [90.84, 46.121, 25.636, 14.973]
y2 = [170.527, 87.198, 45.079, 25.01]
y3 = [89.817, 49.075, 25.88, 15.518]
plt.plot(x, y, marker='o', label="our(first)")
plt.plot(x, y1, marker='1', label="our(full)")
plt.plot(x, y3, marker='x', label="OCC")
plt.plot(x, y2, marker='v', label="lock")
plt.xlabel('number of shards')
# naming the y axis
plt.ylabel('sec')
plt.title('latency')
plt.legend(loc="upper left")
plt.show()
