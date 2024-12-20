import os
import gradio as gr
import shortuuid
import json

databasepath = "" # 数据库路径，自定义即可，建议数据库放在服务器或PC剩余空间较大的盘
uid = shortuuid.ShortUUID().random(5)
# global userpath

def get_request(text, username, request: gr.Request):
    cookie = request.headers['cookie']
    gid = cookie.split(";")[1].replace("_gid=", "").replace(".", "_").replace(" ", "")
    userpath = os.path.join(databasepath, username+"_"+gid)
    with open("./users.json", "w") as f:
        json.dump({uid: userpath}, f)
    if os.path.exists(os.path.join(databasepath, userpath)) is False:
        os.mkdir(userpath)
    return f"欢迎您，用户{username}"

def get_userpath():
    with open("./users.json", "r") as f:
        users = json.load(f)
    userpath = users[uid]
    # print(userpath, "from get_userpath")
    return userpath, uid

Introduction = '''本系统实现了一站式视频换脸、语音克隆、口型拟合功能，可以通过上方选项卡在各功能间切换'''

General = gr.Interface(title="一站式视频换脸&语音克隆系统",
                       fn=get_request,
                    #    fn=None,
                       inputs=[
                           gr.Textbox(label="系统使用说明", value=Introduction),
                           gr.Textbox(label="用户自定义名称")
                       ],
                       outputs=[
                           gr.Textbox(label="欢迎您")
                       ])