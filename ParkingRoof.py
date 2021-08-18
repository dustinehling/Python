def carParkingRoof(cars, k):
    #Sort list
    cars.sort()
    
    #Length of list
    length = len(cars)
    
    #Calculate min roof length
    min = cars[k-1] - cars[0]
    for i in range(1,length):
        if min > cars[k-1+i] - cars[i]:
            min = cars[k-1+i] - cars[i]
            
        return min

#TEST CASE ONE
cars = [2,10,8,17]
k = 3
carParkingRoof(cars, k)