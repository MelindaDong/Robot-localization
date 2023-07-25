# Robot-localization

Robot localization is the process of determining where a mobile robot is located concerning its environment. A map of the environment is available and the robot is equipped with sensors that observe the environment as well as monitor its own motion.

The sensors’ error rate is ε and that errors occur independently for the four sensors(north/south/west/east).

__Our goal is to find where is the robot and the most possible path of the robot through a sequence of sensor readings.__

__The initial state of robot is uniform distributed in all traversable positions.__

__The output is a list of maps(matrix) with each element represent the possibility of robot being at that position at that time step.__

### 2D input
The 2D input format are as follows:
```
4 10                  >> the size of the map (rows by columns)
0000X0000X            >> map ('X' denotes an obstacle;                 
XX00X0XX0X               '0' represents a traversable positions)
X000X0XX00 
00X000X000 
4                     >> the number of sensor observations
1011                  >> the observed values (in order NSWE; '1' means obstacle)
1010
1000
1100
0.2                   >> sensor’s error rate
```

if $d_it$ denotes the number of directions are reporting erroneous values, then the probability that a robot at position i would receive a sensor reading $e_t$ is:

$$
P(E_t = e_t|X_t = i) = (1-\varepsilon )^{4-d_it}\cdot \varepsilon ^{d_it}
$$


`viterbi.py` can be called as:   $ python viterbi.py [input]  

### 3D input
The 3D input format are as follows:
```
9 7 2                  >> the size of the map (rows by columns)
XXXX00XX0XXXXX         >> map (the frist 7 digits represent first/top layer;
X0000XX0XX0X00            the second 7 digits represent second layer) 
0X0X0X0X000000
000X000X0XXXXX
0XXX00XXXXX0X0
0X00XX00XXX0X0
X0XXX000XXXXX0
XX0XXX0XXX000X
00000XX000000X
4                      >> the number of sensor observations
000111                 >> the observed values (in order NSWETB; '1' means obstacle
000011                    north/south/west/east/top/bottom)
000001
101110
0.3                    >> sensor’s error rate

```

similiar with 2D model, the observation/emission model for 3D is:

$$
P(E_t = e_t|X_t = i) = (1-\varepsilon )^{6-d_it}\cdot \varepsilon ^{d_it}
$$

`viterbi_3d.py` can be called as:  $ python viterbi_3d.py [input]  
