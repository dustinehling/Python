def arraySum(numbers):
    # Write your code here
    length = len(numbers)
    sum = 0
    if(isinstance(numbers,list)):
        for number in numbers:
            sum = sum + number
                
        return sum
    else:
        return

#TEST CASE ONE
numbers = [1,2,3,4,5]
print(arraySum(numbers))