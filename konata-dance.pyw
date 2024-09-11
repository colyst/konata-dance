# made by colyst (dc: colyst)
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import keyboard
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QMovie, QPainter, QImage, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

############
# OPTIONAL # use this if you know how to create an app in spotify and put your client id and secret below. put "SPOTIPY_REDIRECT_URI" in "Redirect URIs" part of your app when you're creating it.
############

# spotipy web api
#SPOTIPY_CLIENT_ID = 'put your client id'
#SPOTIPY_CLIENT_SECRET = 'put your client secret'
#SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback' #USE THIS REDIRECT URI FOR SIMPLICITY

class GIFWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # pencere ayarlari
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_AlwaysShowToolTips, False)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.Tool, True)

        # gif yukleme
        gif_path = r'YOUR GIF PATH'  # gif yeri
        self.movie = QMovie(gif_path)

        # gif boyutu
        self.movie.jumpToFrame(0)
        gif_size = self.movie.frameRect().size()

        # aspect ratioyu bozmadan boyut hesaplama
        target_width = 400
        target_height = int(gif_size.height() * target_width / gif_size.width())

        # istenilen boyuta gifi boyutlandirir
        self.movie.setScaledSize(QSize(target_width, target_height))

        # gif display label
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, target_width, target_height)
        self.label.setMovie(self.movie)

        # golgeler
        self.shadow_widgets = [QLabel(self) for _ in range(4)]
        for shadow_widget in self.shadow_widgets:
            shadow_widget.lower() # golgeler gifin arkasinda

        # paddingle pencere ayarlari
        padding = 20
        window_width = target_width + padding
        window_height = target_height + padding
        self.setMinimumSize(QSize(window_width, window_height))

        # pencereyi ekranda ortaliyor (calismiyor galiba)
        screen_geo = QApplication.desktop().screenGeometry()
        window_geo = self.geometry()
        x = (screen_geo.width() - window_geo.width()) // 2
        y = (screen_geo.height() - window_geo.height()) // 2
        self.move(x, y)

        # animasyonu baslatiyor
        self.movie.start()

        # flag yayinla (etkilesim flagi)
        self.interaction_enabled = True

        # golge flagi
        self.shadows_enabled = False

        # hiz flagi
        self.bpm_speed_adjustment_enabled = False

        # base speed
        self.base_speed = 100  # Base speed for 133 BPM

        # you can change the shortcuts here.
        # kisayollar
        keyboard.add_hotkey('ctrl+shift+t', self.toggle_interaction)
        keyboard.add_hotkey('ctrl+shift+q', self.quit_application)
        keyboard.add_hotkey('ctrl+shift+y', self.toggle_shadows)
        keyboard.add_hotkey('ctrl+shift+u', self.toggle_bpm_speed_adjustment)

        # golgelerin gecikmesi ayarlari
        self.shadow_timer = QTimer(self)
        self.shadow_timer.timeout.connect(self.update_shadows)
        self.shadow_timer.start(100) # her 100 msde guncelleniyor

        # sabit golge rengi
        self.shadow_color = QColor(23, 44, 180, 255)

        # golgeler icin delay
        self.shadow_delay_timer = QTimer(self)
        self.shadow_delay_timer.timeout.connect(self.apply_shadow_update)
        self.shadow_delay_timer.start(100)

        # golgelerin gecikmesi icin onceki frameleri cahce'chee kaydediyor.
        self.frame_cache = []

        # spotipy api baslatma
        # FOR SPOTIFY #self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
        # FOR SPOTIFY #                                                    client_secret=SPOTIPY_CLIENT_SECRET,
        # FOR SPOTIFY #                                                    redirect_uri=SPOTIPY_REDIRECT_URI,
        # FOR SPOTIFY #                                                    scope='user-read-playback-state'))

        # bpm e gore hiz ayarlanmasi icin timer
        self.bpm_timer = QTimer(self)
        self.bpm_timer.timeout.connect(self.update_gif_speed)
        self.bpm_timer.start(5000) # her 5 snde bir bakiyor bpme.

    def toggle_interaction(self):
        self.interaction_enabled = not self.interaction_enabled
        if not self.interaction_enabled:
            self.setCursor(Qt.ArrowCursor)

    def toggle_shadows(self):
        self.shadows_enabled = not self.shadows_enabled
        if self.shadows_enabled:
            for shadow_widget in self.shadow_widgets:
                shadow_widget.show()
        else:
            for shadow_widget in self.shadow_widgets:
                shadow_widget.hide()

    def toggle_bpm_speed_adjustment(self):
        self.bpm_speed_adjustment_enabled = not self.bpm_speed_adjustment_enabled
        if not self.bpm_speed_adjustment_enabled:
            # bpm hizi ayarlamasi kapali oldugunda normal hizina doner
            self.movie.setSpeed(self.base_speed)
        # print(f"gif, sarkiya gore hareket {'ediyor.' if self.bpm_speed_adjustment_enabled else 'etmiyor.'}")

    def update_shadows(self):
        if self.shadows_enabled:
            # su anki frami cache icinde depoluyor
            self.frame_cache.append(self.movie.currentImage())
            if len(self.frame_cache) > len(self.shadow_widgets): # golgenin gecikmesi icin frameleri kaydediyor
                self.frame_cache.pop(0)

    def apply_shadow_update(self):
        if self.shadows_enabled and self.frame_cache:
            # farkli gecikmelerde golgeler olusturuluyor
            for i, shadow_widget in enumerate(self.shadow_widgets):
                transparency = 255 - (i + 1) * 85 # hepsi icin ayri transparencey
                shadow_color = QColor(23, 44, 180, transparency)

                # cache'den image cikariliyor
                if len(self.frame_cache) > i:
                    delayed_image = self.frame_cache[-(i + 1)] # frame gecikme ile aliniyor
                else:
                    continue

                colorized_image = self.apply_color(delayed_image, shadow_color)

                # qimage icin qpixmap olusturuluyor
                shadow_pixmap = QPixmap.fromImage(colorized_image)

                # pixmmap golge icin ayarlaniyor.
                shadow_widget.setPixmap(shadow_pixmap)

                # golgeler orijihnal gifin arkasinda mi kontrol ediliyor, yine asagi atiyor iste idk
                shadow_widget.lower()

                # golge gif'ibn yerine gore yerlestiriliyor.
                shadow_widget.move(self.label.pos())
                shadow_widget.resize(self.label.size())

    def apply_color(self, image, color):
        """secilen image frameinin icine secilen rengi boyama/s/.ecilen renkle boyama."""
        color_image = QImage(image.size(), QImage.Format_ARGB32)
        color_image.fill(Qt.transparent) # seffaf image ile baslaniyor sonra renklendiriliyor.

        painter = QPainter(color_image)
        painter.drawImage(0, 0, image)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(color_image.rect(), color)
        painter.end()

        return color_image

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.interaction_enabled:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.interaction_enabled:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def quit_application(self):
        QApplication.quit()

    def update_gif_speed(self):
        """bpme gore hiz ayarlama"""
        if not self.bpm_speed_adjustment_enabled:
            return

        try:
            current_track = self.sp.current_playback()
            if current_track is not None and 'item' in current_track:
                track_id = current_track['item']['id']
                audio_features = self.sp.audio_features(track_id)
                if audio_features and len(audio_features) > 0:
                    bpm = audio_features[0]['tempo']
                    # sarkinin bpmine gore hizi ayarla
                    scaling_factor = 0.4  # sarkinin bpmini sacling factora oranla
                    speed = max(10, min(500, self.base_speed + int((bpm - 133) * scaling_factor)))
                    self.movie.setSpeed(speed)
        except Exception as e:
            print(f"gif hizi ayarlamada hata, spotify api'dan gonderilen mesaj: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GIFWindow()
    window.show()
    sys.exit(app.exec_())

# made by colyst
