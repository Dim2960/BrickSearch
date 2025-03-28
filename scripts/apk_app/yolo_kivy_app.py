from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from ultralytics import YOLO

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
        self.capture = cv2.VideoCapture("data/raw/videos/lego_video_test.mp4")
        # Vous pouvez préciser explicitement le task pour éviter l'avertissement, par exemple:
        self.model = YOLO("scripts/apk_app/best.onnx", task="detect")
        self.selected_class = 23  # Valeur par défaut

        layout = BoxLayout(orientation='vertical')

        # Spinner pour sélectionner la classe (0 à 23)
        self.class_spinner = Spinner(
            text=str(self.selected_class),
            values=[str(i) for i in range(24)],
            size_hint=(None, None),
            size=(100, 44)
        )
        self.class_spinner.bind(text=self.on_class_select) # type: ignore 
        layout.add_widget(self.class_spinner)

        layout.add_widget(KivyCamera(self.capture, self.model, app=self))
        return layout

    def on_class_select(self, spinner, text):
        self.selected_class = int(text)
        print("Classe sélectionnée :", self.selected_class)

    def on_stop(self):
        self.capture.release()

if __name__ == '__main__':
    YOLOKivyApp().run()
