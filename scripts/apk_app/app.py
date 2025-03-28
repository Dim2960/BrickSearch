from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from ultralytics import YOLO



def fetch_classes_data_from_files():
    # Ouvrir le fichier et construire le dictionnaire avec numéro de ligne comme clé
    with open("assets/classes.txt", "r", encoding="utf-8") as file:
        data_dict = {i : line.strip() for i, line in enumerate(file) if line.strip()}
    
    return data_dict


class KivyCamera(Image):
    def __init__(self, capture, model, app, fps=30, **kwargs):
        # Retire 'app' des kwargs afin d'éviter qu'il soit traité comme une propriété
        kwargs.pop('app', None)
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.model = model
        self.app = app  # On stocke la référence vers l'application
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Utilise la classe sélectionnée (par défaut ou choisie via le spinner)
            selected_class = self.app.selected_class
            results = self.model.predict(
                frame,
                conf=0.7,
                iou=0.5,
                classes=selected_class
            )[0]
            annotated_frame = results.plot()
            
            buf = cv2.flip(annotated_frame, 0).tobytes()
            img_texture = Texture.create(
                size=(annotated_frame.shape[1], annotated_frame.shape[0]),
                colorfmt='bgr'
            )
            img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = img_texture

class YOLOKivyApp(App):
    def build(self):
        self.capture = cv2.VideoCapture("/home/dim/clone_repo/BrickSearch/data/raw/videos/lego_video_test.mp4") # (0)
        # Vous pouvez préciser explicitement le task pour éviter l'avertissement, par exemple:
        self.model = YOLO("assets/best.pt", task="detect")
        self.selected_class = 1  # Valeur par défaut

        layout = BoxLayout(orientation='vertical')

        # Récupère le dictionnaire depuis le fichier
        data_dict = fetch_classes_data_from_files() 

        # Stocke le dictionnaire et crée le dictionnaire inversé : valeur -> clé
        self.data_dict = data_dict
        self.reverse_dict = {v: k for k, v in data_dict.items()}

        # Configure le Spinner pour afficher les valeurs du dictionnaire
        self.class_spinner = Spinner(
            text=self.data_dict[self.selected_class],  # Affiche la valeur associée à la clé par défaut
            values=[data_dict[k] for k in sorted(data_dict.keys())],
            size_hint=(None, None),
            size=(150, 44)
        )
        self.class_spinner.bind(text=self.on_class_select)
        layout.add_widget(self.class_spinner)

        layout.add_widget(KivyCamera(self.capture, self.model, app=self))
        return layout

    def on_class_select(self, spinner, text):
        # Récupère la clé entière correspondant à la valeur sélectionnée
        self.selected_class = self.reverse_dict[text]
        print("Classe sélectionnée :", self.selected_class)

    def on_stop(self):
        self.capture.release()


if __name__ == '__main__':
    YOLOKivyApp().run()
