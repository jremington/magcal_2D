% File: magcal_2d.m
% This MATLAB program calculates the calibration parameters for a 2D magnetometer.
% As is customary, data for one or two complete revolutions of the magnetometer
% should be collected while held level, points closely spaced if possible.
% S. James Remington 8/2013
% uses published Matlab function EllipseDirectFit.m
% http://www.mathworks.com/matlabcentral/fileexchange/22684-ellipse-fit-direct-method
%
% First step: collect data and produce a CSV file (comma separated values) of
% magnetometer X and Y values (can be raw).
%
% Second step: execute magcal_2d.m
%
% This work was inspired by the 3D procedure described in:
% http://sailboatinstruments.blogspot.com/2011/08/improved-magnetometer-calibration.html
%

% no column headings allowed!
Book1 = csvread('mag2d_raw.csv');

A = EllipseDirectFit(Book1);

% modified coefficients of equation for ellipse
% from http://mathworld.wolfram.com/Ellipse.html

a = A(1);
b = A(2)/2;
c = A(3);
d = A(4)/2;
f = A(5)/2;
g = A(6);

% X0, Y0 offset (centroid of ellipse)

x0 = (c*d - b*f)/(b^2 - a*c);
y0 = (a*f - b*d)/(b^2 - a*c);

% semimajor and semiminor axes

numer = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g);
denom1 = (b*b-a*c)*( sqrt((a-c)^2 + 4*b*b) - (a+c));
denom2 = (b*b-a*c)*(-sqrt((a-c)^2 + 4*b*b) - (a+c));
a_axis = sqrt(numer/denom1);
b_axis = sqrt(numer/denom2);

% angle of ellipse semimajor axis wrt X-axis

if (a < c) theta =        0.5*acotd((a-c)/(2*b));
else       theta = 90.0 + 0.5*acotd((a-c)/(2*b));
end

s=sprintf('x0 = %5.2f y0 = %5.2f a = %5.2f, b= %5.2f, theta(d) = %4.1f', ...
         x0,y0,a_axis,b_axis, theta);
disp(s);

% rotation matrix to align semimajor axis to X-axis

ct=cosd(theta);
st=sind(theta);
R = [ct st; -st ct];
xy0 = [x0 y0];

%rescale vector, correct for difference in magnetometer X & Y gains

scale = [b_axis/a_axis,1];

% final result: matrix to align ellipse axes wrt coordinates system, normalize X and Y gains and rotate back.

Q = R^-1*([scale(1) 0; 0, scale(2)]*R);

% correct the input data

xy = ( Q*(Book1-xy0)' )';
csvwrite('corrected_data.csv',xy);

% replot scaled data
figure;
axis equal;
scatter(Book1(:,1),Book1(:,2));
hold on;
scatter(xy(:,1),xy(:,2))
legend('raw','corrected');


disp(' ');
disp('scaled rotation matrix and vector to apply: Q*(XY-XY0)');
s = sprintf('(%6.4f %6.4f)*(X - (%5.1f))',Q(1,1),Q(1,2),x0);
disp(s);
s = sprintf('(%6.4f %6.4f)*(Y - (%5.1f))',Q(2,1),Q(2,2),y0);
disp(s);
