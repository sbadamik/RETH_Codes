# -------------------------------------------------------------------------------
# Importing necessary functions
import matplotlib.pyplot as plt
import math
import Functions_RETH as Funcs
import numpy as np

# -------------------------------------------------------------------------------
# Accepting appropriate inputs

a = 0.3 #input('\nEnter the semi-major axis of the ellipsoid: ')
b = 0.05 #input('\nEnter the semi-minor axis of the ellipsoid: ')

# -------------------------------------------------------------------------------
# Setting up appropriate variables for use

P = 1e5																# Pressure
s = 0.05															# Side of square cross-section
dec = 3																# Decimal places for rounding

P2P_Length = [(4*b)]												# Distance between pins

E = 112400e6														# Young's Modulus of Kevlar 49
I = (s**4) / 12														# Second Moment of Inertia
A = s*s 															# Cross-section area

n = 100															# Number of elements in FEM
t = n+1 

K = [0] * (2*t)
for i in range(2*t):
	K[i] = [0] * (2*t)

# ------------------------------------------------------------------------------- 

[X, M_X_All,M_Y_All] = Funcs.Find_M(a, b, P, E, I, P2P_Length, dec)

M_X = M_X_All[0][100]
M_Y = M_Y_All[0][100]
l = X[100]

D_MN = math.sqrt( (M_X-(0.5*P2P_Length[0]))**2 + (M_Y-(a-l))**2 )
Phi_e = math.atan( ((a-l)-M_Y) / ((0.5*P2P_Length[0])-M_X) )
Theta_P = Phi_e - (2*math.atan(1))
l_element = D_MN / n

F_Pn = P * l_element
F_Pn_x = F_Pn * math.cos(Theta_P)
F_Pn_y = F_Pn * math.sin(Theta_P)

k_e = E * A / l_element

for i in range(1,n+1):
	
	Node_L = 2*i
	Node_R = 2*(i+1)

	if i == n:
		Node_R = 0

	K[Node_L][Node_L] 	+= round(math.cos(Phi_e) * math.cos(Phi_e),dec+1)
	K[Node_L][Node_L+1] += round(math.cos(Phi_e) * math.sin(Phi_e),dec+1)
	K[Node_L][Node_R] 	+= round(-math.cos(Phi_e) * math.cos(Phi_e),dec+1)
	K[Node_L][Node_R+1] += round(-math.cos(Phi_e) * math.sin(Phi_e),dec+1)

	K[Node_L+1][Node_L] 	+= round(math.cos(Phi_e) * math.sin(Phi_e),dec+1)
	K[Node_L+1][Node_L+1] 	+= round(math.sin(Phi_e) * math.sin(Phi_e),dec+1)
	K[Node_L+1][Node_R] 	+= round(-math.cos(Phi_e) * math.sin(Phi_e),dec+1)
	K[Node_L+1][Node_R+1] 	+= round(-math.sin(Phi_e) * math.sin(Phi_e),dec+1)

	K[Node_R][Node_L] 	+= round(-math.cos(Phi_e) * math.cos(Phi_e),dec+1)
	K[Node_R][Node_L+1] += round(-math.cos(Phi_e) * math.sin(Phi_e),dec+1)
	K[Node_R][Node_R] 	+= round(math.cos(Phi_e) * math.cos(Phi_e),dec+1)
	K[Node_R][Node_R+1] += round(math.cos(Phi_e) * math.sin(Phi_e),dec+1)

	K[Node_R+1][Node_L] 	+= round(-math.cos(Phi_e) * math.sin(Phi_e),dec+1)
	K[Node_R+1][Node_L+1] 	+= round(-math.sin(Phi_e) * math.sin(Phi_e),dec+1)
	K[Node_R+1][Node_R] 	+= round(math.cos(Phi_e) * math.sin(Phi_e),dec+1)
	K[Node_R+1][Node_R+1] 	+= round(math.sin(Phi_e) * math.sin(Phi_e),dec+1)

d_E = [0,0,0,0]
f_F = [ ((F_Pn_x*(not(i%2))) + (F_Pn_y*(i%2))) for i in range((2*t)-4)]

K_Array = np.array(K)

K_E = K_Array[0:4,0:4]
K_EF = K_Array[0:4,4:]
K_F = K_Array[4:,4:]

# print(K_F)

K_F_inv = np.linalg.inv(K_F)
K_EF_t = np.transpose(K_EF)

# print()
# print(K_F_inv)

# print(np.dot(K_F_inv/10000,f_F))

d_F = np.dot( (K_F_inv / k_e), (f_F - np.dot(K_EF_t,d_E)))
r_E = np.dot(K_E,d_E) + np.dot(K_EF,d_F)

print(d_F)
# print(r_E)

# ------------------------------------------------------------------------------- 
# Using determined changes to plot the initial and final state of the fabric

Init_X = [M_X]
Init_Y = [M_Y]

Final_X = [M_X]
Final_Y = [M_Y]

for i in range(3,t+1):
	
	Init_X.append( Init_X[i-3] + (l_element * math.cos(Phi_e)) )
	Init_Y.append( Init_Y[i-3] + (l_element * math.sin(Phi_e)) )

	Final_X.append( Init_X[i-2] + d_F[(2*(i-3))] )
	Final_Y.append( Init_Y[i-2] + d_F[(2*(i-3))+1] )

Init_X.append(0.5*P2P_Length[0])
Init_Y.append(a-l)
Final_X.append(0.5*P2P_Length[0])
Final_Y.append(a-l)

Ellips_Y = []
Ellips_X = np.arange(0.0,b,0.001)


for X_Temp in Ellips_X:
	Ellips_Y.append( a * math.sqrt( 1 - (X_Temp*X_Temp/(b*b))))

plt.plot(Init_X,Init_Y,'.r-',Ellips_X,Ellips_Y,'k',Final_X,Final_Y,'.b-')
plt.legend(['Initial Fabric State','Piercing Solid','Final Fabric State'])
plt.show()

