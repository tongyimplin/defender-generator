from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import os
import time
from generator_core import GeneratorCore

FRAME_WIDTH = 600
FRAME_HEIGHT = 400
USER_HOME = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + "/defender-generator"

if (os.path.exists(USER_HOME) == False):
    os.mkdir(USER_HOME)

CONFIG_FILE = USER_HOME + "/config.conf"
CONFIG_CONTENT = {'path': '', 'totalCount': '5', 'idcardTpl': '11003319900303****', 'ip': '', 'port': '', 'user': '',
                  'pass': '', 'targetPath': ''}


# 读取配置文件
def read_config_file():
    global CONFIG_CONTENT
    fo = open(CONFIG_FILE, 'r')
    content = fo.readline()
    if (str(content) != ''):
        CONFIG_CONTENT = eval(content)
    print("读取到配置: " + content)
    fo.close()


# 写入配置文件
def write_config_file():
    fo = open(CONFIG_FILE, 'w')
    print("保存配置: " + str(CONFIG_CONTENT))
    fo.write(str(CONFIG_CONTENT))
    fo.close()


if (os.path.exists(CONFIG_FILE) == False):
    write_config_file()

# 加载配置
read_config_file()


class MainFrame(Frame):
    font = ("微软雅黑", 10)
    frameGroupGap = 20
    frameGroupHeight = 30
    labelWidth = 80
    inputStartX = 110
    inputWidth = 300
    nextFrameGroupY = 0
    formFrame = None

    # 组件
    wFilePath = None
    wIdcard = None
    wTotalCount = None

    def __init__(self, master=None):
        super().__init__(master)
        # 增加button
        fm1 = Frame(master)
        # 标题
        Label(fm1, text="档板造数工具", justify=CENTER, font=('微软雅黑', 18)) \
            .place(relx=0, rely=0, width=500, height=30)
        fm1.place(width=500, height=300, x=50, y=20)

        # 表单
        self.formFrame = Frame(master)
        self.createFormControlGroup()
        self.formFrame.place(width=500, height=300, x=50, y=90)

        self.place(width=FRAME_WIDTH, height=FRAME_HEIGHT)

    def _nextLine(self):
        self.nextFrameGroupY = self.nextFrameGroupY + self.frameGroupGap + self.frameGroupHeight

    def _newLabel(self, labelName, y):
        Label(self.formFrame, text=labelName, justify=LEFT, font=self.font) \
            .place(x=0, y=y, width=self.labelWidth, height=self.frameGroupHeight)

    def _newInput(self, y, textvariable="", width=300):
        entry = Entry(self.formFrame, width=width, textvariable=textvariable)
        entry.place(x=self.inputStartX, y=y, width=width, height=self.frameGroupHeight)
        return entry

    def _newButton(self, width, height, x, y, text, command):
        btn = Button(self.formFrame, width=width, height=height, text=text, command=command)
        btn.place(x=x, y=y, width=width, height=height)
        return btn

    def evtFileChooseHandler(self):
        print("开始选择文件...")
        path = tkinter.filedialog.askdirectory(initialdir=CONFIG_CONTENT['path'])
        if (str(path) != ''):
            self._setInputContent(self.wFilePath, path)
            print("您选择的路径是: %s" % path)
            CONFIG_CONTENT['path'] = path
            write_config_file()

    def evtUploadToServerHandler(self):
        tkinter.messagebox.showinfo('提示', '开发中...')

    def _setInputContent(self, input, c=""):
        input.delete(0, END)
        input.insert(0, c)

    def _writeLogs(self, content):
        str = "["+time.strftime('%H:%M:%S', time.localtime())+"] "+content+'\r\n'
        self.wConsole.insert(END, str)
        self.wConsole.see(END)
        self.wConsole.focus_set()


    def evtStartWork(self):
        generator = GeneratorCore(CONFIG_CONTENT['path']
                      , CONFIG_CONTENT['idcardTpl'], CONFIG_CONTENT['totalCount']
                      , os.path.dirname(CONFIG_CONTENT['path'])+"/target")
        zipFile = generator.start_work()
        p = os.path.dirname(zipFile)
        os.startfile(p)

    def createFormControlGroup(self):
        print(CONFIG_CONTENT)
        # 文件位置
        self._newLabel("文件位置：", self.nextFrameGroupY)
        self.wFilePath = self._newInput(self.nextFrameGroupY, CONFIG_CONTENT['path'], 240)
        self._newButton(50, 30, 360, self.nextFrameGroupY, "选择", self.evtFileChooseHandler)
        self._nextLine()
        # 身份证号码
        self._newLabel("身份证模板：", self.nextFrameGroupY)
        self.wIdcard = self._newInput(self.nextFrameGroupY, CONFIG_CONTENT['idcardTpl'])
        self._nextLine()
        # 生成的数量
        self._newLabel("生成数量：", self.nextFrameGroupY)
        self.wTotalCount = self._newInput(self.nextFrameGroupY, CONFIG_CONTENT['totalCount'])
        self._nextLine()
        # 按钮
        self._newButton(80, 30, 100, self.nextFrameGroupY, "生成数据", self.evtStartWork)
        self._newButton(80, 30, 240, self.nextFrameGroupY, "上传至服务器", self.evtUploadToServerHandler)
        self._nextLine()
        # # 创建一个text
        # fm = Frame(self.formFrame, width=500, height=200)
        # fm.place(x=0, y=self.nextFrameGroupY)
        # self.wConsole = Text(fm)
        # self.wScroll = Scrollbar(fm)
        # self.wScroll.pack(side=RIGHT, fill=Y)
        # self.wConsole.pack(side=LEFT, fill=Y)
        #
        # self.wScroll.config(command=self.wConsole.yview)
        # self.wConsole.config(yscrollcommand=self.wScroll.set)


        # 初始化信息
        self._setInputContent(self.wFilePath, CONFIG_CONTENT['path'])
        self._setInputContent(self.wIdcard, CONFIG_CONTENT['idcardTpl'])
        self._setInputContent(self.wTotalCount, CONFIG_CONTENT['totalCount'])


frame = MainFrame()
frame.master.title("档板造数工具")
frame.master.minsize(FRAME_WIDTH, FRAME_HEIGHT)

# 获取屏幕宽高, 屏幕居中
scnWidth, scnHeight = frame.master.maxsize()
frame.master.geometry('%dx%d+%d+%d' % (FRAME_WIDTH, FRAME_HEIGHT, (scnWidth-FRAME_WIDTH)/2, (scnHeight-FRAME_HEIGHT)/2))

frame.mainloop()
