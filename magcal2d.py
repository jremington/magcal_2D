# modified from https://www.mirkosertic.de/blog/2023/01/magnetometer-calibration-ellipsoid/
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# input raw data, CSV file with column labels
rawdata = pd.read_csv('mag2d_raw.csv')
xcol = rawdata["x"]
ycol = rawdata["y"]

# Following code taken from https://scipython.com/blog/direct-linear-least-squares-fitting-of-an-ellipse/
def fit_ellipse(x, y):
    """

    Fit the coefficients a,b,c,d,e,f, representing an ellipse described by
    the formula F(x,y) = ax^2 + bxy + cy^2 + dx + ey + f = 0 to the provided
    arrays of data points x=[x1, x2, ..., xn] and y=[y1, y2, ..., yn].

    Based on the algorithm of Halir and Flusser, "Numerically stable direct
    least squares fitting of ellipses'.


    """

    D1 = np.vstack([x**2, x*y, y**2]).T
    D2 = np.vstack([x, y, np.ones(len(x))]).T
    S1 = D1.T @ D1
    S2 = D1.T @ D2
    S3 = D2.T @ D2
    T = -np.linalg.inv(S3) @ S2.T
    M = S1 + S2 @ T
    C = np.array(((0, 0, 2), (0, -1, 0), (2, 0, 0)), dtype=float)
    M = np.linalg.inv(C) @ M
    eigval, eigvec = np.linalg.eig(M)
    con = 4 * eigvec[0]* eigvec[2] - eigvec[1]**2
    ak = eigvec[:, np.nonzero(con > 0)[0]]
    return np.concatenate((ak, T @ ak)).ravel()

def cart_to_pol(coeffs):
    """

    Convert the cartesian conic coefficients, (a, b, c, d, e, f), to the
    ellipse parameters, where F(x, y) = ax^2 + bxy + cy^2 + dx + ey + f = 0.
    The returned parameters are x0, y0, ap, bp, e, phi, where (x0, y0) is the
    ellipse centre; (ap, bp) are the semi-major and semi-minor axes,
    respectively; e is the eccentricity; and phi is the rotation of the semi-
    major axis from the x-axis.

    """

    # We use the formulas from https://mathworld.wolfram.com/Ellipse.html
    # which assumes a cartesian form ax^2 + 2bxy + cy^2 + 2dx + 2fy + g = 0.
    # Therefore, rename and scale b, d and f appropriately.
    a = coeffs[0]
    b = coeffs[1] / 2
    c = coeffs[2]
    d = coeffs[3] / 2
    f = coeffs[4] / 2
    g = coeffs[5]

    den = b**2 - a*c
    if den > 0:
        raise ValueError('coeffs do not represent an ellipse: b^2 - 4ac must'
                         ' be negative!')

    # The location of the ellipse centre.
    x0, y0 = (c*d - b*f) / den, (a*f - b*d) / den

    num = 2 * (a*f**2 + c*d**2 + g*b**2 - 2*b*d*f - a*c*g)
    fac = np.sqrt((a - c)**2 + 4*b**2)
    # The semi-major and semi-minor axis lengths (these are not sorted).
    ap = np.sqrt(num / den / (fac - a - c))
    bp = np.sqrt(num / den / (-fac - a - c))

    # The angle of anticlockwise rotation of the major-axis from x-axis.
    if b == 0:
        phi = 0 if a < c else np.pi/2
    else:
        phi = np.arctan((2.*b) / (a - c)) / 2
        if a > c:
            phi += np.pi/2
 
    return x0, y0, ap, bp, phi

coeffs = fit_ellipse(xcol, ycol)
x0, y0, ap, bp, phi = cart_to_pol(coeffs)

result = np.array([x0,y0,ap,bp,math.degrees(phi)])
rounded = np.round(result,2)

print('X0, Y0, a, b, phi (degrees): ',rounded)
print(' ')

#scale factors. Normalize to b axis length
sx = bp / ap 
sy = 1
cp = math.cos(phi)
sp = math.sin(phi)

# final result: matrix to align ellipse axes wrt coordinates system, normalize X and Y gains 
# and rotate back. In Matlab matrix notation, where R is a 2x2 rotation matrix
#Q = R^-1*([scale(1) 0; 0, scale(2)]*R);

Q = np.matrix([[sx*cp*cp+sy*sp*sp, sx*cp*sp-sy*cp*sp],
               [sx*sp*cp-sy*sp*cp, sx*sp*sp+sy*cp*cp]])

print('offset to subtract from raw data (x0,y0) ',rounded[0],rounded[1])
print('Correction matrix to apply to offset data')
print(Q)

"""
ellipse = Ellipse((x0, y0), ap * 2, bp * 2, color='r', angle=math.degrees(phi), fill=False)
fig, ax = plt.subplots()
ax.add_patch(ellipse)
ax.scatter(xcol, ycol, label='Data Points', color='b')
plt.show()
"""

def correctdata(row):
    x = np.array(row["x"] - x0)
    y = np.array(row["y"] - y0)

    return [x * Q[0,0] + y * Q[0,1],
           (x * Q[1,0] + y * Q[1,1])]

res = rawdata.apply(correctdata, axis=1, result_type='expand')
circle = plt.Circle((0, 0), bp, color='r', fill=False)
fig, ax = plt.subplots()
ax.add_patch(circle)
ax.scatter(res[0], res[1], label='Corrected Data (b)', color='b')
ax.scatter(xcol, ycol, label='Raw Data (g)', color='g')
plt.legend(loc='best')
plt.show()
exit()
