import os
from Request import get_userpath
import json

W2L_PATH = "./Wav2Lip" # 或自定义的项目路径
VIDEORETALKING_PATH = "./video-retalking" # 或自定义的项目路径

W2L_PYTHON = "" # 根据实际情况添加
VIDEORETALKING_PYTHON = "" # 根据实际情况添加

def lipsync(check_lipsync, algorithm, check_cache=True, source_video=None, source_audio=None):
    if check_lipsync is False:
        return None
    
    userpath, uid = get_userpath()
    resultpath = os.path.join(userpath, "resultlipsync")
    if os.path.exists(resultpath) is False:
        os.mkdir(resultpath)
    resultvideo = os.path.join(resultpath, "resultvideo.mp4")
    if check_cache is True:
        source_video = os.path.join(userpath, "resultvideo", "video.mp4")
        source_audio = os.path.join(userpath, "resultaudio", "audio.wav")

    if algorithm == "Wav2Lip":
        ls_cmd = f"cd {W2L_PATH} && {W2L_PYTHON} inference.py \
            --checkpoint_path checkpoints/wav2lip_gan.pth \
            --face {source_video} \
            --audio {source_audio} \
            --outfile {resultvideo}"
    elif algorithm == "VideoReTalking":
        ls_cmd = f"cd {VIDEORETALKING_PATH} && {VIDEORETALKING_PYTHON} inference.py \
            --face {source_video} \
            --audio {source_audio} \
            --outfile {resultvideo}"
        
    os.system(ls_cmd)
    return resultvideo