def fibonacci(num):  
    if num==0:    
        return num
    elif num==1: 
        return num
    else:
       return fibonacci(num-1)+fibonacci(num-2) 

fibo=int(input("Enter the number: ")) 
for i in range(0,fibo+1):
    result=fibonacci(i)
    print(result)