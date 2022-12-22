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
    points = sorted(points, key=lambda x: x[1])
    for point in points:
        plt.plot(point[0], point[1], 'o')
    qwer = Fortune6.Voronoi(points)
    qwer.process()
    plt.xlim([-10, 10])
    plt.ylim([-10, 10])
    asdf = map(lambda curr: (curr.first.x, curr.first.y, curr.second.x, curr.second.y), qwer.output)
    for a in asdf:
        x_values = [a[0], a[2]]
        y_values = [a[1], a[3]]
        plt.plot(x_values, y_values, 'k-')
    plt.show()
    exit()

if __name__ == '__main__':
    main()
