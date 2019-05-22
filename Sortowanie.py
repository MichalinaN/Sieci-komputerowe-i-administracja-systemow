input_list = [2, 3, 10, 20, 14, 50, 128]

import sys
print sys.argv[1]
 
def sortowanie(input_list):
    for i in range(0,len(input_list),1):
        j=len(input_list)-1
        for j in range(1,len(input_list),1): 
            if input_list[j]<input_list[j-1]: 
                temp=input_list[j]
                input_list[j]=input_list[j-1]
                input_list[j-1]=temp
            j=j-1
         
sortowanie(input_list)
print (input_list)  