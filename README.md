# gait_calculation
Motion sensor analysis with gait calculations.

In this project, we are interested in accelerometer data collected from a person walking.
24 datasets are collected using a mobile sensor application called Physics Toolbox Sensor Suite.

The data was stored by the app in a .csv file format to be processed later. Data was collected by having the person walk in a straight line for roughly sixty seconds, with the time taken to start and stop the recording added to that total. For comparisons, the data was collected with the phone in three different locations: held in hand, placed in a pocket, and placed at the ankle. A data set is also included that includes real step counts to verify step frequency in a later stage.

Since the data had a lot of noise due to phone sensors it was filtered using a low-pass Butterworth filter of order 3 in an attempt to isolate only the frequencies we are interested in. The data was collected by a walking person, so we expect the step frequency to be fairly low. Based on [Yousefian's paper on estimating foot clearance during walking](https://summit.sfu.ca/item/17204), the author used a filter with a cutoff frequency of 8 Hz according to the Fast Fourier Transform (FFT) of their data.

`Required libraries: pandas, numpy, scipy, matplotlib, seaborn, sklearn`

## How to run:
The results and tables can be found in `main.ipynb`. The notebook can simply be opened and run through.
