import cv2
import numpy
import time


class CaptureManager(object):

    def __init__(self, capture, previewWindowManager=None, shouldMirrorPreview=False):

        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview

        # Var's related to capture.
        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None

        # Var's related to writing.
        self._imageFileName = None
        self._videoFileName = None
        self._videoEncoding = None
        self._videoWriter = None

        # Var's related to FPS.
        self._startTime = None
        self._framesElapsed = 0
        self._fpsEstimate = None

    @property
    def channel(self):
        return self._channel
    
    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        """To retrieve the frame."""
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve()
        return self._frame

    @property
    def isWritingImage(self):
        return self._imageFileName is not None

    @property
    def isWritingVideo(self):
        return self._videoFileName is not None

    def enterFrame(self):
        """Capture the next frame, if any."""

        # But first, check that any previous frame was exited.
        assert not self._enteredFrame, 'previous enterFrame() had no matching exitFrame()'

        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        """Draw to the window. Write to the file. Release the frame."""

        # Check whether grabbed frame is retrievable.
        # The getter may retrieve the frame and cache.
        if self.frame is None:
            self._enteredFrame = False
            return

        # Update the FPS estimate and retrieve variables.
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        # Draw to window, if any.
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirrorFrame = numpy.fliplr(self._frame).copy()
                self.previewWindowManager.show(mirrorFrame)
            else:
                self.previewWindowManager.show(self._frame)

        # Draw to the image file, if any.
        if self.isWritingImage:
            cv2.imwrite(self._imageFileName, self._frame)
            self._imageFileName = None

        # Write to video, if any.
        self._writeVideoFrame()

        # Release the frame.
        self._frame = None
        self._enteredFrame = False

    def writeImage(self, fileName):
        """Write the next exited frame to an image file."""
        self._imageFileName = fileName

    def startWritingVideo(self, fileName, encoding=cv2.VideoWriter_fourcc('I', '4', '2', '0')):
        """Start writing exited frame to a video file."""
        self._videoFileName = fileName
        self._videoEncoding = encoding

    def stopWritingVideo(self):
        """Stop writing exited frame to a video file."""
        self._videoFileName = None
        self._videoWriter = None
        self._videoEncoding = None

    def _writeVideoFrame(self):
        if not self.isWritingVideo:
            return

        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps <= 0.0:
                if self._framesElapsed < 20:
                    # Wait for more frames to be elapsed.
                    # So that estimate is more stable.
                    return
                else:
                    fps = self._fpsEstimate
            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(self._videoFileName, self._videoEncoding, fps, size)

        self._videoWriter.write(self._frame)


class WindowManager(object):

    def __init__(self, windowName, keypressCallBack=None):

        self.keypressCallBack = keypressCallBack
        self._windowName = windowName
        self._isWindowCreated = False

    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowName, cv2.WINDOW_AUTOSIZE)
        self._isWindowCreated = True

    def show(self, frame):
        cv2.imshow(self._windowName, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False

    def processEvents(self):
        keyCode = cv2.waitKey(1)
        if self.keypressCallBack is not None and keyCode != -1:
            # Discard any Non-ASCII info encoded by GTK.
            keyCode &= 0xFF
        self.keypressCallBack(keyCode)
