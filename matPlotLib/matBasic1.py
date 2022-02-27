import matplotlib.pyplot as plt

x = [1,2,3,4]
y = [3, 5, 7, 9]
z = [10,8,6,4]

plt.grid(True)
plt.xlabel('My X values')
plt.ylabel('My Y Values')
plt.title('My First Graph')

plt.axis([0,5,2,11])

## dash makes line of best fit * is the icon, r change colour
plt.plot(x,y, 'b-*', linewidth=3, markersize=7, label='Blue Line')
plt.plot(x,z, 'r:o', linewidth=3, markersize=7, label='Red Line')

##to show label, can provide values to change position
plt.legend()
plt.show()

######### ex 2
import numpy as np
a = np.arange(-4,4,.1)
## or to chose data points a = np.linespace(-4,4,25)
b = np.square(a)
c = np.square(a) + 2
d = np.square(a) - 2

plt.grid(True)
plt.xlabel('My a value')
plt.ylabel('My b values')
plt.title('My Second Graph')

##plt.axis([])
plt.plot(a,b, 'b-*', linewidth=3, markersize=7, label='Blue Line')
plt.plot(a,c, 'r:o', linewidth=3, markersize=7, label='Red Line')
plt.plot(a,d, 'g:o', linewidth=3, markersize=7, label='Green Line')
plt.legend()
plt.show()


