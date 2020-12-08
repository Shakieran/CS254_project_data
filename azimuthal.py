from math import cos, sin, acos, radians

#Referenced from: http://www.samuelbosch.com/2014/02/azimuthal-equidistant-projection.html

center = [39.5, -98.35]
location = [42.961, -85.888]

t0 = radians(center[1])
l0 = radians(center[0])

cos1 = cos(t0)
sin1 = sin(t0)


t = radians(location[1])
l = radians(location[0])
costcos = cos(t) * cos(l-l0)
sint = sin(t)


c = acos((sin1)*(sint) + (cos1)*(costcos))
k = c / sin(c)
x = k * cos(t) * sin(l-l0)
y = k * (cos1 * sint - sin1 * costcos)

equidistance = [x,y]

print(equidistance)
