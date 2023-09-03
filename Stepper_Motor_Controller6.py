import tkinter as tk
from   random import randrange
import RPi.GPIO as GPIO
import time
import Limit_Switch_Read
from   multiprocessing import Process, Queue
from   threading import Thread
import loadcell
import run_functions as rf
import csv
import massage_position_input as mpi
 

control_val = list()
limit_sw_val = list()
loadcell_val = list()
loadcell_val_int_1 = loadcell_val_int_2 = loadcell_val_int_3 = 0
loadcell_val_int_4 = loadcell_val_int_5 = 0
loadcell_val_int_rear = loadcell_val_int_front = loadcell_val_int_down = 0
loadcell_val_int_left = loadcell_val_int_right = 0

my_x = 0
my_y = 0
my_z = 0

#####################################################################################3
window = tk.Tk()
window.title("Robot")
window.geometry("435x140")

lblLogs = tk.Label(window, text="Massage Robot Start", bg = "black", fg = "white")
lblLine2 = tk.Label(window, text = "******************************************************", bg = "black", fg = "white")

# create the buttons
buttons = []
#for index in range(0, 10):
#    button = tk.Button(window, text=index, command=lambda index=index : process(index), state=tk.NORMAL) #state=tk.DISABLED)
#    buttons.append(button)

button = tk.Button(window, text="Massage Main Start", command=lambda index=1 : process(index), bg = "black", fg = "white", state=tk.NORMAL) #state=tk.DISABLED)
buttons.append(button)
#button = tk.Button(window, text = "Color", bg = "blue", fg = "red")
button = tk.Button(window, text="Move To The Origin", command=lambda index=2 : home(index), bg = "black", fg = "white", state=tk.NORMAL) #state=tk.DISABLED)
buttons.append(button)
#app = tk.Tk()
button = tk.Button(window, text="Auto Mode", command=lambda index=3 : auto_mode(index), bg = "black", fg = "white", state=tk.NORMAL) #state=tk.DISABLED)
buttons.append(button)#you have to remove this to go back
button = tk.Button(window, text="MANUAL Mode", command=lambda index=4 : manual_mode(index), bg = "black", fg = "white", state=tk.NORMAL) #state=tk.DISABLED)
buttons.append(button)#you have to remove this to go back

window['bg'] = 'black'
#app.mainloop()

btnStartGameList = []
for index in range(0, 1):
    btnStartGame = tk.Button(window, text="Start Read (Key & Limit & Loadcell)", command=lambda : startmassage(index), bg = "black", fg = "white")
    btnStartGameList.append(btnStartGame)

# append elements to grid

lblLogs.grid(row=1, column=0, columnspan=5)  # row 4 - 8 is reserved for showing logs
lblLine2.grid(row=2, column=0, columnspan=5)


#for row in range(0, 2):
#    for col in range(0, 5):
#        i = row * 5 + col  # convert 2d index to 1d. 5= total number of columns
#        buttons[i].grid(row=row+10, column=col)
buttons[0].grid(row=3, column=1)
buttons[1].grid(row=3, column=3)
buttons[2].grid(row=4, column=1)#you have to remove this to go back
buttons[3].grid(row=4, column=3)#you have to remove this to go back


btnStartGameList[0].grid(row=5, column=0, columnspan=5)


KEY_UP = 0xdf
KEY_DN = 0xef
KEY_LT = 0xf7
KEY_RT = 0xfb
KEY_FT = 0xfe
KEY_RR = 0xfd
KEY_UP_LT = 0xd7
KEY_UP_RT = 0xdb
KEY_UP_FT = 0xde
KEY_UP_RR = 0xdd
KEY_DN_LT = 0xe7
KEY_DN_RT = 0xeb
KEY_DN_FT = 0xee
KEY_DN_RR = 0xed
KEY_LT_FT = 0xf6
KEY_LT_RR = 0xf5
KEY_RT_FT = 0xfa
KEY_RT_RR = 0xf9
KEY_UP_LT_FT = 0xd6
KEY_UP_LT_RR = 0xd5
KEY_UP_RT_FT = 0xda
KEY_UP_RT_RR = 0xd9
KEY_DN_LT_FT = 0xe6
KEY_DN_LT_RR = 0xe5
KEY_DN_RT_FT = 0xea
KEY_DN_RT_RR = 0xe9
KEY_NONE = 0xcf
KEY_RI = 0x7f
KEY_FA = 0xbf

SW_UP = 0x001
SW_DN = 0x002
SW_LT = 0x500
SW_RT = 0xa00
SW_FT = 0x008
SW_RR = 0x004
SW_RI = 0x060
SW_FA = 0x090

DIR_UP_DN = 25
DIR_LT_RT = 10
DIR_FT_RR = 8
DIR_RI_FA = 22

DIR_VAL_UP = False
DIR_VAL_DN = True
DIR_VAL_LT = True
DIR_VAL_RT = False
DIR_VAL_FT = True
DIR_VAL_RR = False
DIR_VAL_RI = True
DIR_VAL_FA = False

CLK_UP_DN = 9
CLK_LT_RT = 24
CLK_FT_RR = 11
CLK_RI_FA = 27

CLOCK_TIMER = 0.001
CLOCK_TIMER2 = 0.01
MAX_CLOCK_TIMER = CLOCK_TIMER2 / 20


def process(i):
    print(i)
    MassageMain()

def startgame(i):
    timer = 0
    data_Control = 0
    while(True):
        time.sleep(0.5)
        print("Game started")
    return

def auto_mode(i): #you have to remove this to go back
    
    global MANUAL
    
    MANUAL = False

    
def manual_mode(i): #you have to remove this to go back
    
    global MANUAL
    
    MANUAL = True 
    

###################################################3

def Key_Limit_Read(id, control_val,limit_sw_val):
    timer = 0
    while(True):
        time.sleep(0.01)
        data, Control = Limit_Switch_Read.key_limit_sw( timer )  #read key & limit
        control_val.append(data)
        limit_sw_val.append(Control)
        if len(control_val) > 3:
            continue
    return

def LoadCell_Read(id, loadcell_val):
    while(True):        
        time.sleep(0.1)
        cell_value_1, cell_value_2, cell_value_3, cell_value_4, cell_value_5 = loadcell.read() #read data
        if len(loadcell_val) > 10:
            continue
        loadcell_val.insert(0, cell_value_1)
        loadcell_val.insert(1, cell_value_2)
        loadcell_val.insert(2, cell_value_3)
        loadcell_val.insert(3, cell_value_4)
        loadcell_val.insert(4, cell_value_5)
    return


def startmassage(index):
    
    global control_val, limit_sw_val, loadcell_val
    
    th1 = Thread(target=Key_Limit_Read, args=(1, control_val, limit_sw_val))
    th2 = Thread(target=LoadCell_Read, args=(1, loadcell_val))
    th1.start()
    th2.start()
    return

def home(i):
    
    global my_x, my_y, my_z
    
    control_val, limit_sw_val, loadcell_val
    run_start = True
    loadcell_val_int_1 = loadcell_val_int_2 = loadcell_val_int_3 = 0
    loadcell_val_int_4 = loadcell_val_int_5 = 0
    length = 0
    count_avr = 0

    for i in range(5):
        time.sleep(0.2)
        if (len(loadcell_val) >= 5):
            loadcell_val_int_1 += int(loadcell_val[0])
            loadcell_val_int_2 += int(loadcell_val[1])
            loadcell_val_int_3 += int(loadcell_val[2])
            loadcell_val_int_4 += int(loadcell_val[3])
            loadcell_val_int_5 += int(loadcell_val[4])
            count_avr += 1
    result_avr_1 = int(loadcell_val_int_1 / count_avr)
    result_avr_2 = int(loadcell_val_int_2 / count_avr)
    result_avr_3 = int(loadcell_val_int_3 / count_avr)
    result_avr_4 = int(loadcell_val_int_4 / count_avr)
    result_avr_5 = int(loadcell_val_int_5 / count_avr)

    data_Limit_UD = 0
    data_Limit_LR = 0
    data_Limit_FR = 0
    
    while(True):
        if (data_Limit_UD == SW_UP and data_Limit_LR == SW_RT and data_Limit_FR == SW_RR):
            my_x = my_y = my_z = 0
            break

        length = len(loadcell_val)   # Load Cell Read
        
        if (length >= 5):       
            loadcell_val_int_1 = int(loadcell_val[0])
            loadcell_val_int_2 = int(loadcell_val[1])
            loadcell_val_int_3 = int(loadcell_val[2])
            loadcell_val_int_4 = int(loadcell_val[3])
            loadcell_val_int_5 = int(loadcell_val[4])
            
            loadcell_val_int_rear = result_avr_1 - loadcell_val_int_1
            loadcell_val_int_left = result_avr_2 - loadcell_val_int_2
            loadcell_val_int_down = result_avr_3 - loadcell_val_int_3
            loadcell_val_int_front = result_avr_4 - loadcell_val_int_4
            loadcell_val_int_right = result_avr_5 - loadcell_val_int_5       

        if (length > 5):
            for i in range(length - 5):
                del loadcell_val[5]
                
        length = len(control_val)   # Keyboard Read
        
        if (length > 0):       
            control_val_int = int(control_val[0])
            
        if (length > 1):
            for i in range(length - 1):
                del control_val[0]  
      
        length = len(limit_sw_val)    # Limit SW Read
        
        if (len(limit_sw_val) > 0):       
            limit_sw_val_int = int(limit_sw_val[0])
            
        if (length > 1):
            for i in range(length - 1):
                del limit_sw_val[0]

        data_Limit_UD = limit_sw_val_int & 0x003
        data_Limit_LR = limit_sw_val_int & 0xf00
        data_Limit_FR = limit_sw_val_int & 0x00c
        
        control_val_int = KEY_UP_RT_RR

        loadcell_val_int_left = loadcell_val_int_right = loadcell_val_int_front = loadcell_val_int_rear = 20
        run_end_LR = False
        run_end_FR = False
        run_end_UD = False
        
        #print( hex(control_val_int), hex(limit_sw_val_int) )
        #time.sleep(0.2)

        run_start, run_end_UD = rf.Run_UP_DN(control_val_int, limit_sw_val_int, loadcell_val_int_down, run_start, run_end_UD) #UP_DN call
        run_start, run_end_LR = rf.Run_LT_RT(control_val_int, limit_sw_val_int, loadcell_val_int_left, loadcell_val_int_right, run_start, run_end_LR) #LT_RT call    
        run_start, run_end_FR = rf.Run_FT_RR(control_val_int, limit_sw_val_int, loadcell_val_int_front, loadcell_val_int_rear, run_start, run_end_FR) #FT_RR call
        run_start, run_end_UD, run_end_LR = rf.Run_UP_DN_LT_RT(control_val_int, limit_sw_val_int, loadcell_val_int_down, loadcell_val_int_left, loadcell_val_int_right, run_start, run_end_UD, run_end_LR) #UP_DN_LT_RT call
        run_start, run_end_UD, run_end_FR = rf.Run_UP_DN_FT_RR(control_val_int, limit_sw_val_int, loadcell_val_int_down, loadcell_val_int_front, loadcell_val_int_rear, run_start, run_end_UD, run_end_FR) #UP_DN_FT_RR call
        run_start, run_end_LR, run_end_FR = rf.Run_LT_RT_FT_RR(control_val_int, limit_sw_val_int, loadcell_val_int_left, loadcell_val_int_right, loadcell_val_int_front, loadcell_val_int_rear, run_start, run_end_LR, run_end_FR) #LT_RT_FT_RR call
        run_start, run_end_UD, run_end_LR, run_end_FR = rf.Run_UP_DN_LT_RT_FT_RR(control_val_int, limit_sw_val_int, loadcell_val_int_down, loadcell_val_int_left, loadcell_val_int_right, loadcell_val_int_front, loadcell_val_int_rear, run_start, run_end_UD, run_end_LR, run_end_FR) #UP_DN_LT_RT_FT_RR call
        run_start, run_end_UD, run_end_LR, run_end_FR = rf.All_Key_Relesed(control_val_int, run_start, run_end_UD, run_end_LR, run_end_FR) #All key relesed call
            
    return    

def MassageMain():
    
    global my_x, my_y, my_z
    global MANUAL
    
    limit_sw_val_int = 0
    data_Control_org = 0

    run_start = True
    run_end_LR = False
    run_end_FR = False
    run_end_UD = False

#    control_val = list()
#    limit_sw_val = list()
#    loadcell_val = list()
    control_val_int = 0
    loadcell_val_int_1 = loadcell_val_int_2 = loadcell_val_int_3 = 0
    loadcell_val_int_4 = loadcell_val_int_5 = 0
    loadcell_val_int_rear = loadcell_val_int_front = loadcell_val_int_down = 0
    loadcell_val_int_left = loadcell_val_int_right = 0

    length = 0
    
    count_avr = 0
    for i in range(5):
        time.sleep(0.2)
        if (len(loadcell_val) >= 5):
            loadcell_val_int_1 += int(loadcell_val[0])
            loadcell_val_int_2 += int(loadcell_val[1])
            loadcell_val_int_3 += int(loadcell_val[2])
            loadcell_val_int_4 += int(loadcell_val[3])
            loadcell_val_int_5 += int(loadcell_val[4])
            count_avr += 1
    result_avr_1 = int(loadcell_val_int_1 / count_avr)
    result_avr_2 = int(loadcell_val_int_2 / count_avr)
    result_avr_3 = int(loadcell_val_int_3 / count_avr)
    result_avr_4 = int(loadcell_val_int_4 / count_avr)
    result_avr_5 = int(loadcell_val_int_5 / count_avr)
    
    f = open('massage_position.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    position_data = list(rdr) #x, y, power, repeat, speed
    f.close()
    
    read_count = len(position_data)
    
    count = 0
    x_count = 0
    y_count = 0
    move_done = True
    read_pos = 0
    run_while = True
    z_stop = False
    count_z = 0
    moved = False
    z_state = False
    
    home(i)
    time.sleep(0.5)

################################################################################
    
    while(run_while):    

        length = len(loadcell_val)   # Load Cell Read
        if (length >= 5):       
            loadcell_val_int_1 = int(loadcell_val[0])
            loadcell_val_int_2 = int(loadcell_val[1])
            loadcell_val_int_3 = int(loadcell_val[2])
            loadcell_val_int_4 = int(loadcell_val[3])
            loadcell_val_int_5 = int(loadcell_val[4])
            
            loadcell_val_int_rear = result_avr_1 - loadcell_val_int_1
            loadcell_val_int_left = result_avr_2 - loadcell_val_int_2
            loadcell_val_int_down = result_avr_3 - loadcell_val_int_3
            loadcell_val_int_front = result_avr_4 - loadcell_val_int_4
            loadcell_val_int_right = result_avr_5 - loadcell_val_int_5
            #print("reset loadcell value int")

        if (length > 5):
            for i in range(length - 5):
                del loadcell_val[5]
                
        
        length = len(control_val)   # Keyboard Read
        
        if (length > 0):       
            control_val_int = int(control_val[0])
            
        if (length > 1):
            for i in range(length - 1):
                del control_val[0]  
            
      
        length = len(limit_sw_val)    # Limit SW Read
        
        if (length > 0):       
            limit_sw_val_int = int(limit_sw_val[0])
            
        if (length > 1):
            for i in range(length - 1):
                del limit_sw_val[0]
                
        #print( hex(control_val_int), hex(limit_sw_val_int))
        #time.sleep(0.5)        
                
        #MANUAL = False #**************  MANUAL SET ********************    
###########################################################################################################
        #x = 58 turn
        #y = 99 turn
        if MANUAL == False :
            print("AUTO MODE")
            if(move_done):
                pos_y =  int((int(position_data[read_pos][0])-140)/3.2)   #0~456 (140,140) (280,370) ==> (139, 228)/(58, 99) = (2.4, 2.3)
                pos_x =  int((int(position_data[read_pos][1])-140)/2.7)   #0~679
                power =  int(position_data[read_pos][2])
                repeat = int(position_data[read_pos][3])
                speed =  int(position_data[read_pos][4])
                Cal_x = (pos_x - my_x) * 20 # 10 * 20 = 200 = 1 revolution
                Cal_y = (pos_y - my_y) * 20
                move_done = False
                read_pos += 1
              #  print(pos_x, pos_y)
              #  print(read_pos)
              #  print (Cal_x, Cal_y)            

            if(pos_x > 58) :
                pos_x = 58
            if(pos_y > 99) :
                pos_y = 99
                
            if (Cal_x > 0 and Cal_y > 0 ):
                control_val_int = KEY_LT_FT
                moved = True
                z_state = False            
            elif (Cal_x < 0 and Cal_y < 0 ):
                control_val_int = KEY_RT_RR
                moved = True
                z_state = False            
            elif (Cal_x > 0 and Cal_y < 0 ):
                control_val_int = KEY_LT_RR
                moved = True
                z_state = False            
            elif (Cal_x < 0 and Cal_y > 0 ):
                control_val_int = KEY_RT_FT
                moved = True
                z_state = False            
            elif (Cal_y < 0 and Cal_x == 0 ):
                control_val_int = KEY_RR
                moved = True
                z_state = False            
            elif (Cal_x < 0 and Cal_y == 0 ):
                control_val_int = KEY_RT
                moved = True
                z_state = False            
            elif (Cal_y > 0 and Cal_x == 0 ):
                control_val_int = KEY_FT
                moved = True
                z_state = False            
            elif (Cal_x > 0 and Cal_y == 0 ):
                control_val_int = KEY_LT
                moved = True
                z_state = False            
                
            else: # one action ended
                control_val_int = KEY_NONE
                my_x = pos_x
                my_y = pos_y
                
                if moved == True :
                    
                    if count_z < 200 :
                        if z_state == False:
                            control_val_int = KEY_DN
                            count_z += 1
                            print(count_z)
                            
                        if loadcell_val_int_down > power:
                            control_val_int = KEY_NONE
                            #print(loadcell_val_int_down) #이거주석 풀기
                            print(count_z)
                            count_z = 0
                            time.sleep(1)
                            z_state = True
                            count_z = 200
                            
                    if count_z >= 200 and count_z < 400:
                        control_val_int = KEY_UP
                        count_z += 1
                        print(count_z)
                    
                    if count_z >= 400 :
                        moved = False
                        move_done = True
                        z_state = False
                        #print(count_z)
                        count_z = 0
                        if read_pos == read_count:
                            home(i)
                            run_while = False
                    '''
                    if count_z < 200 :
                        if z_state == False:
                            control_val_int = KEY_DN
                            count_z += 1
                            #print(count_z)
                        if loadcell_val_int_down > power:
                            control_val_int = KEY_NONE
                            print(loadcell_val_int_down) #이거주석 풀기
                            #print(count_z)
                            count_z = 0
                            time.sleep(1)
                            z_state = True
                            count_z = 200 
                    elif count_z > 199 and count_z < 400:
                        control_val_int = KEY_UP
                        count_z += 1
                        #print(count_z)

                        print(loadcell_val_int_down) #이거주석 풀기
                    elif count_z >= 400 :
                        moved = False
                        move_done = True
                        z_state = False
                        #print(count_z)
                        count_z = 0
                        if read_pos == read_count:
                            home(i)
                            run_while = False       
                   '''

           # count += 1
           # if(count == 20):
           #     count = 0
           #     print (Cal_x, Cal_y, my_x, my_y, pos_x, pos_y)            


            if  Cal_x  > 0 :
                Cal_x -= 1
            elif Cal_x < 0 :
                Cal_x += 1
                
            if  Cal_y  > 0 :
                Cal_y -= 1
            elif Cal_y < 0 :
                Cal_y += 1
                
 ##############################################################################################################       
        run_end_UD = False #if Limit SW is pressed then Skip Speed Decrease
        run_end_LR = False #if Limit SW is pressed then Skip Speed Decrease
        run_end_FR = False #if Limit SW is pressed then Skip Speed Decrease
        
        rf.Run_RI_FA(control_val_int, limit_sw_val_int)
        run_start, run_end_UD = rf.Run_UP_DN(control_val_int, limit_sw_val_int, loadcell_val_int_down, run_start, run_end_UD) #UP_DN call
        run_start, run_end_LR = rf.Run_LT_RT(control_val_int, limit_sw_val_int, loadcell_val_int_left, loadcell_val_int_right, run_start, run_end_LR) #LT_RT call    
        run_start, run_end_FR = rf.Run_FT_RR(control_val_int, limit_sw_val_int, loadcell_val_int_front, loadcell_val_int_rear, run_start, run_end_FR) #FT_RR call
        run_start, run_end_UD, run_end_LR = rf.Run_UP_DN_LT_RT(control_val_int, limit_sw_val_int, loadcell_val_int_down, loadcell_val_int_left, loadcell_val_int_right, run_start, run_end_UD, run_end_LR) #UP_DN_LT_RT call
        run_start, run_end_UD, run_end_FR = rf.Run_UP_DN_FT_RR(control_val_int, limit_sw_val_int, loadcell_val_int_down, loadcell_val_int_front, loadcell_val_int_rear, run_start, run_end_UD, run_end_FR) #UP_DN_FT_RR call
        run_start, run_end_LR, run_end_FR = rf.Run_LT_RT_FT_RR(control_val_int, limit_sw_val_int, loadcell_val_int_left, loadcell_val_int_right, loadcell_val_int_front, loadcell_val_int_rear, run_start, run_end_LR, run_end_FR) #LT_RT_FT_RR call
        run_start, run_end_UD, run_end_LR, run_end_FR = rf.Run_UP_DN_LT_RT_FT_RR(control_val_int, limit_sw_val_int, loadcell_val_int_down, loadcell_val_int_left, loadcell_val_int_right, loadcell_val_int_front, loadcell_val_int_rear, run_start, run_end_UD, run_end_LR, run_end_FR) #UP_DN_LT_RT_FT_RR call
        run_start, run_end_UD, run_end_LR, run_end_FR = rf.All_Key_Relesed(control_val_int, run_start, run_end_UD, run_end_LR, run_end_FR) #All key relesed call    
        
window.mainloop()

