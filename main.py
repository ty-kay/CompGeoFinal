import sys
import Fortune6
import Fortune8
import matplotlib.pyplot as plt


def main():
    arr = []
    for l in sys.stdin:
        arr += l.strip().split()
    points = []
    for j in range(len(arr)):
        if j % 2 == 0:
            p = (float(arr[j]), float(arr[j + 1]))
            points.append(p)
    # Ty: Sorts by X coordinate in case same Y coordinate
    # points = sorted(points, key=lambda x: x[1])
    for point in points:
        plt.plot(point[0], point[1], 'o')
    run = Fortune6.Voronoi(points)
    run.compute()
    plt.xlim([-10, 10])
    plt.ylim([-10, 10])
    for line in run.output:
        x_values = [line.first.x, line.second.x]
        y_values = [line.first.y, line.second.y]
        plt.plot(x_values, y_values, 'k-')
    plt.show()
    exit()

if __name__ == '__main__':
    main()
