from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.widget import Widget
import cv2
import pytesseract
from kivy.app import App


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        scan_button = Button(text='Сканировать', background_color=(0.2, 0.6, 1, 1), size_hint=(1, 0.5), font_size=20)
        scan_button.bind(on_release=self.scan) 
        exit_button = Button(text='Выйти', background_color=(1, 0.2, 0.2, 1), size_hint=(1, 0.5), font_size=20)
        exit_button.bind(on_release=self.exit_app) 

        layout.add_widget(scan_button)
        layout.add_widget(exit_button)
        self.add_widget(layout)

    def scan(self, instance):
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction='left')  
        app.root.current = 'second'  

    def exit_app(self, instance):
        App.get_running_app().stop()


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        spacer = Widget(size_hint=(1, 0.2))
        self.camera = Camera(resolution=(640, 480), size_hint=(1, 0.6))
        self.camera.play = True  
        self.image1 = Image(source='image1.png')
        self.image1.allow_stretch = False
        self.image1.keep_ratio = True
        self.text_label = Label(text='Поместите документ ровно в рамку ')
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        retake_button = Button(text='Переснять', background_color=(1, 0.2, 0.2, 1))
        retake_button.bind(on_release=self.retake_photo)
        continue_button = Button(text='Продолжить', background_color=(0.2, 0.6, 1, 1))
        continue_button.bind(on_release=self.show_next_screen)
        image2 = Image(source='image2.png', size_hint=(1, 0.2))
        image2.allow_stretch = False
        image2.keep_ratio = True
        self.layout.add_widget(spacer)
        self.layout.add_widget(self.camera)
        self.layout.add_widget(self.text_label)
        self.layout.add_widget(self.image1)
        self.layout.add_widget(image2)
        buttons_layout.add_widget(retake_button)
        buttons_layout.add_widget(continue_button)
        self.layout.add_widget(buttons_layout)
        self.add_widget(self.layout)
        self.photo_taken = False  

    def retake_photo(self, instance):
        if self.photo_taken:
            self.layout.remove_widget(self.image1)  
            self.image1 = Image(source='image1.png')  
            self.image1.allow_stretch = False
            self.image1.keep_ratio = True
            self.layout.add_widget(self.image1)  
            self.text_label.text = 'Поместите документ ровно в рамку '  
            self.photo_taken = False
        else:
            self.camera.export_to_png("photo.png")  
            self.layout.remove_widget(self.image1)  
            self.image1 = Image(source='photo.png') 
            self.image1.allow_stretch = False
            self.image1.keep_ratio = True
            self.layout.add_widget(self.image1)  
            self.text_label.text = 'Фотография сделана '  
            self.photo_taken = True

    def process_image(self):
        
        img = cv2.imread('photo.png')

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        x1, y1, w1, h1 = 1010, 325, 330, 50
        x2, y2, w2, h2 = 430, 140, 330, 50
        x3, y3, w3, h3 = 440, 200, 500, 50
        x4, y4, w4, h4 = 470, 330, 250, 50
        x7, y7, w7, h7 = 485, 625, 250, 50
        x8, y8, w8, h8 = 1000, 615, 250, 50
        x9, y9, w9, h9 = 440, 265, 500, 50

S
        pass_id = gray[y1:y1 + h1, x1:x1 + w1]
        l_name = gray[y2:y2 + h2, x2:x2 + w2]
        f_name = gray[y3:y3 + h3, x3:x3 + w3]
        date_bd = gray[y4:y4 + h4, x4:x4 + w4]
        date_iss = gray[y7:y7 + h7, x7:x7 + w7]
        validity = gray[y8:y8 + h8, x8:x8 + w8]
        patronymic = gray[y9:y9 + h9, x9:x9 + w9]


        pass_id_text = pytesseract.image_to_string(pass_id)
        l_name_text = pytesseract.image_to_string(l_name)
        f_name_text = pytesseract.image_to_string(f_name)
        date_bd_text = pytesseract.image_to_string(date_bd)
        date_iss_text = pytesseract.image_to_string(date_iss)
        validity_text = pytesseract.image_to_string(validity)
        patronymic_text = pytesseract.image_to_string(patronymic)

        if len(pass_id_text) != 9:
            self.show_error_message()
        else:

            def show_next_screen(self, instance):
                app = App.get_running_app()
                app.root.transition = SlideTransition(direction='left')

                app = App.get_running_app()
                app.root.transition = SlideTransition(direction='left')

                if len(pass_id_text) != 9:
                    self.show_error_message()
                else:
                    app.root.current = 'third'
                    third_screen = app.root.get_screen('third')
                    third_screen.update_labels(pass_id_text, l_name_text, f_name_text, date_bd_text, date_iss_text,
                                               validity_text, patronymic_text)



        self.show_next_screen(pass_id_text, l_name_text, f_name_text, date_bd_text, date_iss_text, validity_text,  patronymic_text)

def show_error_message(self):
    from kivy.uix.popup import Popup
    from kivy.uix.label import Label

    content = Label(text="Что-то пошло не так с нашей стороны.\nПопробуйте еще раз.")
    popup = Popup(title="Ошибка", content=content, size_hint=(0.8, 0.4))
    popup.open()



class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super(ThirdScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.pass_id_label = Label(text="Номер паспорта: ")
        self.l_name_label = Label(text="Фамилия: ")
        self.f_name_label = Label(text="Имя: ")
        self.patronymic = Label(text="Отчество: ")
        self.date_bd_label = Label(text="Дата рождения: ")
        self.date_iss_label = Label(text="Дата выдачи: ")
        self.validity_lable = Label(text="Дата действительности: ")
        layout.add_widget(self.pass_id_label)
        layout.add_widget(self.l_name_label)
        layout.add_widget(self.f_name_label)
        layout.add_widget(self.date_bd_label)
        layout.add_widget(self.date_iss_label)
        self.add_widget(layout)

    def update_labels(self, pass_id_text, l_name_text, f_name_text, date_bd_text, date_iss_text, validity_text, patronymic_text):
        self.pass_id_label.text = "Номер паспорта: " + pass_id_text
        self.l_name_label.text = "Фамилия: " + l_name_text
        self.f_name_label.text = "Имя: " + f_name_text
        self.patronymic_lable = "Отчество" + patronymic_text
        self.date_bd_label.text = "Дата рождения: " + date_bd_text
        self.date_iss_label.text = "Дата выдачи: " + date_iss_text
        self.validity_lable.text = "Дата действительности: " + validity_text

class MyScreenManager:
    pass


class MyApp(App):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(ThirdScreen(name='third'))
        return sm

if __name__ == '__main__':
    MyApp().run()