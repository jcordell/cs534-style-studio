from imutils import face_utils
import imutils
import dlib
import cv2


class FaceDetector:
    # class constructor, initialize face detector
    def __init__(self, image):
        self.image = self.resize_image(image)

        # keep a reference to the original image that hasn't been altered with overlays/colors
        self.original_image = self.image
        self.gray = self.convert_to_gray(self.image)

        self.detector = dlib.get_frontal_face_detector()

        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        self.predictor = dlib.shape_predictor('etc/shape_predictor.dat')

        self.faces = self.detect_features(self.gray, 1)
        self.feature_map = {}
        self.make_feature_map(self.image, self.gray, self.faces)

    def resize_image(self, image):
        return imutils.resize(image, width=500)

    def convert_to_gray(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def detect_features(self, gray_image, dim):
        return self.detector(gray_image, dim)

    def make_feature_map(self, image, gray, faces):
        # loop over the face detections
        for (i, rect) in enumerate(faces):
            # determine the facial landmarks for the face region, then
            # convert the landmark (x, y)-coordinates to a NumPy array
            shape = self.predictor(gray, rect)

            # shape is every feature point mapped to one array
            shape = face_utils.shape_to_np(shape)

            # loop over the face parts individually
            # feature_name one of [mouth, right_eyebrow, left_eyebrow, right_eye, left_eye, nose, jaw]
            for (feature_name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
                # clone the original image so we can draw on it, then
                # display the name of the face part on the image
                self.feature_map[feature_name] = shape[i:j]

            return self.feature_map
