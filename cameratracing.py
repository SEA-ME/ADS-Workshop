import cv2
import time

from piracer.cameras import Camera, MonochromeCamera



camera = MonochromeCamera()
face_Cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
i = 0
while True:
	image = camera.read_image()

	imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	faces = face_Cascade.detectMultiScale(imgGray, 1.1, 4)

	for (x, y, w, h) in faces:
		cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)


	cv2.imwrite(f'../../pictures/image_{i}.png', image)
	cv2.imwrite('../../pictures/image.png', image)
	time.sleep(1)
	i = i + 1