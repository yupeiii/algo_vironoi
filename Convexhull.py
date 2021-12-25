
#coding=UTF-8
#學號: M103140007
#系級: 資安碩碩一
#姓名 :林郁珮

from element import *
from Divider import *

class Convexhull:
    def __init__(self,points,upper=None,lower=None):
        self.points = points
        self.upper = upper
        self.lower = lower
    
    @staticmethod
    def Do_convexhull(points):
       #三點以下直接把點連在一起 兩點=直線 三點=三角形
       if len(points) <= 3:
           Point.sort_counterclockwisely(points)
           #print(points)
           return Convexhull(points)
       elif(len(points)>3 and Point.if_collinear(points)) :
           Point.sort_counterclockwisely(points)
           return Convexhull(points) 
       points.sort(key=lambda p: [p.y,p.x]) #由x排序小到大
       half = int(len(points)/2)
       c_l = Convexhull.Do_convexhull(points[:half])
       c_r = Convexhull.Do_convexhull(points[half:])
       return Convexhull.divider(c_l,c_r)
    
    @staticmethod
    def divider(c_l,c_r):
        p_up,q_up,p_low,q_low,points = Convexhull.merge(c_l,c_r)
        d_up = Divider.Do_divider(p_up,q_up) #upperline 的中垂線
        d_low = Divider.Do_divider(p_low,q_low) #lowerline的中垂腺
        return Convexhull(points,upper=d_up,lower = d_low)
    @staticmethod
    def if_leftturn(p1,p2,p3):
        v1 = Vector.vector_is(p1,p2)
        v2 = Vector.vector_is(p1,p3)
        return Vector.crossproduct(v1,v2) < 0
    
    @staticmethod
    def if_rightturn(p1,p2,p3):
        v1 = Vector.vector_is(p1,p2)
        v2 = Vector.vector_is(p1,p3)
        return Vector.crossproduct(v1,v2) > 0

    @staticmethod
    def merge(c_l,c_r):

        Point.sort_counterclockwisely(c_l.points)
        Point.sort_counterclockwisely(c_r.points)
        p = c_l.points.index(max(c_l.points,key = lambda p:p.x))
        q = c_r.points.index(min(c_r.points,key = lambda p:p.x))

        plen = len(c_l.points)
        qlen = len(c_r.points)
        copy_p = p 
        copy_q = q 

        #upper
        prev_p = None
        prev_q = None

        while(1):
            prev_p = p 
            prev_q = q  
            while (Convexhull.if_leftturn(c_l.points[p],c_r.points[q],c_r.points[(q-1+qlen)%qlen])): #c_r的點由逆時針排序 因此要找尋的下一個順時針的點 = 上一個index
                q = (q-1+qlen)%qlen
            while (Convexhull.if_rightturn(c_r.points[q],c_l.points[p],c_l.points[(p+1+plen)%plen])) :  #c_l的點由逆時針排序 因此要找尋的下一個逆時針點=下一個index
                p = (p+1+plen)%plen
            if p == prev_p and q == prev_q :
                break
        
        #lower
        prev_p = None
        prev_q = None
        while(1):
            prev_p = copy_p
            prev_q = copy_q 
            while (Convexhull.if_rightturn(c_l.points[copy_p],c_r.points[copy_q],c_r.points[(copy_q+1+qlen)%qlen])):
                copy_q = (copy_q+1+qlen)%qlen
            while (Convexhull.if_leftturn(c_r.points[copy_q],c_l.points[copy_p],c_l.points[(copy_p-1+plen)%plen])):
                copy_p = (copy_p-1+plen)%plen
            if copy_p == prev_p and copy_q == prev_q:
                break

        result = []
        #[:X] = 前X項 [x:]從第x個開始取
        if(copy_p < p):
            result += c_l.points[:copy_p+1]+c_l.points[p:]
        else:
            result += c_l.points[p:copy_p+1]

        if(q < copy_q):
            result += c_r.points[:q+1] + c_r.points[copy_q:]
        else: 
            result += c_r.points[copy_q:q+1]

        Point.sort_counterclockwisely(result)
        return (c_l.points[p],c_r.points[q],c_l.points[copy_p],c_r.points[copy_q],result)
        


