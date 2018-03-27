# -------------------------------------------------------------------------------
# Importing necessary functions
import matplotlib.pyplot as plt
import math

def Find_M(a, b, P, E, I, Length, dec):

	# ------------------------------------------------------------------------------- 
	# Creating the data for iteration across the x-axis.

	X_Naught = []
	X = []
	l = 0

	while l<a:
		X.append(l)
		l = l+0.001

	l = 0

	while l<=b:
		X_Naught.append(l)
		l = l+0.00001

	X_Plot = []
	Y_Plot = []

	# ------------------------------------------------------------------------------- 
	# Primary code causing iteration through piercing and determining the location where
	# it departs from the fabric.

	# Iterating for different lengths of pin-pin fabric.
	for L in Length:

		X_Not = []
		Y_Not = []

		# Iterating over piercing 1% of total length at a time
		for l in X:

			# Each value of x0 from 0 to b will be tested
			for x0 in X_Naught:

				y0 = (a/b) * ( b**2 - x0**2 )**0.5
				f = a-l
				l0 = ( (y0-f)**2 + (x0-(0.5*L))**2 )**0.5

				g = ((y0-f) / ((0.5*L)-x0))
				h = (-a*x0) / (b * ( b**2 - x0**2 )**0.5)

				r = round(math.atan(g),dec)
				s = round(math.atan(h),dec)
				t = round(math.atan(P * (l0**3) / (24*E*I)),dec)
			
 				if (r+t) == -s:
   					break

			X_Not.append(x0)
			Y_Not.append(y0)

		X_Plot.append(X_Not)
		Y_Plot.append(Y_Not)

	# plt.figure(1)
	# plt.subplot(221)
	# plt.scatter(X,X_Plot[0])
	# plt.title('a = ' + str(a) + 'm; b = ' + str(b) + 'm; L = ' + str(Length[0]) + 'm')
	# plt.xlabel('Protrusion in m')
	# plt.ylabel('Location of point of separation')

	# plt.subplot(222)
	# plt.scatter(X,X_Plot[1])
	# plt.title('a = ' + str(a) + 'm; b = ' + str(b) + 'm; L = ' + str(Length[1]) + 'm')
	# plt.xlabel('Protrusion in m')
	# plt.ylabel('Location of point of separation')

	# plt.subplot(223)
	# plt.scatter(X,X_Plot[2])
	# plt.title('a = ' + str(a) + 'm; b = ' + str(b) + 'm; L = ' + str(Length[2]) + 'm')
	# plt.xlabel('Protrusion in m')
	# plt.ylabel('Location of point of separation')

	# plt.subplot(224)
	# plt.scatter(X,X_Plot[3])
	# plt.title('a = ' + str(a) + 'm; b = ' + str(b) + 'm; L = ' + str(Length[3]) + 'm')
	# plt.xlabel('Protrusion in m')
	# plt.ylabel('Location of point of separation')

	# plt.show()

	return [X, X_Plot,Y_Plot]

