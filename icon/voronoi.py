import sys
import copy


class VoronoiDiagram:
    def __init__(self,points,bisector,convexhull,left=None,right=None,hyperplanes=None):
        self.points = points
        self.bisector = bisector
        self.convexhull = convexhull
        self.left = left
        self.right = right
        self.hyperplanes = hyperplanes

    @staticmethod
    def Voronoi_Point(points,debug = None):
        if(len(points)==1):
            return VoronoiDiagram(points,[],Convexhull.convexhull_of(points))
        elif (len(points)==2):
            divider = Divider.divider_of(points[0],points[1])
            convex = ConvesHull.convexhull_of(points)
            return VoronoiDiagram(points,[divider],convex)


        points.sort(key=lambda p: p.x)
		half = int(len(points) / 2)
		vleft = VoronoiDiagram.voronoi_Point(points[:half])
		vright = VoronoiDiagram.voronoi_Point(points[half:])
		mpoints, mdividers, mconvexhull, hyperplanes = VoronoiDiagram.merge(vleft, vright, debug=debug)
		return VoronoiDiagram(mpoints, mdividers, mconvexhull, vleft, vright, hyperplanes)

    @staticmethod
	def voronoi_merge(left, right, debug=None):
		mpoints, mdividers, mconvexhull, hyperplanes = VoronoiDiagram.merge(left, right)
		# debug.draw_dividers(hyperplanes)
		return VoronoiDiagram(mpoints, mdividers, mconvexhull, left, right, hyperplanes)

	@staticmethod
	def merge(vleft, vright, debug=None):
		mpoints, mdividers, hyperplanes = vleft.points + vright.points, [], []
		mconvexhull = ConvexHull.convexhull_merge(vleft.convexhull, vright.convexhull)

		# Hyperplane
		need_trim = []
		ldividers = Divider.copy_list(vleft.dividers)
		rdividers = Divider.copy_list(vright.dividers)
		candidates = ldividers + rdividers
		curr = Divider.copy(mconvexhull.upper)
		pre_point, pre_divider = None, None
		while (curr != mconvexhull.lower):
			ymin, d_candidate, d_inpoint = None, None, None
			for d in candidates:
				if (d == pre_divider):
					continue
				inpoint = curr.get_inpoint_with(d)
				if (inpoint == None):
					continue
				if (pre_point != None and pre_point.y > inpoint.y):
					continue
				if (ymin == None or inpoint.y < ymin):
					ymin, d_candidate, d_inpoint = inpoint.y, d, inpoint
			if (d_candidate == None):
				print("append curr")
				hyperplanes.append(curr)
			
			curr.end = d_inpoint
			if (pre_point != None):
				curr.start = pre_point
			hyperplanes.append(curr)
			# debug.draw_dividers([curr])
			# debug.draw_dividers([d_candidate], 'green')
			need_trim.append(d_candidate)
			
			if (curr.A == d_candidate.A):
				curr = Divider.divider_of(curr.B, d_candidate.B)
			elif (curr.A == d_candidate.B):
				curr = Divider.divider_of(curr.B, d_candidate.A)
			elif (curr.B == d_candidate.A):
				curr = Divider.divider_of(curr.A, d_candidate.B)
			elif (curr.B == d_candidate.B):
				curr = Divider.divider_of(curr.A, d_candidate.A)
			else:
				print("Error! next_curr")
			pre_point, pre_divider = d_inpoint, d_candidate
		curr.start = pre_point
		hyperplanes.append(curr)
		
		
		# if (debug != None):
			# debug.draw_dividers(hyperplanes)
			# input()
		
		#trim divider and delete redundant line
		for i in range(len(need_trim)):
			d = need_trim[i]
			hp1, hp2 = hyperplanes[i], hyperplanes[i+1]
			if (Vector.cross(hp1.start, hp1.end, hp2.end) >= 0): # clockwise
				#divider d.start is over 180 degree with hyperplane
				if (Vector.cross(hp1.start, hp1.end, d.start) > 0):
					#check if any line is interscet with d.start
					for c in candidates:
						if (d.start == c.start and d.end != c.end):
							if (Vector.cross(hp1.end, c.start, c.end) > 0):
								candidates.remove(c)
						elif (d.start == c.end and d.end != c.start):
							if (Vector.cross(hp1.end, c.end, c.start) > 0):
								candidates.remove(c)
					d.start = hp1.end
				#divider d.end is over 180 degree with hyperplane
				else:
					for c in candidates:
						#check if any line is interscet with d.end
						if (d.end == c.start and d.start != c.end):
							if (Vector.cross(hp1.end, c.start, c.end) > 0):
								candidates.remove(c)
						elif (d.end == c.end and d.start != c.start):
							if (Vector.cross(hp1.end, c.end, c.start) > 0):
								candidates.remove(c)
					d.end = hp1.end
			else: #counterclockwise
				#divider d.end is over 180 degree with hyperplane
				if (Vector.cross(hp1.start, hp1.end, d.start) < 0):
					for c in candidates:
						#check if any line is interscet with d.start
						if (d.start == c.start and d.end != c.end):
							if (Vector.cross(hp1.end, c.start, c.end) < 0):
								candidates.remove(c)
						elif (d.start == c.end and d.end != c.start):
							if (Vector.cross(hp1.end, c.end, c.start) < 0):
								candidates.remove(c)
					d.start = hp1.end
				#divider d.end is over 180 degree with hyperplane
				else:
					for c in candidates:
						#check if any line is interscet with d.end
						if (d.end == c.start and d.start != c.end):
							if (Vector.cross(hp1.end, c.start, c.end) < 0):
								candidates.remove(c)
						elif (d.end == c.end and d.start != c.start):
							if (Vector.cross(hp1.end, c.end, c.start) < 0):
								candidates.remove(c)
					d.end = hp1.end

		mdividers += candidates
		mdividers += hyperplanes

		return mpoints, mdividers, mconvexhull, hyperplanes