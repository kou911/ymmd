import tkinter as tk
import math
from tkinter import filedialog
import re

A = list('あぁゃかがさざただなはばぱまやらわ')
I = list("いぃきぎしじちぢにひびぴみきシキィヒピシチツ")
U = list("うぅゅくぐすずつづぬふぶぷゆむるクスフプ")
E = list("えぇけげせぜてでねへべぺめれテ")
O = list("おぉょこごそぞとどのほぼぽもよろをト")
n = list("ばびぶべぼぱぴぷぺぽまみむめもピプ")
small = list("ゃゅょュ")
stay = ["ー","っ","。","、"," ","　"]
dic = [A,I,U,E,O]
can = []
for i in range(len(dic)):
  can += dic[i]
can += stay
jp = list("あいうえお")
Value = bytearray([0x00,0x00,0x80,0x3F])
ZERO = bytearray([0x00,0x00,0x00,0x00])

def mouse(Serif):
  voice = []
  voice.append("ん")
  for i in range(len(Serif)):
    if Serif[i] == "わ":
      voice.append("ぅ")
    if Serif[i] in small:
      voice.pop(-1)
    if Serif[i] == "ん":
      voice.append("ん")
    if Serif[i] in n:
      voice.append("n")
    if Serif[i] in stay:
      if i!=0:
        voice.append(voice[-1])
    for d in range(len(dic)):
      if Serif[i] in dic[d]:
        if Val1.get() == True and d == 1:
          voice.append("い")
        voice.append(jp[d])
        break
  voice.append("ん")
  return voice

def act(a,b,f):   #act(文字、前フレーム,所要フレーム) 戻り値 そのフレームのバイナリ、現フレーム
  n = 0
  if (a in jp)or(a=="ん"):
    fl = b+f
  if a == "ぅ":
    fl = b
    a = "う"
  if a=="n":
    fl = b
    a = "ん"
  z = bytearray([])
  for i in range(len(jp)):
    z += bytes(jp[i], 'SHIFT-JIS')
    z += n.to_bytes(13,"little")
    z += (b+f).to_bytes(4,"little")
    if a == jp[i]:
      z += Value
    else:
      z += ZERO
  return z,fl

def bind(event):
  if Button2["text"]==u"最前面に固定":
    root.attributes("-topmost", True)
    Button2["text"]=u"固定を解除"
  else:
    root.attributes("-topmost", False)
    Button2["text"]=u"最前面に固定"

def run(event):
  Static3.place_forget()
  binary = bytearray\
 ([0x56, 0x6F, 0x63, 0x61, 0x6C, 0x6F, 0x69, 0x64, 0x20, 0x4D, 0x6F, 0x74, 0x69, 0x6F, 0x6E, 0x20, \
   0x44, 0x61, 0x74, 0x61, 0x20, 0x30, 0x30, 0x30, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8E, 0xA9, \
   0x93, 0xAE, 0x8C, 0xFB, 0x83, 0x70, 0x83, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
  voice = []
  text = list(EditBox.get())
  for i in range(len(text)):
    if text[i] not in can:
      text[i] = "@"

  frame = framescale.get()
  sframe = math.floor(frame/2+0.5)

  voice = mouse(text)
  text = "".join(text)
  if len(text)>10:
    text = text[:8] + "ry"
  if Val1.get() == True:
    text += "_え無し"

  if len(voice) == 2:
    Static3.place(relx=0.5,rely=0.7,anchor=tk.CENTER)
    return
  else :
    Static3.place_forget()

  binary += ((len(voice))*5).to_bytes(4,"little")
  before = -1*frame
  for k in range(len(voice)):
    if (voice[k] == 'ぅ') or (voice[k] == 'n'):
      x,before = act(voice[k],before,sframe)
    else:
      x,before = act(voice[k],before,frame)
    binary += x
  binary += bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

  i = 0
  while(True):
    try:
      if i == 0:
        f = open(text+".vmd", "xb")
      else:
        f = open(text+"("+str(i)+")"+".vmd", "xb")
      f.write(binary)
      f.close()
      Static3.place(relx=0.5,rely=0.7,anchor=tk.CENTER)
      Static3["text"]=text + u"\nのモーションファイルを作成しました"
      return
    except FileExistsError:
      i += 1

def choice(event):
  binary = bytearray\
 ([0x56, 0x6F, 0x63, 0x61, 0x6C, 0x6F, 0x69, 0x64, 0x20, 0x4D, 0x6F, 0x74, 0x69, 0x6F, 0x6E, 0x20, \
   0x44, 0x61, 0x74, 0x61, 0x20, 0x30, 0x30, 0x30, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8E, 0xA9, \
   0x93, 0xAE, 0x8C, 0xFB, 0x83, 0x70, 0x83, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
  
  name = filedialog.askopenfilename(filetypes=[ ( 'YMMプロジェクトファイル' , '.ymmp' ) ])
  f = open(name,"r",encoding = "utf_8")
  
  l = f.readlines()
  date = {} # key:開始フレーム　内容：セリフ、キャラ、発音時間、アイテム時間、口の動き
  intkey = []
  add = 0
  al = 0
  for i in range(len(l)):
    if f'"Name": "{Charbox.get()}"' in l[i]:
      d = 1
      while True:
          if '"AdditionalTime"' in l[i+d]:
              add = float((re.sub(' |\n|"|,|AdditionalTime|:', '',l[i+d])))
              print(add)
              break
          d = d+1
  for i in range(len(l)):
      info = []
      bool = False
      if '"Hatsuon"' in l[i]:
          info.append(re.sub(' |NUMK|NUM|VAL|=|COUNT|\n|[_＿",<>1234567890]|Hatsuon|:', '',l[i]))
          d = -1
          while True:
              if '"CharacterName"' in l[i+d]:
                  ch = (re.sub(' |\n|"|,|CharacterName|:', '',l[i+d]))
                  if ch == Charbox.get():
                    info.append(ch)
                    break
                  else:
                    bool = True
                    break
              d = d-1
          if bool:
            continue
          d = 1
          while True:
              if '"VoiceLength"' in l[i+d]:
                  length = (re.sub(' |\n|"|,|VoiceLength|:', '',l[i+d]))
                  seconds = \
                  float(length[0:2])*360+\
                  float(length[2:4])*60+\
                  float(length[4:14]) - add
                  print(add)
                  info.append(seconds)
                  break
              d = d+1
          d = 1
          while True:
              if '"Frame"' in l[i+d]:
                  intkey.append(round(int(re.sub(' |\n|"|,|Frame|:', '',l[i+d]))/2))
                  strkey = str(round(int(re.sub(' |\n|"|,|Frame|:', '',l[i+d]))/2))
                  break
              d = d+1
          d = 1
          while True:
              if '"Length"' in l[i+d]:
                  info.append(round(int(re.sub(' |\n|"|,|Length|:', '',l[i+d]))/2))
                  break
              d = d+1
          info.append(mouse(list(info[0])))
          date[strkey] = info
      
  if len(date) == 0:
    Static3.place(relx=0.5,rely=0.7,anchor=tk.CENTER)
    f.close()
    return
  else :
    Static3.place_forget()

  intkey.sort()
  print(intkey)
  before = 0
  frame = 4
  for i in range(len(date)):
      beforeframe = frame
      frame = round(date[str(intkey[i])][2]*30/len(date[str(intkey[i])][0]))
      sframe = math.floor(frame/2+0.5)

      if before < -1 * frame + intkey[i]:
        before = -1 * frame + intkey[i]

      elif before == -1 * frame + intkey[i]:
        before = frame + intkey[i]
        date[str(intkey[i])][4].pop(0)

      elif before > -1 * frame + intkey[i] and before <= intkey[i]:
        date[str(intkey[i])][4].pop(0)
        if not before == 0:
          date[str(intkey[i])][4].insert(0, date[str(intkey[i-1])][4])
          binary = binary[:len(binary)-115]
          before = -2 * frame + intkey[i]
        else:
          before = -1 * frame + intkey[i]
      elif before > intkey[i] and before - beforeframe < intkey[i]:
        if not before == 0:
          date[str(intkey[i])][4].pop(0)
          binary = binary[:len(binary)-115]
          before = -1 * frame + intkey[i]
        else:
          date[str(intkey[i])][4].pop(0)
          before = -1 * frame + intkey[i]
      else:
        continue

      for k in range(len(date[str(intkey[i])][4])):
        if before - intkey[i] >  date[str(intkey[i])][3]:
          al = al - (len(date[str(intkey[i])][4]) - k)
          break
        if (date[str(intkey[i])][4][k] == 'ぅ') or (date[str(intkey[i])][4][k] == 'n'):
          x,before = act(date[str(intkey[i])][4][k],before,sframe)
        else:
          x,before = act(date[str(intkey[i])][4][k],before,frame)
        binary += x
      al += len(date[str(intkey[i])][4])
  binary += bytearray([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
  point = (al*5).to_bytes(4,"little")
  binary = binary[:54] + point + binary[54:]
  f.close()
  i = 0
  while(True):
    try:
      if i == 0:
        name = name.replace(".ymmp",".vmd")
      else:
        if i == 1:
          name = name[:len(name)-4]+"(1)"+name[len(name)-4:]
        else:
          name = name.replace(f"({str(i-1)})",f"({str(i)})")
      f = open(name, "xb")
      f.write(binary)
      f.close()
      Static3.place(relx=0.5,rely=0.7,anchor=tk.CENTER)
      Static3["text"]=name[name.rfind("/")+1:] + u"を同フォルダに作成しました"
      return
    except FileExistsError:
      i += 1


root = tk.Tk()
root.title(u"MMD口パク君")
root.geometry("400x300")
root.resizable(False, False)

EditBox = tk.Entry(width=50)
EditBox.place(relx=0.5,rely=0.05,anchor=tk.CENTER)

Static1 = tk.Label(text=u'セリフを入力')
Static1.place(relx=0.5,rely=0.115,anchor=tk.CENTER)

Static2 = tk.Label(text=u'1音にかけるフレーム数')
Static2.place(relx=0.5,rely=0.3,anchor=tk.CENTER)

framescale = tk.Scale(root, orient=tk.HORIZONTAL, from_ = 2, to = 30, length = 300)
framescale.place(relx=0.5,rely=0.21,anchor=tk.CENTER)

Val1 = tk.BooleanVar()
Val1.set(False)
CheckBox1 = tk.Checkbutton(text=u"「え」を「い」に置き換える", variable=Val1)
CheckBox1.place(relx=0.5,rely=0.4,anchor=tk.CENTER)

Button = tk.Button(text=u'モーションファイル生成')
Button.bind("<Button-1>",run) 
Button.place(relx=0.65,rely=0.85,anchor=tk.CENTER)

Button2 = tk.Button(text=u'最前面に固定')
Button2.bind("<Button-1>",bind) 
Button2.place(relx=0.35,rely=0.85,anchor=tk.CENTER)

file = tk.Button(text=u"ymmpファイルを選択して生成")
file.bind("<Button-1>",choice)
file.place(relx=0.25,rely=0.5,anchor=tk.CENTER)

Charbox = tk.Entry(width=20)
Charbox.place(relx=0.7,rely=0.5,anchor=tk.CENTER)

Ch = tk.Label(text=u'ymmpのキャラクター名を入力')
Ch.place(relx=0.7,rely=0.55,anchor=tk.CENTER)

filename = tk.Label(text=u"")
filename.place(relx=0.5,rely=0.59,anchor=tk.CENTER)

Static3 = tk.Label(text=u"セリフが入力されていないか\n無効な文字のみで構成されています")


voice = []



root.mainloop()