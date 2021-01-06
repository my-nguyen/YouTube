import joblib
import json
import numpy as np
import base64
import cv2
from wavelet import w2d

__class_name_to_number = {}
__class_number_to_name = {}
__model = None


def classify_image(base64, file_path=None):
    # get a cropped face either from disk or from base64 encoded string
    imgs = crop_face(file_path, base64)

    result = []
    # iterate thru each image
    for img in imgs:
        # resize raw image to 32x32
        scaled_raw_img = cv2.resize(img, (32, 32))
        # wavelet-transform raw image
        img_har = w2d(img, 'db1', 5)
        # resize the waveleted image to 32x32 also
        scaled_img_har = cv2.resize(img_har, (32, 32))
        # stack the 2 images on top of each other
        combined_img = np.vstack((scaled_raw_img.reshape(32*32*3, 1), scaled_img_har.reshape(32*32, 1)))

        # scaled raw is 32*32*3, and scaled waveleted is 32*32
        len_image_array = 32*32*3 + 32*32

        # reshape the combined image and convert type to float, for ML model training
        final = combined_img.reshape(1, len_image_array).astype(float)
        # save some model result data
        class_name = class_number_to_name(__model.predict(final)[0])
        class_probability = np.around(__model.predict_proba(final)*100, 2).tolist()[0]
        result.append({ 'class':class_name, 'class_probability':class_probability, 'class_dictionary':__class_name_to_number })

    return result


def class_number_to_name(class_num):
    return __class_number_to_name[class_num]


def load_artifacts():
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name

    # load the dictionary of player name to number
    with open("./artifacts/class_dictionary.json", "r") as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v:k for k,v in __class_name_to_number.items()}

    # load the saved ML model
    global __model
    if __model is None:
        with open('./artifacts/saved_model.pkl', 'rb') as f:
            __model = joblib.load(f)
    print("loading saved artifacts...done")


# function that converts a base-64 encoded string to CV image
def base64_to_img(base64):
    '''
    credit: https://stackoverflow.com/questions/33754935/read-a-base-64-encoded-image-from-memory-using-opencv-python-library
    :param uri:
    :return:
    '''
    encoded_data = base64.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def crop_face(image_path, base64):
    if image_path:
        # if image_path exists, load image from image_path
        img = cv2.imread(image_path)
    else:
        # else, load image from base-64 encoded string
        img = base64_to_img(base64)

    face_cascade = cv2.CascadeClassifier('./CelebrityFaceRecognition/server/opencv/haarcascades/haarcascade_frontalface_default.xml')
    # make a gray-scaled copy of image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect faces with Haar-cascade
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    eye_cascade = cv2.CascadeClassifier('./CelebrityFaceRecognition/server/opencv/haarcascades/haarcascade_eye.xml')
    cropped_faces = []
    for (x, y, w, h) in faces:
        # get gray face
        roi_gray = gray[y:y+h, x:x+w]
        # get color face
        roi_color = img[y:y+h, x:x+w]
        # detect eyes from gray face with Haar-cascade
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            # only save color face if there's 2 eyes in it
            cropped_faces.append(roi_color)

    # return color face
    return cropped_faces


def virat_b64():
    # b64.txt is a text file containing a base-64 encoded string converted from an actual image
    # the conversion is done on base64-image.de
    with open("b64.txt") as file:
        return file.read()

    
if __name__ == '__main__':
    load_artifacts()

    print(classify_image(virat_b64(), None))

    # print(classify_image(None, "./test_images/federer1.jpg"))
    # print(classify_image(None, "./test_images/federer2.jpg"))
    # print(classify_image(None, "./test_images/virat1.jpg"))
    # print(classify_image(None, "./test_images/virat2.jpg"))
    # print(classify_image(None, "./test_images/virat3.jpg")) # Inconsistent result could be due to https://github.com/scikit-learn/scikit-learn/issues/13211
    # print(classify_image(None, "./test_images/serena1.jpg"))
    # print(classify_image(None, "./test_images/serena2.jpg"))
    # print(classify_image(None, "./test_images/sharapova1.jpg"))
