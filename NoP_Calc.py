import matplotlib.pyplot as plt
import math

a = input('\nEnter the semi-major axis of the ellipsoid: ')
b = input('\nEnter the semi-minor axis of the ellipsoid: ')

Length = [ (3*b), (4*b), (5*b), (6*b) ]

Theta1 = [];
Theta2 = [];
Theta3 = [];
Theta4 = [];

X = []
l = 0

while l<a:
	X.append(l)
	l = l+0.001


for i in range(len(Length)):
	for l in X:
		
		L = Length[i]

		P = ((L/(2*b))**2)  +  ((1-(l/a))**2)
		Q = -L
		R = (b*b*l/a) * (2-(l/a))

		X0 = (-Q + ( ((Q*Q) - (4*P*R))**0.5 )) / (2*P)
		Y0 = (a/b) * ( ( (b*b)-(X0*X0) )**0.5 )

		delY = Y0 - (a-l)
		delX = X0 - (0.5*L)

		Theta0 = math.degrees(math.atan(delY/delX)) + 180

		if i == 0:
			Theta1.append(Theta0)
		elif i == 1:
			Theta2.append(Theta0)
		elif i == 2:
			Theta3.append(Theta0)
		elif i == 3:
			Theta4.append(Theta0)

	

plt.figure(1)
plt.subplot(221)
plt.scatter(X,Theta1)
plt.title('a = ' + str(a) + 'm; b = ' + str(b) + 'm; L = ' + str(Length[0]) + 'm')
plt.xlabel('Protrusion in m')
plt.ylabel('Angle of fabric with +ve X-axis')

plt.subplot(222)
plt.scatter(X,Theta2)
plt.title('a = ' + str(a) + 'm; b = ' + str(b) + 'm; L = ' + str(Length[1]) + 'm')
plt.xlabel('Protrusion in m')
plt.ylabel('Angle of fabric with +ve X-axis')

plt.subplot(223)
plt.scatter(X,Theta3)
plt.title('a = ' + str(a) + 'm; b = ' + str(b) + 'm; L = ' + str(Length[2]) + 'm')
plt.xlabel('Protrusion in m')
plt.ylabel('Angle of fabric with +ve X-axis')

plt.subplot(224)
plt.scatter(X,Theta4)
plt.title('a = ' + str(a) + 'm; b = ' + str(b) + 'm; L = ' + str(Length[3]) + 'm')
plt.xlabel('Protrusion in m')
plt.ylabel('Angle of fabric with +ve X-axis')

plt.show()