import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from pathlib import Path
def get_bbox_center(labeled, label = 1):
    data = np.where(labeled == label)
    y_min, y_max = np.min(data[0]), np.max(data[0])
    x_min, x_max = np.min(data[1]), np.max(data[1])
    return ((y_min + y_max) / 2, (x_min + x_max) / 2)

def get_file_number(file_name):
    name = Path(file_name).stem
    name = name.split("_")
    return int(name[1])

data_dir = Path("./trajectory/out")
dist = {}
image = np.load(data_dir / "h_0.npy")
labeled = label(image)
for i in range(1, labeled.max() + 1):
    dist[i] = [get_bbox_center(labeled, i)]
file_list = sorted(list(data_dir.glob("*npy")), key = lambda x: get_file_number(x))[1:]
for file in file_list:
    image = np.load(file)
    labeled = label(image)
    last_point = {key: value[-1] for key, value in dist.items()}
    for i in range(1, labeled.max() + 1):
        current_coordinates = get_bbox_center(labeled, i)
        d_min = 10 ** 16
        k = ""
        for key, value in last_point.items():
            distance = ((current_coordinates[0] - value[0]) ** 2 + 
                        (current_coordinates[1] - value[1]) ** 2) ** 0.5
            if distance < d_min:
                d_min = distance
                k = key
        dist[k].append(current_coordinates)
        last_point.pop(k)
plt.figure(figsize = (10, 7))
for label, points in dist.items():
    points = np.array(points)
    coord_y, coord_x = points[:, 0], points[:, 1]
    plt.plot(coord_x, coord_y, linestyle = "-", marker = "o", ms = 3, label = f"Перемещение фигуры - {label}")
plt.legend()
plt.xlabel("Координаты по оси x")
plt.ylabel("Координаты по оси y")
plt.axis('equal')
plt.show()

    




