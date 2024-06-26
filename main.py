from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

class MainApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.camera = Camera(play=True, index=0, resolution=(640, 480))
        self.layout.add_widget(self.camera)

        self.button = Button(text='Распознать')
        self.button.bind(on_press=self.detect)
        self.layout.add_widget(self.button)


    def carplate_extract(image, carplate_haar_cascade):
        carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)

        for x, y, w, h in carplate_rects:
            carplate_img = image[y+15:y+h-10, x+15:x+w-20]

        return carplate_img


    def enlarge_img(image, scale_percent):
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        plt.axis('off')
        resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        return resized_image


    def detect(self, instance):
        frame = self.camera.texture.pixels
        frame = np.frombuffer(frame, dtype='uint8')
        frame = frame.reshape(480, 640, 4)
        carplate_haar_cascade = cv2.CascadeClassifier('haar_cascades/haarcascade_russian_plate_number.xml')
        carplate_extract_img = self.carplate_extract(frame, carplate_haar_cascade)
        carplate_extract_img = self.enlarge_img(carplate_extract_img, 150)
        plt.imshow(carplate_extract_img)
        carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
        plt.axis('off')
        plt.imshow(carplate_extract_img_gray, cmap='gray')
        plt.show()
        print('Номер авто: ', pytesseract.image_to_string(
            carplate_extract_img_gray,
            config='--psm 6 --oem 3 -c tessedit_char_whitelist=АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789')
        )


if __name__ == '__main__':
    MainApp().run()
