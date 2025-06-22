import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
import time
from collections import defaultdict

def load_label_map(filepath="labels.txt"):
    label_map = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                idx, name = line.strip().split(":", 1)
                label_map[int(idx)] = name
    return label_map

class FaceRecognitionThread(QThread):
    # Signal: QImage hasil kamera + list face_infos
    frame_updated = pyqtSignal(QImage, list)

    def __init__(self, model_path, label_map):
        super().__init__()
        self.model = load_model(model_path)
        self.label_map = label_map
        self.running = True
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.conf_threshold = 0.6
        # Track: key = (pred_idx, x, y) untuk unik, value = t_start muncul
        self.face_appear_times = {}
        self.last_seen = {}

    def run(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue

            faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
            face_infos = []
            now = time.time()

            for i, (x, y, w, h) in enumerate(faces[:4]):
                face_img = frame[y:y+h, x:x+w]
                face_resized = cv2.resize(face_img, (96, 96))
                face_array = face_resized.astype("float32") / 255.0
                face_array = np.expand_dims(face_array, axis=0)

                pred = self.model.predict(face_array)[0]
                pred_idx = int(np.argmax(pred))
                pred_acc = float(pred[pred_idx])
                nama = self.label_map.get(pred_idx, f"ID {pred_idx}")

                # Key untuk tracking: id+posisi (agak toleran jika wajah geser dikit)
                key = (pred_idx, round(x/10)*10, round(y/10)*10)

                # Track waktu muncul
                if key not in self.face_appear_times:
                    self.face_appear_times[key] = now
                detik_muncul = now - self.face_appear_times[key]
                self.last_seen[key] = now

                if pred_acc >= self.conf_threshold:
                    face_infos.append({
                        "box": (x, y, w, h),
                        "nama": nama,
                        "akurat": pred_acc,
                        "detik": detik_muncul,
                        "pred_idx": pred_idx,
                    })
                    # Gambar bounding box + label di bawah kotak
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                    cv2.putText(frame, f"{nama} | {detik_muncul:.1f}s | {pred_acc:.2f}", (x, y+h+28),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            # Bersihkan wajah yang tidak terlihat >1.2 detik
            to_del = [k for k, t in self.last_seen.items() if now - t > 1.2]
            for k in to_del:
                self.face_appear_times.pop(k, None)
                self.last_seen.pop(k, None)

            # Konversi frame ke QImage untuk PyQt5
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            qimg = QImage(rgb_frame.data, w, h, ch * w, QImage.Format_RGB888)
            self.frame_updated.emit(qimg, face_infos)
            time.sleep(0.03)  # ~30 fps

        cap.release()

    def stop(self):
        self.running = False

# --- TEST (opsional, tidak perlu jika hanya dipanggil dari PyQt) ---
if __name__ == "__main__":
    label_map = load_label_map("labels.txt")
    model_path = "farsfea25.keras"
    recog_thread = FaceRecognitionThread(model_path, label_map)
