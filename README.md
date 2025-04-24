# magcal_2D

Calibration of 2D magnetometer data

To be used as electronic compasses, magnetometers need to be calibrated in their final resting place. The calibration process corrects for local magnetic fields and field distortions due to nearby ferrous materials. 

Most current calibration methods require one to collect raw data from the magnetometer in a large number of different 3D orientations. For a good overview and tutorial, see https://thecavepearlproject.org/2015/05/22/calibrating-any-compass-or-accelerometer-for-arduino/

On the other hand, for a magnetometer mounted on a vehicle or large robot, it is not practical to collect data for 3D orientations. However, a simpler calibration works well in 2D, where the vehicle or robot is simply rotated about the horizontal axis for one or more complete turns. For navigation, the heading relative to magnetic North can be determined very simply by taking the arctangent of the corrected X and Y data. 

The magnetometer MUST be mounted with the Z axis vertical. 

The procedure used here is very simple: an ellipse is fitted to the raw data, an offset is calculated and subtracted, the ellipse is rotated so that the major axis is aligned along X, the data are rescaled to circularize, then rotated back into the original orientation.

The program output is a 2x2 correction matrix Q and offsets X0 and Y0, so that the corrected values are

Corrected_X = Q00*(rawX - X0) + Q01*(rawY - Y0)

Corrected_Y = Q10*(rawX - X0) + Q11*(rawY - Y0)

Example plot, before (green) and after (blue) calibration. The ideal case is represented by a red circle is centered on the plot origin. Working code is presented for Matlab or Gnu Octave, and in Python, along with the sample data set (magcal2d_cut.csv) that resulted in the plot below. 

The Matlab/Gnu Octave and Python results are equivalent.

*Note: in this example, the offsets applied to the raw data are very small. They are usually much larger.

![Capture](https://github.com/user-attachments/assets/605aeee7-60a4-4b0b-855c-d8e23f04e2c1)

