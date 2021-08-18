def generalizedGCD(num, arr):
    #Sort list 
    arr.sort()
    
    #Initial value to get iteration started
    res = arr[0]
    
    for i in range(1, num):
        c = gcd(res, arr[i])
        
        return c 
    
def gcd(a, b):
    if(a == 0):
        return 1
    if(b == 0):
        return a
    else:
        #Absolute values for negative values
        return gcd(abs(b),abs(a) % abs(b))
        
#TEST CASE ONE 
num = 5
arr = [2,4,6,8,10]
generalizedGCD(num, arr)

#TEST CASE TWO
num = 5
arr = [2,3,4,5,6]
generalizedGCD(num, arr)

#TEST CASE THREE
num = 3 
arr = [0, 3, 9]
generalizedGCD(num, arr)

#TEST CASE THREE
num = 3 
arr = [0, 3, 10]
generalizedGCD(num, arr)