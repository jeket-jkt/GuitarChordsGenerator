from PyQt5 import QtWidgets
from ui_main import Ui_MainWindow
from chord_generator import ChordGenerator
from sound_player import SoundPlayer
import sys
from pathlib import Path
import random

PROJECT_ROOT = Path(__file__).parent

class ChordApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.generator = ChordGenerator(chords_file=PROJECT_ROOT / "data" / "chords.json")
        self.player = SoundPlayer(samples_path=PROJECT_ROOT / "data" / "samples")

        self.ui.btn_generate.clicked.connect(self.generate_progression)
        self.ui.btn_play.clicked.connect(self.play_current)
        self.ui.btn_stop.clicked.connect(self.stop_playback)
        self.ui.cmb_available.currentTextChanged.connect(self.on_available_selected)
        self.ui.btn_generate_pattern.clicked.connect(self.generate_pattern)
        self.ui.btn_save.clicked.connect(self.save_to_file)

        self.ui.cmb_available.addItems(self.generator.get_chord_list())

        self.current_prog = []
        self.current_pattern = ""

    def on_available_selected(self, text):
        text = text.strip()
        if not text:
            return
        self.current_prog = [text]
        self.ui.lbl_chord.setText(text)

    def generate_progression(self):
        mode = self.ui.cmb_mode.currentText()
        key = self.ui.cmb_key.currentText()
        length = int(self.ui.spn_length.value())

        prog = []

        if mode == 'pattern':
            pattern_key = getattr(self, "current_pattern", "")
            if not pattern_key:
                pattern_key = "I-vi-IV-V"
            prog = self.generator.get_progression(
                mode='pattern',
                pattern_key=pattern_key,
                key=key,
                length=length
            )
        elif mode == 'circle_walk':
            prog = self.generator.get_progression(mode='circle_walk', key=key, length=length)
        elif mode == 'diatonic':
            prog = self.generator.get_progression(mode='diatonic', key=key)
        elif mode == 'random':
            prog = [self.generator.get_random_chord() for _ in range(length)]
        else:
            prog = self.generator.get_progression(mode='rules', key=key, length=length)

        if prog is None:
            prog = []

        self.ui.lbl_chord.setText("  -  ".join(prog) if prog else "Ошибка генерации")
        self.current_prog = prog

    def generate_pattern(self):
        patterns = [
            "I-vi-IV-V",
            "I-IV-V-I",
            "ii-V-I",
            "I-V-vi-IV"
        ]
        self.current_pattern = random.choice(patterns)
        self.ui.lbl_pattern.setText(self.current_pattern)

    def play_current(self):
        prog = getattr(self, "current_prog", None)
        if not prog:
            label = self.ui.lbl_chord.text().strip()
            if not label:
                return
            prog = [s.strip() for s in label.split("-") if s.strip()]

        missing = [p for p in prog if not self.player.has_sample_for(p)]
        if missing:
            QtWidgets.QMessageBox.warning(self, "Отсутствуют сэмплы", ", ".join(missing))
            return

        self.player.play_progression(prog, delay=0.25)

    def stop_playback(self):
        self.player.stop()

    def save_to_file(self):
        prog = getattr(self, "current_prog", [])
        pattern = getattr(self, "current_pattern", "")
        key = self.ui.cmb_key.currentText()
        mode = self.ui.cmb_mode.currentText()
        bpm = self.ui.spn_bpm.value()

        if not prog:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Сначала сгенерируйте аккорды!")
            return

        text = []
        text.append(f"Key: {key}")
        text.append(f"Mode: {mode}")
        text.append("")
        text.append("Chord progression:")
        text.append("  " + " - ".join(prog))
        text.append("")
        text.append("Strumming pattern:")
        text.append("  " + (pattern if pattern else "not generated"))
        text.append("")
        text.append(f"Tempo: {bpm} BPM")
        text.append("")
        text.append("------------------------------------")

        content = "\n".join(text)

        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Сохранить как",
            "progression.txt",
            "Text Files (*.txt)"
        )

        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            QtWidgets.QMessageBox.information(self, "Готово", "Файл успешно сохранён!")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", str(e))

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ChordApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()