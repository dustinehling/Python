# Roman Numerials to integer converter

# Function to get value from character
def integer(i):
    if(i == 'I'):
        return 1
    if(i == 'V'):
        return 5
    if(i == 'X'):
        return 10
    if(i == 'L'):
        return 50
    if(i == 'C'):
        return 100
    if(i == 'D'):
        return 500
    if(i == 'M'):
        return 1000

def romanToInteger(str):
    res = 0
    i = 0

    while(i < len(str)):
        #  Get str[i] value
        a = integer(str[i])

        # Interate through input
        if(i + 1 < len(str)):

            # Get next integer
            b = integer(str[i + 1])

            # Compare the two values 
            if(a >= b):

                # Value of current is greater than next
                res = res + a
                i = i + 1 
            else:

                # Value of next is greater than current
                res = res + b - a
                i = i + 2
        else:
            res = res + a 
            i = i + 1
        
    return res

print(romanToInteger("IV"))





