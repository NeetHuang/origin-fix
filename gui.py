# -*- coding: UTF-8 -*-
import _tkinter
import tkinter
import tkinter.messagebox as tkmessagebox#访问标准Tk对话框。
import tkinter.filedialog as tkfiledialog#通用对话框，允许用户指定要打开或保存的文件。
import shutil,re,os,winreg,base64,time
from icon import img
def  del_file(path):
	for i in os.listdir(path):
		path_file = os.path.join(path,i)
		if os.path.isfile(path_file):
			try:
				os.remove(path_file)
			except:
				continue
		else:
			del_file(path_file)

def fix_origin_A():
	env_dist = os.environ
	origin = env_dist.get('Appdata')  # 获取本地appdata路径
	Roaming_origin1 = origin + '\\Origin'
	local_origin2 = origin[0:-7] + 'Local\\Origin'
	if os.path.exists(local_origin2):
		os.system('taskkill /F /IM Origin.exe /T | taskkill /F /IM OriginWebHelperService.exe /T | taskkill /F /IM QtWebEngineProcess.exe /T | exit')
		try:
			shutil.rmtree(local_origin2) ####优先删除这个尝试#####
		except:
			del_file(local_origin2)
		tkmessagebox.showinfo(title='成功',message='修复完成')
	else:
		tkmessagebox.showinfo(title='警告',message='目录未找到或已修复过')

def fix_origin_B():
	env_dist = os.environ
	origin = env_dist.get('Appdata')  # 获取本地appdata路径
	temp = env_dist.get('temp')
	Roaming_origin1 = origin + '\\Origin'
	local_origin2 = origin[0:-7] + 'Local\\Origin'
	set_origin3 = "C:\\ProgramData\\Origin"
	if os.path.exists(local_origin2):
		os.system('taskkill /F /IM explorer.exe | taskkill /F /IM Origin.exe /T | taskkill /F /IM OriginWebHelperService.exe /T | taskkill /F /IM QtWebEngineProcess.exe /T | exit')
		# os.system("tskill  Origin | tskill  OriginWebHelperService | tskill  QtWebEngineProcess | exit")
		command_a = '''
		attrib -r %APPDATA%\Origin /s
		Takeown /F %APPDATA%\Origin /r /d y
		cacls %APPDATA%\Origin /t /e /g Administrators:F
		rd /s /q %APPDATA%\Origin
		Takeown /F C:\ProgramData\Origin /r /d y
		cacls C:\ProgramData\Origin /t /e /g Administrators:F
		rd /s /q C:\ProgramData\Origin
		Takeown /F %TEMP% /r /d y
		cacls %TEMP% /t /e /g Administrators:F
		rd /s /q %TEMP%
		del /f /s /q %0
		'''
		try:
			with open(temp+"/fixall.bat", 'w') as reg:
					reg.write("@echo off\n"+command_a)
					os.system(temp+"/fixall.bat")
					time.sleep(5)
					os.system('taskkill /F /IM cmd.exe | taskkill /F /IM conhost.exe | explorer.exe ')
					tkmessagebox.showinfo(title='成功',message='最终修复完成,如果没有桌面请注销或重启')
		except:
			tkmessagebox.showinfo(title='警告',message='权限不足或BUG')
	else:
		tkmessagebox.showinfo(title='警告',message='目录未找到或已修复过')

def origin_akamai():
	aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
	get_key = winreg.OpenKey(aReg, r'SOFTWARE\\WOW6432Node\\Electronic Arts\\EA Core')  # 获取origin的注册表
	origin_path = winreg.QueryValueEx(get_key, 'EADM6InstallDir')[0]  # 获取origin的注册表数据
	EACore=origin_path+"\\EACore.ini"
	text='''[connection]
EnviromentName=production
[Feature]
CdnOverride=akamai
'''
	with open(EACore, 'w') as EA:
		EA.write(text)

	hosts = ['184.28.218.98 origin-a.akamaihd.net', '23.198.105.69  www.origin.com']
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
	# print(path_)
	tkinter.Label(text="你的安装位置-"+path_).place(x=35,y=170,anchor='w')
	path = path_
	game_path = '"'+path_+'/__Installer/Touchup.exe"'
	check = path_+'/__Installer/Touchup.exe'
	command_s = game_path+' install -locale {zh_TW} -installPath "{%s}" -autologging -startmenuIcon=1 -desktopIcon=1' %path
	apex_path = path_ + '/__Installer/customcomponent/EasyAntiCheat/'
	apex = apex_path + 'EasyAntiCheat_Setup.exe'
	apex_command = '"' + apex + '" install 154 -console'
	# print(apex)
	# print(apex_command)
	if os.path.isfile(check):
			env_dist = os.environ
			temp = env_dist.get('temp')
			try:
				if os.path.isfile(apex):
					# print("APEX")
					with open(temp+'/regapex.bat', 'w') as reg:
						reg.write(apex_command)
					os.system(temp+'\\regapex.bat')
					with open(temp+'/regfix.bat', 'w') as reg:
						reg.write(command_s)
					os.system(temp+'\\regfix.bat')
				else:
					# print("NO-APEX")
					with open(temp+'/regfix.bat', 'w') as reg:
						reg.write(command_s)
					os.system(temp+'\\regfix.bat')
				time.sleep(2)
				tkmessagebox.showinfo(title='成功',message='修复完成')
			except:
				tkmessagebox.showinfo(title='失败',message='请使用管理员权限打开或者检查文件')
	else:
		tkmessagebox.showinfo(title='提示',message='请检查是否为游戏目录且存在__Installer目录')

def main():
	root = tkinter.Tk()
	fm1 = tkinter.Frame()
	label = tkinter.Label(text='origin多功能修复工具',height=2,width=20)
	label.pack(side='top')
	fm1.pack()

	fm2 = tkinter.Frame()
	LabelA=tkinter.Label(text='修复origin发生了一些问题')
	A = tkinter.Button(text ="修复", command = fix_origin_A,height=1,width = 10)
	LabelA.place(x=35,y=60,anchor='w')
	A.place(x=210,y=60,anchor='w')

	LabelB=tkinter.Label(text='最终修复方案')
	B = tkinter.Button(text ="修复", command = fix_origin_B,height=1,width = 10)
	LabelB.place(x=35,y=100,anchor='w')
	B.place(x=210,y=100,anchor='w')

	LabelC =tkinter.Label(text='origin加速')
	C = tkinter.Button(text ="加速", command = origin_akamai,height=1,width = 10)
	LabelC.place(x=35,y=140,anchor='w')
	C.place(x=210,y=140,anchor='w')

	LabelD=tkinter.Label(text='游戏位置修改后修复')
	D = tkinter.Button(text ="选择游戏目录", command = file_path,height=1,width = 15)
	LabelD.place(x=35,y=200,anchor='w')
	D.place(x=190,y=200,anchor='w')

	tkmessagebox.showinfo(title='注意',message='请使用管理员权限打开,已使用管理员打开请无视')
	fm2.pack()


	root.title('origin多功能修复工具V2.1')#标题
	root.geometry('320x220')#窗体大小
	root.resizable(False, False)#固定窗体
	tmp = open("tmp.ico","wb+")
	tmp.write(base64.b64decode(img))
	tmp.close()
	root.iconbitmap("tmp.ico")
	os.remove("tmp.ico")
	root.mainloop()

if __name__ == '__main__':
	main()
