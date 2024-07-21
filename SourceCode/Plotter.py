# Umgesetzt in Python 3.8

# Import, um die Punktescharen auf dem Bildschirm plotten zu können
import matplotlib.pyplot as plt

# Definierung des Aussehens des auf dem Bildschirm erscheinenden Koordinatensystem
plt.xlim(-600, 500)
plt.ylim(-600, 500)
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
plt.draw()

x,y = [], [] # die beiden Arrays zur Speicherung der Koordinaten

with open('set1.otsp') as file:

	for _ in range(6):
		next(file)

	# Einlesen der Koordinaten
	for l in file:
	    row = l.split()
	    x.append(float(row[1]))
	    y.append(float(row[2]))

# Definierung des Aussehens des auf dem Bildschirm erscheinenden Koordinatensystem
plt.xlim(-600, 500)
plt.ylim(-600, 500)
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
plt.draw()

with open('set1.tour') as file:

	for _ in range(5):
		next(file)

	# Einlesen des auszugebenden Wegs
	x1, y1 = [], []
	toggle = True
	insertPos = 0
	for ele in file:
		if int(ele) == -1: break
		if int(ele) == len(x): 
			toggle = False
			continue
		if toggle:
			x1.append(x[int(ele)-1])
			y1.append(y[int(ele)-1])
		else:
			x1.insert(insertPos, x[int(ele)-1])
			y1.insert(insertPos, y[int(ele)-1])
			insertPos+=1

	# Ausgabe des Wegs
	plt.plot(x1, y1, 'ro-')

	plt.show()