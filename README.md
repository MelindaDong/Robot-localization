# Robot-localization

Robot localization is the process of determining where a mobile robot is located con- cerning its environment. A map of the environment is available and the robot is equipped with sensors that observe the environment as well as monitor its own motion.

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

`viterbi.py` accept 2D map as input, can be called as:

$ python viterbi.py [input]  

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

`viterbi_3d.py` accept 3D map as input, can be called as:

$ python viterbi_3d.py [input]  
