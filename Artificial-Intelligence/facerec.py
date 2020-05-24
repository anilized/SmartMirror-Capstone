import face_recognition
import os
import cv2
import time
from pymongo import MongoClient


class FaceAssistant:
    
    userName = "Unknown"

    def __init__(self, userName):
        self.userName = userName

    def face_rec():
        cluster = MongoClient('mongodb+srv://anilized:29061996acc@cluster0-0fa34.mongodb.net/test?retryWrites=true&w=majority')
        db = cluster['smartmirror']
        collection = db['users']
        KNOWN_FACE_DIR = "known_faces"
        # UNKNOWN_FACE_DIR = "unknown_faces"
        BOOLEAN = True
        TOLERANCE = 0.6
        MODEL = "hog"  #or hog
        FaceAssistant.userName = "Unknown"
        #AUTHORIZED = False

        video = cv2.VideoCapture(0) # could put in a filename

        print("Face Identification Started")
        tic_train = time.perf_counter()
        known_faces = [] #encoded faces
        known_names = [] #known name list
        
        """
        for name in os.listdir(KNOWN_FACE_DIR):
            for filename in os.listdir(f"{KNOWN_FACE_DIR}/{name}"):
                image = face_recognition.load_image_file(f"{KNOWN_FACE_DIR}/{name}/{filename}")
                encoding = face_recognition.face_encodings(image)[0] #for getting the first one and only one
                #collection.insert_one({'name': name, 'encoding': encoding.tolist()})
                known_faces.append(encoding)
                known_names.append(name)
        """
        #print(user_dict)

        toc_train = time.perf_counter()
        train_time = toc_train - tic_train
        train_time = round(train_time,2)
        train_str = (f"Train time: {train_time}")

        data = list(collection.find({}))
        for item in data:
            known_names.append(item['name'])
            known_faces.append(item['encoding'])

        while BOOLEAN:
            tic = time.perf_counter()
            # print(filename)
            # image = face_recognition.load_image_file(f"{UNKNOWN_FACE_DIR}/{filename}")

            ret, image = video.read()

            locations = face_recognition.face_locations(image, model=MODEL)
            encodings = face_recognition.face_encodings(image, locations)
            # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # convert for opencv


            for face_encoding, face_location in zip(encodings, locations):
                results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
                match = None
                if True in results:
                    match = known_names[results.index(True)]
                    if match:
                        FaceAssistant.userName = match
                        BOOLEAN = False
                        #return FaceAssistant.userName
                else:
                    FaceAssistant.userName = "Unknown"
                    BOOLEAN = False
                    #return FaceAssistant.userName
        toc = time.perf_counter()
        runtime = toc - tic
        runtime = round(runtime, 2)
        run_string = f"Recognition Time: {runtime} seconds."
        sum_of_runtime = runtime + train_time
        sum_str = f"Total: {sum_of_runtime} seconds."
        print(f"{toc - tic:0.4f} seconds")
        return FaceAssistant.userName, train_str, run_string, sum_str

# print("Can't recognize face")   
# cv2.waitKey(20)
# cv2.destroyAllWindows(filename)
a = FaceAssistant
print(a.face_rec())
#print(a.face_rec())
#print(a.userName)