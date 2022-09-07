
#coding=UTF-8


import copy 
import sys
from element import *
from Divider import *
from Convexhull import *

class VoronoiDiagram:
    def __init__(self,points,dividers,convexhull,left=None,right=None,hyperplanes=None):
        self.points = points
        self.dividers = dividers
        self.convexhull = convexhull
        self.left = left
        self.right = right
        self.hyperplanes = hyperplanes
    
    @staticmethod
    def Do_Voronoi(points):

        
        if(len(points)==1):

            return VoronoiDiagram(points,[],Convexhull.Do_convexhull(points))
        
        elif(len(points)==2):

            divider = Divider.Do_divider(points[0],points[1])
            convex =  Convexhull.Do_convexhull(points)
            return VoronoiDiagram(points,[divider],convex)

        elif(len(points)==3):
           
            if(Triangle.Check_Triangle(points[0],points[1],points[2]) == False):
                points.sort(key=lambda p:p.x)
                d1 = Divider.Do_divider(points[0],points[1])
                d2 = Divider.Do_divider(points[1],points[2])
                convex = Convexhull.Do_convexhull(points)
                return VoronoiDiagram(points,[d1,d2],convex)
            
            else:
                print(points[0],points[1],points[2])
                Point.sort_counterclockwisely(points)
                trc = Triangle.circumcenter(points[0],points[1],points[2])
                dividers = []
                for i in range(len(points)):
                
                    d = Divider.Do_divider(points[i],points[(i+1)%3])
                    v1 = Vector.vector_is(points[i],points[(i+1)%3])
                    nv1 = Vector.normal_vector(v1)
                    d.start = Point(trc.x + nv1.dx*600 , trc.y + nv1.dy*600)
                    d.end  = trc
                    if (d.start.y > d.end.y):
                        d.start,d.end = d.end,d.start     
                    dividers.append(d)

                convex = Convexhull.Do_convexhull(points)            
                return VoronoiDiagram(points,dividers,convex)
        
        elif(len(points)>3 and Point.if_collinear(points)):
            divider = []             
            #print("is collinear")
            for i in range(len(points)-1):
                print(points[i],points[i+1])
                d = Divider.Do_divider(points[i],points[i+1])
                divider.append(d)
            convex = Convexhull.Do_convexhull(points)
            return VoronoiDiagram(points,divider,convex)
        



        #>3點
        #分割左右兩邊 最後merge
        points.sort(key=lambda p:p.x)
        half = int(len(points)/2)
        
        l = VoronoiDiagram.Do_Voronoi(points[:half])
        r = VoronoiDiagram.Do_Voronoi(points[half:])
        all_points , merge_divider,merge_convexhull,hyperplanes = VoronoiDiagram.merge(l,r)
        return VoronoiDiagram(all_points,merge_divider,merge_convexhull,l,r,hyperplanes)

    @staticmethod
    def do_merge(l,r):
        all_points , merge_divider,merge_convexhull,hyperplanes = VoronoiDiagram.merge(l,r)
        return VoronoiDiagram(all_points,merge_divider,merge_convexhull,l,r,hyperplanes)

    @staticmethod
    def merge(l,r):
        
        eliminate = []
        left_divider = Divider.list(l.dividers)
        right_divider = Divider.list(r.dividers)
        all_divider = left_divider + right_divider
        all_points = l.points + r.points


        merge_convexhull = Convexhull.divider(l.convexhull,r.convexhull)
        scan = Divider.clone(merge_convexhull.upper) #d.start,d.end(掃描線的中垂線)d.A,d.B(掃描線)
        merge_divider = []
        hyperplanes = []
        prev_point  = None
        prev_divider = None

        if (left_divider[0].start == right_divider[0].start):
        #if (Point.if_lensame(all_points)):
            print("circle")
            d = Divider.Do_divider(merge_convexhull.upper.A,merge_convexhull.upper.B)
            hyperplanes.append(d)
            merge_divider = all_divider + hyperplanes
            return all_points,merge_divider,merge_convexhull,hyperplanes
            

        #由上切線當hyperline的進入點
        while(scan != merge_convexhull.lower):
            intersection_point = None #交點
            candidate = None
            ymin = None
            for d in all_divider :
                if(d == prev_divider): 
                    continue
                intersection = scan.get_point(d)
                if(intersection == None):
                    continue #還沒找到交點
                if(prev_point != None and prev_point.y > intersection.y):
                    #前一個儲存的交點 > 現在的交點
                    continue
                #原點在左上角
                if(ymin == None or intersection.y < ymin):
                    ymin = intersection.y
                    candidate = d        
                    #print("candidate.A is ", candidate.A) 
                    intersection_point = intersection
            if(candidate == None):
                #print("hyperplanes append!")  
                hyperplanes.append(scan)
            
            scan.end = intersection_point
            if(prev_point != None):
                scan.start = prev_point
            hyperplanes.append(scan)

            eliminate.append(candidate)

            #find for next scan
            #print("Find the next scan")
            if(scan.A == candidate.A):
                scan = Divider.Do_divider(scan.B,candidate.B)
                #scan.A = candidate.B
            elif (scan.A == candidate.B):
                scan = Divider.Do_divider(scan.B,candidate.A)
                #scan.A = candidate.A
            elif (scan.B == candidate.A):
                scan = Divider.Do_divider(scan.A,candidate.B)
                #scan.B = candidate.B
            elif (scan.B == candidate.B):
                scan = Divider.Do_divider(scan.A,candidate.A)
                #scan.B == candidate.A  
            else :
                print("Error! next scan") 

            prev_point = intersection_point
            prev_divider = candidate

        scan.start = prev_point
        hyperplanes.append(scan)

        #消線
        for i in range (len(eliminate)):
            e = eliminate[i]
            hp1 = hyperplanes[i]
            hp2 = hyperplanes[i+1]

            if(Vector.cross(hp1.start,hp1.end,hp2.end) >= 0 ) :
                #順時針
                if(Vector.cross(hp1.start,hp1.end,e.start) > 0):
                    #消除多餘的線段
                    for d in all_divider:
                        if(d.start == e.start and d.end != e.end):
                            if (Vector.cross(hp1.end,d.start,d.end)>0):
                                all_divider.remove(d)
                            elif (Vector.cross(hp1.end,d.start,d.end) < 0):
                                if(int(d.end.x)<0):
                                    all_divider.remove(d)
                        elif (d.end == e.start and d.start != e.end):
                            if(Vector.cross(hp1.end,d.end,d.start)>0):
                                all_divider.remove(d)
                            elif(Vector.cross(hp1.end,d.end,d.start)<0):
                               # print(d.start)
                                if(int(d.start.x) < 0):
                                    all_divider.remove(d)
                    
                    e.start = hp1.end
                
                else:
                    for d in all_divider:
                        if (d.start == e.end and d.end != e.start):
                            if(Vector.cross(hp1.end,d.start,d.end)>0):
                                all_divider.remove(d)
                        elif (d.end == e.end and d.start != e.start):
                            if(Vector.cross(hp1.end,d.end,d.start)>0):
                                all_divider.remove(d)
       
                    e.end = hp1.end
                #逆時針
            elif (Vector.cross(hp1.start,hp1.end,hp2.end)<0):
                if(Vector.cross(hp1.start,hp1.end,e.start)<0):
                    
                    for d in all_divider:
                        if(d.start == e.start and d.end != e.end):
                            if(Vector.cross(hp1.end,d.start,d.end)< 0):
                                all_divider.remove(d)
                            elif(Vector.cross(hp1.end,d.start,d.end)> 0):
                                if(int(d.end.x)>600):
                                    all_divider.remove(d)
                        elif(d.end == e.start and d.start != e.end):
                            if(Vector.cross(hp1.end,d.end,d.start) < 0):
                                all_divider.remove(d)
                            elif(Vector.cross(hp1.end,d.end,d.start) > 0):
                                if(int(d.start.x)>600):
                                    all_divider.remove(d)   
                    
                    e.start = hp1.end
                else:
                    
                    for d in all_divider:
                        if(d.start == e.end and d.end != e.start):
                            if(Vector.cross(hp1.end,d.start,d.end) < 0):
                                all_divider.remove(d)
                        elif(d.end == e.end and d.start != e.start):
                            if(Vector.cross(hp1.end,d.end,d.start) < 0):
                                all_divider.remove(d)
                    
                    e.end = hp1.end


        merge_divider += all_divider
        merge_divider += hyperplanes

        return all_points,merge_divider,merge_convexhull,hyperplanes
      










