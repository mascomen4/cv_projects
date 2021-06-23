# This is my PyCharm CV projects
## 1. car_number_detection. Car Plate detection algoritgm
### This is the project for car numbers detection. Let's decompose the problem

1. Find data. 
    1. Download [https://avto-nomer.ru/cron/export_example.xml](https://avto-nomer.ru/cron/export_example.xml)
    2. Augment
2. Preprocess it. 
    1. Median filtering 
    2. Lighting correction
    3. Expand the quality of the image to make the quality higher
3. Find where is the number located.
    1. Use Canny filtering.
    2. Then Contour finding.
    3. **It seems I need to build the template matching after distance transform by myself. Похоже, нужно поменять ноль на 255. Но перед этим посмотреть какие данные в контейнере изображения** 
    4. TODO: Can I feed the contour to findContours() in OpenCV?
4. Perform the segmentation. 
    1. For Russian Numbers we have:
        1. Region on the right
        2. Car number on the left 
5. Use an algorithm to detect the digits and the letter
    1. Use SVM. 
        1. Build an SVM algorithm
        2. Probably, train it on the MNIST dataset
        3. Test it on the 
        4. Store it's val score, test score, mse
    2. MLP
        1. Build simple mlp.
        2. Use LRelu, Relu, Regression? activation
        3. Store it's val score, test score, mse
    3. CNN
        1. Define the CNN archtecture
        2. Build the CNN using Keras.
        3. Store it's val score, test score, mse
    4. GAN. ### START WITH THE GAN ###
        1. Steal the GAN architecture from my HT
        2. Train it on MNIST and then let's try that on new dataset.
        3. Store it's val score, test score, mse
6. Compare the Validation accuracy of the algs above

## 2.OpenCVBook - Exercises on the OpenCV book. 
