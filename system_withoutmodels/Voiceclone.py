import os
from Request import get_userpath
import json

OSVC_PATH = "./One-Shot-Voice-Cloning" # 或自定义的项目路径
VITS_PATH = "./VITS-fast-fine-tuning" # 或自定义的项目路径
OPENVOICE_PATH = "./OpenVoice" # 或自定义的项目路径

OSVC_PYTHON = "" # 根据实际情况添加
VITS_PYTHON = "" # 根据实际情况添加
OPENVOICE_PYTHON = "" # 根据实际情况添加

def voiceclone(check_voiceclone, algorithm, epochnum, source_audio, check_expasion, source_zip, speakername, text):
    if check_voiceclone is False:
        return None
    
    userpath, username = get_userpath()
    resultpath = os.path.join(userpath, "resultaudio")
    if os.path.exists(resultpath) is False:
        os.mkdir(resultpath)

    if algorithm == "OSVC":
        punclist = ["，", "。", "、", "！", "？", "："]
        for punc in punclist:
            if text.find(punc) > 0:
                text = text.replace(punc, "#3")
        vc_cmd = f"cd {OSVC_PATH} && \
            {OSVC_PYTHON} UnetTTS_syn.py --audio {source_audio} --text {text} --output_dir {resultpath}"
        os.system(vc_cmd)
        
    elif algorithm == "VITS":
        uploadpath = os.path.join(userpath, "custom_character_voice/")
        if source_audio is not None and source_zip is None:
            for i in range(15):
                os.system(f"cp {source_audio} {uploadpath}/speaker/audio{i}.wav")
        get_audio_cmd = f"unzip {source_zip} -d {uploadpath}"
        os.system(get_audio_cmd)
        # if check_expasion: # TODO: check
        #     for root,dirs,files in os.walk(uploadpath):
        #         expnum = int(10/len(files)) + 1
        #         for num in range(expnum):

        vc_cmd = f"cd {VITS_PATH} && {VITS_PYTHON} scripts/denoise_audio.py && \
            {VITS_PYTHON} scripts/short_audio_transcribe.py --languages C --whisper_size large --audio_dir {uploadpath} && \
            {VITS_PYTHON} scripts/resample.py && \
            {VITS_PYTHON} preprocess_v2.py --languages C && \
            {VITS_PYTHON} finetune_speaker_v2.py -m OUTPUT_MODEL --max_epochs {epochnum} --drop_speaker_embed True"
        os.system(vc_cmd)
        produce_audio_cmd = f"{VITS_PYTHON} cmd_inference.py -m OUTPUT_MODEL/G_latest.pth -c configs/modified_finetune_speaker.json \
            -o {resultpath} -t {text} -s {speakername}"
        os.system(produce_audio_cmd)
        
    elif algorithm == "OpenVoice": 
        vc_cmd = f"cd {OPENVOICE_PATH} && \
            {OPENVOICE_PYTHON} main.py --audio {source_audio} --text {text} --output_dir {resultpath}"
        os.system(vc_cmd)

    audiopath = os.path.join(resultpath, "audio.wav")
    # with open("audios.json", "w") as f:
    #     json.dump({uid: audiopath})

    return audiopath
