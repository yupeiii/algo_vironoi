#coding=UTF-8


from element import *

class Divider:
    def __init__(self,start,end,A,B):
        
        self.A = A
        self.B = B 
        if(start.y < end.y or (start.y == end.y and start.x < end.x)):
            self.start =start
            self.end = end
        else:
            self.start = end
            self.end = start
    
    def __ne__ (self,other): #not equal
        if(other == None):
            return True
        if (self.A == other.A and self.B == other.B):
            return False
        if(self.A == other.B and self.B == other.A):
            return False
        return True
  
    def clone(d):
        return Divider(d.start,d.end,d.A,d.B)
    
    def list(l):
        return [Divider(d.start,d.end,d.A,d.B) for d in l]

    #找交點
    def get_point(self,d2):
        if(self.start == d2.start or self.start == d2.end):
            return self.start
        if(self.end == d2.start or self.end == d2.end):
            return self.end
        
        v1 = Vector.vector_is(self.start,self.end)
        v2 = Vector.vector_is(d2.start,d2.end)
        v3 = Vector.vector_is(self.start,d2.start)
        v4 = Vector.vector_is(d2.start,self.start)

        c1 = Vector.crossproduct_with(v1,v2)
        c2 = Vector.crossproduct_with(v3,v2)
        c3 = Vector.crossproduct_with(v2,v1)
        c4 = Vector.crossproduct_with(v4,v1)

        if(c1 < 0):
            c1 = -c1
            c2 = -c2
        if(c3 < 0):
            c3 = -c3
            c4 = -c4
        
        if(c2 >= 0 and c2 <= c1 and c4 >= 0 and c4 <= c3):
           
            x = self.start.x + v1.dx*c2/c1
            y = self.start.y + v1.dy*c2/c1

            return Point(x,y)
        return None 

    def Do_divider(p1,p2):
        midp = Point.midpoint(p1,p2)
        v1 = Vector.vector_is(p1,p2)
        nv1 = Vector.normal_vector(v1)
        p_start = Point(midp.x+nv1.dx*600 , midp.y+nv1.dy*600)
        p_end  = Point(midp.x-nv1.dx*600 , midp.y-nv1.dy*600)
        return Divider(p_start,p_end,p1,p2)
    
