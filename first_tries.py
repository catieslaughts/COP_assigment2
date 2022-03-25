import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as c
import warnings
warnings.filterwarnings("error")
from helper_functions import *


def create_system(N):
	system_arr = np.random.choice([-1,1], size=(N, N))
	#system_arr = np.random.randint(0, 2, (N, N))
	#system_arr[system_arr == 0] = -1
	if verbose:
		print('Created System')
	return (system_arr)
    
def calc_energy(system_arr):
	int_energy = get_neighbor_sum(system_arr)
	mag_energy = get_mag(system_arr)
	
	ham = -J * int_energy - H * mag_energy
	
	return(ham)
	
	
def get_neighbor_sum(system_arr):
	e = 0
	for i in range(N):
		for j in range(N):
			spin = system_arr[i, j]
			#print(system_arr[i,j]*system_arr[i,(j+1)%N])
			e += (system_arr[i,j]*system_arr[(i-1)%N,j] + system_arr[i,j]*system_arr[(i+1)%N,j] + system_arr[i,j]*system_arr[i,(j+1)%N] + system_arr[i,j]*system_arr[i,(j-1)%N])
	return(e/2) #divide by two so we don't double-count pairs

def get_mag(system_arr):
	return(np.sum(system_arr))

def get_next_state(system_arr):
	next_state = np.copy(system_arr)
	
	i = np.random.randint(0, N) #implicitly enforcing w
	j = np.random.randint(0, N) #only one spin is flipped w/ uniform probability
	next_state[i,j] *= -1
	
	return (next_state)

def calc_A(system_arr, next_state):
	curr_e = calc_energy(system_arr)
	new_e = calc_energy(next_state)
	
	if new_e < curr_e:
		A = 1.
		
	else:
		A = (get_prob(new_e) / get_prob(curr_e))
		
	if verbose:
		print('Current System Energy: {}'.format(curr_e))
		print('New State Energy: {}'.format(new_e))
		#print('A = {}'.format(A))
	
	return A
		
def get_prob(energy): #make beta a global variable
	#prob = np.exp(np.float128(-beta*energy))
	try:
		prob = np.exp(-beta*energy)
	except RuntimeWarning:
		prob = np.exp(np.float128(-beta*energy))
	return prob

def change_state(A):
	return(np.random.choice([True,False], p=[A, 1-A]))

def step(system_arr):
	next_state = get_next_state(system_arr)
	A = calc_A(system_arr, next_state)
	if change_state(A):
		if verbose:
			print('Changing state...\n')
		system_arr = np.copy(next_state)
	else:
		if verbose:
			print('Retaining state...\n')
		
	return(system_arr)

def plt_system(system_arr):
	plt.imshow(system_arr)
	plt.show()
	return


global N, T, J, H, beta, verbose, scale_energy

J = 1
H = 0
kB = 1. #check if we're using dimensionless units
N = 50
T = 1.
beta = 1/(T*kB)
verbose = False


system_arr = create_system(N)
plt_system(system_arr)

for i in range(N**2):
	ProgressBar(N**2,i)
	system_arr = step(system_arr)
	#print(system_arr)

plt_system(system_arr)
