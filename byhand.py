# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 03:44:54 2020

@author: Kieran
"""
'''
file = open("temp.txt" ,'r')
output = open("output_temp.txt", "w")

for line in file:
    index = len(line) - 1
    
    while(not(line[index] == '(')):
        index -= 1
        
    output.write(line[:index] + "\n")
    
    
file.close()
output.close()
'''

output = open("output_temp_2.txt", "w")

#output.write("Written")
names = []

for file_path in os.listdir("Data_Final/"):
    file = open("Data_Final/" + file_path, 'r')
    
    names.append(file.readline().strip())
    
    file.close()

names = list(set(names))
names.sort()

for name in names:
    output.write(name + "\n")
    

output.close()