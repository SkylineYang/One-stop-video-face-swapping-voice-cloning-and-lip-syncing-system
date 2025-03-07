import cv2
import os
import face_recognition
import numpy as np
from ultralytics import YOLO
import argparse

def face_classification(videopath, facepath, face_detection_conf=0.8, face_recognition_conf=0.6):
    # 加载视频
    cap = cv2.VideoCapture(videopath)
    path = './face_detection/yolov8n-face-lindevs.pt'
    model = YOLO(path, task='detect')

    pic_path = facepath #"./faces"
    if os.path.exists(pic_path) is False:
        os.mkdir(pic_path)

    face_num = 0
    i = 0
    s = 0
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    while True:
        ret, frame = cap.read()
        face_num = len(os.listdir(pic_path))
        if (i % fps == 0):
            s = i / fps + 1
            print("获取第" + str(s) + "秒")
            if not ret:  # 读完视频后falg返回False
                break
            results = model(frame, conf=face_detection_conf, verbose=False) # 调整人脸检测置信度
            res = results[0].boxes.xyxy.tolist()
            if len(res) != 0:
                if len(os.listdir(pic_path)) == 0:
                    for each in res:
                        x1,y1,x2,y2 = each[:4]
                        x1 = int(x1)
                        y1 = int(y1)
                        x2 = int(x2)
                        y2 = int(y2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 50, 250), 3)
                    cv2.imwrite(pic_path+f'/face{face_num}.png', frame)
                    print("New Face Detected")
                    continue
                rgb_frame = frame[:, :, ::-1]
                cv2.imwrite("temp.jpg", rgb_frame)
                rgb_frame = face_recognition.load_image_file("temp.jpg")
                os.system(f"rm temp.jpg")
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                face_is_same = False
                for pic in os.listdir(pic_path):
                    video_face = face_recognition.load_image_file(os.path.join(pic_path, pic))  # 加载待比对的人脸图片
                    video_face_encoding = face_recognition.face_encodings(video_face)
                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(video_face_encoding, face_encoding, tolerance=face_recognition_conf)# 调整人脸相似度检测置信度
                        face_distances = face_recognition.face_distance(video_face_encoding, face_encoding)
                        try:
                            best_match_index = np.argmin(face_distances)
                        except:
                            return False
                        if matches[best_match_index]:
                            face_is_same = True
                if not face_is_same:
                    for each in res:
                        x1,y1,x2,y2 = each[:4]
                        x1 = int(x1)
                        y1 = int(y1)
                        x2 = int(x2)
                        y2 = int(y2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 50, 250), 3)
                    cv2.imwrite(pic_path+f'/face{face_num}.png', frame)
                    print("New Face Detected")
        i += 1

    cap.release()
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='识别视频中出现的人脸')
    parser.add_argument("--videopath", type=str)
    parser.add_argument("--facepath", type=str)
    parser.add_argument("--face_detection_conf", type=float)
    parser.add_argument("--face_recognition_conf", type=float)

    args = parser.parse_args()

    if face_classification(args.videopath, args.facepath, args.face_detection_conf, args.face_recognition_conf):
        print("OK")
    else:
        print("Not OK")
