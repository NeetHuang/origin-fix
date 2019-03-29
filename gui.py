# -*- coding: UTF-8 -*-
import tkinter
import tkinter.messagebox as tkmessagebox#访问标准Tk对话框。
import tkinter.filedialog as tkfiledialog#通用对话框，允许用户指定要打开或保存的文件。
import shutil,re,os,winreg,base64,time,sys
from icon import img
import win32com.shell.shell as shell
ASADMIN = 'sudo'

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

def fix_origin_Full():
	env_dist = os.environ
	origin = env_dist.get('Appdata')  # 获取本地appdata路径
	Roaming_origin1 = origin + r'/Origin'
	local_origin2 = origin[0:-7] + r'Local/Origin'
	prodata3 = r'C:/ProgramData/Origin' 
	# print(Roaming_origin1)
	# print(local_origin2)
	# print(prodata3)
	os.system('taskkill /F /IM Origin.exe /T | taskkill /F /IM OriginWebHelperService.exe /T | taskkill /F /IM QtWebEngineProcess.exe /T | taskkill /F /IM explorer.exe /T')
	try:
		if os.path.isdir(Roaming_origin1):
			shutil.rmtree(Roaming_origin1)
		if os.path.isdir(local_origin2):
			shutil.rmtree(local_origin2)
		if os.path.isdir(prodata3):
			shutil.rmtree(prodata3)
	except:
		del_file(Roaming_origin1)
		del_file(local_origin2)
		del_file(prodata3)
	shell.ShellExecuteEx(lpVerb='runas', lpFile="C:/Windows/explorer.exe")
	tkmessagebox.showinfo(title='成功',message='修复完成')

def origin_akamai():
	aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
	get_key = winreg.OpenKey(aReg, r'SOFTWARE\\WOW6432Node\\Electronic Arts\\EA Core')  # 获取origin的注册表
	origin_path = winreg.QueryValueEx(get_key, 'EADM6InstallDir')[0]  # 获取origin的注册表数据
	EACore=origin_path+"/EACore.ini"#找到游戏目录里面的EACore.ini
	text='''[connection]
EnviromentName=production
[Feature]
CdnOverride=akamai
'''
	with open(EACore, 'w') as EA:
		EA.write(text)
	backs =	shutil.copy(r'C:/Windows/System32/drivers/etc/hosts','C:/Windows/System32/drivers/etc/hosts.back')
	hosts = ['23.57.66.80 origin-a.akamaihd.net', '69.192.10.215 www.origin.com','159.153.191.240 accounts.ea.com','159.153.191.238 gateway.ea.com']
	if os.path.isfile('C:/Windows/System32/drivers/etc/hosts'):
		with open(r'C:/Windows/System32/drivers/etc/hosts', 'r+') as hos:
			if re.search(r"akamai",hos.read()):
				ask = tkmessagebox.askyesno(title='警告',message='已存在加速优化,是否仍要继续？')
				if ask ==True:
					backs
					with open(r'C:/Windows/System32/drivers/etc/hosts', 'w') as hos:
						for host in hosts:
							hos.write("\n"+host+"\n")
						tkmessagebox.showinfo(title='成功',message='加速优化完毕')
			else:
				backs
				for host in hosts:
				# print(host)
					hos.write("\n"+host+"\n")
				tkmessagebox.showinfo(title='成功',message='加速优化完毕')
	else:
		with open(r'C:/Windows/System32/drivers/etc/hosts', 'a') as hos:
			for host in hosts:
				hos.write("\n"+host+"\n")

def file_path():
	path_ = tkfiledialog.askdirectory(initialdir='C:/')
	tkinter.Label(text="你的安装位置-"+path_).place(x=35,y=170,anchor='w')
	Game_Path = path_+r'/__Installer/Touchup.exe'
	Game_Fix = r'install -locale zh_TW -installPath "%s" -autologging -startmenuIcon=1 -desktopIcon=1' %path_
	EasyAnti_Path = path_ + r'/__Installer/customcomponent/EasyAntiCheat/EasyAntiCheat_Setup.exe'
	EasyAnti_Fix = r'install 154 -console'
	if os.path.isfile(Game_Path):
		tkmessagebox.showinfo(title='提示',message='修复中,请等待数十秒')
		if os.path.isfile(EasyAnti_Path):
			#print("APEX")
			shell.ShellExecuteEx(lpVerb='runas', lpFile=EasyAnti_Path, lpParameters=EasyAnti_Fix)
			shell.ShellExecuteEx(lpVerb='runas', lpFile=Game_Path, lpParameters=Game_Fix)
		else:
			#print("NO-EasyAnti")
			shell.ShellExecuteEx(lpVerb='runas', lpFile=Game_Path, lpParameters=Game_Fix)
		time.sleep(10)
		tkmessagebox.showinfo(title='成功',message='修复完成,请检查桌面是否出现游戏图标,如果提示VC安装失败,请进入游戏目录__Installer/vc,手动安装成功后再次运行')
	else:
		tkmessagebox.showinfo(title='提示',message='请检查是否为游戏目录且存在__Installer目录')

def main():
	root = tkinter.Tk()
	fm1 = tkinter.Frame()
	label = tkinter.Label(text='origin多功能修复工具',height=2,width=20)
	label.pack(side='top')
	#fm1.pack()

	#fm2 = tkinter.Frame()
	LabelA=tkinter.Label(text='修复origin发生了一些问题')
	A = tkinter.Button(text ="修复", command = fix_origin_Full,height=1,width = 10)
	LabelA.place(x=20,y=60,anchor='w')
	A.place(x=210,y=60,anchor='w')

	LabelB =tkinter.Label(text='origin加速下载和解决登陆问题')
	B = tkinter.Button(text ="加速", command = origin_akamai,height=1,width = 10)
	LabelB.place(x=20,y=100,anchor='w')
	B.place(x=210,y=100,anchor='w')

	LabelC=tkinter.Label(text='游戏位置移动(免验证完整性)')
	C = tkinter.Button(text ="选择游戏目录", command = file_path,height=1,width = 15)
	LabelC.place(x=20,y=140,anchor='w')
	C.place(x=190,y=140,anchor='w')
	fm1.pack()

	root.title('origin多功能修复工具V3.0')#标题
	root.geometry('320x200')#窗体大小
	root.resizable(False, False)#固定窗体
	tmp = open("tmp.ico","wb+")
	tmp.write(base64.b64decode(img))
	tmp.close()
	root.iconbitmap("tmp.ico")
	os.remove("tmp.ico")
	root.mainloop()

if __name__ == '__main__':
	#获取管理员权限
	if sys.argv[-1] != ASADMIN:
	    script = os.path.abspath(sys.argv[0])
	    params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
	    shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
	    sys.exit(0)
	else:
		main()