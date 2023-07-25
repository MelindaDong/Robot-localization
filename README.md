# Robot-localization

Robot localization is the process of determining where a mobile robot is located con- cerning its environment. A map of the environment is available and the robot is equipped with sensors that observe the environment as well as monitor its own motion.

The input map format are as follows:

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

*examples of input format can be find in `example_input_2D.txt` and `example_input_2D.txt`*

`viterbi.py` accept 2D map as input, can be called as:

$ python viterbi.py [input]  

``
