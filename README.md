# gait_calculation
Motion sensor analysis with gait calculations.

In this project, we are interested in accelerometer data collected from a person walking.
24 datasets are collected using a mobile sensor application called Physics Toolbox Sensor Suite.

The data was stored by the app in a .csv file format to be processed later. Data was collected by having the person walk in a straight line for roughly sixty seconds, with the time taken to start and stop the recording added to that total. For comparisons, the data was collected with the phone in three different locations: held in hand, placed in a pocket, and placed at the ankle. A data set is also included that includes real step counts to verify step frequency in a later stage.

Since the data had a lot of noise due to phone sensors it was filtered using a low-pass Butterworth filter of order 3 in an attempt to isolate only the frequencies we are interested in. The data was collected by a walking person, so we expect the step frequency to be fairly low. Based on [Yousefian's paper on estimating foot clearance during walking](https://summit.sfu.ca/item/17204), the author used a filter with a cutoff frequency of 8 Hz according to the Fast Fourier Transform (FFT) of their data. For our project, the frequencies with the largest magnitudes are mostly situated on the lower end of the frequency range, so our cutoff frequency was set at 5 Hz.

We attempted to determine an individual’s step frequency, measured in Hz (or steps per second). Since the data was recorded with approximately sixty seconds of walking, the individual would have reached a steady pace, and that should occupy the majority of the observed signal. However, the frequency spectrum of the signals showed a large spike at 0 Hz, pointing to that as the dominant frequency in the total acceleration. That result is not meaningful given the context, so the 0 Hz value has been excluded from the rest of the analysis.

The ten frequencies with the largest magnitudes are then taken as “candidate frequencies”, from which a single value for step frequency will be calculated. There were three methods to determine the step frequency. Using the data set with real step counts, they can be compared for correctness at different phone recording positions. The first method is to simply take the frequency with the largest magnitude. The second is to take the mean of all candidate frequencies. Lastly, the third method is to take the mean of candidate frequencies whose magnitudes were at least half of the largest within that set.

We extracted the average walking speed, in meters per second, and total distance walked, in meters from the filtered dataset. Given that each person walks with a steady pace on a mostly straight path, the output for the average speed looks to be accurate, with a few outliers in our ‘hand’ datasets. The speed of the phone held in hand ranges from 2.14 m/s to 38.54m/s, while the speed of the phone tucked in the pocket looks to be the most consistent across all datasets, ranging from 1.30m/s to 5.01m/s. Similarly, since distance is directly proportional to speed, the total distance walked when the phone is in the pocket also reflects accurately in accordance with our input. The largest value for the distance walked in our filtered dataset is 2312.85 meters, which is impossible for a walking pace in a span of a minute.



## How to run:
`Required libraries: pandas, numpy, scipy, matplotlib, seaborn, sklearn`

The results and tables can be found in `main.ipynb`. The notebook can simply be opened and run through.
