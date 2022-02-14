from timeit import default_timer as timer

max_n = 50
array1 = []
array2 = []

def is_good(cols):
    if len(cols) != len(set(cols)):
        return False
    if len(set(cols[i] + i for i in range(len(cols)))) != len(cols):
        return False
    if len(set(cols[i] - i for i in range(len(cols)))) != len(cols):
        return False
    #print("cols added:",[cols])
    return True

def solver(n):
    start_time = timer()
    cols = []
    candidate = 0
    while (len(cols)<n):
        if((timer() - start_time)>600):
            return 600
        new_cols = cols + [candidate]  #try array with new col
        #print("candidate",candidate)
        #print("new_cols",new_cols)
        if (is_good(new_cols)): #if candidate is good, use new_col as next col
            #print("candidate " + str(candidate)+" is good") #,candidate)
            #print("new cols:",new_cols)
            candidate = 0
            cols = new_cols
        
        else:                          #if new col is not good:
            if candidate < (n - 1):    #if candidate is not the last col value (n-1), more cols left
                candidate = candidate + 1
            else:                                   #if candidate is the last col value (n-1) (aka no more cols left)
                while (True):
                    if(cols == []):
                        print("n: "+str(n)+" ",cols)
                        elapsed_time = timer() - start_time
                        return elapsed_time
                    #print("before pop",cols)
                    candidate = cols.pop() + 1      #pop off last cols value, new candidate = last value after pop
                    #print("pop")
                    if n > candidate:
                        break                       #if n =/= new candidate: break loop
                #print("after pop",cols)

    print("n: "+str(n)+" ",cols)    #sloved
    elapsed_time = timer() - start_time
    return elapsed_time


for n in range(1,max_n):
    elapsed_time = solver(n)
    print(elapsed_time)
    #print("time = %.5f (s)" % elapsed_time)
    if(elapsed_time==600):
        print("over 10 min")
        break
    array1 = array1 + [elapsed_time]
    array2 = array2 + [n]
print(array1)
print(array2)
    
