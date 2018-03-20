#from __future__ import print_function
import keras
from keras.layers import Dense, Flatten, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from scipy import ndimage
from sklearn.utils import shuffle
from PIL import ImageTk, Image, ImageDraw
import PIL
import Tkinter as tk
import math  
import cv2
import numpy as np
import os
import glob

# next two functions are used to adjust image acc to center of mass 
def getBestShift(img):
    cy,cx = ndimage.measurements.center_of_mass(img)

    rows,cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)

    return shiftx,shifty

def shift(img,sx,sy):
    rows,cols = img.shape
    M = np.float32([[1,0,sx],[0,1,sy]])
    shifted = cv2.warpAffine(img,M,(cols,rows))
    return shifted

def preprocessing(gray):
    # resize and invert colors(i.e convert to image with black background and white number)
    gray = cv2.resize(255-gray, (28, 28))
            
    # convert to perfect black and white image
    (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY| cv2.THRESH_OTSU) 
    
    # we crop the unless edges of the image
    while np.sum(gray[0]) == 0:
        gray = gray[1:]

    while np.sum(gray[:,0]) == 0:
        gray = np.delete(gray,0,1)

    while np.sum(gray[-1]) == 0:
        gray = gray[:-1]

    while np.sum(gray[:,-1]) == 0:
        gray = np.delete(gray,-1,1)
            
    # make aspect ratio such that any one side is of 20 pixel (jst to make sure all images are of same ratio)
    rows,cols = gray.shape
    if rows > cols:
        factor = 20.0/rows
        rows = 20
        cols = int(round(cols*factor))
        gray = cv2.resize(gray, (cols,rows))
    else:
        factor = 20.0/cols
        cols = 20
        rows = int(round(rows*factor))
        gray = cv2.resize(gray, (cols, rows))

    # add padding to make it 28 x 28 image and adjust acc to center of mass
    colsPadding = (int(math.ceil((28-cols)/2.0)),int(math.floor((28-cols)/2.0)))
    rowsPadding = (int(math.ceil((28-rows)/2.0)),int(math.floor((28-rows)/2.0)))
    gray = np.lib.pad(gray,(rowsPadding,colsPadding),'constant')

    shiftx,shifty = getBestShift(gray)
    shifted = shift(gray,shiftx,shifty)
    return shifted

# List of folders where the images of the digits are located
input_folder_list = ["eng","hindi","odia"]

'''
batch_size = 128
num_classes =30
epochs = 20
# input image dimensions
img_x, img_y = 28, 28

# Init empty arrays to store image, language used and digit shown in the image
input_data = []
language_labels = []
digit_labels = []

# Traverse through all files in the language folder and read data
for folder in input_folder_list:
    subfolders = os.listdir("./" + folder)
    for subfolder in subfolders:
        images = os.listdir("./" + folder + "/" + subfolder)
# lots of preprocessing were required to achieve good accuracy(86%)
        for image in images:
            gray = cv2.imread("./" + folder + "/" + subfolder + "/" + image, cv2.IMREAD_GRAYSCALE)
            gray = preprocessing(gray)
            # append image and correct value
            input_data.append(np.asarray(gray))
            language_labels.append(folder)
            digit_labels.append(subfolder)

input_data = np.asarray(input_data)
n_sample= len(input_data)
data = input_data.reshape((n_sample, -1))
digit_labels = np.asarray(digit_labels)
x_train = input_data
y_train = digit_labels

# shuffle the training data 
x_train,y_train = shuffle(x_train,y_train,random_state=2)

x_train = x_train.reshape(x_train.shape[0], img_x, img_y, 1)
input_shape = (img_x, img_y, 1)

# convert the data to the right type
x_train = x_train.astype('float32')
x_train /= 255

print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')

# convert class vectors to binary class matrices - this is for use in the
# categorical_crossentropy loss below
y_train = keras.utils.to_categorical(y_train, num_classes)


model = Sequential()
model.add(Conv2D(32, kernel_size=(5,5), strides=(1, 1),
                 activation='relu',
                 input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(64, (5, 5), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1)

# serialize model to JSON
model_json = model.to_json()
with open("model.json","w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

'''
# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = keras.models.model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])





def paint_window():
# FOR PAINT
    width = 200
    height = 200
    center = height//2
    white = (255, 255, 255)
    green = (0,128,0)
    
    def save():
        np_image1=np.array(image1)
        cv2.imwrite("./Predict/image.png",np_image1)
        
        predicted=[]
        images_for_prediction = []
        images = os.listdir("./Predict")
        for image in images:
            gray = cv2.imread("./Predict/" + image, cv2.IMREAD_GRAYSCALE)
            # same preprocessing as above
            images_for_prediction.append(np.asarray(gray))
            gray = preprocessing(gray)
            pr = model.predict_classes(gray.reshape((1,28, 28,1)),verbose=0)
            predicted.append(pr[0])
      
    
        images_for_prediction = np.asarray(images_for_prediction)
        predicted = np.asarray(predicted)
            
        n = len(predicted)
        
        for i in range(0,n,1):
            lan_index =  predicted[i]/10
            no = predicted[i]%10
            cv2.imwrite(".//Predicted//"+str(i)+str(input_folder_list[lan_index])+" "+str(no)+".jpg",images_for_prediction[i])
            
            if  predicted[i]==0:
                possibilities = " or hindi 0 or odia 0"+"\nas they have exact similar structure"
            elif predicted[i]==2:
                possibilities = " or hindi 2"+"\nas they have exact similar structure"
            elif predicted[i]==3:
                possibilities = " or hindi 3"+"\nas they have exact similar structure"
            elif predicted[i]==9:
                possibilities = " or hindi 1 or odia 2"+"\nas they have exact similar structure"
            elif predicted[i]==14:
                possibilities = " or odia 4"+"\nas they have exact similar structure"
            elif predicted[i]==17:
                possibilities = " or odia 7"+"\nas they have exact similar structure"
            elif predicted[i]==19:
                possibilities = " or odia 1"+"\nas they have exact similar structure"
            else:
                possibilities = ""
            
            print ("Seems like its "+str(input_folder_list[lan_index])+" "+str(no) +possibilities)

        print("Please draw something again or close window to exit\n")

    def paint(event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        cv.create_oval(x1, y1, x2, y2, fill="black",width=10)
        draw.line([x1, y1, x2, y2],fill="black",width=10)

    def clear():
        # delete all widgets 
        cv.delete("all")
        points = [0,0,200,200]
        cv.create_rectangle(points, outline='white',fill='white', width=2)
        draw.rectangle(points,fill='white')
    
    
    root = tk.Tk()
    # Tkinter create a canvas to draw on
    cv = tk.Canvas(root, width=width, height=height, bg='white')
    cv.pack()

    # PIL create an empty image and draw object to draw on
    # memory only, not visible
    image1 = PIL.Image.new("RGB", (width, height), white)
    draw = ImageDraw.Draw(image1)
    
    # do the Tkinter canvas drawings (visible)
    cv.pack(expand="YES", fill="both")
    cv.bind("<B1-Motion>", paint)
    
    # add buttons 
    button=tk.Button(text="Predict",command=save)
    button.pack()
    button=tk.Button(text="Clear",command=clear)
    button.pack()
    root.mainloop()



def page_scan():
    # FOR PAGE
    # crop the individual digits from the whole image
    #Specifiy the folder name
    im=cv2.imread('photo.jpg')
    height, width, channels = im.shape
    if height>=1000 and width>=1000:      
        print(str(height)+'\t'+str(width)+'\t'+str(channels)) 
        im = cv2.resize(im, (560, 780))
    gray= cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    cv2.normalize(gray,gray,0,255,cv2.NORM_MINMAX)
    (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY| cv2.THRESH_OTSU) # | cv2.THRESH_OTSU
        
 
    if gray.max()%2==0:
        ret,im_th = cv2.threshold(gray,0.5*gray.max(),255,1)
    else:
        ret,im_th=cv2.threshold(gray,0.5*(gray.max()-1),255,1)
            
    thresh2,ctrs, hier = cv2.findContours(im_th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
     
    rects = [cv2.boundingRect(ctr) for ctr in ctrs]
    pth="./Predict/"
    temp=1
    for rect in rects:
        # Draw the rectangle
        cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3) 
        # Make the rectangular region around the digit
        leng = int(rect[3] * 1)
        pt1 = int(rect[1] + rect[3] / 2 - leng / 2)
        pt2 = int(rect[0] + rect[2] / 2 - leng / 2)
        roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
        h,w=roi.shape
        if h>=10 and w>=10:
            cv2.imwrite(os.path.join(pth , "img"+str(temp)+".jpg"),255-roi)
            
        temp=temp+1
     

def predict_folder():
    predicted=[]
    images_for_prediction = []
    images = os.listdir("./Predict")
    for image in images:
        gray = cv2.imread("./Predict/" + image, cv2.IMREAD_GRAYSCALE)
        
        images_for_prediction.append(np.asarray(gray))
        # same preprocessing as above
        gray = preprocessing(gray)
        pr = model.predict_classes(gray.reshape((1,28, 28,1)),verbose=0)
        predicted.append(pr[0])
    
    images_for_prediction = np.asarray(images_for_prediction)
    predicted = np.asarray(predicted)

    count=[0,0,0] # at index  0->eng,1->hindi,2->odia
    n = len(predicted)
    for i in range(0,n,1):
        lan_index =  predicted[i]/10
        no = predicted[i]%10
        name = str(i+1)+")"+str(input_folder_list[lan_index])+" "+str(no)
        count[lan_index]=count[lan_index]+1
        
        if  predicted[i]==0:
            possibilities = ",hindi 0,odia 0"
            count[1]=count[1]+1
            count[2]=count[2]+1
        elif predicted[i]==2:
            possibilities = ",hindi 2"
            count[1]=count[1]+1
        elif predicted[i]==3:
            possibilities = ",hindi 3"
            count[1]=count[1]+1
        elif predicted[i]==9:
            possibilities = ",hindi 1,odia 2"
            count[1]=count[1]+1
            count[2]=count[2]+1
        elif predicted[i]==14:
            possibilities = ",odia 4"
            count[2]=count[2]+1
        elif predicted[i]==17:
            possibilities = ",odia 7"
            count[2]=count[2]+1
        elif predicted[i]==19:
            possibilities = ",odia 1"
            count[2]=count[2]+1
        else:
            possibilities = ""
                   
        cv2.imwrite(".//Predicted//"+name+possibilities+".jpg",images_for_prediction[i])
    return count
    




# menu

print "-----------WELCOME-----------"
print "Press 1: to Draw and Predict"
print "Press 2: Predict Language and equivalent value in English of single digit images"
print "Press 3: Predict Language of the written digits (supports multiple digits in the same image)"

choice = input("Enter your choice: ")

files = glob.glob('./Predicted/*')
for f in files:
    os.remove(f)

if   choice==1:
    files = glob.glob('./Predict/*')
    for f in files:
        os.remove(f)
    paint_window()
elif choice==2:
    predict_folder()
    print("done with predictions")
    print ("check the folder named as Predicted")
    print("Thank You")
elif choice==3:
    files = glob.glob('./Predict/*')
    for f in files:
        os.remove(f)
    page_scan()

    counta=predict_folder()
    
    if (counta[0]>=counta[1]) and (counta[0]>=counta[2]):
        lang="English"
    elif (counta[1]>=counta[0]) and (counta[1]>=counta[2]):
        lang="Hindi"
    elif (counta[2]>=counta[0]) and (counta[2]>=counta[1]):
        lang="Odia"    
        
    print "Script seems to be in "+lang
    print("Thank You")
else:
    print "Ops!! wrong input"
    











