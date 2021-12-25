@staticmethod
    def cmerge(c_l,c_r):
        pu,qu,pl,ql,points = Convexhull.merge(c_l,c_r)
        du = Divider.Do_divider(pu,qu)
        dl = Divider.Do_divider(pl,ql)
        return Convexhull(points,upper=du,lower=dl)

    @staticmethod
    def clockwise(p1,p2,p3):
        v1 = Vector.vector_is(p1,p2)
        v2 = Vector.vector_is(p1,p3)
        return Vector.crossproduct_with(v1,v2) > 0
    
    @staticmethod 
    def counterclockwise(p1,p2,p3):
        v1 = Vector.vector_is(p1,p2)
        v2 = Vector.vector_is(p1,p3)
        return Vector.crossproduct_of(v1,v2) < 0
    @staticmethod
    def merge(c_l,c_r):
	    Point.sort_counterclockwisely(cl.points)
	    Point.sort_counterclockwisely(cr.points)
	    pi = cl.points.index(max(cl.points, key=lambda p: p.x))
	    qi = cr.points.index(min(cr.points, key=lambda p: p.x))
	    pn, qn = len(cl.points), len(cr.points)
		

	    # upper
	    prev_p = None
	    prev_q = None
	    pu, qu = pi, qi
	    while (True):
	        prev_p, prev_q = pu, qu
	        while (ConvexHull.counterclockwise(cl.points[pu], cr.points[qu], cr.points[(qu-1+qn)%qn])):
	            qu = (qu-1+qn)%qn
			
	        while (ConvexHull.clockwise(cr.points[qu], cl.points[pu], cl.points[(pu+1+pn)%pn])):
	            pu = (pu+1+pn)%pn

	        if pu == prev_p and qu == prev_q:
	            break

		
	    #lower
	    prev_p = None
	    prev_q = None
	    pl, ql = pi, qi
	    while (True):
	        prev_p, prev_q = pl, ql
	        while (ConvexHull.counterclockwise(cr.points[ql], cl.points[pl], cl.points[(pl-1+pn)%pn])):
	            pl = (pl-1+pn)%pn

	        while (ConvexHull.clockwise(cl.points[pl], cr.points[ql], cr.points[(ql+1+qn)%qn])):
	            ql = (ql+1+qn)%qn

	        if pl == prev_p and ql == prev_q:
	            break

	    res = []
		#upper index is bigger to lower for left and right
	    if (pl < pu):
	        res += cl.points[:pl+1] + cl.points[pu:]
	    else:
	        res += cl.points[pu:pl+1]
		
	    if (qu < ql):
	        res += cr.points[:qu+1] + cr.points[ql:]
	    else:
		    res += cr.points[ql:qu+1]

	    Point.sort_counterclockwisely(res)

	    return (cl.points[pu], cr.points[qu], cl.points[pl], cr.points[ql], res)        
	