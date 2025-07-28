import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
import qrcode
import cv2
import os
from tkinter import filedialog, Tk
from PIL import Image as PILImage

class QRApp(BoxLayout):
    def __init__(self, **kwargs):
        super(QRApp, self).__init__(orientation='vertical', **kwargs)

        self.label = Label(text="Enter text to generate QR", size_hint=(1, 0.1))
        self.add_widget(self.label)

        self.text_input = TextInput(hint_text="Enter data", multiline=False, size_hint=(1, 0.1))
        self.add_widget(self.text_input)

        self.qr_image = Image(size_hint=(1, 0.5))
        self.add_widget(self.qr_image)

        self.generate_btn = Button(text="Generate QR Code", size_hint=(1, 0.1))
        self.generate_btn.bind(on_press=self.generate_qr)
        self.add_widget(self.generate_btn)

        self.scan_btn = Button(text="Scan QR from Camera", size_hint=(1, 0.1))
        self.scan_btn.bind(on_press=self.scan_qr)
        self.add_widget(self.scan_btn)

        self.select_btn = Button(text="Scan QR from Image", size_hint=(1, 0.1))
        self.select_btn.bind(on_press=self.select_image)
        self.add_widget(self.select_btn)

    def generate_qr(self, instance):
        data = self.text_input.text
        if not data:
            self.label.text = "Enter valid text"
            return

        img = qrcode.make(data)
        img.save("qr.png")
        self.display_qr("qr.png")

    def display_qr(self, path):
        pil_image = PILImage.open(path).convert('RGB')
        pil_image = pil_image.resize((200, 200))
        img_data = pil_image.tobytes()
        texture = Texture.create(size=pil_image.size, colorfmt='rgb')
        texture.blit_buffer(img_data, colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        self.qr_image.texture = texture

    def scan_qr(self, instance):
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        while True:
            ret, frame = cap.read()
            data, bbox, _ = detector.detectAndDecode(frame)
            if data:
                self.label.text = f"Scanned: {data}"
                break
            cv2.imshow("Scan QR (Press Q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def select_image(self, instance):
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            img = cv2.imread(file_path)
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(img)
            if data:
                self.label.text = f"Scanned from Image: {data}"
            else:
                self.label.text = "No QR code found in image."

class QRCodeApp(App):
    def build(self):
        return QRApp()

if __name__ == '__main__':
    QRCodeApp().run()
