'''
 CS 7649 Robot Intelligence: Planning
 PSet1
 Cody Houff: Partnered with Jeremy Collins
'''
import time


graph = {
        'AL': ('MS', 'TN', 'GA', 'FL'),
        'AZ': ('CA', 'NV', 'UT', 'NM'),
        'AR': ('MO', 'TN', 'MS', 'LA', 'TX', 'OK'),
        'CA': ('OR', 'NV', 'AZ'),
        'CO': ('WY', 'NE', 'KS', 'OK', 'NM', 'UT'),
        'CT': ('NY', 'MA', 'RI'),
        'DE': ('NJ', 'PA', 'MD'),
        'DC': ('MD', 'VA'),
        'FL': ('AL', 'GA'),
        'GA': ('TN', 'NC', 'SC', 'FL', 'AL'),
        'ID': ('WA', 'MT', 'WY', 'UT', 'NV', 'OR'),
        'IL': ('WI', 'IN', 'KY', 'MO', 'IA'),
        'IN': ('MI', 'OH', 'KY', 'IL'),
        'IA': ('MN', 'WI', 'IL', 'MO', 'NE', 'SD'),
        'KS': ('NE', 'MO', 'OK', 'CO'),
        'KY': ('IN', 'OH', 'WV', 'VA', 'TN', 'MO', 'IL'),
        'LA': ('AR', 'MS', 'TX'),
        'ME': ('NH',),
        'MD': ('PA', 'DE', 'DC', 'VA', 'WV'),
        'MA': ('NH', 'RI', 'CT', 'NY', 'VT'),
        'MI': ('OH', 'IN', 'WI'),
        'MN': ('WI', 'IA', 'SD', 'ND'),
        'MS': ('TN', 'AL', 'LA', 'AR'),
        'MO': ('NE', 'IA', 'IL', 'KY', 'TN', 'AR', 'OK', 'KS'),
        'MT': ('ND', 'SD', 'WY', 'ID'),
        'NE': ('SD', 'IA', 'MO', 'KS', 'CO', 'WY'),
        'NV': ('OR', 'ID', 'UT', 'AZ', 'CA'),
        'NH': ('ME', 'MA', 'VT'),
        'NJ': ('NY', 'DE', 'PA'),
        'NM': ('CO', 'OK', 'TX', 'AZ'),
        'NY': ('VT', 'MA', 'CT', 'NJ', 'PA'),
        'NC': ('VA', 'SC', 'GA', 'TN'),
        'ND': ('MN', 'SD', 'MT'),
        'OH': ('PA', 'WV', 'KY', 'IN', 'MI'),
        'OK': ('KS', 'MO', 'AR', 'TX', 'NM', 'CO'),
        'OR': ('WA', 'ID', 'NV', 'CA'),
        'PA': ('NY', 'NJ', 'DE', 'MD', 'WV', 'OH'),
        'RI': ('MA', 'CT'),
        'SC': ('NC', 'GA'),
        'SD': ('ND', 'MN', 'IA', 'NE', 'WY', 'MT'),
        'TN': ('KY', 'VA', 'NC', 'GA', 'AL', 'MS', 'AR', 'MO'),
        'TX': ('NM', 'OK', 'AR', 'LA'),
        'UT': ('ID', 'WY', 'CO', 'AZ', 'NV'),
        'VT': ('NH', 'MA', 'NY'),
        'VA': ('WV', 'MD', 'DC', 'NC', 'TN', 'KY'),
        'WA': ('ID', 'OR'),
        'WV': ('OH', 'PA', 'MD', 'VA', 'KY'),
        'WI': ('MI', 'IL', 'IA', 'MN'),
        'WY': ('MT', 'SD', 'NE', 'CO', 'UT', 'ID')
}

# breadth first search no visited list (most up to date)


def bfs_no_visit(graph, start, goal):
        start_time = time.time()
        pop_count = 0;
        queue_length = 0;
        queue = [[start]];
        N = start;
        while queue:
                #print("queue = ", queue)
                if(len(queue)>queue_length):
                        queue_length = len(queue);
                        
                path = queue.pop(0)
                pop_count = pop_count+1;
                N = path[-1]
                #print("N = ",N)
                #print("queue after popping = ", queue)
                # print("vertex = ",vertex)
                #print("path = ", path)

                for next in sorted(graph[N]):  
                        if N == goal:

                                print("bfs no visited list")
                                print("time = %.5f (s)" % (time.time() - start_time))
                                print(path)
                                print("pop count = ", pop_count)
                                print("max length of queue = ", queue_length)
                                print("length of path to goal = ", len(path)-1)
                                print(" ")
                                return 0
                        else:
                                queue.append((path + [next]))

                # print("queue after append = ",queue)

def bfs_visit(graph, start, goal):
        start_time = time.time()
        visited = [];
        pop_count = 0;
        queue_length = 0;
        queue = [[start]];
        N = start;
        visited.append(([N]))
        while queue:
                #print("queue = ", queue)
                if(len(queue)>queue_length):
                        queue_length = len(queue);
                   
                path = queue.pop(0)
                pop_count = pop_count+1;
                N = path[-1] 
                #print("queue after popping = ", queue)
                #print("N = ",N)
                #print("path = ", path)

                for next in sorted(graph[N]):  # - set(path):
                        if N == goal:

                                print("bfs visited list")
                                print("time = %.5f (s)" % (time.time() - start_time))
                                print(path)
                                print("pop count = ", pop_count)
                                print("max length of queue = ", queue_length)
                                print("length of path to goal = ", len(path)-1)
                                print(" ")
                                return 0
                        else:
                                #print("[next] = ",[next])
                                if not [next] in visited:
                                        visited.append(([next]))
                                        queue.append((path + [next]))

                #print("queue after append = ",queue)
                #print("visited list = ",visited)

def dfs_no_visit(graph, start, goal):
        start_time = time.time()
        pop_count = 0;
        queue_length = 0;
        queue = [[start]];
        N = start;
        while queue:
                #print("queue = ", queue)
                if(len(queue)>queue_length):
                        queue_length = len(queue);
                   
                path = queue.pop(0)
                pop_count = pop_count+1;
                N = path[-1] 
                #print("queue after popping = ", queue)
                print("N = ",N)
                #print("path = ", path)

                for next in sorted(graph[N], reverse=True):
                        if N == goal:

                                print("dfs no visited list")
                                print("time = %.5f (s)" % (time.time() - start_time))
                                print(path)
                                print("pop count = ", pop_count)
                                print("max length of queue = ", queue_length)
                                print("length of path to goal = ", len(path)-1)
                                print(" ")
                                return 0
                        else:
                                #print("[next] = ",[next])
                                queue.insert(0, path+[next])

                #print("queue after append = ",queue)
                #print("visited list = ",visited)
                
def dfs_visit(graph, start, goal):
        start_time = time.time()
        visited = [];
        pop_count = 0;
        queue_length = 0;
        queue = [[start]];
        N = start;
        visited.append(([N]))
        while queue:
                print("queue = ", queue)
                if(len(queue)>queue_length):
                        queue_length = len(queue);
                   
                path = queue.pop(0)
                pop_count = pop_count+1;
                N = path[-1] 
                print("queue after popping = ", queue)
                print("N = ",N)
                print("path = ", path)

                for next in sorted(graph[N], reverse=True):
                        if N == goal:

                                print("dfs visited list")
                                print("time = %.5f (s)" % (time.time() - start_time))
                                print(path)
                                print("pop count = ", pop_count)
                                print("max length of queue = ", queue_length)
                                print("length of path to goal = ", len(path)-1)
                                print(" ")
                                return 0
                        else:
 
                                if not [next] in visited:
                                        visited = [[next]]+visited
                                        queue.insert(0, path+[next])

                print("queue after append = ",queue)
                print("visited list = ",visited)
                print(" ")

def ids_visit(graph, start, goal):

        depth = 1;
        start_time = time.time()
        pop_count = 0;
        queue_length = 0;
        while True:

                goal_reached = False;        
                visited = [];
                i = 1;
                queue = [[start]];
                N = start;
                visited.append(([N]))
                while queue:
                        #print("queue = ", queue)
                        if(len(queue)>queue_length):
                                queue_length = len(queue);
                           
                        path = queue.pop(0)
                        pop_count = pop_count+1;
                        N = path[-1] 
                        #print("queue after popping = ", queue)
                        #print("N = ",N)
                        #print("path = ", path)

                        for next in sorted(graph[N], reverse=True):
                                if N == goal:
                                        goal_reached = True;
                                        final_path = path; 
                                if (queue == [] and goal_reached == True):

                                        print("dfs visited list")
                                        print("time = %.5f (s)" % (time.time() - start_time))
                                        print(final_path)
                                        print("pop count = ", pop_count)
                                        print("max length of queue = ", queue_length)
                                        print("length of path to goal = ", len(final_path)-1)
                                        print(" ")
                                        return 0
                                else:
                                        if(len(path)<depth+1):
                                                if not [next] in visited:
                                                        visited = [[next]]+visited
                                                        queue.insert(0, path+[next])

                        #print("queue after append = ",queue)
                        #print("visited list = ",visited)
                        #print("depth = ",depth) 
                        #print(" ") 
                                                
                        #reset queue and visited list
                        if (queue == []):
                                depth = depth+1;
                                visited = [];
                                queue = [];
                                #print("_________________________________________")
                                break
                                
def ids_no_visit(graph, start, goal):

        depth = 1;
        start_time = time.time()
        pop_count = 0;
        queue_length = 0;
        while True:

                goal_reached = False;        
                i = 1;
                queue = [[start]];
                N = start;
                while queue:
                        #print("queue = ", queue)
                        if(len(queue)>queue_length):
                                queue_length = len(queue);
                           
                        path = queue.pop(0)
                        pop_count = pop_count+1;
                        N = path[-1] 
                        #print("queue after popping = ", queue)
                        #print("N = ",N)
                        #print("path = ", path)

                        for next in sorted(graph[N], reverse=True):
                                if N == goal:
                                        goal_reached = True;
                                        final_path = path; 
                                if (queue == [] and goal_reached == True):

                                        print("dfs no visited list")
                                        print("time = %.5f (s)" % (time.time() - start_time))
                                        print(final_path)
                                        print("pop count = ", pop_count)
                                        print("max length of queue = ", queue_length)
                                        print("length of path to goal = ", len(final_path)-1)
                                        print(" ")
                                        return 0
                                else:
                                        if(len(path)<depth+1):
                                                queue.insert(0, path+[next])

                        #print("queue after append = ",queue)
                        #print("visited list = ",visited)
                        #print("depth = ",depth) 
                        #print(" ") 
                                                
                        #reset queue and visited list
                        if (queue == []):
                                depth = depth+1;
                                queue = [];
                                #print("_________________________________________")
                                break
                                

                


#bfs_visit(graph, 'WA', 'GA')

#bfs_no_visit(graph, 'WA', 'GA')

#dfs_visit(graph, 'WA', 'GA') 

dfs_no_visit(graph, 'WA', 'GA')

ids_visit(graph, 'WA', 'GA')

ids_no_visit(graph, 'WA', 'GA')





