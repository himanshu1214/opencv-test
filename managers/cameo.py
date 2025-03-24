import cv2
from video_stream_managers import windowManager, captureManager
#
class Cameo:
    def __init__(self):
        self._windowManager = windowManager('myWindow', self.oneKeyPress)
        self._captureManager = captureManager(cv2.VideoCapture(0), self._windowManager, True)

    def run(self):
        """
        here we are getting the windowManager to create window
        and then using the enterFrame method on captureManager Object to which give access to frames
        Returns:
        """
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreate:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            if frame is not None:
                # DO something
                pass

            self._captureManager.exitFrame()
            # then process
            self._windowManager.processEvents()


    def oneKeyPress(self, keyCode):
        """Manage the different keys such as space to take snapshot
        Tab for taking videos and
        Esc to Quit
        """
        if keyCode == 32: # this is in ASCII values for space
            # use captureManager to get the snapshot
            self._captureManager.writeImage('currentImage.png')

        elif keyCode == 9: # For Tab
            if not self._captureManager.isWritingVideo: # if the object is available to record video
                self._captureManager.startWritingVideo('video-test.avi')
            else:
                self._captureManager.stopWritingVideo()

        elif keyCode == 27: # escape
            self._windowManager.destroyWindow()


if __name__ == '__main__':
    Cameo().run()

