import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from skimage.morphology import (opening, dilation, closing, erosion)
image= np.load("wires/wires6.npy")
struct_element = np.ones((3, 1))
processed = opening(image, footprint= struct_element)
labeled = label(image)
print(f"{labeled.max()}")

for n in range(1, labeled.max() + 1):
    marked = labeled == n
    marked = label(opening(marked, footprint= struct_element))
    print(f"Wire = {n}, parts = {label(marked).max()}")

    print()
plt.subplot(121)
plt.imshow(image)
plt.subplot(122)

plt.imshow(processed)
plt.show()
