import cv2
from cameo.managers import CaptureManager, WindowManager


class Cameo(object):

    def __init__(self):

        self._windowManager = WindowManager('Cameo', self.onKeypress)
        self._captureManager = CaptureManager(cv2.VideoCapture(0), self._windowManager, True)

    def run(self):
        """Run the main loop."""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    def onKeypress(self, keyCode):
        """
        Handle a keypress.

        space -> Take a screen-shot.
        x -> Start/Stop Drawing Rectangles around Faces.
        tab -> Start/Stop recording screen-cast.
        esc -> Quit.
        """
        # Space
        if keyCode == 32:
            self._captureManager.writeImage('screenshot.jpg')
        # Tab
        elif keyCode == 9:
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo('screencast.avi')
            else:
                self._captureManager.stopWritingVideo()
        # ESC
        elif keyCode == 27:
            self._windowManager.destroyWindow()


if __name__ == "__main__":
    Cameo().run()
