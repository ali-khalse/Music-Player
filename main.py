#=============== imports =============
from tkinter import *
import time
import mutagen 
from mutagen.mp3 import MP3 
import pygame
from tkinter.messagebox import showinfo,showwarning,showerror
from tkinter import filedialog as fd
import validators
import requests
import threading
#=============== configure ===========
root = Tk()
root.title('Subino')
root.geometry("500x500")
root.resizable(0, 0)
root.configure(background='grey')

pygame.init()
pygame.mixer.init()

#root.attributes('-alpha',0.5)
#=============== icons ===============
play_ico = PhotoImage(file = "icons/play.png")
pause_ico = PhotoImage(file = "icons/pause.png")
next_ico = PhotoImage(file = "icons/next.png")
previous_ico = PhotoImage(file = "icons/previous.png")
st_ico = PhotoImage(file = "icons/stop.png")
circle_ico = PhotoImage(file = "icons/icons8-filled-circle-64.png").subsample(1,1)
icon_ico = PhotoImage(file = "icons/0262f4dd643e39d3a8a5376b08d51125.png").subsample(2,2)
list_ico = PhotoImage(file = "icons/list.png")
back_ico = PhotoImage(file = "icons/back.png")
add_ico = PhotoImage(file = "icons/add-song.png")
remove_ico = PhotoImage(file = "icons/remove-song.png")
download_ico = PhotoImage(file = "icons/download.png")
#============== musics ==============
musics = {}
number_m = int(0)
#=============== def ================
def select_files():
    filetypes = (('mp3 files', '*.mp3'),('All files', '*.*'))

    filename = fd.askopenfilenames(title='Open a file',initialdir='Desktop',filetypes=filetypes)
    
    if not filename =="":
        for i in filename:
            name = i.split("/")[-1]
            if not name in musics:
                playlist.insert(END,name)
                musics[name] = i
        #print(musics)
    else:
        showwarning(title='Selected File',message="! هيچ فايلي انتخاب نکرديد")
        
def audio_duration(length): 
    hours = length // 3600  # calculate in hours 
    length %= 3600
    mins = length // 60  # calculate in minutes 
    length %= 60
    seconds = length  # calculate in seconds 
    return str(hours), str(mins), str(seconds)  # returns the duration 


  
def change(i=2):
    global ids
    ids = label1.after(1000,change,i+1 )
    currente = pygame.mixer.music.get_pos()/1000
    xi= (currente/audio_leng)*400+2
    label1.place(x=xi,y=2)
    hours, mins, seconds = audio_duration((int(currente))) 
    #print('Total Duration: {}:{}:{}'.format(hours, mins, seconds)) 
    current_time.config(text=('{}:{}:{}'.format(hours.zfill(2), mins.zfill(2), seconds.zfill(2))))
    #print()
    if currente < 0:
        label1.after_cancel(ids)
        label1.place(x=2,y=2)
        p_and_s.config(image = play_ico,command=play)
        
def play():
    global audio_leng
    global number_m
    try:
        if not musics == {} :
            if number_m == 0:
                previous_b["state"] = "disabled"
            else:
                previous_b["state"] = "normal"
            if number_m == len(list(musics.keys()))-1:
                next_b["state"] = "disabled"
            else:
                next_b["state"] = "normal"
            res = list(musics.keys())[number_m]
            name_music.configure(text= str(res)[-20:])
            #print(musics[res])
            music = musics[res]
            audio = MP3(music)
            audio_info = audio.info 
            length = int(audio_info.length)
            audio_leng = length
            hours, mins, seconds = audio_duration(length) 
            total_time.config(text=('{}:{}:{}'.format(hours.zfill(2), mins.zfill(2), seconds.zfill(2))))
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(loops=0)
            p_and_s.config(image = st_ico,command=stop)
            change()
        else:
            showwarning(title='Selected File',message="! هيچ فايلي انتخاب نکرديد")
    except:
        number_m = 0
        play()
        #showwarning(title='Selected File',message="به دليل دستکاري ليست از نو پلي کنيد.")
def next_m():
    global number_m
    if not number_m >len(list(musics.keys()))-1 :
        number_m += 1
    play()

def previous_m():
    global number_m
    if not number_m <1 :
        number_m -= 1
    play()
def stop():
    pygame.mixer.music.stop()
    p_and_s.config(image = play_ico,command=play)
    label1.after_cancel(ids)
def change_vol(_=None):
    pygame.mixer.music.set_volume(w.get()/100)
def paste_to():
    clip_text = root.clipboard_get()
    if validators.url(clip_text) == True:
        url_get.config(textvariable=StringVar(root, value=clip_text))
    else:
        showwarning(title='Error',message=". لينک در کليپ برد شما معتبر نيست")
#def downloads_m():
    #req = requests.get('https://dl.fara-download.ir/audio/sound_effect/countdown/10sec_digital_countdown_3.mp3')

def downloads_ms():
    url  = url_get.get()
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below

    with requests.get(url, stream=True) as r:
        total_size = int(r.headers['content-length'])
        print(total_size)
        r.raise_for_status()
        currnt = 0
        
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                #if chunk:
                currnt += 8192
                print(int((currnt/total_size)*100))
                f.write(chunk)

    if not local_filename in musics:
        playlist.insert(END,local_filename)
        musics[local_filename] = local_filename
        print( local_filename)
    else:
        print("exist")
def downloads_m():
    download_thread = threading.Thread(target=downloads_ms)
    download_thread.start()
#---------
def CreateNewWindow():
    #next_b.destroy()
    create()

def destroy_main():
    pygame.mixer.music.stop()
    list_b.destroy()
    previous_b.destroy()
    p_and_s.destroy()
    next_b.destroy()
    current_time.destroy()
    total_time.destroy()
    iconsn.destroy()
    w.destroy()
    our_canvas.destroy()
    name_music.destroy()
    create_list()
def destroy_list():
    songsframe.destroy()
    deleter.destroy()
    adder.destroy()
    backer.destroy()
    url_get.destroy()
    url_label.destroy()
    paste_b.destroy()
    download_b.destroy()
    create_main()
def create_list():
    #=============== buttons ============
    global backer
    backer = Button(image=back_ico,bg='grey',border=0,activebackground="grey",command=destroy_list)
    backer.place(x=0,y=385)
    #---------
    global songsframe
    songsframe = LabelFrame(text="Song Playlist",font=("times new roman",12,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
    songsframe.place(x=10,y=10,width=480,height=300)
    scrol_y = Scrollbar(songsframe,orient=VERTICAL)
    #-------------
    global playlist
    playlist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="gold",selectmode=SINGLE,font=("times new roman",12,"bold"),bg="silver",fg="navyblue",bd=5,relief=GROOVE)
    playlist.place(x=10,y=10,width=450,height=250)
    #-------------
    global adder
    adder = Button(image=add_ico,bg='grey',border=0,activebackground="grey",command=select_files)
    adder.place(x=100,y=385)
    #--------------
    global deleter
    deleter = Button(image=remove_ico,bg='grey',border=0,activebackground="grey",command=delt)
    deleter.place(x=200,y=385)
    #-------------
    global download_b
    download_b = Button(image=download_ico,bg='grey',border=0,activebackground="grey",command=downloads_m)
    download_b.place(x=300,y=385)
    #--------------
    global url_label
    url_label = Label(text="URL : ",font=("Calibri", 15),fg="yellow",bg='grey')
    url_label.place(x=20,y=320)
    #--------------
    global url_get
    clip_text = root.clipboard_get()
    url_get = Entry(root,width=50,bd=3)
    if validators.url(clip_text) == True:
        url_get.config(textvariable=StringVar(root, value=clip_text))
    url_get.place(x=90,y=324)
    #--------------
    global paste_b
    paste_b = Button(text ="paste",bg='#60BE92',border=0,activebackground="grey",command=paste_to)
    paste_b.place(x=425,y=327)
    #------------
    for i in musics:
        playlist.insert(END,f"{i}")
def create_main():
    #=============== buttons ============
    global name_music
    name_music = Label(root,text="",font=("Calibri", 15),fg='yellow',bg='grey')
    name_music.place(x=150,y=350)
    #----------
    global list_b
    list_b = Button(image = list_ico,bg='grey',border=0,activebackground="grey",command=destroy_main)
    list_b.place(x=0,y=385)
    #--------
    global previous_b
    previous_b = Button(image = previous_ico,bg='grey',border=0,activebackground="grey",command=previous_m,state = "disabled")
    previous_b.place(x=100,y=385)
    #--------
    #stp = Button(image = st_ico,bg='grey',border=0,activebackground="grey")
    #stp.place(x=200,y=385)
    #--------
    global p_and_s
    p_and_s = Button(image = play_ico,command=play,bg='grey',border=0,activebackground="grey")
    p_and_s.place(x=300,y=385)
    #---------
    global next_b
    next_b = Button(image = next_ico,bg='grey',border=0,activebackground="grey",command=next_m)
    next_b.place(x=400,y=385)
    #--------
    global current_time
    current_time = Label(text="00:00:00",bg='grey',fg='yellow')
    current_time.place(x=15,y=350)
    #--------
    global total_time
    total_time = Label(text="00:00:00",bg='grey',fg='yellow')
    total_time.place(x=430,y=350)
    #---------
    global iconsn
    iconsn = Label(image=icon_ico,bg='grey')
    iconsn.place(x=100,y=5)
    #---------
    global w
    w = Scale(from_=0, to=100,command=change_vol,length=100, orient=HORIZONTAL,bd=4,bg="grey",fg="yellow",activebackground="#F05B6C",highlightbackground="grey",troughcolor="#60BE92")
    w.set(100)
    w.place(x=198,y=398)
    #--------
    global our_canvas
    our_canvas=Canvas(root,width=468,height=68,bg="grey", highlightbackground="black")
    our_canvas.place(x=15,y=275)
    our_canvas.create_line(0, 34, 470, 34,fill="black")
    #--------
    global label1
    label1 = Label(our_canvas,image=circle_ico,bg='grey')
    label1.place(x=2,y=2)
    
create_main()
 



def delt():
    index = playlist.curselection()
    if not index == ():
        del musics[playlist.get(ACTIVE)]
        playlist.delete(index) 
    else:
        showerror(title='ERROR',message="هيچ فايلي را انتخاب نکرده ايد.")


#=============== run ================
root.mainloop()

