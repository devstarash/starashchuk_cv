import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.io import imread
from pathlib import Path

save_path = Path(__file__).parent

def count_lines(region):
    shape = region.image.shape
    image = region.image
    v_lines = (np.sum(image, 0) / shape[0] == 1).sum()
    h_lines = (np.sum(image, 1) / shape[1] == 1).sum()
    return v_lines, h_lines

def symmetry(region, transponce = False):
    image = region.image
    if transponce:
        image = image.T
    shape = image.shape
    top = image[: shape[0] // 2]
    if shape[0] % 2 != 0:
        bottom = image[shape[0] // 2 + 1:]
    else:
        bottom = image[shape[0] // 2 :]
    bottom = bottom[ : : -1]
    result = bottom == top
    return result.sum() / result.size

def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0] + 2, shape[1] + 2))
    new_image[1 : -1, 1 : -1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled) - 1

def extractor(region):
    cy, cx = region.centroid_local
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]
    perimetr = region.perimeter / region.image.size
    holes = count_holes(region)
    v_lines, h_lines = count_lines(region)
    v_lines /= region.image.shape[1]
    h_lines /= region.image.shape[0]
    eccentricity = region.eccentricity
    aspect = region.image.shape[0] / region.image.shape[1]
    h_symmetry = symmetry(region)
    v_symmetry = symmetry(region, True)
    return np.array([region.area/region.image.size, cy, cx, perimetr,
                      holes, v_lines, h_lines, eccentricity, aspect, h_symmetry, v_symmetry])

def classificator(region, templates):
    features = extractor(region)
    result = ""
    min_d = 10 ** 16
    for symbol, t in templates.items():
        d = ((t - features) ** 2).sum() ** 0.5
        if d < min_d:
            result = symbol
            min_d = d
    return result


template = imread('./vector_recognition/alphabet-small.png')[:,:,:-1]
template = template.sum(2)
binary = template != 765.

labeled = label(binary)
props = regionprops(labeled)

templates = {}

for region, symbol in zip(props, ["8","O","A","B","1","W","X","*","/","-"]):
    templates[symbol] = extractor(region)


image = imread('./vector_recognition/alphabet.png')[:,:,:-1]
abinary = image.mean(2) > 0
alabeled = label(abinary)

aprops = regionprops(alabeled)

result = {}
image_path = save_path / "out"
image_path.mkdir(exist_ok=True)

plt.figure(figsize=(5,7))

for region in aprops:
    symbol = classificator(region, templates)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1
    plt.cla()
    plt.title(f"Class: {symbol}")
    plt.imshow(region.image)
    plt.savefig(image_path / f"{region.label}.png")
print(result)
