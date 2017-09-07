from Tkinter import *
import ttk
import tkMessageBox
import subprocess
import threading
import time
import os
        
'''#ADB Devices serial numbers'''
cmd = ["adb devices"]
list1=[]
l2=[]
for adb in cmd:
    p = subprocess.Popen(adb,stdout=subprocess.PIPE,shell="TRUE")
    list1.append(p.stdout.read().decode('utf-8'))
test=list1[0].split()
l2=(test)
i=len(l2)
cnt=0
snl=[]
if i>2:
  for i in range(len(l2)):
    if i > 3 and i% 2==0:
      snl.append(l2[i])
      cnt=cnt+1 
else:
   pass
'''Action blocks'''
def getvalue(value):
    lock.acquire()
    SV.set(serial.get())
    lock.release()
    t1 = threading.Thread(name='modelnumber',target=mn)
    t1.start()
    t2 = threading.Thread(name='buildnumber',target=bn)
    t2.start()
def mn():
    print os.getpid(),'MN'
    print threading.currentThread().getName(), 'START'
    subprocess.call('adb wait-for-device' ,shell=True)
    x='adb -s {} shell getprop ro.build.flavor'.format(SV.get())
    p = subprocess.Popen(x,stdout=subprocess.PIPE,shell="True")
    MN.set((p.stdout.read().decode("utf-8")))
    print os.getpid()
    print threading.currentThread().getName(), 'END'
def bn():
    print os.getpid(),'BN'
    print threading.currentThread().getName(), 'START'
    subprocess.call('adb wait-for-device' ,shell=True)
    x='adb -s {} shell getprop ro.build.id'.format(SV.get())
    p = subprocess.Popen(x,stdout=subprocess.PIPE,shell="True")
    BN.set((p.stdout.read().decode("utf-8")))
    print os.getpid(),'BN'
    print threading.currentThread().getName(), 'END'
def savelog(i):
    print os.getpid(),'Savelog'
    print threading.currentThread().getName(), 'START'
    subprocess.call('adb wait-for-device' ,shell=True)
    x="adb -s {} logcat -b {} -v time>{}_log.txt".format(SV.get(),i,i)
    subprocess.call(x ,shell=True)
    print os.getpid(),'Savelog'
    print threading.currentThread().getName(), 'START'
def viewlog(i):
    if cnt!=0 and serial.current() != -1:
        print os.getpid(),'View log'
        print threading.currentThread().getName(), 'START'
        subprocess.call('adb wait-for-device' ,shell=True)
        x="start adb -s {} logcat -b {} -v time".format(SV.get(),i)
        subprocess.call(x ,shell=True)
        print os.getpid(),'View log'
        print threading.currentThread().getName(), 'START'
    else:
        tkMessageBox.showinfo("ADB logs ", "Kindly Select Serial Number from the list box")
def start():
    if cnt!=0 and serial.current() != -1:
        testset=["main","events","radio"]
        for i in testset:
            t1 = threading.Thread(name='savelog',target=savelog, args=(i,))
            t1.start()
            t2 = threading.Thread(name='viewlog',target=viewlog, args=(i,))
            t2.start()
    else:
        tkMessageBox.showinfo("ADB logs ", "Kindly Select Serial Number from the list box ")
def exitlog():
    if cnt!=0 and serial.current() != -1:
        subprocess.call('adb kill-server' ,shell=True)
        tkMessageBox.showinfo("ADB logs ", "ADB log File:\n File->Open saved logs!!")
def stvideo():
    if cnt!=0 and serial.current() != -1:
        x='adb -s {} shell screenrecord /sdcard/Issue.mp4'.format(SV.get())
        subprocess.call(x ,shell=True)
def vstart():
    t = threading.Thread(target=stvideo)
    t.start()   
def vstop():
    if cnt!=0 and serial.current() != -1:
        subprocess.call('adb kill-server' ,shell=True)
        subprocess.call('adb tcpip' ,shell=True)
        tkMessageBox.showinfo("Screen record video ", "Screen video is saved in internal memory of the DUT!!")
def stop():
    subprocess.call('adb kill-server' ,shell=True)
    tkMessageBox.showinfo("Thank you  ", "Credits:\n MUTHUVEL G and SOMC-OTC-Members")
    box.destroy()
def about():
    def astop():
        abox.destroy()
        
    abox= Tk()
    abox.title("Log&video capture tool")
    #abox.iconbitmap(default="an.ico")
    abox.attributes("-toolwindow", 1)
    aframe = ttk.Frame(abox)
    aframe.grid(column=0, row=0)
    ttk.Label(aframe, text="Copyrights@").grid(column=2, row=3)
    ttk.Label(aframe, text="Log&video capture tool").grid(column=2, row=1)
    ttk.Label(aframe, text="Version 1.1").grid(column=2, row=2)
    ttk.Label(aframe,text="Contact:\n Muthuvelucea@outlook.com").grid(column=2, row=4)
    ttk.Button(aframe, text="OK",command=astop).grid(column=2, row=5)
    for elements in aframe.winfo_children(): elements.grid_configure(padx=5, pady=5)
    abox.mainloop()
def openfile():
    if cnt!=0:
        os.startfile(os.getcwd())                 
'''#BOX layout:'''
box = Tk()
s=ttk.Style()
s.theme_use('clam')
s.configure('my.TLabel',font=('Helvetica',12),foreground='maroon')
box.title("Log&video capture tool")
#box.iconbitmap(default="an.ico")
box.resizable(0,0)
#box.attributes("-toolwindow", )
mainframe = ttk.Frame(box)
menubar=Menu(box)
mainframe.grid(column=0, row=0)

'''
#Element value Decelearation:
#Connected Devices number,Nodel Number,Build Number
'''
lock = threading.Lock()
CDN = StringVar()
MN=StringVar()
BN=StringVar()
SV=StringVar()
CDN.set(cnt)

'''#Menu element Decelearation'''
helpmenu=Menu(menubar,tearoff=0)
helpmenu.add_command(label="About",command=about)
filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="Open saved logs ",command=openfile)
filemenu.add_command(label="Exit",command=stop)
'''#Elements Decelearation:'''
menubar.add_cascade(label="File",menu=filemenu)
menubar.add_cascade(label="Help",menu=helpmenu)
ttk.Label(mainframe, text="Connected Devices").grid(column=1, row=1)
ttk.Label(mainframe, textvariable=CDN,style='my.TLabel').grid(column=1, row=2)
ttk.Label(mainframe, text="Serial Number").grid(column=2, row=1,sticky=N)
serial=ttk.Combobox(mainframe)
serial.grid(column=2, row=2)

serial['values'] = snl
serial['state']=state
serial.bind('<<ComboboxSelected>>',getvalue)
ttk.Label(mainframe, text="Model").grid(column=3, row=1,sticky=N)
ttk.Label(mainframe, textvariable=MN,style='my.TLabel').grid(column=3, row=2)
ttk.Label(mainframe, text="Build Number").grid(column=4, row=1,sticky=N)
ttk.Label(mainframe, textvariable=BN,style='my.TLabel').grid(column=4, row=2)
ttk.Label(mainframe, text="ADB_logcat").grid(column=1, row=3)
ttk.Button(mainframe, text="Start", command=start).grid(column=2, row=3)
ttk.Button(mainframe, text="Stop", command=exitlog).grid(column=3, row=3)
ttk.Label(mainframe, text="Screen Video").grid(column=1, row=4)
ttk.Button(mainframe, text="Start", command=vstart).grid(column=2, row=4)
ttk.Button(mainframe, text="Stop", command=vstop).grid(column=3, row=4)
ttk.Button(mainframe, text="Quit", command=stop).grid(column=4, row=4)

for elements in mainframe.winfo_children(): elements.grid_configure(padx=5, pady=5)
box.config(menu=menubar)
box.mainloop()

