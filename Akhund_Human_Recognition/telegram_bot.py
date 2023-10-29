import tensorflow as tf
import telebot
import cv2
from keras.models import load_model
import numpy as np

mybot = telebot.TeleBot("token")

model = load_model('weight\Akhund_Human_Recognition.h5', compile=False)

@mybot.message_handler(commands=['start'])
def send_welcome(message):
    msg = mybot.send_message(message.chat.id,"سلام "+str(message.chat.first_name)+" خوش اومدی"+" \n"+
                            "/Recognition- یه عکس بفرست تا بهت بگم از ما هست یا نیست"+'\n'+
                            '/help- عکس شخص بفرست')
    

@mybot.message_handler(commands=['Recognition'])
def send_photo(message):
    msg = mybot.reply_to(message,"یه عکس بفرست")
    mybot.register_next_step_handler(msg,recognize_flowers)

def recognize_flowers(message):
    

    fileID = message.photo[-1].file_id
    file_info = mybot.get_file(fileID)
    downloaded_file = mybot.download_file(file_info.file_path)
    width = height = 224


    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    img = cv2.imread("image.jpg")
    image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = cv2.resize(image ,(width,height))
    img = img / 255
    img = img.reshape(1,width,height,3) 
    
    result = np.argmax(model.predict(img))
    print(result)
    
    if result == 0:
        mybot.send_message(message.chat.id,'از ما نیست👳🏻‍♂️')

    elif result == 1:
        mybot.send_message(message.chat.id,'از ماست 👨🏻👩🏻')


    
mybot.enable_save_next_step_handlers(delay=2)
mybot.load_next_step_handlers()

mybot.polling()