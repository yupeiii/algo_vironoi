
#coding=UTF-8


from functools import *
import math

class Point:
    def __init__(self,x,y):
        self.x = float(x)
        self.y = float(y)
    
    def __eq__ (self,p):
        if (p == None) :
            return False
        else:
            return ((self.x == p.x) and (self.y == p.y))
    def __str__ (self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    
    @staticmethod
    def midpoint(p1,p2):
        return Point( (p1.x+p2.x)/2.0 , (p1.y+p2.y)/2.0)

    @staticmethod
    def findcenter(points):
       size = float(len(points))
       sum_x = sum([p.x for p in points]) 
       sum_y = sum([p.y for p in points])
       return Point(sum_x/size , sum_y/size)    
 

    @staticmethod
    def sort_counterclockwisely(points):
        center = Point.findcenter(points)
        def counterclockwise_cmp(pa,pb):
            va = (pa.x - center.x, pa.y - center.y)
            vb = (pb.x - center.x, pb.y - center.y)
            return -1 if va[0]*vb[1] - va[1] * vb[0] <= 0 else 1
        points.sort(key = cmp_to_key(counterclockwise_cmp))
    '''
    @staticmethod
    def get_len(p1,p2):
        x = p1.x - p2.x
        y = p1.y - p2.y
        return math.sqrt((x**2)+(y**2))
    
    @staticmethod
    def if_lensame(points):
        pre_len = Point.get_len(points[0],points[1])
        for i in range(len(points)):
            print(pre_len)
            if(Point.get_len(points[i],points[i+1]) != pre_len):
                print(Point.get_len(points[i],points[i+1]))
                return False
        return True      
    '''
    
    @staticmethod
    def calculate_k(p1,p2):
        return (p2.y-p1.y) / (p2.x-p1.x)

    @staticmethod
    def if_collinear(points):

        v1 = Vector.vector_is(points[1],points[0])
        for i in range(2,len(points)):
            v2 = Vector.vector_is(points[i],points[0])
            if(Vector.crossproduct(v1,v2)!=0):
                return False
        return True       

        '''
        x0 = points[0].x
        y0 = points[0].x
        x = points[1].x - x0
        y = points[1].y - y0
        for i in range(2,len(points)):
            xi = points[i].x - x0
            yi = points[i].y - y0
           
            if(x * yi - y * xi):
                
                return False
        return True  
        '''      
        '''
        for p in range (len(points)-1):
            if points[p].x == points[p+1].x:
                return True
            elif points[p].y == points[p+1].y:
                return True
            else:
                pre_k = Point.calculate_k(points[0],points[1])
                curr_k = Point.calculate_k(points[p],points[p+1])
                if(curr_k != pre_k):
                    return False
                else:
                    return True
        '''
            


    
class Vector:
    def __init__ (self,dx,dy):
        self.dx = dx
        self.dy = dy

    def is_zero(self):
        return (self.dx==0 and self.dy==0)

    def crossproduct_with(self,v):
        return Vector.crossproduct(self,v)

    @staticmethod
    def vector_is(start,end):
        return Vector(end.x-start.x,end.y-start.y)

    @staticmethod
    def cross(p1,p2,p3):
        v1 = Vector.vector_is(p1,p2)
        v2 = Vector.vector_is(p1,p3)
        return Vector.crossproduct(v1,v2)

    @staticmethod
    def crossproduct(v1,v2):
        return v1.dx * v2.dy - v1.dy * v2.dx

    @staticmethod
    def normal_vector(v):
        return Vector(-v.dy,v.dx)

class Triangle:
    @staticmethod
    def cal_area(pa,pb,pc):
        x1,y1 = pa.x,pa.y
        x2,y2 = pb.x,pb.y
        x3,y3 = pc.x,pc.y
        return 0.5*abs(pb.x*pc.y+pa.x*pb.y+ pc.x*pa.y - pc.x*pb.y - pb.x*pa.y - pa.x*pc.y)

          
    @staticmethod
    def Check_Triangle(pa,pb,pc):
        x1,y1 = pa.x,pa.y
        x2,y2 = pb.x,pb.y
        x3,y3 = pc.x,pc.y

        a = x1 * (y2-y3) + x2 * (y3-y1) + x3 * (y1-y2)   
        if(a==0):
            return False
        else:
            return True    
    @staticmethod
    def circumcenter(pa,pb,pc):

        x1,y1 = pa.x,pa.y
        x2,y2 = pb.x,pb.y
        x3,y3 = pc.x,pc.y
      
        A = 0.5*((x2-x1)*(y3-y2)-(y2-y1)*(x3-x2))
        if (A==0):
            return 0
        xnum = ((y3-y1)*(y2-y1)*(y3-y2))-((x2**2-x1**2)*(y3-y2)) + (( x3**2-x2**2 )*(y2-y1))
        x = xnum/(-4*A)
        try:
            y = (-1*(x2-x1) / (y2-y1 ) ) * (x-0.5*(x1+x2))+0.5*(y1+y2)
          
        except ZeroDivisionError:
            v1 = Vector.vector_is(pa,pb)
            v2 =  Vector.vector_is(pa,pc)
            mid1 = Point.midpoint(pa,pb)
            mid2 = Point.midpoint(pa,pc)
            constant_v1 = v1.dx*mid1.x + v1.dy*mid1.y
            constant_v2 = v2.dx*mid2.x + v2.dy*mid2.y

            delta = v1.dx * v2.dy - v1.dy * v2.dx
            delta_x = constant_v1 * v2.dy - v1.dy * constant_v2
            delta_y = v1.dx * constant_v2 - constant_v1*v2.dx
            if delta == 0 :
                return 0
            else:
                x = int(delta_x/delta)
                y = int(delta_y/delta)

 
        #print(x,y)
        return Point(x,y)
