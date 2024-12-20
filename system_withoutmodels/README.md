## FaceSwap&VoiceClone&LipSync System

### 一站式视频换脸、语音克隆、口型拟合系统

#### 0. 系统概述

本系统主要包括前端、视频换脸、语音克隆和口型拟语音克隆和口型语音克隆和口型拟合四个部分，文件结构如下：

```plaintext
.
├── environments
├── face_detection
├── One-Shot-Voice-Cloning
├── OpenVoice
├── SimSwap
├── Thin-Plate-Spline-Motion-Model
├── video-retalking
├── VITS-fast-fine-tuning
├── Wav2Lip
├── Faceswap.py
├── Lipsync.py
├── Request.py
├── Voiceclone.py
├── main.py
├── install_models.sh
└── install_projects.sh
```

其中**environments**是环境配置文件夹，**One-Shot-Voice-Cloning**到**Wav2Lip**是GitHub的克隆项目，**Faceswap.py**到**main.py**是系统代码，**install_models.sh**和**install_projects.sh**模型安装脚本。

由于本系统所需要的部分模型、代码及代码运行需要访问国外网站，此处默认用户系统可以连接GitHub、HuggingFace以及Gradio相关网址。如无法访问，部分代码和模型可以通过网盘进行下载。

#### 1. 环境搭建

本系统的后端代码主要包括视频换脸、语音克隆、口型拟合以及前端代码四个部分，与之相配的需要建立8个不同的虚拟conda环境。环境文件已经配置在**environments**文件夹中，只需要对文件夹中的每个文件运行下方命令即可创建对应虚拟环境：

```bash
conda env create -f (文件名称).yaml
```

#### 2. 系统代码及模型下载

系统代码中前端代码部分已经配置在项目中，而GitHub克隆项目部分需要在GitHub上面下载，可以通过运行以下脚本安装：

```bash
bash install_projects.sh
```

系统实现所需要的预训练模型中的部分可以通过脚本进行安装（VITS-fast-fine-tuning的三个预训练模型只能选择一组下载）：

```bash
bash install_models.sh
```

但如Thin-Plate-Spline-Motion-Model、Wav2Lip等项目的模型，需要用户手动下载，下载链接如下：

[Thin-Spline-Motion-Model](https://pan.baidu.com/s/1hzMWftcY6DIxOsi-WeZOKA?pwd=5xn8 "百度网盘网址")：https://pan.baidu.com/s/1hzMWftcY6DIxOsi-WeZOKA?pwd=5xn8

下载完解压后得到四个模型，安装在**Thin-Plate-Spline-Motion-Model/checkpoints**文件夹下即可；

Wav2Lip：（如Wav2Lip项目的README.md中所示）

|            Model            |                      Description                      |                                                                  国外网盘网址                                                                  |                               国内网盘网址                               |
| :--------------------------: | :---------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------: |
|           Wav2Lip           |               Highly accurate lip-sync               | [Link](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/Eb3LEzbfuKlJiR600lQWRxgBIY27JZg80f7V9jtMfbNDaQ?e=TBFBVW) | [Link](https://pan.baidu.com/s/1iJy32nCR9Zp-WyH1hle-Lg?pwd=7q8z "百度网盘网址") |
|        Wav2Lip + GAN        | Slightly inferior lip-sync, but better visual quality | [Link](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA?e=n9ljGW) |                                   同上                                   |
|     Expert Discriminator     |          Weights of the expert discriminator          | [Link](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/EQRvmiZg-HRAjvI6zqN9eTEBP74KefynCwPWVmF57l-AYA?e=ZRPHKP) |                                   同上                                   |
| Visual Quality Discriminator |   Weights of the visual disc trained in a GAN setup   | [Link](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/EQVqH88dTm1HjlK11eNba5gBbn15WMS0B0EZbDBttqrqkg?e=ic0ljo) |                                   同上                                   |

上述模型下载完解压后，放在**Wav2Lip/checkpoints**文件夹下或直接替换该文件夹即可。

#### 3. 前端代码路径修改

前端代码（**Faceswap.py**、**Lipsync.py**、**Voiceclone.py**、**Request.py**和**main.py**）均需要根据配置路径对代码进行修改。具体参见代码注释。主要需要修改各环境的Python路径、项目文件所在路径以及数据库所在路径等。

其中Python路径可以在进入对应conda虚拟环境后在命令行输入以下命令查看（Windows系统路径记得加反斜杠）：

```bash
# Linux/MacOS
which python
# Windows
where python
```

#### 4. 系统运行

配置好上述所有步骤后即可运行系统。如仍有部分报错，请检查上述步骤是否全部完成，或有部分错误自行修改即可。

可以通过执行如下命令运行系统：

```bash
cd (本项目所在路径)
conda activate system
python main.py
```

Gradio会产生两个网址，其中http://127.0.0.1:7860为本地网址，可以离线运行；另外一个生成的含有哈希值的网址为公用网址，可以分享给其他非本机用户访问，是否生成公共链接可以在**main.py**中进行修改。
