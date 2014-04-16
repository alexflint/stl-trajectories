import numpy as np

RADIUS = .1
trajectory = [(0,0,1), (0,10,2)]#, (10,10,1), (15,5,-1)]

def axis(i, n):
    x = np.zeros(n)
    x[i] = 1.
    return x

def make_quad(a, b, c, d):
    # write triangles in both clockwise and anti-clockwise direction
    # so that we see them from both sides
    return [(a, b, c),
            (a, c, b),
            (a, d, c),
            (a, c, d)]

def make_cube(x):
    return (make_quad(x[0], x[1], x[3], x[2]) +
            make_quad(x[1], x[3], x[7], x[5]) +
            make_quad(x[2], x[3], x[7], x[6]) +
            make_quad(x[0], x[1], x[5], x[4]) +
            make_quad(x[4], x[5], x[7], x[6]) +
            make_quad(x[0], x[2], x[6], x[4]))

def make_strut(start, end, radius):
    start = np.asarray(start)
    end = np.asarray(end)
    diff = end - start

    idx = np.argmin(diff)
    u = np.cross(diff, axis(idx, 3))
    v = np.cross(diff, u)

    corners = []
    for i in range(8):
        base = start if i&4==0 else end
        du = radius if i&1 == 0 else -radius
        dv = radius if i&2 == 0 else -radius
        corners.append(base + du*u + dv*v)

    return make_cube(corners)

def write_solid(solid, out):
    out.write('solid trajectory\n')
    for facet in solid:
        normal = np.cross(facet[1]-facet[0], facet[2]-facet[0])
        out.write('  facet %f %f %f\n' % tuple(normal))
        out.write('    outer loop\n')
        for vertex in facet:
            out.write('      vertex %f %f %f\n' % tuple(vertex))
        out.write('    endloop\n')
        out.write('  endfacet\n')

def main():
    solid = []
    for i in range(len(trajectory)-1):
        solid.extend(make_strut(trajectory[i], trajectory[i+1], RADIUS))
    with open('trajectory.stl', 'w') as fd:
        write_solid(solid, fd)

if __name__ == '__main__':
    main()
