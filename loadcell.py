import RPi.GPIO as GPIO
import time
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT) #2
GPIO.setup(5, GPIO.IN) #3
GPIO.setup(4, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(6, GPIO.IN)

GPIO.output(7, False)


def read ():
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_5 = 0

    count_1_old = 0
    count_2_old = 0
    count_3_old = 0
    count_4_old = 0
    count_5_old = 0
    
    count_new_1 = count_new_2 = count_new_3 = count_new_4 = count_new_5 = 0    
    
    while(GPIO.input(5) == True or GPIO.input(4) == True or GPIO.input(15)
        == True or GPIO.input(17) == True or GPIO.input(6) == True):

        if (GPIO.input(5) == True):
            print("5")
        if (GPIO.input(4) == True):
            print("4")
        if (GPIO.input(15) == True):
            print("15")
        if (GPIO.input(17) == True):
            print("17")
        if (GPIO.input(6) == True):
            print("6")

        #print("Weight ready signal from load cell")
        time.sleep(0.5)       
          

        

    for i in range(24):
        GPIO.output(7, True)
        #time.sleep(0.000001)
        
        count_1 = count_1 << 1
        count_2 = count_2 << 1
        count_3 = count_3 << 1
        count_4 = count_4 << 1
        count_5 = count_5 << 1       
        
        GPIO.output(7, False)
        #time.sleep(0.000001)
        
        if(GPIO.input(5) == True):
           count_1 = count_1 + 1
        if(GPIO.input(4) == True):
           count_2 = count_2 + 1
        if(GPIO.input(15) == True):
           count_3 = count_3 + 1
        if(GPIO.input(17) == True):
           count_4 = count_4 + 1
        if(GPIO.input(6) == True):
           count_5 = count_5 + 1           
    GPIO.output(7, True)
    GPIO.output(7, False)           
        
      
    count_1 = ((count_1 >> 12 ^ 0x800)) 
    count_2 = ((count_2 >> 12 ^ 0x800))
    count_3 = ((count_3 >> 12 ^ 0x800))
    count_4 = ((count_4 >> 12 ^ 0x800))    
    count_5 = ((count_5 >> 12 ^ 0x800)) 

    time.sleep(0.1)
    #print(count_1, count_2, count_3, count_4, count_5)
    #count_1 = count_2 = count_3 = count_4 = count_5 = 0
    return count_1, count_2, count_3, count_4, count_5
'''
while(True): 
    read()
'''
'''
cell_value_1 = cell_value_2 = cell_value_3 = cell_value_4 = cell_value_5 = 0

while (True):        
    cell_value_1, cell_value_2, cell_value_3, cell_value_4, cell_value_5 = read()
    print(cell_value_1, cell_value_2, cell_value_3, cell_value_4, cell_value_5)
'''