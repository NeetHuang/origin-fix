# -*- coding: UTF-8 -*-
import _tkinter
import tkinter
import tkinter.messagebox as tkmessagebox#访问标准Tk对话框。
import tkinter.filedialog as tkfiledialog#通用对话框，允许用户指定要打开或保存的文件。
import shutil,re,os,winreg,base64
from icon import img

def fix_origin():
	env_dist = os.environ
	origin = env_dist.get('Appdata')  # 获取本地appdata路径
	Roaming_origin1 = origin + '\Origin'
	local_origin2 = origin[0:-7] + 'Local\Origin'
	if os.path.exists(local_origin2):
		os.system('taskkill /IM Origin.exe /F')
		os.system('taskkill /IM OriginWebHelperService.exe /F')
		os.system('taskkill /IM QtWebEngineProcess.exe /F')
		shutil.rmtree(local_origin2) ####优先删除这个尝试#####
		tkmessagebox.showinfo(title='成功',message='修复完成')
	else:
		tkmessagebox.showinfo(title='警告',message='目录未找到或已清理')
	# if os.path.exists(Roaming_origin1):
	#     os.removedirs(Roaming_origin1)

def origin_akamai():
	aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
	get_key = winreg.OpenKey(aReg, r'SOFTWARE\WOW6432Node\Electronic Arts\EA Core')  # 获取origin的注册表
	origin_path = winreg.QueryValueEx(get_key, 'EADM6InstallDir')[0]  # 获取origin的注册表数据
	EACore=origin_path+"\origin_path"
	text='''[connection]
		EnviromentName=production
		[Feature]
		CdnOverride=akamai
		'''
	with open(EACore, 'w+') as EA:
		EA.write(text)


	hosts = ['219.76.10.192 origin-a.akamaihd.net', '104.76.93.69  www.origin.com']
	if os.path.isfile('C:/Windows/System32/drivers/etc/hosts'):
		with open(r'C:/Windows/System32/drivers/etc/hosts', 'r+') as hos:
			if re.search(r"akamai",hos.read()):
				tkmessagebox.showinfo(title='警告',message='已存在加速优化')
			else:
				shutil.copy(r'C:/Windows/System32/drivers/etc/hosts','C:/Windows/System32/drivers/etc/hosts.back')
				for host in hosts:
				# print(host)
					hos.write("\n"+host+"\n")
				tkmessagebox.showinfo(title='成功',message='加速优化完毕')
	else:
		with open(r'C:/Windows/System32/drivers/etc/hosts', 'a') as hos:
			for host in hosts:
			# print(host)
				hos.write("\n"+host+"\n")

def file_path():
	path_ = tkfiledialog.askdirectory(initialdir='C:/')
	print(path_)
	tkinter.Label(text="你的安装位置-"+path_).place(x=30,y=130,anchor='w')
	path = path_
	game_path = '"'+path_+'/__Installer/Touchup.exe"'
	command_s = game_path+' install -locale {zh_TW} -installPath "{%s}" -autologging -startmenuIcon=1 -desktopIcon=1' %path
	print(command_s)
	if os.path.isfile(game_path):
		try:
			command_fix = os.system(command_s)
			tkmessagebox.showinfo(title='成功',message='修复完成')
		except:
			tkmessagebox.showinfo(title='失败',message="请检查权限或者文件是否缺失")
def main():
	root = tkinter.Tk()
	fm1 = tkinter.Frame()
	label = tkinter.Label(text='origin多功能修复工具',height=2,width=20)
	label.pack(side='top')
	fm1.pack()

	fm2 = tkinter.Frame()
	LabelA=tkinter.Label(text='修复origin发生了一些问题')
	A = tkinter.Button(text ="修复", command = fix_origin,height=1,width = 10)
	LabelA.place(x=30,y=60,anchor='w')
	A.place(x=200,y=60,anchor='w')

	LabelB =tkinter.Label(text='origin加速')
	B = tkinter.Button(text ="加速", command = origin_akamai,height=1,width = 10)
	LabelB.place(x=30,y=100,anchor='w')
	B.place(x=200,y=100,anchor='w')

	LabelC=tkinter.Label(text='游戏位置修改后修复')
	C = tkinter.Button(text ="选择游戏目录", command = file_path,height=1,width = 15)
	LabelC.place(x=30,y=160,anchor='w')
	C.place(x=180,y=160,anchor='w')
	fm2.pack()


	root.title('origin多功能修复工具')#标题
	root.geometry('300x200')#窗体大小
	root.resizable(False, False)#固定窗体
	tmp = open("tmp.ico","wb+")
	tmp.write(base64.b64decode(img))
	tmp.close()
	root.iconbitmap("tmp.ico")
	os.remove("tmp.ico")
	root.mainloop()

if __name__ == '__main__':
	main()
