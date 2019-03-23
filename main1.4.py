
# -----------------------------------------------------------------------------
# 用于微信群消息的存储
# -----------------------------------------------------------------------------


import sys
import itchat
#import queue as Queue
#from collections import deque
import os
import time
from itchat.content import *
# from mysqlconnector import MySqlConnector
import time
import itchat.storage.messagequeue
import importlib
import sys
importlib.reload(sys)
# from appium import webdriver
# queue = deque()
@itchat.msg_register([TEXT], isGroupChat=True)
def handle_group_text_msg(msg):

    group_name = get_group_name(msg)  # 群名称
#    msg_type = '文本'  # 消息内容
    content = msg['Content']  # 聊天内容
    actual_nick_name = msg['ActualNickName']  # 群里发消息的人
    create_time = timestamp_to_fromat(msg['CreateTime'])  # 消息是timestamp格式，转化为2019/02/23 22:53:05格式
    print(group_name, create_time, actual_nick_name, ':', content, sep=' ')
    L = [create_time, group_name, actual_nick_name, content]
    savepath = r'D:/itchat/'+str(group_name)  # 文件路径
    # 看文件路径存在与否创建相应文件夹
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    file_handle = open(savepath + r'/message.txt', mode='a+', encoding='utf-8')  # 打开该路径
    file_handle.write(str(L) + '\r\n')  # 写入数据
    file_handle.close()  # 关闭保存
    # 图片和文件消息，下面统一为ATTACHMENT
@itchat.msg_register([PICTURE, ATTACHMENT,RECORDING,VIDEO], isGroupChat=True)
def handle_group_attachment_files(msg):

    group_name = get_group_name(msg)  # 群名称
    savepath = r'D:/itchat/' + str(group_name)
    if os.path.exists(savepath):
        path = savepath + r'/ATTACHMENT'     # ATTACHMENT保存的路径
        if not os.path.exists(path):
         os.makedirs(path)
    else:
        path = savepath + r'/ATTACHMENT'
        os.makedirs(path)
    if msg['MsgType'] == 3 or msg['MsgType'] == 47:        # picture
        purl = str(time.time()) + '.png' if msg['MsgType'] == 3 else str(time.time()) + '.gif'
        url = os.path.join(path, purl)
        # print(queue)
    else:
        if msg['MsgType'] == 34:                           # voice
            purl = str(time.time()) + '.mp3'
            url = os.path.join(path, purl)
        else:
            url = os.path.join(path, msg['FileName'])         # others
    msg.download(url)
    content = url  # 聊天内容
    actual_nick_name = msg['ActualNickName']  # 群里发消息的人
    create_time = timestamp_to_fromat(msg['CreateTime'])  # 消息是timestamp格式，转化为2019/02/23 22:53:05格式
    print(group_name, create_time, actual_nick_name, ':', content, sep=' ')
    L = [create_time, group_name, actual_nick_name, content]
    file_handle = open(savepath + '/message.txt', mode='a+', encoding='utf-8')
    file_handle.write(str(L) + '\r\n')
    file_handle.close()

def get_group_name(group_msg):
    nick_name = group_msg['User'].get('NickName')
    if nick_name and nick_name != '':
        return nick_name
    if group_msg['FromUserName'] == myUserName: # 如果是自己发送的消息
        chatroom_id = group_msg['ToUserName']
    else:
        chatroom_id = group_msg['FromUserName']
    itchat.get_chatrooms(update=True) # 更新群
    memberList = itchat.search_chatrooms(userName=chatroom_id)  # 返回memberList
    nameList =[]
    # 取前10个的NickName作为群名
    for member in memberList['MemberList']:
        if len(nameList) >= 10:
            break
        nameList.append(member['NickName'])
    return ','.join(nameList)

# 格式化事时间f
def timestamp_to_fromat(timestamp = None, format = '%Y/%m/%d %H:%M:%S'):
    if timestamp:
        time_tuple = time.localtime(timestamp)
        res = time.strftime(format, time_tuple)
    else:
        res = time.strftime(format)
    return res

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    myUserName = itchat.get_friends(update=True)[0]["UserName"] # 获取自己的UserName
    itchat.run()
