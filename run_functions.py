import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.OUT) #clock V1
GPIO.setup(22, GPIO.OUT) #dir V1
GPIO.setup(24, GPIO.OUT) #clock H1
GPIO.setup(10, GPIO.OUT) #dir H1
GPIO.setup(9, GPIO.OUT) #clock H2
GPIO.setup(25, GPIO.OUT) #dir H2
GPIO.setup(11, GPIO.OUT) #clock V2
GPIO.setup(8, GPIO.OUT) #dir V2

GPIO.output(22, True)
GPIO.output(8, True)

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

LOADCELL_DOWN_VALUE = 20
LOADCELL_LRFR_VALUE = 50

CLK_UP_DN = 9
CLK_LT_RT = 24
CLK_FT_RR = 11
CLK_RI_FA = 27

CLOCK_TIMER = 0.001
CLOCK_TIMER2 = 0.01
MAX_CLOCK_TIMER = CLOCK_TIMER2 / 20

def Run_RI_FA(data_Control_org, data_Limit):
    
    data_Limit_UD2 = data_Limit & 0x0f0
    #############################   UP2  #######################    
    if(data_Control_org == KEY_RI and data_Limit_UD2 != SW_RI): #Rising
        GPIO.output(DIR_RI_FA, DIR_VAL_RI)
        for i in range(10):
            GPIO.output(CLK_RI_FA, True)
            time.sleep(CLOCK_TIMER)
            GPIO.output(CLK_RI_FA, False)
            time.sleep(CLOCK_TIMER)
    
    #############################   DN2  #######################    
    if(data_Control_org == KEY_FA and data_Limit_UD2 != SW_FA): #Falling       
        GPIO.output(DIR_RI_FA, DIR_VAL_FA)
        for i in range(10):
            GPIO.output(CLK_RI_FA, True)
            time.sleep(CLOCK_TIMER)
            GPIO.output(CLK_RI_FA, False)
            time.sleep(CLOCK_TIMER)
    return

def Run_UP_DN(data_Control_org, data_Limit, new_loadcell_val_int_down, run_start, run_end_UD):

    data_Limit_UD = data_Limit & 0x003

    ######## Go X, Y ,Z  ###########
    ## Go Up Down     
    if( (new_loadcell_val_int_down < LOADCELL_DOWN_VALUE and  data_Control_org == KEY_UP) or   #Up 
        (new_loadcell_val_int_down < LOADCELL_DOWN_VALUE and  data_Control_org == KEY_DN) ):  #Down

        if( data_Control_org == KEY_UP) :       #Up
            GPIO.output(DIR_UP_DN, DIR_VAL_UP)
        elif(data_Control_org == KEY_DN) :      #Down
            GPIO.output(DIR_UP_DN, DIR_VAL_DN)
            
        for i in range(10):
            if((data_Control_org == KEY_DN and data_Limit_UD != SW_DN) or
               (data_Control_org == KEY_UP and data_Limit_UD != SW_UP)): 

                GPIO.output(CLK_UP_DN, True)

                if(run_start == True) :
                    time.sleep(CLOCK_TIMER2 / (i+1) )
                else :
                    time.sleep(MAX_CLOCK_TIMER)
                    
                GPIO.output(CLK_UP_DN, False)
                
                if(run_start == True) :
                    time.sleep(CLOCK_TIMER2 / (i+1) )
                else :
                    time.sleep(MAX_CLOCK_TIMER)
                    
        if(run_start == True) :
            run_start = False  # to continue MAX speed
        else:
            run_end_UD = True       # to decrease speed
            
        if(data_Control_org == KEY_NONE):  
            if(run_end_UD == True):
                for i in range(10):
                    GPIO.output(CLK_UP_DN, True)
                    time.sleep((CLOCK_TIMER2 / 20) + i*0.0001)
                    GPIO.output(CLK_UP_DN, False)
                    time.sleep((CLOCK_TIMER2 / 20) + i*0.0001)
                run_end_UD = False
                run_start = True            
                #print("runend UD")
    return run_start, run_end_UD

def Run_LT_RT(data_Control_org, data_Limit, new_loadcell_val_int_left, new_loadcell_val_int_right, run_start, run_end_LR):

    data_Limit_LR = data_Limit & 0xf00
    
    ## Go Left Right
    if( (new_loadcell_val_int_left  < LOADCELL_LRFR_VALUE and  data_Control_org == KEY_LT) or #Left
        (new_loadcell_val_int_right < LOADCELL_LRFR_VALUE and  data_Control_org == KEY_RT) ):  #Right
        
        if( data_Control_org == KEY_LT) :     #Left
            GPIO.output(DIR_LT_RT, DIR_VAL_LT)
        elif(data_Control_org == KEY_RT) :      #Right
            GPIO.output(DIR_LT_RT, DIR_VAL_RT)
        
        for i in range(10):
            if((data_Control_org == KEY_LT and data_Limit_LR != SW_LT) or
               (data_Control_org == KEY_RT and data_Limit_LR != SW_RT)): 

                GPIO.output(CLK_LT_RT, True)

                if(run_start == True) :
                    time.sleep(CLOCK_TIMER2 / (i+1) )
                else :
                    time.sleep(MAX_CLOCK_TIMER)
                    
                GPIO.output(CLK_LT_RT, False)
                
                if(run_start == True) :
                    time.sleep(CLOCK_TIMER2 / (i+1) )
                else :
                    time.sleep(MAX_CLOCK_TIMER)
                    
        if(run_start == True) :
            run_start = False  # to continue MAX speed
        else:
            run_end_LR = True       # to decrease speed
            
    return run_start, run_end_LR

def Run_FT_RR(data_Control_org, data_Limit, new_loadcell_val_int_front, new_loadcell_val_int_rear, run_start, run_end_FR):
    
    data_Limit_FR = data_Limit & 0x00c
    
    ## Go Front Rear
    if((new_loadcell_val_int_front < LOADCELL_LRFR_VALUE and  data_Control_org == KEY_FT or  #Front
        new_loadcell_val_int_rear  < LOADCELL_LRFR_VALUE and  data_Control_org == KEY_RR) ):  #Rear
        
        if( data_Control_org == KEY_FT) :     #Front
            GPIO.output(DIR_FT_RR, DIR_VAL_FT)
        elif(data_Control_org == KEY_RR) :      #Rear
            GPIO.output(DIR_FT_RR, DIR_VAL_RR)            
        
        for i in range(10):
            if((data_Control_org == KEY_FT and data_Limit_FR != SW_FT) or
               (data_Control_org == KEY_RR and data_Limit_FR != SW_RR)): 

                GPIO.output(CLK_FT_RR, True)

                if(run_start == True) :
                    time.sleep(CLOCK_TIMER2 / (i+1) )
                else :
                    time.sleep(MAX_CLOCK_TIMER)
                    
                GPIO.output(CLK_FT_RR, False)
                
                if(run_start == True) :
                    time.sleep(CLOCK_TIMER2 / (i+1) )
                else :
                    time.sleep(MAX_CLOCK_TIMER)
                    
        if(run_start == True) :
            run_start = False  # to continue MAX speed
        else:
            run_end_FR = True       # to decrease speed
            
    return run_start, run_end_FR

def Run_UP_DN_LT_RT(data_Control_org, data_Limit, new_loadcell_val_int_down, new_loadcell_val_int_left, new_loadcell_val_int_right, run_start, run_end_UD, run_end_LR):
    
    data_Limit_UD = data_Limit & 0x003
    data_Limit_LR = data_Limit & 0xf00
    
    ## Go UP & LT : UP & RT : DN & LT : DN & RT 
    if(  (new_loadcell_val_int_down  < LOADCELL_DOWN_VALUE and new_loadcell_val_int_left  < LOADCELL_LRFR_VALUE and data_Control_org == KEY_UP_LT) or  #Up & Left
         (new_loadcell_val_int_down  < LOADCELL_DOWN_VALUE and new_loadcell_val_int_right < LOADCELL_LRFR_VALUE and data_Control_org == KEY_UP_RT) or  #Up & Right
         (new_loadcell_val_int_down  < LOADCELL_DOWN_VALUE and new_loadcell_val_int_left  < LOADCELL_LRFR_VALUE and data_Control_org == KEY_DN_LT) or  #Down & Left
         (new_loadcell_val_int_down  < LOADCELL_DOWN_VALUE and new_loadcell_val_int_right < LOADCELL_LRFR_VALUE and data_Control_org == KEY_DN_RT)):   #Down & Right   
        
        if( data_Control_org == KEY_UP_LT) :  #Up & Left
            GPIO.output(DIR_UP_DN, DIR_VAL_UP)
            GPIO.output(DIR_LT_RT, DIR_VAL_LT)
        elif(data_Control_org == KEY_UP_RT) :   #Up & Right
            GPIO.output(DIR_UP_DN, DIR_VAL_UP)
            GPIO.output(DIR_LT_RT, DIR_VAL_RT)

        elif( data_Control_org == KEY_DN_LT) :  #Down & Left
            GPIO.output(DIR_UP_DN, DIR_VAL_DN)
            GPIO.output(DIR_LT_RT, DIR_VAL_LT)
        elif(data_Control_org == KEY_DN_RT) :   #Down & Right
            GPIO.output(DIR_UP_DN, DIR_VAL_DN)
            GPIO.output(DIR_LT_RT, DIR_VAL_RT)
            

        for i in range(10):
            if(((data_Control_org == KEY_UP_LT or data_Control_org == KEY_UP_RT) and (data_Limit_UD != SW_UP)) or  #Up=1 Left=7 or Up Right=b
               ((data_Control_org == KEY_DN_LT or data_Control_org == KEY_DN_RT) and (data_Limit_UD != SW_DN))):   #Down=2 Left=7 or Down Right=b

                GPIO.output(CLK_UP_DN, True)
                
            if(((data_Control_org == KEY_UP_LT or data_Control_org == KEY_DN_LT) and (data_Limit_LR != SW_LT)) or  #Up=1 Left=500 or Up Right=a00
               ((data_Control_org == KEY_UP_RT or data_Control_org == KEY_DN_RT) and (data_Limit_LR != SW_RT))):   #Down Left or Down Right
                
                GPIO.output(CLK_LT_RT, True)

            if(run_start == True) :
                time.sleep(CLOCK_TIMER2 / (i+1) )
            else :
                time.sleep(MAX_CLOCK_TIMER)

            if(((data_Control_org == KEY_UP_LT or data_Control_org == KEY_UP_RT) and (data_Limit_UD != SW_UP)) or  #Up=1 Left=7 or Up Right=b
               ((data_Control_org == KEY_DN_LT or data_Control_org == KEY_DN_RT) and (data_Limit_UD != SW_DN))):   #Down=2 Left=7 or Down Right=b

                GPIO.output(CLK_UP_DN, False)
                
            if(((data_Control_org == KEY_UP_LT or data_Control_org == KEY_DN_LT) and (data_Limit_LR != SW_LT)) or  #Up=1 Left=500 or Up Right=a00
               ((data_Control_org == KEY_UP_RT or data_Control_org == KEY_DN_RT) and (data_Limit_LR != SW_RT))):   #Down Left or Down Right
                
                GPIO.output(CLK_LT_RT, False)
                
            if(run_start == True) :
                time.sleep(CLOCK_TIMER2 / (i+1) )
            else :
                time.sleep(MAX_CLOCK_TIMER)
                
        if(run_start == True) :
            run_start = False  # to continue MAX speed
        else:
            run_end_UD = True       # to decrease speed
            run_end_LR = True       # to decrease speed
            
    return run_start, run_end_UD, run_end_LR          

def Run_UP_DN_FT_RR(data_Control_org, data_Limit, new_loadcell_val_int_down, new_loadcell_val_int_front, new_loadcell_val_int_rear, run_start, run_end_UD, run_end_FR):
    
    data_Limit_UD = data_Limit & 0x003
    data_Limit_FR = data_Limit & 0x00c
    
    ## Go UP & FT : UP & RR : DN & FT : DN & RR
    if( (new_loadcell_val_int_down  < LOADCELL_DOWN_VALUE and new_loadcell_val_int_front < LOADCELL_LRFR_VALUE and data_Control_org == KEY_UP_FT) or  #Up & Front
        (new_loadcell_val_int_down  < LOADCELL_DOWN_VALUE and new_loadcell_val_int_rear  < LOADCELL_LRFR_VALUE and data_Control_org == KEY_UP_RR) or  #Up & Rear
        (new_loadcell_val_int_down  < LOADCELL_DOWN_VALUE and new_loadcell_val_int_front < LOADCELL_LRFR_VALUE and data_Control_org == KEY_DN_FT) or  #Down & Front
        (new_loadcell_val_int_down  < LOADCELL_DOWN_VALUE and new_loadcell_val_int_rear  < LOADCELL_LRFR_VALUE and data_Control_org == KEY_DN_RR)):   #Down & Rear   

        if( data_Control_org == KEY_UP_FT) :  #Up & Front
            GPIO.output(DIR_UP_DN, DIR_VAL_UP)
            GPIO.output(DIR_FT_RR, DIR_VAL_FT)
        elif(data_Control_org == KEY_UP_RR) :   #Up & Rear
            GPIO.output(DIR_UP_DN, DIR_VAL_UP)
            GPIO.output(DIR_FT_RR, DIR_VAL_RR)

        elif( data_Control_org == KEY_DN_FT) :  #Down & Front
            GPIO.output(DIR_UP_DN, DIR_VAL_DN)
            GPIO.output(DIR_FT_RR, DIR_VAL_FT)
        elif(data_Control_org == KEY_DN_RR) :   #Down & Rear
            GPIO.output(DIR_UP_DN, DIR_VAL_DN)
            GPIO.output(DIR_FT_RR, DIR_VAL_RR)
        
        for i in range(10):
            if(((data_Control_org == KEY_UP_FT or data_Control_org == KEY_UP_RR) and (data_Limit_UD != SW_UP)) or  
               ((data_Control_org == KEY_DN_FT or data_Control_org == KEY_DN_RR) and (data_Limit_UD != SW_DN))):   

                GPIO.output(CLK_UP_DN, True)
                
            if(((data_Control_org == KEY_UP_FT or data_Control_org == KEY_DN_FT) and (data_Limit_FR != SW_FT)) or  
               ((data_Control_org == KEY_UP_RR or data_Control_org == KEY_DN_RR) and (data_Limit_FR != SW_RR))):   
                
                GPIO.output(CLK_FT_RR, True)

            if(run_start == True) :
                time.sleep(CLOCK_TIMER2 / (i+1) )
            else :
                time.sleep(MAX_CLOCK_TIMER)

            if(((data_Control_org == KEY_UP_FT or data_Control_org == KEY_UP_RR) and (data_Limit_UD != SW_UP)) or  
               ((data_Control_org == KEY_DN_FT or data_Control_org == KEY_DN_RR) and (data_Limit_UD != SW_DN))):   

                GPIO.output(CLK_UP_DN, False)
                
            if(((data_Control_org == KEY_UP_FT or data_Control_org == KEY_DN_FT) and (data_Limit_FR != SW_FT)) or  
               ((data_Control_org == KEY_UP_RR or data_Control_org == KEY_DN_RR) and (data_Limit_FR != SW_RR))):   
                
                GPIO.output(CLK_FT_RR, False)
                
            if(run_start == True) :
                time.sleep(CLOCK_TIMER2 / (i+1) )
            else :
                time.sleep(MAX_CLOCK_TIMER)
                
        if(run_start == True) :
            run_start = False  # to continue MAX speed
        else:
            run_end_UD = True       # to decrease speed
            run_end_FR = True       # to decrease speed
    
    return run_start, run_end_UD, run_end_FR

def Run_LT_RT_FT_RR(data_Control_org, data_Limit, new_loadcell_val_int_left, new_loadcell_val_int_right, new_loadcell_val_int_front, new_loadcell_val_int_rear, run_start, run_end_LR, run_end_FR):
    
    data_Limit_LR = data_Limit & 0xf00
    data_Limit_FR = data_Limit & 0x00c
    
    ## Go LT & FT : LT & RR : RT & FT : RT & RR 
    if((new_loadcell_val_int_left  < LOADCELL_LRFR_VALUE and new_loadcell_val_int_front < LOADCELL_LRFR_VALUE and data_Control_org == KEY_LT_FT) or  #Left & Front
       (new_loadcell_val_int_left  < LOADCELL_LRFR_VALUE and new_loadcell_val_int_rear  < LOADCELL_LRFR_VALUE and data_Control_org == KEY_LT_RR) or  #Left & Rear
       (new_loadcell_val_int_right < LOADCELL_LRFR_VALUE and new_loadcell_val_int_front < LOADCELL_LRFR_VALUE and data_Control_org == KEY_RT_FT) or  #Right & Front
       (new_loadcell_val_int_right < LOADCELL_LRFR_VALUE and new_loadcell_val_int_rear  < LOADCELL_LRFR_VALUE and data_Control_org == KEY_RT_RR)):   #Right & Rear   

        if( data_Control_org == (KEY_LT_FT)): #Left & Front
            GPIO.output(DIR_LT_RT, DIR_VAL_LT)
            GPIO.output(DIR_FT_RR, DIR_VAL_FT)
        elif(data_Control_org == (KEY_LT_RR)):  #Left & Rear
            GPIO.output(DIR_LT_RT, DIR_VAL_LT)
            GPIO.output(DIR_FT_RR, DIR_VAL_RR)
            
        elif( data_Control_org == (KEY_RT_FT)): #Right & Front
            GPIO.output(DIR_LT_RT, DIR_VAL_RT)
            GPIO.output(DIR_FT_RR, DIR_VAL_FT)
        elif(data_Control_org == (KEY_RT_RR)):  #Right & Rear
            GPIO.output(DIR_LT_RT, DIR_VAL_RT)
            GPIO.output(DIR_FT_RR, DIR_VAL_RR)
        
        for i in range(10):
            if(((data_Control_org == KEY_LT_FT or data_Control_org == KEY_LT_RR) and (data_Limit_LR != SW_LT)) or  
               ((data_Control_org == KEY_RT_FT or data_Control_org == KEY_RT_RR) and (data_Limit_LR != SW_RT))):   

                GPIO.output(CLK_LT_RT, True)
                
            if(((data_Control_org == KEY_LT_FT or data_Control_org == KEY_RT_FT) and (data_Limit_FR != SW_FT)) or  
               ((data_Control_org == KEY_LT_RR or data_Control_org == KEY_RT_RR) and (data_Limit_FR != SW_RR))):   
                
                GPIO.output(CLK_FT_RR, True)

            if(run_start == True) :
                time.sleep(CLOCK_TIMER2 / (i+1) )
            else :
                time.sleep(MAX_CLOCK_TIMER)

            if(((data_Control_org == KEY_LT_FT or data_Control_org == KEY_LT_RR) and (data_Limit_LR != SW_LT)) or  
               ((data_Control_org == KEY_RT_FT or data_Control_org == KEY_RT_RR) and (data_Limit_LR != SW_RT))):   

                GPIO.output(CLK_LT_RT, False)
                
            if(((data_Control_org == KEY_LT_FT or data_Control_org == KEY_RT_FT) and (data_Limit_FR != SW_FT)) or  
               ((data_Control_org == KEY_LT_RR or data_Control_org == KEY_RT_RR) and (data_Limit_FR != SW_RR))):   
                
                GPIO.output(CLK_FT_RR, False)
                
            if(run_start == True) :
                time.sleep(CLOCK_TIMER2 / (i+1) )
            else :
                time.sleep(MAX_CLOCK_TIMER)
                
        if(run_start == True) :
            run_start = False  # to continue MAX speed
        else:
            run_end_LR = True       # to decrease speed
            run_end_FR = True       # to decrease speed
            
    return run_start, run_end_LR, run_end_FR

def Run_UP_DN_LT_RT_FT_RR(data_Control_org, data_Limit, new_loadcell_val_int_down, new_loadcell_val_int_left, new_loadcell_val_int_right, new_loadcell_val_int_front, new_loadcell_val_int_rear, run_start, run_end_UD, run_end_LR, run_end_FR):           
     
    data_Limit_UD = data_Limit & 0x003
    data_Limit_LR = data_Limit & 0xf00
    data_Limit_FR = data_Limit & 0x00c     
     
    ## Go UP & LT & FT : UP & LT & RR : UP & RT & FT : UP & RT & RR    :    DN & LT & FT : DN & LT & RR : DN & RT & FT : DN & RT & RR
    if( (new_loadcell_val_int_down < LOADCELL_DOWN_VALUE and new_loadcell_val_int_left  < LOADCELL_LRFR_VALUE and new_loadcell_val_int_front < LOADCELL_LRFR_VALUE and data_Control_org == KEY_UP_LT_FT) or  #Up & Left & Front
        (new_loadcell_val_int_down < LOADCELL_DOWN_VALUE and new_loadcell_val_int_left  < LOADCELL_LRFR_VALUE and new_loadcell_val_int_rear  < LOADCELL_LRFR_VALUE and data_Control_org == KEY_UP_LT_RR) or  #Up & Left & Rear
        (new_loadcell_val_int_down < LOADCELL_DOWN_VALUE and new_loadcell_val_int_right < LOADCELL_LRFR_VALUE and new_loadcell_val_int_front < LOADCELL_LRFR_VALUE and data_Control_org == KEY_UP_RT_FT) or  #Up & Right & Front
        (new_loadcell_val_int_down < LOADCELL_DOWN_VALUE and new_loadcell_val_int_right < LOADCELL_LRFR_VALUE and new_loadcell_val_int_rear  < LOADCELL_LRFR_VALUE and data_Control_org == KEY_UP_RT_RR) or  #Up & Right & Rear
        (new_loadcell_val_int_down < LOADCELL_DOWN_VALUE and new_loadcell_val_int_left  < LOADCELL_LRFR_VALUE and new_loadcell_val_int_front < LOADCELL_LRFR_VALUE and data_Control_org == KEY_DN_LT_FT) or  #Down & Left & Front
        (new_loadcell_val_int_down < LOADCELL_DOWN_VALUE and new_loadcell_val_int_left  < LOADCELL_LRFR_VALUE and new_loadcell_val_int_rear  < LOADCELL_LRFR_VALUE and data_Control_org == KEY_DN_LT_RR) or  #Down & Left & Rear
        (new_loadcell_val_int_down < LOADCELL_DOWN_VALUE and new_loadcell_val_int_right < LOADCELL_LRFR_VALUE and new_loadcell_val_int_front < LOADCELL_LRFR_VALUE and data_Control_org == KEY_DN_RT_FT) or  #Down & Right & Front
        (new_loadcell_val_int_down < LOADCELL_DOWN_VALUE and new_loadcell_val_int_right < LOADCELL_LRFR_VALUE and new_loadcell_val_int_rear  < LOADCELL_LRFR_VALUE and data_Control_org == KEY_DN_RT_RR)):   #Down & Right & Rear                 

        if( data_Control_org == KEY_UP_LT_FT): #Up & Left & Front
            GPIO.output(DIR_UP_DN, DIR_VAL_UP)
            GPIO.output(DIR_LT_RT, DIR_VAL_LT)
            GPIO.output(DIR_FT_RR, DIR_VAL_FT)
        elif( data_Control_org == KEY_UP_LT_RR): #Up & Left & Rear
            GPIO.output(DIR_UP_DN, DIR_VAL_UP)
            GPIO.output(DIR_LT_RT, DIR_VAL_LT)
            GPIO.output(DIR_FT_RR, DIR_VAL_RR)
        elif(data_Control_org == KEY_UP_RT_FT):  #Up & Right & Front
            GPIO.output(DIR_UP_DN, DIR_VAL_UP)
            GPIO.output(DIR_LT_RT, DIR_VAL_RT)
            GPIO.output(DIR_FT_RR, DIR_VAL_FT)
        elif(data_Control_org == KEY_UP_RT_RR):  #Up & Right & Rear
            GPIO.output(DIR_UP_DN, DIR_VAL_UP)
            GPIO.output(DIR_LT_RT, DIR_VAL_RT)
            GPIO.output(DIR_FT_RR, DIR_VAL_RR)
        elif( data_Control_org == KEY_DN_LT_FT): #Down & Left & Front
            GPIO.output(DIR_UP_DN, DIR_VAL_DN)
            GPIO.output(DIR_LT_RT, DIR_VAL_LT)
            GPIO.output(DIR_FT_RR, DIR_VAL_FT)
        elif( data_Control_org == KEY_DN_LT_RR): #Down & Left & Rear
            GPIO.output(DIR_UP_DN, DIR_VAL_DN)
            GPIO.output(DIR_LT_RT, DIR_VAL_LT)
            GPIO.output(DIR_FT_RR, DIR_VAL_RR)
        elif( data_Control_org == KEY_DN_RT_FT): #Down & Right & Front
            GPIO.output(DIR_UP_DN, DIR_VAL_DN)
            GPIO.output(DIR_LT_RT, DIR_VAL_RT)
            GPIO.output(DIR_FT_RR, DIR_VAL_FT)
        elif(data_Control_org == KEY_DN_RT_RR):  #Down & Right & Rear
            GPIO.output(DIR_UP_DN, DIR_VAL_DN)
            GPIO.output(DIR_LT_RT, DIR_VAL_RT)
            GPIO.output(DIR_FT_RR, DIR_VAL_RR)
        
        for i in range(10):
            if(((data_Control_org == KEY_UP_LT_FT or data_Control_org == KEY_UP_LT_RR or data_Control_org == KEY_UP_RT_FT or data_Control_org == KEY_UP_RT_RR) and (data_Limit_UD != SW_UP)) or  
               ((data_Control_org == KEY_DN_LT_FT or data_Control_org == KEY_DN_LT_RR or data_Control_org == KEY_DN_RT_FT or data_Control_org == KEY_DN_RT_RR) and (data_Limit_UD != SW_DN))):   

                GPIO.output(CLK_UP_DN, True)
                
            if(((data_Control_org == KEY_UP_LT_FT or data_Control_org == KEY_UP_LT_RR or data_Control_org == KEY_DN_LT_FT or data_Control_org == KEY_DN_LT_RR) and (data_Limit_LR != SW_LT)) or  
               ((data_Control_org == KEY_UP_RT_FT or data_Control_org == KEY_UP_RT_RR or data_Control_org == KEY_DN_RT_FT or data_Control_org == KEY_DN_RT_RR) and (data_Limit_LR != SW_RT))):   

                GPIO.output(CLK_LT_RT, True)
                
            if(((data_Control_org == KEY_UP_LT_FT or data_Control_org == KEY_UP_RT_FT or data_Control_org == KEY_DN_LT_FT or data_Control_org == KEY_DN_RT_FT) and (data_Limit_FR != SW_FT)) or  
               ((data_Control_org == KEY_UP_LT_RR or data_Control_org == KEY_UP_RT_RR or data_Control_org == KEY_DN_LT_RR or data_Control_org == KEY_DN_RT_RR) and (data_Limit_FR != SW_RR))):   
                
                GPIO.output(CLK_FT_RR, True)

            if(run_start == True) :
                time.sleep(CLOCK_TIMER2 / (i+1) )
            else :
                time.sleep(MAX_CLOCK_TIMER)
                
            if(((data_Control_org == KEY_UP_LT_FT or data_Control_org == KEY_UP_LT_RR or data_Control_org == KEY_UP_RT_FT or data_Control_org == KEY_UP_RT_RR) and (data_Limit_UD != SW_UP)) or  
               ((data_Control_org == KEY_DN_LT_FT or data_Control_org == KEY_DN_LT_RR or data_Control_org == KEY_DN_RT_FT or data_Control_org == KEY_DN_RT_RR) and (data_Limit_UD != SW_DN))):   

                GPIO.output(CLK_UP_DN, False)
                
            if(((data_Control_org == KEY_UP_LT_FT or data_Control_org == KEY_UP_LT_RR or data_Control_org == KEY_DN_LT_FT or data_Control_org == KEY_DN_LT_RR) and (data_Limit_LR != SW_LT)) or  
               ((data_Control_org == KEY_UP_RT_FT or data_Control_org == KEY_UP_RT_RR or data_Control_org == KEY_DN_RT_FT or data_Control_org == KEY_DN_RT_RR) and (data_Limit_LR != SW_RT))):   

                GPIO.output(CLK_LT_RT, False)
                
            if(((data_Control_org == KEY_UP_LT_FT or data_Control_org == KEY_UP_RT_FT or data_Control_org == KEY_DN_LT_FT or data_Control_org == KEY_DN_RT_FT) and (data_Limit_FR != SW_FT)) or  
               ((data_Control_org == KEY_UP_LT_RR or data_Control_org == KEY_UP_RT_RR or data_Control_org == KEY_DN_LT_RR or data_Control_org == KEY_DN_RT_RR) and (data_Limit_FR != SW_RR))):   
                
                GPIO.output(CLK_FT_RR, False)
                
            if(run_start == True) :
                time.sleep(CLOCK_TIMER2 / (i+1) )
            else :
                time.sleep(MAX_CLOCK_TIMER)
                
        if(run_start == True) :
            run_start = False  # to continue MAX speed
        else:
            run_end_UD = True       # to decrease speed               
            run_end_LR = True       # to decrease speed
            run_end_FR = True       # to decrease speed
            
    return run_start, run_end_UD, run_end_LR, run_end_FR

def All_Key_Relesed(data_Control_org, run_start, run_end_UD, run_end_LR, run_end_FR):
      
    if(data_Control_org == KEY_NONE):  
        if(run_end_UD == True):
            for i in range(10):
                GPIO.output(CLK_UP_DN, True)
                time.sleep((CLOCK_TIMER2 / 20) + i*0.0001)
                GPIO.output(CLK_UP_DN, False)
                time.sleep((CLOCK_TIMER2 / 20) + i*0.0001)
            run_end_UD = False
            run_start = True            
            #print("runend UD")

        if(run_end_LR == True):
            for i in range(10):
                GPIO.output(CLK_LT_RT, True)
                time.sleep((CLOCK_TIMER2 / 20) + i*0.0001)
                GPIO.output(CLK_LT_RT, False)
                time.sleep((CLOCK_TIMER2 / 20) + i*0.0001)
            run_end_LR = False
            run_start = True             
            #print("runend LR")

        if(run_end_FR == True):
            for i in range(10):
                GPIO.output(CLK_FT_RR, True)
                time.sleep((CLOCK_TIMER2 / 20) + i*0.0001)
                GPIO.output(CLK_FT_RR, False)
                time.sleep((CLOCK_TIMER2 / 20) + i*0.0001)
            run_end_FR = False
            run_start = True            
            #print("runend FR")
            
    return run_start, run_end_UD, run_end_LR, run_end_FR
