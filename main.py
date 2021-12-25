#$LAN=PYTHON$
#執行方法 python ./main.py
#coding=UTF-8
#學號: M103140007
#系級: 資安碩碩一
#姓名 :林郁珮

import tkinter as tk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as messagebox
from functools import cmp_to_key
from element import *
from voronoi import *



class InputData (list):

        @staticmethod 
        def read_file(filename):
                 
                 read_line = open(filename,encoding='utf-8').readlines()
                 read_line = [l.strip() for l in read_line if l.strip() != "" and l.strip().split()[0][0] != "#"] #儲存成list  l.strip().split()[0][0] = the program will only take the first number as input.
                 if(len(read_line)<=0 or read_line[0][0].isdigit() == 0):
                         return None
                 i = 0
                 n = len(read_line)
                 res = []
                 while(i<n): #讀取每一行                  
                    num  = int(read_line[i]) #資料筆數輸入 2、3、4、5...
                    points = []
                   # print("num : ",num)
                    if(num==0 or i+num > n): # 0 = 測資結束
                        break

                    for j in range(num):
                        #print("J : ",j)                      
                        data = read_line[i+j+1].split() #存取點座標 以空白為分隔
                        #print("data : ",data)                       
                        p = Point(int(data[0]),int(data[1]))
                        points.append(p)
                                               
                    res.append(points)    
                    i = i + num + 1
                    
                 return res
        
class Read_SaveData:
    def __init__(self,points,dividers):
        self.points = points
        self.dividers = dividers
  
    @staticmethod
    def read_file(filename):
        read_line =open(filename,encoding='utf-8').readlines()
        read_line = [l.strip() for l in read_line if l.strip() != "" and l.strip().split()[0][0] != "#"]
        #print(read_line)
        #print(len(read_line))
        if(len(read_line)<=0 or not read_line[0][0].isalpha() ):
            print("error")
            return None
        i = 0
        n = len(read_line)
       
        points = []
        dividers = []
        while(i<n):
            data = read_line[i].split()
            #print(data)
            if(data[0] == 'P'):
                p = Point(float(data[1]),float(data[2]))

                points.append(p)
            elif(data[0] == 'E'):
                start = Point(float(data[1]),float(data[2]))
                end = Point(float(data[3]),float(data[4]))
                dividers.append(Divider(start,end,end,end))
            i+=1
            record = Read_SaveData(points,dividers)
        return record


    
class Interface(tk.Tk):
     def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Voronoi Diagram _ M103140007")
        self.geometry("700x600")
       

        #data info
        self.input_data = InputData()
        self.click_data=[]
        self.index=0

        self.segment = []
        self.merge = []
        
        self.record_list = []

        #menu 
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar,tearoff=1,foreground='black')
        filemenu.add_command(label="open file",command=self.open_data) #輸入資料檔
        filemenu.add_command(label="save file",command = self.save) #儲存結果
        filemenu.add_command(label="clear",command =self.clean_canvas) #清除畫布
        menubar.add_cascade(label="File", menu=filemenu)
        runmenu = tk.Menu(menubar,tearoff=1,foreground='black')
        runmenu.add_command(label="run",command=self.Play)
        runmenu.add_command(label="step by step",command=self.step_by_step)
        menubar.add_cascade(label="Run",menu=runmenu)
        self.config(menu=menubar)


        #右側資訊欄為
        self.right_frame = tk.LabelFrame(self,width=100,height=400,borderwidth=10)
        self.right_frame.pack(side="right",fill='y')
      
        #上面資訊欄位
        self.top_frame = tk.Frame(self,width=100)
        self.top_frame.pack(side="top",anchor='n')

        self.play_image = tk.PhotoImage(file="./icon/play.png")
        self.step_image = tk.PhotoImage(file="./icon/step.png")
        self.clear_image = tk.PhotoImage(file="./icon/clean.png")

        self.play_btn = tk.Button(self.top_frame,text="Run",image = self.play_image,command=self.Play).grid(column=0,row=0)
        self.step_btn = tk.Button(self.top_frame,text="Step by step",image = self.step_image,command=self.step_by_step).grid(column=1,row=0)
        self.clear_btn = tk.Button(self.top_frame,text="clear",image = self.clear_image,command =self.clean_canvas).grid(column=2,row=0)


        
        #canvas畫布生成
        self.mycanvas = tk.Canvas(self,width=600,height=600)
        self.mycanvas.pack(expand=1,fill="both")
        self.mycanvas.bind("<Button-1>",self.draw_on_canvas)

        #在畫布上繪製座標
     def draw_on_canvas(self,event):
              #x1,y1=(event.x-1),(event.y-1)
              x1,y1=(event.x-1),(event.y-1)
              x2,y2=(event.x+1),(event.y+1)
              #x2,y2=(event.x+1),(event.y+1)
              self.mycanvas.create_oval(x1-2,y1-2,x2+2,y2+2,fill="black")
              xy = '(%d, %d)' % (event.x, event.y)
              pointxy = tk.Label(self.right_frame, text=xy,bd=10, anchor=tk.NE,compound="top",bg="white")
              pointxy.pack(side=tk.TOP)
              p = Point(event.x,event.y)
              #store data
              self.click_data.append(p)

     def draw_points(self, points, color="black"):
        for p in points:
            self.mycanvas.create_oval(p.x-2, p.y-2, p.x+2, p.y+2, fill=color)

     def draw_lines(self,dividers,color="black",thick=1):
        # self.mycanvas.create_line(259,50,343,489,fill=color,smooth=True,width=1)
         print("draw_lines")
         for d in dividers:
             self.mycanvas.create_line(d.start.x, d.start.y, d.end.x, d.end.y,fill=color,smooth=True,width=thick)

     def draw_convexhull(self,convexhull):
        n = len(convexhull.points)
        for i in range(n):
            x1, y1 = convexhull.points[i].x, convexhull.points[i].y
            x2, y2 = convexhull.points[(i+1)%n].x, convexhull.points[(i+1)%n].y
            self.mycanvas.create_line(x1, y1, x2, y2, fill='red', dash=(4,4))



        #清空畫布
     def clean_canvas(self):
             self.mycanvas.delete("all")
             for info in self.right_frame.winfo_children():
                     info.destroy()
             del self.click_data[:]
             del self.segment[:]
             del self.merge[:]
             

     def open_data(self):
             filename = askopenfilename(title = "Select file",filetypes = (("input files",".txt"),("all files",".")))
             self.input_data = InputData.read_file(filename)
             if(self.input_data):
                self.index = 0 #從第0個側資開始
                self.clean_canvas()
                points = self.input_data[0]
                #for i in range(len(self.input_data)):
                   # print(self.input_data[i])
                self.draw_points(points)  
             else:
                 print("read saved data")
                 save_data = Read_SaveData.read_file(filename)
                 self.mycanvas.delete("all")
                 self.draw_points(save_data.points)
                 self.draw_lines(save_data.dividers)
                
                  
             
# play the voronoi function
     def Play(self):
        print('Display the Voronoi')
        self.mycanvas.delete("all")

        #查看是畫布上的點 還是 資料檔
        if (len(self.click_data) == 0 and self.index > len(self.input_data)):
            return

        if (self.index < len(self.input_data)):  
            print("input data")
            points = self.input_data[self.index]
            self.index += 1
        else:
            print("click data")
            points = self.click_data
            # for i in range(len(self.click_data)):
                #print(self.click_data[i])      

        self.voronoi = VoronoiDiagram.Do_Voronoi(points)
        self.draw_points(points)
        self.draw_voronoi()
        
        
        
     def draw_voronoi(self):
        # draw line and point from divider
        for d in self.voronoi.dividers:
            self.mycanvas.create_oval(d.A.x-2, d.A.y-2, d.A.x+2, d.A.y+2, fill='black')
            self.mycanvas.create_oval(d.B.x-2, d.B.y-2, d.B.x+2, d.B.y+2, fill='black')
           # print(d.start.x,d.start.y,d.end.x,d.end.y)
            self.mycanvas.create_line(d.start.x, d.start.y, d.end.x, d.end.y)
    
        # draw point from convexhull
        for p in self.voronoi.convexhull.points:
            self.mycanvas.create_oval(p.x-1, p.y-1, p.x+1, p.y+1, fill='red')
    
        #draw edge from convexhull
        n = len(self.voronoi.convexhull.points)
        for i in range(n):
            x1, y1 = self.voronoi.convexhull.points[i].x, self.voronoi.convexhull.points[i].y
            x2, y2 = self.voronoi.convexhull.points[(i+1)%n].x, self.voronoi.convexhull.points[(i+1)%n].y
            self.mycanvas.create_line(x1, y1, x2, y2, fill='red', dash=(4,4))

            
     def save(self):
        print("save result") 
        f = open("output.txt","w")
        self.voronoi.points.sort(key=cmp_to_key(lambda p1,p2:-1 if(p1.x <= p2.x)or (p1.x == p2.x and p1.y <= p2.y)else 1))

        for p in self.voronoi.points:
            f.write("P %d %d\n" % (p.x,p.y))

        for d in self.voronoi.dividers:
            f.write("E %d %d %d %d\n" % (d.start.x,d.start.y,d.end.x,d.end.y))
        f.close()        
    
     #click_data = 滑鼠點擊
     #input_data = 檔案

    
     def step_by_step(self):
         
         if(len(self.segment)==0 and len(self.merge)==0):
             self.mycanvas.delete("all")
             if (len(self.click_data) == 0 and self.index > len(self.input_data)):
                return
             if (self.index < len(self.input_data)):  
                print("input data")
                points = self.input_data[self.index]
                self.index += 1
             else:
                print("click data")
                points = self.click_data

             self.segment.append((0,points))   
         
         #self.voronoi = VoronoiDiagram.Do_Voronoi(points)
    
         while(not((len(self.merge)==1 and self.merge[-1][0] == 0 or len(self.merge) >= 2 and self.merge[-1][0] == self.merge[-2][0]))):
             flag , points = self.segment.pop()
             #從segment裡面取出分段的點
             if(len(points)<=3):
                 #如果小於3放進merge中(flag相同=左右兩個不同邊)
                 self.merge.append((flag,VoronoiDiagram.Do_Voronoi(points)))
             elif(len(points)>3 and Point.if_collinear(points)):
                 self.merge.append((flag,VoronoiDiagram.Do_Voronoi(points)))
             else:
                 #分左右邊
                 half = int(len(points)/2)
                 points.sort(key=lambda p:p.x)
                 self.segment.append((flag+1,points[half:]))
                 self.segment.append((flag+1,points[:half]))
            
         self.mycanvas.delete("all")

        #
         if(len(self.merge)>=2 and self.merge[-1][0] == self.merge[-2][0]):
             #[-1] = 倒數第一個 [-2] = 倒數第二個
             flag = self.merge[-1][0] -1 #用於合併整合

             right = self.merge.pop()[1] #取出Do_Voronoi的值
             left = self.merge.pop()[1]
             domerge = VoronoiDiagram.do_merge(left,right) #進行merge
             
             self.record_list.append(domerge)
             self.merge.append((flag,domerge))
             #把合併好的存起來
             
             self.draw_points(domerge.left.points,color='blue')
             self.draw_lines(domerge.left.dividers,color='blue')
             self.draw_convexhull(domerge.left.convexhull)
             self.draw_points(domerge.right.points,color='orange')
             self.draw_lines(domerge.right.dividers,color='orange')
             self.draw_convexhull(domerge.right.convexhull)
             self.draw_lines(domerge.hyperplanes,color="red",thick=2)
             
         else:
             self.res = self.merge.pop()[1]
             self.draw_points(self.res.points)
             self.voronoi = VoronoiDiagram.Do_Voronoi(self.res.points)
             self.draw_voronoi()       


window = Interface()
window.mainloop()
