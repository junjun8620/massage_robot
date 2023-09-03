import time

count = 0
x_count = 0
y_count = 0
move_done = True
read_pos = 0
run_while = True

################################################################################
while(run_while):   

    if(move_done):

        move_done = False
        if (read_pos < 4):
            read_pos += 1
        if read_pos == 4 :
            run_while = False
        print(read_pos)

        
    else:
        move_done = True

        time.sleep(0.5)
        print( "one work end" )
