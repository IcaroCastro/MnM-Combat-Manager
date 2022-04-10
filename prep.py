import os

file = open('Images/0.txt', 'w+')
file.close()
os.remove('Images/0.txt')

file = open('Sheets/0.txt', 'w+')
file.close()
os.remove('Sheets/0.txt')
