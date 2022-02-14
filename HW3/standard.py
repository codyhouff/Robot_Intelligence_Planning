from timeit import default_timer as timer

max_n = 100
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
    while (True):
        if((timer() - start_time)>600):
            return 600
        #print("cols",cols)
        #print("candidate",candidate)
        cols = cols + [candidate]
        #print("cols",cols)
        if(len(cols) == n): #if equal to the length of n    
            if(is_good(cols)): #if good
                #print("good")  
                print("n: "+str(n)+" ",cols)    #sloved
                elapsed_time = timer() - start_time
                return elapsed_time

                
            else: #if not good
                #print("not good")
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
            
        else: #not the length of n
            candidate = 0
        

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
    


#solver(4)
