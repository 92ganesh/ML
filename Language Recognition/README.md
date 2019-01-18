# Language Recognition
This project aims to recognize handwritten digits and to which language they belong. Currently three languages are supported i.e English(International), Hindi(National), Odia(Regional). 
This project was developed for an Machine Learning intership by JH Nirmal Sir(HOD of ETRX, KJSCE) in second year of Engineering.
To use the program just run the 'lang_recognition.py'
```bash
$ python lang_recognition.py
```

------------


## libraries/packages required:-
- numpy
- scipy
- keras
- Theano
- scikit-learn
- PIL
- Tkinter
- OpenCV (cv2) 

and all their dependencies

**Note:- **This program is created with python 2.7.14 and it is tested and proved to be working for conda distribution for python 2.7.

------------

## Special features of the Program:-
We have also saved the **trained model** and have provided with this program. So, now you do not have to waste time to train the network again. However training dataset have been provided too in case training is required.
There are 3 options in the menu that can be used:-
1.  To Draw and Predict
2.  Predict Language and equivalent value in English of single digit images
3. Predict Language of the written digits (supports multiple digits in the same image)

**For 1st option:-**
- Just Draw any digit in either English, Hindi or Odia and click **Predict**  button to view the prediction in the console. 
- Some structures have different meaning in different language. E.g. 1 in Hindi looks exactly same as 9 in English. For such cases Program will show both answer.
- **Please draw slowly**. The window on which you are drawing is fast enough to track moderate cursor movements but the same image is being
drawn in PIL at backend which is not so fast. This can lead to wrong predictions.
<br>

**For 2nd option:-**
- This option needs at least one image (no upper limit)
- Keep the images of digits in ‘Predict’ folder prior to the execution of the program and then select this
option.
- Each image should have exactly one digits on it written in any of the supported language (English, Hindi and Oriya).
- Try to keep the image with white background and black text format.
- You can either write them on paper and crop or else use any drawing tool (e.g. MS paint)
<br>

**For 3rd option:-**
- This option needs a image where multiple digits are written on it. Rename the image as ‘Photo.jpg’
- Keep the image in the same folder where you have kept the .py file prior to the execution of the program and then select this option. 
- Digits on it must be in any of the supported language.
- Try to keep the image in white background and black text format and separated by large distance (see the sample image that is provided).
- You can either write them on paper and crop or else use any drawing tool (e.g. MS paint)

------------

## How we did it:-
We used CNN for this purpose. 2000+ samples of digits written in three languages (English,Hindi and Odia) are used for training and around 400 samples are used for testing. Accuracy comes out to be above 90%. The model comprises of two 2D convolution layers.  Each followed by maxpooling and dropout.
Lots of preprocessing were required for images before they can be used for training. Those are explained in the code itself.
