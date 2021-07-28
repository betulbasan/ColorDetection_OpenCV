import cv2
import pandas as pd

#Reading the image with opencv
#Resmi okutma
img = cv2.imread("a.jpg")

# değişken tanımlama
clicked = False
r = g = b = xpos = ypos = 0

#Reading csv file with pandas and giving names to each column
# Panda kütüphanesi ile csv dosyasını okuma ve her sütuna ad verme
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

#function to calculate minimum distance from all colors and get the most matching color
# tüm renkler ile minimum mesafeyi hesaplama ve en uygun rengi elde etme
#d = abs(Red – RedColor) + (Green – GreenColor) + (Blue – BlueColor)
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

#function to get x,y coordinates of mouse double click
#farenin çift tıklaması ile x, y koordinatlarını alma fonksiyonu
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK: # çift tıklamayı kontrol
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]     #rgb değerlerini  tıklanan x,y ile hesaplatma
        b = int(b)
        g = int(g)
        r = int(r)
       
cv2.namedWindow('image') #giriş görüntüsünün görüntüleceği pencere
cv2.setMouseCallback('image',draw_function)  # fare callback

while(1):

    cv2.imshow("image",img)
    if (clicked):  #çift tıklama geldiğinde rengi güncelle
   
        #cv2.rectangle(image, startpoint, endpoint, color)-1 dikdörtgeni renk ile doldurma
        cv2.rectangle(img,(20,20), (750,60), (b,g,r),-1)

        #Creating text string to display( Color name and RGB values )
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        #yazının rengi tipi
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #çok açık renkler için siyah yaz
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    #ESC ye basınca ekranı kapat
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()