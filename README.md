# magcal_2D

##Calibration of 2D magnetometer data

To be used as electronic compasses, magnetometers need to be calibrated in their final resting place, to correct for local magnetic fields and distortions due to ferrous materials. Most current calibration methods require to collect raw data from the magnetometer in a large number of different 3D orientations. For a good overview and tutorial, see https://thecavepearlproject.org/2015/05/22/calibrating-any-compass-or-accelerometer-for-arduino/

On the other hand, for a magnetometer mounted on a vehicle or large robot, it is not practical to collect data for 3D orientations. However, a simpler calibration works well in 2D, where the vehicle or robot is simply rotated about the horizontal axis for one or more complete turns.
