#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import wx
import taiwaControl
import datetime

windowWidth = 1000
windowHeight = 1000
Senselessflag = True
textinstance = None
loginstance = None
MainWindowInstance = None

api_key = '564f5a7a34756c7a422f31644633622e6e64327169326c452f2f433045332e6c3559727351307763656a42'
chat = taiwaControl.DocomoChat(api_key)

todaydetail = datetime.datetime.today()
date = (str(todaydetail.month) + "_" + str(todaydetail.day) + "_" + str(todaydetail.hour) + "_" + str(todaydetail.minute))
fw = open("taiwalog/taiwalog_" + date + ".txt","w")
resp = chat.set_name('subject', '被験者')
uttID = 1

#---------------------------------------------------------
#	便利な関数達
#---------------------------------------------------------

def write_file(utt):
	fw.write(utt)

#---------------------------------------------------------
#	イベント管理
#---------------------------------------------------------

def click_button_1(event):
	global Senselessflag
	frame.SetStatusText("通常の発話が選択されました。")
	Senselessflag = False

def click_button_2(event):
	global Senselessflag
	frame.SetStatusText("非常識な発話が選択されました。")
	Senselessflag = True

def click_submitbutton(event):
	global resp
	global uttID
	frame.SetStatusText("送信が完了しました。")
	print ("Senselessflag : " + str(Senselessflag))
	print (textinstance.GetText())
	write_file(str(uttID) + " Senselessflag:" + str(Senselessflag) + " u:" + textinstance.GetText() + "\n")
	loginstance.setTextArray[uttID-1].SetLabel(str(uttID) + " u:" + textinstance.GetText())
	uttID += 1
	resp = chat.send_and_get(textinstance.GetText())
	write_file(str(uttID) + " s:" + resp.decode("utf-8") + "\n")
	loginstance.setTextArray[uttID-1].SetLabel(str(uttID) + " s:" + resp.decode("utf-8"))
	uttID += 1

#---------------------------------------------------------
#	トップレベルウインドウ
#---------------------------------------------------------
class MainWindow(wx.Frame):
	def __init__(self):
		
		global textinstance
		global loginstance
		wx.Frame.__init__(self,None, wx.ID_ANY, u"Docomo雑談対話",size=(windowWidth,windowHeight))
		self.CreateStatusBar()

		rootPanel = wx.Panel(self, wx.ID_ANY)
		rootPanel.SetBackgroundColour("#AFAFAF")

		log = Log(rootPanel)
		loginstance = log
		choosebuttons = ChooseButton(rootPanel) 
		textctrl = TextCtrl(rootPanel)
		textinstance = textctrl
		submitbutton = SubmitButton(rootPanel)

		rootLayout = wx.BoxSizer(wx.VERTICAL)
		rootLayout.Add(log, proportion=1)
		rootLayout.Add(textctrl, proportion=1)
		rootLayout.Add(choosebuttons, proportion=1)		
		rootLayout.Add(submitbutton, proportion=1)		

		rootPanel.SetSizer(rootLayout)
		rootLayout.Fit(rootPanel)

#---------------------------------------------------------
#	対話ログの部分
#---------------------------------------------------------
class Log(wx.Panel):

	def __init__(self, parent):

		wx.Panel.__init__(self, parent, wx.ID_ANY,pos=(0,30),size=(windowWidth,820))

		self.SetBackgroundColour("#AFAFAF")

		font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

		self.s_text_1 = wx.StaticText(self, wx.ID_ANY, str(1) + " s:" + resp.decode("utf-8"))
		self.s_text_2 = wx.StaticText(self, wx.ID_ANY, u"2")
		self.s_text_3 = wx.StaticText(self, wx.ID_ANY, u"3")
		self.s_text_4 = wx.StaticText(self, wx.ID_ANY, u"4")
		self.s_text_5 = wx.StaticText(self, wx.ID_ANY, u"5")
		self.s_text_6 = wx.StaticText(self, wx.ID_ANY, u"6")
		self.s_text_7 = wx.StaticText(self, wx.ID_ANY, u"7")
		self.s_text_8 = wx.StaticText(self, wx.ID_ANY, u"8")
		self.s_text_9 = wx.StaticText(self, wx.ID_ANY, u"9")
		self.s_text_10 = wx.StaticText(self, wx.ID_ANY, u"10")
		self.s_text_11 = wx.StaticText(self, wx.ID_ANY, u"11")
		self.s_text_12 = wx.StaticText(self, wx.ID_ANY, u"12")
		self.s_text_13 = wx.StaticText(self, wx.ID_ANY, u"13")
		self.s_text_14 = wx.StaticText(self, wx.ID_ANY, u"14")
		self.s_text_15 = wx.StaticText(self, wx.ID_ANY, u"15")
		self.s_text_16 = wx.StaticText(self, wx.ID_ANY, u"16")
		self.s_text_17 = wx.StaticText(self, wx.ID_ANY, u"17")
		self.s_text_18 = wx.StaticText(self, wx.ID_ANY, u"18")
		self.s_text_19 = wx.StaticText(self, wx.ID_ANY, u"19")
		self.s_text_20 = wx.StaticText(self, wx.ID_ANY, u"20")

		self.setTextArray = [self.s_text_1,self.s_text_2,self.s_text_3,self.s_text_4,\
		self.s_text_5,self.s_text_6,self.s_text_7,self.s_text_8,self.s_text_9,self.s_text_10,\
		self.s_text_11,self.s_text_12,self.s_text_13,self.s_text_14,self.s_text_15,self.s_text_16,\
		self.s_text_17,self.s_text_18,self.s_text_19,self.s_text_20]


		self.s_text_2.SetForegroundColour("#FF0000")
		self.s_text_4.SetForegroundColour("#FF0000")
		self.s_text_6.SetForegroundColour("#FF0000")
		self.s_text_8.SetForegroundColour("#FF0000")
		self.s_text_10.SetForegroundColour("#FF0000")
		self.s_text_12.SetForegroundColour("#FF0000")
		self.s_text_14.SetForegroundColour("#FF0000")
		self.s_text_16.SetForegroundColour("#FF0000")
		self.s_text_18.SetForegroundColour("#FF0000")
		self.s_text_20.SetForegroundColour("#FF0000")

		self.s_text_1.SetForegroundColour("#000000")
		self.s_text_3.SetForegroundColour("#000000")
		self.s_text_5.SetForegroundColour("#000000")
		self.s_text_7.SetForegroundColour("#000000")
		self.s_text_9.SetForegroundColour("#000000")
		self.s_text_11.SetForegroundColour("#000000")
		self.s_text_13.SetForegroundColour("#000000")
		self.s_text_15.SetForegroundColour("#000000")
		self.s_text_17.SetForegroundColour("#000000")
		self.s_text_19.SetForegroundColour("#000000")

		self.s_text_1.SetFont(font)
		self.s_text_2.SetFont(font)
		self.s_text_3.SetFont(font)
		self.s_text_4.SetFont(font)
		self.s_text_5.SetFont(font)
		self.s_text_6.SetFont(font)
		self.s_text_7.SetFont(font)
		self.s_text_8.SetFont(font)
		self.s_text_9.SetFont(font)
		self.s_text_10.SetFont(font)
		self.s_text_11.SetFont(font)
		self.s_text_12.SetFont(font)
		self.s_text_13.SetFont(font)
		self.s_text_14.SetFont(font)
		self.s_text_15.SetFont(font)
		self.s_text_16.SetFont(font)
		self.s_text_17.SetFont(font)
		self.s_text_18.SetFont(font)
		self.s_text_19.SetFont(font)
		self.s_text_20.SetFont(font)

		box = wx.StaticBox(self, wx.ID_ANY, "対話ログ")

		layout = wx.StaticBoxSizer(box,wx.VERTICAL)
		layout.Add(self.s_text_1, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_2, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_3, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_4, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_5, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_6, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_7, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_8, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_9, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_10, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_11, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_12, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_13, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_14, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_15, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_16, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_17, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_18, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_19, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(self.s_text_20, flag=wx.GROW| wx.BOTTOM, border = 10)

		self.SetSizer(layout)

#---------------------------------------------------------
#	ボタンの部分
#---------------------------------------------------------
class ChooseButton(wx.Panel):
	def __init__(self, parent):

		wx.Panel.__init__(self, parent, wx.ID_ANY,size=(windowWidth,50))

		self.SetBackgroundColour("#AFAFAF")

		button_1 = wx.Button(self, wx.ID_ANY, u"通常")
		button_2 = wx.Button(self, wx.ID_ANY, u"非常識")

		layout = wx.BoxSizer(wx.HORIZONTAL)
		layout.Add(button_1, proportion=1,flag = wx.ALIGN_BOTTOM | wx.BOTTOM, border = 10)
		layout.Add(button_2, proportion=1,flag = wx.ALIGN_BOTTOM | wx.BOTTOM, border = 10)
		
		button_1.Bind(wx.EVT_BUTTON, click_button_1)
		button_2.Bind(wx.EVT_BUTTON, click_button_2)

		self.SetSizer(layout)

#---------------------------------------------------------
#	入力スペースの部分
#---------------------------------------------------------
class TextCtrl(wx.Panel):
	textcolumn = ""
	def __init__(self, parent):

		wx.Panel.__init__(self, parent, wx.ID_ANY,size=(windowWidth,50))

		self.SetBackgroundColour("#AFAFAF")

		self.textcolumn = wx.TextCtrl(self, wx.ID_ANY,u"ここに入力してください")

		layout = wx.BoxSizer(wx.HORIZONTAL)
		layout.Add(self.textcolumn, proportion=1,flag = wx.ALIGN_BOTTOM | wx.ALL, border = 10)
		self.SetSizer(layout)

	def GetText(self):
		return self.textcolumn.GetValue()

#---------------------------------------------------------
#	ボタンの部分
#---------------------------------------------------------
class SubmitButton(wx.Panel):
	def __init__(self, parent):

		wx.Panel.__init__(self, parent, wx.ID_ANY,size=(windowWidth,50))

		self.SetBackgroundColour("#AFAFAF")

		button = wx.Button(self, wx.ID_ANY, u"送信")

		button.Bind(wx.EVT_BUTTON, click_submitbutton)

		layout = wx.BoxSizer(wx.HORIZONTAL)
		layout.Add(button, proportion=1,flag = wx.ALIGN_BOTTOM | wx.ALL, border = 10)
		self.SetSizer(layout)


#---------------------------------------------------------
#	main
#---------------------------------------------------------

write_file(str(uttID) + " s:" + resp.decode("utf-8") + "\n")
uttID += 1
application = wx.App()
frame = MainWindow()
frame.Show()
application.MainLoop()
