# mass-measurament system-based-on-Newton-s-Second-Law
SUSTech SDM273 Intelligent Sensing and Signal Processing

In this project, we will build a mass measurement system based on Newton's second law. And implemented on Arduino UNO.

## Experimental setup

As shown in the figure below, the trolley is placed on a smooth horizontal plate, a thin rope is tied at the front end, the other end of the rope, and the other end of the rope is hung over the fixed pulley to hang a small barrel, and heavy objects can be placed in the barrel.

![image](https://user-images.githubusercontent.com/117464811/232413380-7defca28-a844-4ccb-a46d-6de98be35083.png)

## Basic principle

Newton's second law shows that mass $m$ is inversely proportional to acceleration $a$ when the external force on an object is $F$ unchanged:

$$
F = ma
$$

We think of the high school physics experiment "The Relationship between Acceleration and Mass". In this experiment, Newton's second law is verified by changing the mass of the object and measuring the acceleration of the comparison object. And if we want to get the mass of the object, we can get it by measuring the acceleration.

The gravity of $mg$ on the keg and heavy objects is approximately equal to the pull force on the string $T$ , which is the force that makes the trolley accelerate evenly:

$$
T \approx mg
$$

**Note**: The condition is that the mass of the barrel and heavy objects is much smaller than the mass of the trolley.

In an ideal case, the total mass of the trolley is $M% and its acceleration is inversely proportional to $a$ relationship:

$$
M = \frac{F}{a}
$$

In this experiment, the friction force $f$ is not negligible. From Newton's second law, the general formula can be expressed as follows:

$$
T - f = M a
$$

Assuming that the rolling friction coefficient is $mu$, expand the formula to get:

$$
m g - \mu M g = M a
$$

suppose $a_mu = mu g$ , which we can get by averaging multiple measurements. For a given $M_i$ and $a_i$ :

$$
a_\mu = \frac{1}{n} \sum_{i=0}^n (\frac{m}{M_i}-a_i)
$$

Substituting the resulting $a_mu$ into the formula yields the final expression that measures the total mass of the trolley $M$:

$$
M = \frac{m g}{a_\mu + a}
$$






