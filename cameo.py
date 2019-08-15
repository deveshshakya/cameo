import cv2
# import filters
from managers import CaptureManager, WindowManager
# from trackers import FaceTracker
# import rects


class Cameo(object):

    def __init__(self):

        self._windowManager = WindowManager('Cameo', self.onKeypress)
        self._captureManager = CaptureManager(cv2.VideoCapture(0), self._windowManager, True)
        # self._curveFilter = filters.BGRProviaCurveFilter()
        # self._faceTracker = FaceTracker()
        # self._shouldDrawDebugRect = False

    def run(self):
        """Run the main loop."""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame

            # self._faceTracker.update(frame)
            # faces = self._faceTracker.faces

            # filters.strokeEdges(frame, frame)
            # self._curveFilter.apply(frame, frame)

            # if self._shouldDrawDebugRect:
            #     self._faceTracker.drawDebugRects(frame)

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
        # # x
        # if keyCode == 120:
        #     self._shouldDrawDebugRect = not self._shouldDrawDebugRect
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
