import gradio as gr
import os
from Request import *
from Faceswap import faceswap
from Voiceclone import voiceclone
from Lipsync import lipsync

# css = """
# body{
#     background-color: white;
#     font-family: Arial, sans-serif;
#     text-align: center;
# }
# """

os.environ['GRADIO_TEMP_DIR'] = "" # Gradio上传文件的暂存路径，可以自行配置。如想采用Gradio默认路径，注释掉本行即可

# Introduction = '''本系统实现了一站式视频换脸、语音克隆、口型拟合功能，可以通过上方选项卡在各功能间切换'''

# General = gr.Interface(title="一站式视频换脸&语音克隆系统",
#                        fn=get_request,
#                     #    fn=None,
#                        inputs=[
#                            gr.Textbox(label="系统使用说明", value=Introduction)
#                        ],
#                        outputs=None)

Faceswap = gr.Interface(title="视频换脸部分",
                        fn=faceswap,
                        inputs=[
                            gr.Checkbox(label="是否需要进行视频换脸"),
                            # gr.CheckboxGroup(["FSGAN", "IIM", "RLE"], label="视频换脸算法"),
                            gr.Dropdown(["FSGAN", "IIM", "RLE"], label="视频换脸算法"),
                            gr.Video(sources=["upload", "webcam"], label="上传视频"),
                            gr.Image(sources=["upload", "webcam"], label="上传人脸图片", type="filepath"),
                            gr.Checkbox(label="是否检测视频中出现的不同人脸"),
                            gr.Slider(0, 1, 0.87, label="人脸识别置信度"),
                            gr.Slider(0, 1, 0.4, label="人脸相似度置信度"),
                            gr.Image(sources=["upload", "webcam"], label="上传要替换的指定人脸图片", type="filepath")
                        ],
                        outputs=[
                            gr.Video(label="输出视频换脸结果"),
                            gr.File(label="识别出的不同人脸"),
                            gr.Gallery(label="合成的视频帧")
                        ])

VC = gr.Interface(title="语音克隆部分",
                  fn=voiceclone,
                  inputs=[
                      gr.Checkbox(label="是否需要进行语音克隆"),
                    #   gr.CheckboxGroup(["OSVC", "VITS", "OpenVoice"], label="语音克隆算法"),
                      gr.Dropdown(["OSVC", "VITS", "OpenVoice"], label="语音克隆算法"),
                      gr.Slider(1, 100, 100, label="VITS模型训练Epoch数"),
                      gr.Audio(sources=["upload", "microphone"], label="上传音频", type="filepath"),
                      gr.Checkbox(label="是否要进行音频扩充"),
                      gr.File(label="上传语音素材压缩包（仅限zip格式文件）"),
                      gr.Textbox(label="说话人名称（与zip文件中的文件夹名一致）"),
                      gr.Textbox(label="上传自定义文字")
                  ],
                  outputs=[
                      gr.Audio(label="输出语音克隆结果")
                  ])

Mouth = gr.Interface(title="口型拟合部分",
                  fn=lipsync,
                  inputs=[
                      gr.Checkbox(label="是否需要进行口型拟合"),
                    #   gr.CheckboxGroup(["Wav2Lip", "VideoReTalking"], label="口型拟合算法"),
                      gr.Dropdown(["Wav2Lip", "VideoReTalking"], label="口型拟合算法"),
                      gr.Checkbox(label="是否要用视频换脸、口型拟合部分产生的视频、音频作为输入"),
                      gr.Video(sources=["upload", "webcam"], label="上传视频"),
                      gr.Audio(sources=["upload", "microphone"], label="上传音频", type="filepath")
                  ],
                  outputs=[
                      gr.Video(label="输出口型拟合结果")
                  ])

app = gr.TabbedInterface([General, Faceswap, VC, Mouth], ["首页", "视频换脸", "语音克隆", "口型拟合"])
# launch函数的参数可以进行修改，具体请自行搜索Gradio用法
app.launch(inbrowser=True, ssl_verify=False, share=True)