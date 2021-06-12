import numpy as np
#from obspy.signal.invsim import paz_to_freq_resp

b = [1, 0.2, 1]
a = [1, 0, 0]
b = [1,-1]
a = [0,0]  #the coef of the equation poles
b = [1, -1j]
b = [1, -.707-.707j] #the coef of the equation zeros
poles1 = [-4.440 + 4.440j, -4.440 - 4.440j, -1.083 + 0.0j ,0.5,-0.5 -0.9 , 0.9]
zeros1 = [0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j , 2, -2, -1/0.9 , 1/0.9]
#poles1 = [-4.440 + 4.440j, -4.440 - 4.440j, -1.083 + 0.0j ]
#zeros1 = [0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j ]
#zeros1 = [-1/0.5]
#poles1 = [-0.5]
poles = np.roots(a)
zeros = np.roots(b)

coef_zeros = np.poly(zeros1) #to get the coefs from the roots(x,y location on the z plane)
coef_poles = np.poly(poles1) #to get the coefs from the roots(x,y location on the z plane)
print(coef_zeros,coef_poles)
print("The poles are:  ", poles)
print("The zeros are:  ", zeros)
angle = (1/180) * 2 * np.pi
frequency = np.exp(1j*angle)

print("")
print(frequency)
dist_one = frequency - zeros[0]
#dist_two = frequency - zeros[1]

dist_one_mag = np.absolute(dist_one)
#dist_two_mag = np.absolute(dist_two)

print("")
print("The distances from 1 KHz to the zeros are:")
print(dist_one_mag)
#print(dist_two_mag)

print("")
print("And multiplied together we get")
#print(dist_one_mag * dist_two_mag)
#%matplotlib inline
#%config InlineBackend.figure_format = 'retina'

import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

# plt.rcdefaults() 
# plt.xkcd()

# Reset default params
#sns.set()

# Set context to paper | talk | notebook | poster
# sns.set_context("poster")

fig = plt.figure(figsize=(8,8))  # sets size and makes it square
ax = plt.axes()                  # ax.set_aspect(1)

# plot unit circle

theta = np.linspace(-np.pi, np.pi, 201)
plt.plot(np.sin(theta), np.cos(theta), color = 'gray', linewidth=0.5)

# plot x-y axis

ax.axhline(y=0, color='gray', linewidth=1)
ax.axvline(x=0, color='gray', linewidth=1)

# plot poles and zeros

plt.plot(np.real(poles), np.imag(poles), 'Xb', label = 'Poles')
plt.plot(np.real(zeros), np.imag(zeros), 'or', label = 'Zeros')

# plot frequency point

angle = (1/32) * 2 * np.pi
frequency = np.exp(1j*angle)

plt.plot(np.real(frequency), np.imag(frequency), '.g', label = '1 KHz')


plt.title("Cool Pole-Zero Plot")
plt.xlabel("Real")
plt.ylabel("Imaginary")
#plt.legend(loc='upper left')

plt.grid()
plt.show()

import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns


fig = plt.figure(figsize=(8,6))
ax = plt.axes()

# H(z) = b/a

b = [1, 0.2, 1]   #    z^2 + 0.2z + 1
a = [1, 0, 0]     #         z^2

b = [1,-1]
a = [0,0]
b = [1, -1j]
b = [1, -.707-.707j]

# create w array which travels around unit circle

w = np.linspace(0,np.pi, 200)    # for evauluating H(w)
print(len(w))
z = np.exp(1j*w)

f = np.linspace(0, 180, 200)         # for ploting H(w)

# evalue H over the w array

H = np.polyval(coef_zeros, z) / np.polyval(coef_poles, z) 
#H = np.polyval(b, z) / np.polyval(a, z)
#print(np.polyval(a,z))
#print(H)
# plot the magnitude of H vs frequency.  H is a complex number array.
plt.figure()
plt.subplot(121)
plt.loglog(f, abs(H))
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude')
plt.subplot(122)
phase =  np.unwrap(np.angle(H))
plt.plot(f,phase)

# plt.subplot(223)
# #phase = 2 * np.pi + np.unwrap(np.angle(H))
# plt.plot(f,abs(H))
# plt.subplot(224)
# plt.semilogx(f, phase)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Phase [radian]')


# plt.plot(f, np.absolute(H))

# plt.title("H(w) Frequency Response",y=1.03)
# plt.xlabel("Frequency (KHz)")
# plt.ylabel("Magnitude |H(w)|")

#plt.xlim(0, 32)
#plt.xticks(np.linspace(0, 32, 17))   # I want every 2 KHz
#plt.ylim(ymin=0)                     # let ymax auto scale
plt.grid()
    
plt.show()