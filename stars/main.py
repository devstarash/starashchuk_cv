import numpy as np
from skimage.morphology import erosion
image = np.load("./stars/stars.npy")
mask_plus = np.zeros( (5,5) )
mask_cross = np.eye(5)
mask_cross = np.logical_or(mask_cross, np.fliplr(np.eye(5))).astype(int)
mask_plus[2 , : ] = 1
mask_plus[ : , 2] = 1
image_plus = erosion(image, footprint = mask_plus)
image_cross = erosion(image, footprint= mask_cross)
print(f"Количество плюсиков - {np.sum(image_plus).astype(int)}. Количество крестиков - {np.sum(image_cross).astype(int)}. \n Общая сумма звездочек - {(np.sum(image_plus) + np.sum(image_cross)).astype(int)}")
