## 一站式视频换脸、语音克隆、口型拟合系统

本系统实现了一站式视频换脸、语音克隆、口型拟合功能，用户可以根据自己的需要进行视频换脸。

本文件夹包含纯代码版系统（system_withoutmodels）和代码+项目+模型版系统（system_withmodels），可以根据自己的需要解压获得系统文件。系统使用请参考对应文件夹内的README。

在系统实现中，视频换脸部分使用[SimSwap](https://github.com/neuralchen/SimSwap)和[Thin-Plate-Spline-Motion-Model](https://github.com/yoyo-nb/Thin-Plate-Spline-Motion-Model)算法，语音克隆部分使用[One-Shot-Voice-Cloning](https://github.com/CMsmartvoice/One-Shot-Voice-Cloning)、[VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning)和[OpenVoice](https://github.com/myshell-ai/OpenVoice)算法，口型拟合部分使用[Wav2Lip](https://github.com/Rudrabha/Wav2Lip)和[video-retalking](https://github.com/OpenTalker/video-retalking)算法。

后续开发人员如果想要对各部分增加/删除算法，可以通过以下步骤完成：

1. 将算法对应的GitHub项目放在系统文件夹中；
2. 修改Gradio前端代码，main.py中在对应的部分删除旧算法/添加新算法，Faceswap.py/Voiceclone.py/Lipsync.py中在对应位置添加算法启动的终端命令字符串，通过os.system()函数在终端运行；
3. 建议增加算法后更新Result文件夹内的实验结果，以便后续研究人员进行改进与优化。
