import os
from Request import get_userpath
import json

SIMSWAP_PATH = "./SimSwap" # 或自定义的项目路径
IIM_PATH = "./Thin-Plate-Spline-Motion-Model" # 或自定义的项目路径

YOLO_PYTHON = "" # 根据实际情况添加
APP_PYTHON = "" # 根据实际情况添加

def faceswap(check_faceswap, algorithm, source_video, source_image, check_multifaces=False, face_detection_conf=0.87, face_recognition_conf=0.4, special_face=None):
    if check_faceswap == False and check_multifaces == False:
        return [None, None, None]
    userpath, uid = get_userpath()
    facepath = os.path.join(userpath, "faces")
    if os.path.exists(facepath) is False:
        os.mkdir(facepath)
    if check_multifaces == True:
        facedetetion_cmd = f"{YOLO_PYTHON} ./face_detection/face_detection.py \
            --videopath {source_video} --facepath {facepath} \
            --face_detection_conf {face_detection_conf} --face_recognition_conf {face_recognition_conf}"
        os.system(facedetetion_cmd)
        zipfile = os.path.join(userpath, "detected_faces.zip")
        if os.path.exists(zipfile):
            os.system(f"rm {zipfile}")
        os.system(f"cd {userpath} && zip -r -j detected_faces.zip faces")
        return [None, zipfile, None]

    resultpath = os.path.join(userpath, "resultvideo")
    if os.path.exists(resultpath) is False:
        os.mkdir(resultpath)
    temppath = os.path.join(userpath, "temp")
    if os.path.exists(temppath) is False:
        os.mkdir(temppath)
    videopath = os.path.join(resultpath, "video.mp4")
    if check_faceswap is True:
        if special_face is None:
            if algorithm == "FSGAN":
                faceswap_cmd = f"cd {SIMSWAP_PATH} && {APP_PYTHON} test_video_swapsingle.py --crop_size 224 --use_mask \
                    --name people --Arc_path arcface_model/arcface_checkpoint.tar \
                    --pic_a_path {source_image} --video_path {source_video} \
                    --output_path {videopath} --temp_path {temppath}" # 在videoswap.py中修改保存视频名称
            elif algorithm == "IIM":
                faceswap_cmd = f"cd {IIM_PATH} && {APP_PYTHON} demo.py \
                    --config config/vox-256.yaml \
                    --checkpoint checkpoints/vox.pth.tar  \
                    --source_image {source_image} --driving_video {source_video} \
                    --result_video {videopath}"
            elif algorithm == "RLE":
                faceswap_cmd = f"cd {SIMSWAP_PATH} && {APP_PYTHON} test_video_swapsingle.py --crop_size 224 --use_mask \
                    --name people --Arc_path arcface_model/arcface_checkpoint.tar \
                    --pic_a_path {source_image} --video_path {source_video} \
                    --output_path {videopath} --temp_path {temppath}"
            os.system(faceswap_cmd)
        else:
            if algorithm == "FSGAN":
                faceswap_cmd = f"cd {SIMSWAP_PATH} && {APP_PYTHON} test_video_swapspecific.py --crop_size 224 --use_mask \
                    --name people --Arc_path arcface_model/arcface_checkpoint.tar \
                    --pic_a_path {source_image} --video_path {source_video} \
                    --output_path {videopath} --temp_path {temppath} --pic_specific_path {special_face}" 
            elif algorithm == "IIM":
                faceswap_cmd = None
            elif algorithm == "RLE":
                faceswap_cmd = f"cd {SIMSWAP_PATH} && {APP_PYTHON} test_video_swapspecific.py --crop_size 224 --use_mask \
                    --name people --Arc_path arcface_model/arcface_checkpoint.tar \
                    --pic_a_path {source_image} --video_path {source_video} \
                    --output_path {videopath} --temp_path {temppath} --pic_specific_path {special_face}"
            os.system(faceswap_cmd)
        
        # with open("videos.json", "w") as f:
        #     json.dump({uid: resultpath}, f)
        piclist = []
        for root,dirs,files in os.walk(temppath):
            for file in files:
                piclist.append(os.path.join(temppath, file))
        return [videopath, None, piclist]
