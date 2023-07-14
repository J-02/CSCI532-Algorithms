import matplotlib.pyplot as plt
import numpy as np

segments = 3

# Generates random points that are linearly correlated and in segments/clusters
def generate_points(num_points=300, segments=segments, x_range=100, equal=True):
    x = np.round(np.sort(np.append(np.random.uniform(0, x_range, size=segments - 1), [0, x_range])), 2)

    x.sort()

    # Range of x-values for each segment to generate on (even sized or odd sized)
    if equal == True:
        x_ranges = [(round((x_range / segments) * i,2), (round((x_range / segments) * (i + 1),2))) for i in range(segments)]
    else:
        x_ranges = [(round(x[i],2), round(x[i + 1],2)) for i in range(segments)]

    # Slopes and intercepts for each segment
    slopes = np.round(np.random.uniform(-1, 1, size=segments),2)
    intercepts = np.round(np.random.uniform(-10, 10, size=segments),2)

    # Generate random points for each segment
    points = np.empty([0,2])
    for i in range(segments):
        x_start, x_end = x_ranges[i]
        x = np.random.uniform(x_start, x_end, size=num_points)
        y = slopes[i] * x + intercepts[i] + np.random.uniform(-2, 2, size=num_points)  # Y-coordinates + error
        p = np.column_stack((x,y))
        points = np.row_stack((points,p))

    # Sort points by x-value
    points = np.round(points[points[:, 0].argsort()],2)
    lines = list(zip(slopes, intercepts))
    return points, lines, x_ranges


def segmented_linear_regression(points, k=segments):
    n = len(points)
    OPT = np.zeros(shape=[k, n])

    # Compute the cost matrix for each segment and each data point
    for i in range(n):
        OPT[0][i] = squared_error(points[:i + 1])

    for i in range(1, k):
        for j in range(i, n):
            # Compute the cost for all possible segmentations
            OPT[i][j] = min([OPT[i - 1][m] + squared_error(points[m + 1:j + 1]) for m in range(i - 1, j)])

    # Finding the best segmentation by backtracking through the cost matrix
    segments = []
    xcoords = []
    j = n - 1
    for i in range(k - 1, -1, -1):
        for m in range(i - 1, j):
            if OPT[i][j] == OPT[i - 1][m] + squared_error(points[m + 1:j + 1]):
                currentRange = points[m + 1:j + 1]  # selects the current range where the segment is located
                x = currentRange[:, 0]  # gets x and y coordinates of data points in the current range
                y = currentRange[:, 1]
                slope, intercept = np.polyfit(x, y, 1)  # linear regression for points in current range
                segments.append((round(slope,2), round(intercept,2))) # add line to segments
                xcoords.append([currentRange[0][0], currentRange[-1][0]])  # add range of segment
                j = m
                if len(segments) == k - 1:  # final cluster is the points remaining since backtracking
                    currentRange = points[:m]
                    x = currentRange[:, 0]
                    y = currentRange[:, 1]
                    slope, intercept = np.polyfit(x, y, 1)
                    segments.append((round(slope,2), round(intercept,2)))
                    xcoords.append([currentRange[0][0], currentRange[-1][0]])
                break
    segments.reverse()
    xcoords.reverse()
    return segments, xcoords


def squared_error(points):
    # Computing the squared error for given points
    n = len(points)
    x = [points[i][0] for i in range(n)]
    y = [points[i][1] for i in range(n)]
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xx = sum(x[i] ** 2 for i in range(n))
    sum_xy = sum(x[i] * y[i] for i in range(n))
    denominator = n * sum_xx - sum_x ** 2
    if denominator == 0:
        return float('inf')  # vertical slope
    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n
    error = sum((y[i] - (slope * x[i] + intercept)) ** 2 for i in range(n))
    return error


def plot(points, lines, coords):
    # Plot the input data points
    plt.figure()
    x = points[:,0]
    y = points[:,1]
    plt.scatter(x, y)

    # Add each segment to the plot w/in its range
    for idx, i in enumerate(segments):
        slope, intercept = i
        x0, xn = coords[idx]
        x = [x0, xn]
        y = [slope * x0 + intercept, slope * xn + intercept]
        plt.plot(x, y, 'r-')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Segmented Lines')


# Test example
points, lines, x_ranges= generate_points()
segments, x_coords = segmented_linear_regression(points)

# Plotting results
plot(points, segments, x_coords)
plt.show()
print("Regression:")
print(segments)
print("Actual")
print(lines)
print("Regression Ranges")
print(x_coords)
print("Actual Ranges")
print(x_ranges)
