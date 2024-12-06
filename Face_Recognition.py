import cv2
import dlib
import numpy as np

# Load Dlib's face detection and face recognition models
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor('./source/shape_predictor_68_face_landmarks.dat')
face_encoder = dlib.face_recognition_model_v1('./source/dlib_face_recognition_resnet_model_v1.dat')


def get_face_encoding(image_path):
    # Load image
    img = cv2.imread(image_path)
    # Convert to RGB (Dlib uses RGB images)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Detect faces
    faces = detector(img_rgb)

    
    if len(faces) == 0:
        raise ValueError(f"No face found in the image:{image_path}")

    if len(faces) > 1:
        raise ValueError(f"Not only one face found in the image:{image_path}")

        
    # Get the first face's landmarks
    landmarks = shape_predictor(img_rgb, faces[0])
    # Get the face encoding
    encoding = face_encoder.compute_face_descriptor(img_rgb, landmarks)
    
    return np.array(encoding)
    

def compare_faces(image_path1, image_path2):
    # Get face encodings
    encoding1 = get_face_encoding(image_path1)
    encoding2 = get_face_encoding(image_path2)
    
    # Compute the distance between the encodings
    distance = np.linalg.norm(encoding1 - encoding2)
    
    # Use a threshold to determine if they are the same person
    threshold = 0.5  # You can adjust this threshold
    return distance < threshold


def main(name):
    # Paths to your images
    image_path1 = f'image/data/{name}.jpg'
    image_path2 = 'image/output.jpg'
    # Compare the images
    try:
        if compare_faces(image_path1, image_path2):
            print("The images are of the same person.")
        else:
            print("The images are of different people.")
    except ValueError as e:
        print(e)
