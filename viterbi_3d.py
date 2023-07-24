import numpy as np
import sys

# Open the file in read mode
#file_path = 'input.txt' 
file_path = sys.argv[1]
file = open(file_path, 'r')

# Read all lines from the file
lines = file.readlines()

# Extract the required lines
first_line = lines[0].strip()
map_size = [int(x) for x in first_line.split()]

raw_map = []
for i in range(1, map_size[0] + 1):
    row = lines[i].strip().split()
    raw_map.append(row)

observations = []
for i in range(map_size[0] + 2, len(lines) - 1):
    observations.append(lines[i].strip())

error_rate = float(lines[-1].strip())

# Close the file
file.close()

r,c,n_layers = map_size # row, col, layer// everything starts from 0
# count how many '0' in map
def count_zero(map):
    count = 0
    for row in map:
        for col in row:
            if col == '0':
                count += 1
    return count

K = count_zero(raw_map)
init_prob = 1/K


# convert raw_map to numpy matrix, where '0' is init_prob, 'X' is 0.0
init_map = np.array(raw_map)
init_map = np.where(init_map == '0', init_prob, init_map)
init_map = np.where(init_map == 'X', 0.0, init_map)
init_map = init_map.astype(np.float64)
# Get the dimensions of the 2D matrix
r,c,n_layers = map_size # row, col, layer// everything starts from 0

# Create a 3D matrix by stacking the left and right halves as layers
init_map_3d = np.zeros(map_size)
split_map = np.hsplit(init_map, n_layers)
for i in range(n_layers):
    for j in range(c):
        init_map_3d[:, j, i] = split_map[i][:, j]

# Generate all possible permutations
permutations = []
for a in range(2):
    for b in range(2):
        for c in range(2):
            for d in range(2):
                for e in range(2):
                    for f in range(2):
                        permutations.append((a,b,c,d,e,f))

# observation
O = {i+1: permutation for i, permutation in enumerate(permutations)}
N = len(O)

S = {} # state space
r,c,n_layers = map_size # row, col, layer// everything starts from 0
# Iterate over the matrix and find the non-zero values
for i in range(len(init_map)):
    for j in range(len(init_map[i])):
        if init_map[i][j] != 0:
            state = len(S)+1 
            S[state] = (i+1, j+1)

for key, value in S.items():
    S[key] = (value[0],  (value[1] - 1)%c + 1, (value[1] - 1)//c + 1) # (row, col, layer)

#Pi = [1/K] * K # initial state probability
Pi = [(1/K) for i in range(K)]
#[np.zeros(map_size) for i in range(T)]
Y = observations # a list of observations
T = len(Y) # number of observations
# convert Y to a list of tuples
Y = [tuple(int(i) for i in y) for y in Y]
# convert Y to a list of index based on O
Y = [list(O.keys())[list(O.values()).index(y)] for y in Y]

# given a state, return the key in S
def get_state_key(state):
    for key, value in S.items():
        if value == state:
            return key
        
# define the probability of transition
def transition_probability(state_key):
    state = S[state_key]
    neighbors_dict = {}
    neighbors = []
    a, b, c = state # a is layer, b is row, c is col
    possible_neighbors = [(a-1,b,c), (a+1,b,c), (a,b-1,c), (a,b+1,c), (a,b,c-1),(a,b,c+1)] # in order N, S, W, E, T, B
    count_neighbors = 0
    for neighbor in possible_neighbors:
        if neighbor in S.values():
            neighbors.append(neighbor)
            count_neighbors += 1

    for neighbor in neighbors:
        key = get_state_key(neighbor)
        neighbors_dict[key] = 1/count_neighbors

    return neighbors_dict

# initial Tm a matrix of size K x K
Tm = np.zeros((K, K))
# both row and column are the possible states from S, the value is the probability of transition
for i in range(1, K+1):
    neighbors_dict = transition_probability(i)
    for j in range(1, K+1):
        if j in neighbors_dict.keys():
            Tm[i-1][j-1] = neighbors_dict[j] # the index of matrix starts from 0

# method of calculating the true observation
def true_observation(state_key):
    state = S[state_key]
    a, b, c = state
    possible_neighbors = [ (a-1,b,c), (a+1,b,c), (a,b-1,c), (a,b+1,c), (a,b,c-1),(a,b,c+1)] # in order N, S, W, E, T, B
    true_observation = [0, 0, 0, 0, 0, 0] # 1 means obsticle, 0 means no obsticle
    for k, neighbor in enumerate(possible_neighbors):
        if neighbor not in S.values():
            true_observation[k] = 1
    return true_observation

def count_different_items(tuple1, tuple2): # count means the difference
    return sum(x != y for x, y in zip(tuple1, tuple2))

# initial Em a matrix of size K x N
Em = np.zeros((K, N))#
# row is the possible states from S, column is the possible observations from O, 
# the value is the probability of observation
for i in range(1, K+1):
    #state = S[i] # (row, col)
    true_obs = true_observation(i) # [N, S, W, E, T, B]
    for j in range(1, N+1):
        observation = O[j] #[N, S, W, E, T, B]
        count = count_different_items(true_obs, observation)
        Em[i-1][j-1] = (1-error_rate)**(6 - count) * error_rate**count
        
def viterbi_forward(O, S, pi, Y, Tm, Em):
    K = len(S)
    N = len(O)
    T = len(Y)

    trellis = np.zeros((K, T))

    # Initialization
    for i in range(K):
        trellis[i, 0] = pi[i] * Em[i][Y[0]-1]

    # Recursion
    for j in range(1,T):
        for i in range(K):
            max_prob = max([trellis[k][j-1] * Tm[k][i] * Em[i][Y[j]-1] for k in range(K)])
            trellis[i][j] = max_prob 

    return trellis

trellis = viterbi_forward(O, S, Pi, Y, Tm, Em)

result = [np.zeros(init_map_3d.shape) for i in range(T)]  

transposed_trellis = np.transpose(trellis)
for t, prob in enumerate(transposed_trellis):
    for index, p in enumerate(prob):
        a, b, c = S[index+1]
        result[t][a-1][b-1][c-1] = p

np.savez("output.npz", *result)
#print(result)