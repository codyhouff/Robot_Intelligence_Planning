import random
from timeit import default_timer as timer

dim = 0                 # dimension of the locations (n value)
locations = []              
str_conf = []      # straight conflicts
diag_right_conf = []    # right diagonal conflicts
diag_left_conf = []    # left diagonal conflicts
max_n = 3374
array1 = []
array2 = []

def change_conf(col, row, val, locations, str_conf, diag_right_conf, diag_left_conf):
    str_conf[row]+= val
    diag_right_conf[col+row]+= val
    diag_left_conf[col+(dim-row-1)]+= val

def min_conf(col):
    min_confs = dim
    min_conf_rows = []
    for row in range(dim):       
        conflicts = str_conf[row] + diag_right_conf[col+row] + diag_left_conf[col+(dim-row-1)] # calculate the number of conflicts 
        
        if conflicts == 0:  # if there are no conflicts in a row, return that row value
            return row
        
        if conflicts < min_confs:  # if the number of conflicts is less, change it to the min_confs_rows
            min_conf_rows = [row]
            min_confs = conflicts
        
        elif conflicts == min_confs:  # if the number of conflicts is equal, add onto the min_conf_rows
            min_conf_rows.append(row)
    
    row_choice = random.choice(min_conf_rows)  # if tie, randomly choose the row
    return row_choice


def create_locations():  # sets up the locations using a greedy algorithm
    #global locations
    #global str_conf
    #global diag_right_conf
    #global diag_left_conf

    locations = [] 
    diag_right_conf = [0]*((2*dim)-1)
    diag_left_conf = [0]*((2*dim)-1)
    str_conf = [0]*dim   
    row_values = set(range(0,dim)) # set of all possible row values   
    col_open = [] # open columns

    for col in range(0, dim):       
        row_test = row_values.pop() # Pop the next possible row location to test        
        conflicts = str_conf[row_test] + diag_right_conf[col+row_test] + diag_left_conf[col+(dim-row_test-1)] # calculate the conflicts 
        
        if conflicts == 0: # if no conflicts, place a queen
            locations.append(row_test)
            change_conf(col, locations[col], 1, locations, str_conf, diag_right_conf, diag_left_conf)
        
        else:  # if a conflict is found           
            row_values.add(row_test) # Place the potential row to the back of the row values           
            row_test2 = row_values.pop() # use the next row from the row values to test            
            conflicts2 = str_conf[row_test2] + diag_right_conf[col+row_test2] + diag_left_conf[col+(dim-row_test2-1)]  # calculate the conflicts
            
            if conflicts2 == 0: # if no conflicts, place a queen 
                locations.append(row_test2)
                change_conf(col, locations[col], 1, locations, str_conf, diag_right_conf, diag_left_conf)
            else:               
                row_values.add(row_test2) # add the possible row back to the row values 
                locations.append(None) # add a None to the locations as a place holder                 
                col_open.append(col)  # column that was not placed

    for col in col_open:       
        locations[col] = row_values.pop()  # place the remaining queen locations       
        change_conf(col, locations[col], 1, locations, str_conf, diag_right_conf, diag_left_conf) # update the conflict lists

    return locations, str_conf, diag_right_conf, diag_left_conf


# Finds the column with the most conflicts
def max_conf(locations, str_conf, diag_right_conf, diag_left_conf):
    conflicts = 0
    max_confs = 0
    max_conf_cols = []

    for col in range(0,dim):           
        row = locations[col] # determine the row value for the current column           
        conflicts = str_conf[row] + diag_right_conf[col+row] + diag_left_conf[col+(dim-row-1)] # calculate the number of conflicts using the conflict lists
           
        if (conflicts > max_confs):   # if conflicts are greater than the current max, make that column the maximum
            max_conf_cols = [col]
            max_confs = conflicts
        
        elif conflicts == max_confs:  # if the conflicts equal the current max, add the value to the max_conf_cols list
            max_conf_cols.append(col)
    
    col_choice = random.choice(max_conf_cols)  # if tied, randomly choose
    return col_choice, max_confs


# sets up the locations using create_locations() and then solves it with a iterative repair (min conflict)
def solve():
    create_locations()
    print(locations)
    i = 0
    max_i = 0.6*dim    # max iterations

    while (i < max_i):       
        col, num_confs = max_conf(locations, str_conf, diag_right_conf, diag_left_conf) # Calculate the maximum conflicting column and the number of conflicts it contains
        
        if (num_confs > 3):  # if the number of conflicts is greater than 3 there are conflicts       
            new_location = min_conf(col) # used to find the row with the least number of conflicts
            
            if (new_location != locations[col]):  # if the better location is found switch location
                change_conf(col, locations[col], -1, locations, str_conf, diag_right_conf, diag_left_conf) # Remove the conflict moving away
                locations[col] = new_location  # add a conflict if queen is moving in        
                change_conf(col, new_location, 1, locations, str_conf, diag_right_conf, diag_left_conf)
  
        elif num_confs == 3: # if the max number of conflicts is 3, there are no conflicts
            return True  # solution is found
        i+=1    
    return False  # If no solution is found, return False

for n in range(1,max_n+1):
    dim = n    
    start_time = timer()  # Start timer 
    solved = False
   
    if (dim == 2 or dim == 3): # 2 and 3: no solution 
        locations = []
        solved = True
    if (dim == 6): # 6 is special, return hard coded solution
        locations = [1,3,5,0,2,4]
        solved = True
    if (dim == 10): # 10 is also special, return hard coded solution
        locations = [0, 2, 5, 7, 9, 4, 8, 1, 3, 6]
        solved = True
    
    while (not solved):  # do solve() until a solution is found      
        solved = solve()  # solved equals true when a solution is returned
   
    cols_array = str([x + 1 for x in locations])	 
    elapsed_time = timer() - start_time
    print(n)
    #print(cols_array)
    print(round(elapsed_time,5))
    if(elapsed_time>=600):
        print("over 10 min")
        break
    array1 = array1 + [round(elapsed_time,5)]
    array2 = array2 + [n]
    
print(array1)
print(array2)
