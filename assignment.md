#Teleportation System

You have discovered the secrets of teleportation and have several teleportation routes up and running. Each route
 allows instantaneous travel from one city to another. All routes are two way: if you can teleport from city A
 to city B, you can also teleport from city B to city A. You want to create a system to make it easier for you to
 answer specific questions about your network. You should assume anyone using your network wants to travel only by teleportation.

Questions you must be able to answer:

1. What cities can I reach from city X with a maximum of N jumps?
2. Can someone get from city X to city Y?
3. Starting in city X, is it possible to travel in a loop (leave the city on one route and return on another, without traveling along the same route twice)?

 Input to the program will be a list of teleportation routes, followed by a list of queries.

Example input:

```
Washington - Baltimore
Washington - Atlanta
Baltimore - Philadelphia
Philadelphia - New York
Los Angeles - San Fransisco
San Fransisco - Oakland
Los Angeles - Oakland
Seattle - New York
Seattle - Baltimore
cities from Seattle in 1 jumps
cities from Seattle in 2 jumps
can I teleport from New York to Atlanta
can I teleport from Oakland to Atlanta
loop possible from Oakland
loop possible from Washington
```

 Example output:

```
cities from Seattle in 1 jumps: New York, Baltimore
cities from Seattle in 2 jumps: New York, Baltimore, Philadelphia, Washington
can I teleport from New York to Atlanta: yes
can I teleport from Oakland to Atlanta: no
loop possible from Oakland: yes
loop possible from Washington: no
```


