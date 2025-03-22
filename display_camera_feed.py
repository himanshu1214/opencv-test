import cv2


clicked = False

def onMouse(event, x, y, flags, params):
    global clicked
    if event == cv2.EVENT_LBUTTONUP:
        clicked = True

cameraCapture = cv2.VideoCapture(0)
cv2.namedWindow('My-window')
cv2.setMouseCallback('My-window', onMouse)

success, frame = cameraCapture.read()
while success and cv2.waitKey(1) == -1 and not clicked:
    cv2.imshow('My-window', frame)
    success, frame = cameraCapture.read()

cv2.destroyWindow('My-window')
cameraCapture.release()
