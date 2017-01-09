#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
windowWidth = 1000
windowHeight = 1000
Senselessflag = True
textinstance = None

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
	frame.SetStatusText("送信が完了しました。")
	print ("Senselessflag : " + str(Senselessflag))
	print (textinstance.GetText())

#---------------------------------------------------------
#	トップレベルウインドウ
#---------------------------------------------------------
class MainWindow(wx.Frame):

	def __init__(self):
		global textinstance
		wx.Frame.__init__(self,None, wx.ID_ANY, u"Docomo雑談対話",size=(windowWidth,windowHeight))
		self.CreateStatusBar()

		rootPanel = wx.Panel(self, wx.ID_ANY)
		rootPanel.SetBackgroundColour("#AFAFAF")

		log = Log(rootPanel)
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

		s_text_1 = wx.StaticText(self, wx.ID_ANY, u"1")
		s_text_2 = wx.StaticText(self, wx.ID_ANY, u"2")
		s_text_3 = wx.StaticText(self, wx.ID_ANY, u"3")
		s_text_4 = wx.StaticText(self, wx.ID_ANY, u"4")
		s_text_5 = wx.StaticText(self, wx.ID_ANY, u"5")
		s_text_6 = wx.StaticText(self, wx.ID_ANY, u"6")
		s_text_7 = wx.StaticText(self, wx.ID_ANY, u"7")
		s_text_8 = wx.StaticText(self, wx.ID_ANY, u"8")
		s_text_9 = wx.StaticText(self, wx.ID_ANY, u"9")
		s_text_10 = wx.StaticText(self, wx.ID_ANY, u"10")
		s_text_11 = wx.StaticText(self, wx.ID_ANY, u"11")
		s_text_12 = wx.StaticText(self, wx.ID_ANY, u"12")
		s_text_13 = wx.StaticText(self, wx.ID_ANY, u"13")
		s_text_14 = wx.StaticText(self, wx.ID_ANY, u"14")
		s_text_15 = wx.StaticText(self, wx.ID_ANY, u"15")
		s_text_16 = wx.StaticText(self, wx.ID_ANY, u"16")
		s_text_17 = wx.StaticText(self, wx.ID_ANY, u"17")
		s_text_18 = wx.StaticText(self, wx.ID_ANY, u"18")
		s_text_19 = wx.StaticText(self, wx.ID_ANY, u"19")
		s_text_20 = wx.StaticText(self, wx.ID_ANY, u"20")

		s_text_2.SetForegroundColour("#FF0000")
		s_text_4.SetForegroundColour("#FF0000")
		s_text_6.SetForegroundColour("#FF0000")
		s_text_8.SetForegroundColour("#FF0000")
		s_text_10.SetForegroundColour("#FF0000")
		s_text_12.SetForegroundColour("#FF0000")
		s_text_14.SetForegroundColour("#FF0000")
		s_text_16.SetForegroundColour("#FF0000")
		s_text_18.SetForegroundColour("#FF0000")
		s_text_20.SetForegroundColour("#FF0000")

		s_text_1.SetForegroundColour("#000000")
		s_text_3.SetForegroundColour("#000000")
		s_text_5.SetForegroundColour("#000000")
		s_text_7.SetForegroundColour("#000000")
		s_text_9.SetForegroundColour("#000000")
		s_text_11.SetForegroundColour("#000000")
		s_text_13.SetForegroundColour("#000000")
		s_text_15.SetForegroundColour("#000000")
		s_text_17.SetForegroundColour("#000000")
		s_text_19.SetForegroundColour("#000000")

		s_text_1.SetFont(font)
		s_text_2.SetFont(font)
		s_text_3.SetFont(font)
		s_text_4.SetFont(font)
		s_text_5.SetFont(font)
		s_text_6.SetFont(font)
		s_text_7.SetFont(font)
		s_text_8.SetFont(font)
		s_text_9.SetFont(font)
		s_text_10.SetFont(font)
		s_text_11.SetFont(font)
		s_text_12.SetFont(font)
		s_text_13.SetFont(font)
		s_text_14.SetFont(font)
		s_text_15.SetFont(font)
		s_text_16.SetFont(font)
		s_text_17.SetFont(font)
		s_text_18.SetFont(font)
		s_text_19.SetFont(font)
		s_text_20.SetFont(font)

		box = wx.StaticBox(self, wx.ID_ANY, "対話ログ")

		layout = wx.StaticBoxSizer(box,wx.VERTICAL)
		layout.Add(s_text_1, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_2, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_3, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_4, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_5, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_6, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_7, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_8, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_9, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_10, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_11, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_12, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_13, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_14, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_15, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_16, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_17, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_18, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_19, flag=wx.GROW| wx.BOTTOM, border = 10)
		layout.Add(s_text_20, flag=wx.GROW| wx.BOTTOM, border = 10)

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

application = wx.App()
frame = MainWindow()
frame.Show()
application.MainLoop()
