import cv2
import numpy as np
import os
import json

class Grid():
	x = 0
	y = 0
	z = 0
	typeId = 0

	def __init__(self, x, z, typeId):
		self.x = x
		self.z = z
		self.typeId = typeId


class LoadMap():
	grids = []

	def __init__(self, fileName):
		self.img = cv2.imread(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\data\\' + fileName)
		self.imgRGB = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
		self.height, self.width, _ = self.img.shape

		self.colorTypes = self.readJson('colorType.json')

	def readJson(self, fileName):
		with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\data\\' + fileName, encoding='utf-8') as file_obj:
			contents = file_obj.read()

			return json.loads(contents)

	def createGrids(self): 
		h = 0
		for row in self.imgRGB:
			w = 0
			for item in row:
				for colorType in self.colorTypes:
					if item[0] == colorType['R'] and item[1] == colorType['G'] and item[2] == colorType['B']:
						grid = Grid(w - 2955, h + 5982, colorType['id'])
						self.grids.append(grid)

				w += 1

			h += 1

if __name__ == '__main__':
	map = LoadMap('map.jpg')
	print(map.height)
	print(map.width)
	map.createGrids()
	print(len(map.grids))