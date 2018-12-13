from tkinter import *

FRAME_WIDTH = 600
FRAME_HEIGHT = 400

class MainFrame(Frame):
    nextFrameGroupY = 0
    frameGroupGap = 20
    frameGroupHeight = 30
    font = ("微软雅黑", 10)
    def __init__(self, master=None):
        super().__init__(master)
        # 增加button
        fm1 = Frame(master)
        # 标题
        Label(fm1, text="我是标题", justify=CENTER, font=('微软雅黑', 18))\
            .place(relx=0, rely=0, width=500, height=30)
        fm1.place(width=500, height=300, x=50, y=20)

        # 表单
        fm2 = Frame(master)
        self.createFormControlGroup(fm2, "文件位置: ")
        fm2.place(width=500, height=300, x=50, y=90)

        self.place(width=FRAME_WIDTH, height=FRAME_HEIGHT)

    def  createFormControlGroup(self, fm, labelName):
        Label(fm, text=labelName, justify=LEFT, font=self.font)\
            .place(relx=0, rely=self.nextFrameGroupY, width=80, height=self.frameGroupHeight)
        Text(fm, width=300, height=20).place(relx=110, rely=self.nextFrameGroupY)
        self.nextFrameGroupY = self.nextFrameGroupY+self.frameGroupHeight+self.frameGroupGap


frame = MainFrame()
frame.master.title("挡板服务器-人行征信造数器")
frame.master.minsize(FRAME_WIDTH, FRAME_HEIGHT)

frame.mainloop()
