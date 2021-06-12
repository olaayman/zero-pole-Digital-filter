import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,8))  # sets size and makes it square
ax = plt.axes()                  # ax.set_aspect(1)

# plot unit circle

theta = np.linspace(-np.pi, np.pi, 201)
plt.plot(np.sin(theta), np.cos(theta), color = 'gray', linewidth=0.5)

# plot x-y axis

#ax.axhline(y=0, color='gray', linewidth=1)
#ax.axvline(x=0, color='gray', linewidth=1)

plt.title("Z Plane")
plt.xlabel("Real")
plt.ylabel("Imaginary")
plt.legend(loc='upper left')

plt.grid()
plt.show()