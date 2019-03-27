import cv2 as cv

video = cv.VideoCapture('footage.mp4')

while True:
	check, frame = video.read()

	cv.imshow('frame', frame)


	if cv.waitKey(1) == 27:
		break

cv.destroyAllWindows()
video.release()

