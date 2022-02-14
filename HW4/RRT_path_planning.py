# Cody Houff


import random, math, copy

iterations = 1000
x_dim = 10
y_dim = 10
start_node = [1,1]
end_node = [9,9]
nodes = [start_node]
#nodes[0] = [1,1]
paths = [[start_node]]
solution_paths = []
sq_pts = [(3,7),(7,7),(3,3),(7,3)]
#array1 = array1 + [elapsed_time]
i = 0
sq_pt1 = sq_pts[0]
sq_pt2 = sq_pts[1]
sq_pt3 = sq_pts[2]
sq_pt4 = sq_pts[3]

#node_paths = [ [[1,1],[2,2]], [[1,1],[3,3]] ]

# A Python3 program to find if 2 given line segments intersect or not
def dist(p1,p2):
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def onSegment(p, q, r):
    if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
           (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
        return True
    return False
 
def orientation(p, q, r):    
    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
    if (val > 0): 
        return 1  # Clockwise orientation
    elif (val < 0):  
        return 2 # Counterclockwise orientation
    else:
        return 0 # Collinear orientation
 
def test_intersect(p1,q1,p2,q2): # true if the line segment 'p1q1' and 'p2q2' intersect.
     
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if ((o1 != o2) and (o3 != o4)): # General case
        return True
 
    if ((o1 == 0) and onSegment(p1, p2, q1)): # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        return True

    if ((o2 == 0) and onSegment(p1, q2, q1)): # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        return True
 
    if ((o3 == 0) and onSegment(p2, p1, q2)): # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        return True

    if ((o4 == 0) and onSegment(p2, q1, q2)): # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        return True

    return False # If none of the cases

def add_node_paths(paths,closest_node,rand):
    for path in paths:
        if (path[-1] == closest_node):
            new_path = copy.deepcopy(path)
            new_path = new_path + [rand]
            paths = paths + [new_path]
            break
    #print("add_node_paths: done")
    return paths

def check_path_to_end(sq_pt, paths, end_node, solution_paths):
    existing_path = paths[-1]
    i = 0
    intersect = False
    for sq_pt in sq_pts:
        if(i==0):
            prev_pt = sq_pts[3]
            
        if (test_intersect(prev_pt, sq_pt, existing_path[-1], end_node)):
            intersect = True
            #print("intersect: True")
            break
      
        prev_pt = sq_pt
        i=i+1
            
        
    if (intersect == False):
        #print("end path works")

        new_path = copy.deepcopy(existing_path)
        new_path = new_path + [end_node]
        paths = paths + [new_path]
        solution_paths = solution_paths + [new_path]
        
            
    return paths, solution_paths
            

for j in range(iterations):

    #print("j: ",j)
    rand = [random.random()*x_dim, random.random()*y_dim]

    #print("rand:",rand)
    if(rand[0]>sq_pt1[0] and rand[0]<sq_pt4[0] and rand[1]<sq_pt1[1] and rand[1]>sq_pt4[1]):
        rand = end_node
        

    #print("rand:",rand)

    closest_node = [1,1]
    if (rand not in nodes):
        for node in nodes:
             #print("node: ", node)
            if (dist([node[0],node[1]],[rand[0],rand[1]]) < dist([closest_node[0],closest_node[1]],[rand[0],rand[1]])):
                closest_node = [node[0],node[1]]

        #print("closest_node: ",closest_node)
        i = 0
        intersect = False
        for sq_pt in sq_pts:
            if(i==0):
                prev_pt = sq_pts[3]
                
            if (test_intersect(prev_pt, sq_pt, closest_node, rand)):
                intersect = True
                #print("intersect: True")
                break
          
            prev_pt = sq_pt
            i=i+1
            
        if (intersect == False):
            #print("intersect: False")
            if(closest_node != end_node):
                nodes = nodes + [rand]
                paths = add_node_paths(paths,closest_node,rand)
         
                #print("try for end path")
                paths, solution_paths = check_path_to_end(sq_pt, paths, end_node, solution_paths)
                #print("paths: ",paths)

        #print("j: ",j)
        #print("nodes: ",nodes)
        #print("solution_paths: ",solution_paths)
   
       
print(len(solution_paths))
print(solution_paths)

best_solution = []
existing_dist_total = 1000
dist_total = 0

#solution_paths = [[[1.0, 1.0], [0.5178568060313504, 8.033679863661146], [9.321233931106182, 9.003334474359534], [5.378995378707076, 8.273015817220085], [6.881788049088911, 8.447529416734865], [9, 9]]]


for solution in solution_paths:
    i = 0
    #print("solution: ",solution)
    for pt in solution:
        if(i>0):
            #print("pt: ",pt)
            #print("prev_pt: ",prev_pt)
            distance = dist(prev_pt,pt)
            dist_total = dist_total + distance
            
        prev_pt = pt
        i = i+1
    #print("dist_total: ",dist_total)
    if (dist_total<existing_dist_total):
        best_solution = solution
        existing_dist_total = dist_total
        #print(existing_dist_total)
    dist_total = 0
    distance = 0
print(best_solution)
        


    





