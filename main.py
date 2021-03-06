from  preprocess import Preprocess
from tensorflow.keras.models import load_model
import numpy as np
import cv2
from config import params

print("###################################################")
print("# uygun video isimleri: 'Oguzhan', 'Sherlock'")
video = input("# video adını yazınız: ")
print("# " + video + " yükleniyor...")
print("###################################################")

class main:
    def __init__(self):
        self.model = load_model('./model/facenet_keras.h5')
        self.init_Database()
        print("statement: main çalıştırıldı",flush=True)

    def run(self, path):
        print("statement: run metotu çağrıldı",flush=True)

        person, similarity = self.execute(path)
        print("Şu fotoğraftakini {0} kişisine benzettim.".format(person))
        
        im = cv2.imread(path)
        self.show(im,person)
        print("statement: run metotu sonlandırıldı",flush=True)

    def execute(self,path):
        print("statement: execute metotu çağrıldı",flush=True)
        
        who = None
        similarity = None
        
        img = cv2.imread(path)
        img_face = self.p.getFace(img)
        print("test:: " + self.database.items())
        for i in img_face:
            i = cv2.resize(i, (160, 160))
            embeded_face = self.p.embedding(i)

            min_distance = 200
            for person, db_face in self.database.items():
                x = self.euclid_distance(embeded_face,db_face)
                if x < min_distance:
                    min_distance = x
                    who = person
                    similarity = x

        print("statement: execute metotu sonlandırıldı",flush=True)
        return who, similarity

    def euclid_distance(self, input_embed, db_embed):
        return np.linalg.norm(db_embed-input_embed)

    def init_Database(self):
        self.p = Preprocess(database_path="./train/",folders=params["People"])
        self.database = self.p.load_images()

    def show(self,img,text):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,text, (10, 10), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('img',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def recognize_faces_in_video(self, videopath):
    
        who = None
        similarity = None
        
        cv2.namedWindow("face recognizer for cse564")
        vc = cv2.VideoCapture(videopath)
    
        font = cv2.FONT_HERSHEY_SIMPLEX
        face_cascade = cv2.CascadeClassifier("../haarcascade_frontalface_default.xml")
            
        while vc.isOpened():
            _, frame = vc.read()
            img = frame
            height, width, channels = frame.shape
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # Loop through all the faces detected 
            for (x, y, w, h) in faces:
                x1 = x
                y1 = y
                x2 = x+w
                y2 = y+h
                
                face_image = frame[max(0, y1):min(height, y2), max(0, x1):min(width, x2)]    
                img = cv2.resize(face_image, (160, 160))
                embeded_face = self.p.embedding(img)
                
                min_distance = 200
                for person, db_face in self.database.items():
                    x = self.euclid_distance(embeded_face,db_face)
                    if x < min_distance:
                        min_distance = x
                        who = person
                        similarity = x
                
                print("Benzerlik:",similarity)


                if similarity <= params["Thresold"]:
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
                    cv2.putText(frame,who, (x1-10, y1-10), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
                    
            key = cv2.waitKey(100)
            cv2.imshow("face recognizer for cse564", frame)
            if key == 27: # exit on ESC
                break
        
        vc.release()
        cv2.destroyAllWindows()
                

m = main()
m.recognize_faces_in_video("../test/" + str(video) + ".mp4")

