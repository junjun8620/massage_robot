import cv2 as cv    # OpenCV import
import numpy as np  # 행렬(img)를 만들기 위한 np import
import time

power = 7
repeat = 5
speed = 5

loop_exit = True
file_save = False

in_data = list()


# function that handles the mousclicks
def process_click(event, x, y,flags, params):
    # check if the click is within the dimensions of the button
    global loop_exit, file_save
    if event == cv.EVENT_LBUTTONDOWN:
        if y > button[0] and y < button[1] and x > button[2] and x < button[3]:   
            loop_exit = False
            print('Clicked on Exit Button!')
        if y > button2[0] and y < button2[1] and x > button2[2] and x < button2[3]:   
            file_save = True
            print('Clicked on Save Button!')

# function that handles the trackbar
def power_set(val):
    # check if the value of the slider
    global power
    power = val
    print(val)
                
def repeat_set(val):
    # check if the value of the slider
    global repeat
    repeat = val
    print(val)

def speed_set(val):
    # check if the value of the slider
    global speed
    speed = val
    print(val)

def onmouse(event,x,y,flags,params): 
    global in_data, power, repeat, speed
    blue = green = red = 0
    if event == cv.EVENT_LBUTTONDOWN: 
        in_data.append(str(x))
        in_data.append(str(y))
        in_data.append(str(power * 2))
        in_data.append(str(repeat))
        in_data.append(str(speed))        
        if power < 4 :
            blue = ((power) * 50) + 100
            green = red = 0
        elif power >=4 and power < 7  :
            green = ((power-3) * 40) + 90
            blue = red = 0
        elif power >= 7 :
            red = ((power-6) * 40) + 90
            blue = green = 0
        
        cv.circle(img2,(x,y),8,(blue,green,red),-1)        
        #print(x, y)
        #print(in_data)
    #elif event == cv.EVENT_MOUSEMOVE: 
    #    a=1 
    elif event == cv.EVENT_LBUTTONUP: 
        a=1
        
#img = np.zeros((256, 256, 3), np.uint8)  # 행렬 생성, (가로, 세로, 채널(rgb)),bit)
img = cv.imread('person_back.jpg'); #이미지 불러오기

cv.namedWindow('image')  #마우스 이벤트 영역 윈도우 생성
cv.setMouseCallback('image', onmouse)
    
# create a window and attach a mousecallback and a trackbar
cv.namedWindow('Control')
cv.setMouseCallback('Control',process_click)

cv.createTrackbar(" Power", 'image', 7, 9, power_set)
cv.createTrackbar("Repeat", 'image', 5, 9, repeat_set)
cv.createTrackbar("Speed", 'image', 5, 9, speed_set)

# create button image
# button dimensions (y1,y2,x1,x2)
button = [20,60,30,310]
button2 = [80,120,30,310]

control_image = np.zeros((160,320), np.uint8) #control_image 변경
control_image[button[0]:button[1],button[2]:button[3]] = 220 #control_image 변경
control_image[button2[0]:button2[1],button2[2]:button2[3]] = 220 #control_image 변경
cv.putText(control_image, '   Exit Only  ',(50,50),cv.FONT_HERSHEY_PLAIN, 2,(0),3) #control_image 변경
cv.putText(control_image, 'Exit w/ Append',(40,110),cv.FONT_HERSHEY_PLAIN, 2,(0),3) #control_image 변경

#show 'control panel'
cv.imshow('Control', control_image)

img = cv.line(img, (70, 70),  (70, 185), (255, 0, 0), 1, 4)
img = cv.line(img, (70, 185), (140, 185),(255, 0, 0), 1, 4)
img = cv.line(img, (140,185), (140, 70), (255, 0, 0), 1, 4)
img = cv.line(img, (140,70),  (70, 70),  (255, 0, 0), 1, 4)

print('Original Dimensions : ',img.shape)
scale_percent = 200 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)

dim = (width, height)
img2 = cv.resize(img, dim, interpolation = cv.INTER_AREA)

counter1 = 0
while(loop_exit):

    cv.imshow('image', img2)

    k = cv.waitKey(1) & 0xFF
    if k == 27:    # ESC 키 눌러졌을 경우 종료
        print("ESC 키 눌러짐")
        break
    
    counter1 += 1
    if counter1 > 1000 :
        #time.sleep(0.5)
        print(in_data)
        counter1 = 0
        
    if file_save == True :
        f = open("massage_position.csv", "a")
        for i in range(0, len(in_data), 5):
            f.write(in_data[i] + ',' + in_data[i+1] + ',' + in_data[i+2] + ',' + in_data[i+3] + ',' + in_data[i+4] + '\n')
        f.close()
        loop_exit = False
        print("exit")


cv.destroyAllWindows()

