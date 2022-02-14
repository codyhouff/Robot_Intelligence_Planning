from timeit import default_timer as timer

max_n = 40
array1 = []
array2 = []

def domain_clear(domain,a):
    i=1
    for col in domain[:]:

        for row in col[:]: 
            if(row == a):
                col.remove(row) #straight
            if(row == a-i):
                col.remove(row) #up
            if(row == a+i):
                col.remove(row) #down                  
        i = i+1
 
    return domain

def solver(n):
    start_time = timer()
    domain_saved = []
    a_array = []

    domain = [[col for col in range(n)] for row in range(n)]
    #print("domain: ",domain)

    while(len(a_array)<n):
        if((timer() - start_time)>600):
            return 600
        
        while(domain[0] == []):
            
            if(domain_saved == []):
                elapsed_time = timer() - start_time
                return elapsed_time            

            domain = domain_saved[-1]
            domain_saved.pop(-1)
            a_array.pop(-1)
            
        
        a = domain[0].pop(0)
        a_array = a_array + [a]
        #domain_copy = domain[:] 
        domain_copy = [col[:] for col in domain]
        domain_saved = domain_saved + [domain_copy] 
        #print("domain_saved: ",domain_saved)
        domain.pop(0)

        domain = domain_clear(domain,a)

    print("a_array: ",a_array)
    elapsed_time = timer() - start_time
    return elapsed_time


for n in range(1,max_n):
    print(n)
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


#solver(1)
