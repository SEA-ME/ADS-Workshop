
from pathlib import Path
import time
from typing import List

import cv2
import numpy as np
from matplotlib import pyplot as plt
from piracer.cameras import Camera, MonochromeCamera

camera = MonochromeCamera()


def take_image() -> np.ndarray:
	image = camera.read_image()
	cv2.imwrite('image.png', image)
	image_array = np.array(image, dtype=np.uint8)
	return image_array

def read_template(path: Path) -> np.ndarray:
	"""Read template from path and return numpy array with type uint8."""
	image = cv2.imread(path, 1)
	return image.astype(np.uint8)

def get_locations(screenshot: np.ndarray, template: np.ndarray, accuracy: float) -> List[List]:
	"""Calculate matching positions of template and screenshot with a given accuracy."""
	oScores = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
	yloc, xloc = np.where(oScores >= accuracy)
	locations = zip(yloc, xloc)
	result = []
	for y, x in locations:
		percentage = oScores[y][x]
		result.append([(y,x), percentage])
	return result

def find_element(path: Path) -> None:
	"""Finds the template element and moves cursor to all occurences."""
	arrayimage = take_image()
	template = read_template(path)
	loc = get_locations(arrayimage, template, 0.95)
	print(loc)
	time.sleep(1)
	for attr in loc:
		print(f"Template {path} found at coordinates {attr[0][1]}, {attr[0][0]} with accuracy {attr[1]}")
		time.sleep(1)

def main() -> None:
	while True:
		find_element('ball.png')
		time.sleep(1)

if __name__ == '__main__':

	main()