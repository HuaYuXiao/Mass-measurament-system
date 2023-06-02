# Mass-measurament system-based-on-Newton-s-Second-Law
SUSTech SDM273 Intelligent Sensing and Signal Processing

12010508 Yuxiao Hua 12011827 Hongjing Tang

In this project, we will build a mass measurement system based on Newton's second law. And implemented on Arduino UNO. For sake of the rule that strain transducers are not allowed, we decide to design a mass measurement system based on force pinciples.

## Experiment setup

As shown in the figure below, the trolley is placed on a smooth horizontal plate with accerlator sensor fixed in the carriage. A thin rope is tied at the front end, the other end of the rope, and the other end of the rope is hung over the fixed pulley to hang a small barrel, and weights is placed in the barrel.

![image](https://github.com/HuaYuXiao/Mass-measurament-system-based-on-Newton-s-Second-Law/assets/117464811/a6031ac0-ae3d-47d6-a924-3ca410e9f9f8)

## Basic principle

Newton's second law shows that mass $m$ is inversely proportional to acceleration $a$ when the external force on an object is $F$ unchanged:

$$
F = ma
$$

We think of the high school physics experiment "The Relationship between Acceleration and Mass". In this experiment, Newton's second law is verified by changing the mass of the object and measuring the acceleration of the comparison object. And if we want to get the mass of the object, we can get it by measuring the acceleration.

![image](https://user-images.githubusercontent.com/117464811/232413380-7defca28-a844-4ccb-a46d-6de98be35083.png)

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

Suppose $a_mu = mu g$ , which we can get by averaging multiple measurements. For a given $M_i$ and $a_i$ :

$$
a_\mu = \frac{1}{n} \sum_{i=0}^n (\frac{m}{M_i}-a_i)
$$

Substituting the resulting $a_mu$ into the formula yields the final expression that measures the total mass of the trolley $M$:

$$
M = \frac{m g}{a_\mu + a}
$$

Therefore, the whole formula for the mass measuring system is given as below. Where $para_a$, $para_b$ and $para_c$ is the three parameters to be obtained through future experienments.

$$
M = f(a) = para_a + \frac{para_b}{para_c + a}
$$

## Data tranformation











## Data processing

### Data import

#### .txt preprocessing

The data we obtain from the upper computer provided by **WIT motion** is in **.txt** form. Each time we run a test sample, there will be a new **.txt** file generated. However, only the newest one is necessary for our experienment. Therefore, we create a function called `deltxt()` to keep the specific **.txt** file.

```python
import os
import glob


def deltxt():
    txt_files = glob.glob("*.txt")

    newest_file = max(txt_files, key=os.path.getmtime)

    for file in txt_files:
        if file != newest_file:
            os.remove(file)
```

#### .txt to Dataframe

We wish to process the **.txt** file in `Dataframe` form. Note that the first line of the **.txt** file is of 1 column. If we directly import the **.txt** file into `Datframe`, there must be bugs for reading **ax(g)**, **ay(g)** and **az(g)**. 

![无标题](https://github.com/HuaYuXiao/Mass-measurament-system-based-on-Newton-s-Second-Law/assets/117464811/6c3c28b1-649a-44b9-b238-24ab7dda268c)

Therefore, before we import the file into `Dataframe`, we have to delete the first line of the file. Also note that the file is split by **Tab**.

```python
import pandas as pd
import fileinput
import os


def txt2df():
    file_list = [file for file in os.listdir() if file.endswith('.txt')]

    for file in file_list:
        with fileinput.FileInput(file, inplace=True) as f:
            for line_number, line in enumerate(f, 1):
                if line_number != 1:
                    print(line, end='')

    df = pd.read_csv(file, delimiter='\t')

    return df
```

#### Valid data section

The time series data we read from the `Dataframe` is the whole running process. However, the section we need is that before the sudden slump. There is a slump because the cart hits the spring and the accerlaration and velocity decreased sharply.

![1_1](https://github.com/HuaYuXiao/Mass-measurament-system-based-on-Newton-s-Second-Law/assets/117464811/fe789af3-fa1a-489d-a0f9-42f5fad6743e)

We set a threshold for the valid data. Once the **ay(g)** is below -0.1, then we define the measuring process is finished. 

```python
import pandas as pd


def find(df):
# 骤降的阈值，根据实际情况调整
    threshold = -0.1  
    index_of_drop = df[df < threshold].index[0]
    df = df.loc[:index_of_drop-10]

    return df
```    

#### Data filter

In this project, we apply `KalmanFilter`, `MeanFilter` and `KalmanSmoother` to filter data.

```python
import matplotlib.pyplot as plt
from pykalman import KalmanFilter
from tsmoothie.smoother import *
import pandas as pd


def filter(df):
    _, axs = plt.subplots(2, 2)

    plot(df, axs[0, 0],'original')

    measurements = df.values

    filter = KalmanFilter()
    filtered_state_means, _ = filter.filter(measurements)
    filtered_values = filtered_state_means[:, 0]
    df = pd.DataFrame(filtered_values, columns=['Filtered_Data'])

    plot(df, axs[0, 1],'KalmanFilter')

    df = df.rolling(20, center=True).mean()

    plot(df, axs[1, 0],'MeanFilter')

    smoother = KalmanSmoother(component='level_trend',component_noise={'level': 0.1, 'trend': 0.1}) 
    df = smoother.smooth(df).smooth_data.T

    plot(df, axs[1, 1],'KalmanSmoother')

    plt.show()

    df = df[5:-5]

    return df


def plot(df,ax,title):
    ax.plot(df)
    ax.set_xlabel('Time')
    ax.set_ylabel('ay(m/s^2)')
    ax.set_title(title)
```

The figure below reflects the effect of the three filter methods, compared to the original data.

![filter](https://github.com/HuaYuXiao/Mass-measurament-system-based-on-Newton-s-Second-Law/assets/117464811/4a445057-2b47-401d-84b7-c869b84383ac)

### Model fitting


















