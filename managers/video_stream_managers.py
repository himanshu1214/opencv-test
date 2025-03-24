import time

import cv2
import numpy

class captureManager:
    def __init__(self, capture, previewWindowManager= None, shouldMirrorPreview = False ):
        self._frame = None
        self._imageFileName = None
        self._videoFileName = None
        self._channel = 0 # by default its zero unless the camera is multihead
        self._enteredFrame = False
        self._capture = capture
        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview
        self._framesElapsed = 0
        self._fpsEstimate = None
        self._videoEncoding = None
        self._videoWriter = None
        self._startTime = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channelVal):
        if self._channel != channelVal:
            self._channel = channelVal
            self._frame = None

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve(self._frame, self._channel)

        return self._frame

    @property
    def isWritingVideo(self):
        return self._videoFileName is not None

    @property
    def isWritingImage(self):
        return self._imageFileName is not None

    def enterFrame(self):
        print(self._enteredFrame, "self._enteredFrame")
        assert not self._enteredFrame, \
            'previous enterFrame() had no matching exitFrame()'
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        """

        Returns:

        """
        # Check for the frame
        if self._frame is None:
            self._enteredFrame = False
            return

        # Update the FPS estimate
        if self._framesElapsed == 0:
            self._startTime = time.perf_counter()
        else:
            timeElapsed = time.perf_counter() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        # Check the previewWindowManager and add a MirrorPreview
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirroredFrame = numpy.fliplr(self._frame)
                self.previewWindowManager.show(mirroredFrame)
            else:
                self.previewWindowManager.show(self._frame)

        # write to image file
        if self.isWritingImage:
            cv2.imwrite(self._imageFileName, self._frame)
            self._imageFileName = None

        # Write to video file
        self._writeVideoFrame()
        # Then release frame
        self._frame = None

    def _writeVideoFrame(self):
        if not self.isWritingVideo:
            return
        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)

            if numpy.isnan(fps) or fps <= 0.0:
                if self._framesElapsed < 20:
                    return
                fps = self._fpsEstimate
                size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                self._videoWriter = cv2.VideoWriter(self._videoFileName, self._videoEncoding, fps, size)
                self._videoWriter.write(self._frame)

    def writeImage(self, imageName):
        self._imageFileName = imageName

    def startWritingVideo(self, filename, encoding = cv2.VideoWriter_fourcc('M','J','P','G')):
        self._videoFileName = filename
        self._videoEncoding = encoding

    def stopWritingVideo(self):
        self._videoEncoding = None
        self._videoWriter = None
        self._videoFileName = None



# we are abstracting the opencv window control
class windowManager:
    def __init__(self, windowName, keypressCallback):
        self._windowName = windowName
        self.keypressCallback = keypressCallback
        self._isWindowExist = False

    @property
    def isWindowCreate(self):
        return self._isWindowExist

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowExist = True

    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowExist = False

    def show(self, frame):
        cv2.imshow(self._windowName, frame)

    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            self.keypressCallback(keycode)



