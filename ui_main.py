from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Генератор аккордов для электрогитары")
        MainWindow.resize(820, 520)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)

        left_panel = QtWidgets.QVBoxLayout()
        main_layout.addLayout(left_panel, 2)

        group_chords = QtWidgets.QGroupBox("Генерация аккордов")
        block_chords = QtWidgets.QVBoxLayout(group_chords)

        self.lbl_chord = QtWidgets.QLabel("Аккорд / Прогрессия появится здесь")
        self.lbl_chord.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_chord.setMinimumHeight(40)
        block_chords.addWidget(self.lbl_chord)

        row1 = QtWidgets.QHBoxLayout()
        block_chords.addLayout(row1)

        self.btn_generate = QtWidgets.QPushButton("Сгенерировать")
        row1.addWidget(self.btn_generate)

        self.cmb_mode = QtWidgets.QComboBox()
        self.cmb_mode.addItems(['random', 'rules', 'pattern', 'circle_walk', 'diatonic'])
        row1.addWidget(self.cmb_mode)

        self.cmb_key = QtWidgets.QComboBox()
        self.cmb_key.addItems(["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"])
        self.cmb_key.setMaximumWidth(70)
        row1.addWidget(self.cmb_key)

        self.spn_length = QtWidgets.QSpinBox()
        self.spn_length.setRange(1, 12)
        self.spn_length.setValue(4)
        self.spn_length.setMaximumWidth(60)
        row1.addWidget(self.spn_length)

        left_panel.addWidget(group_chords)

        group_pattern = QtWidgets.QGroupBox("Ритмический рисунок (бой)")
        block_pattern = QtWidgets.QVBoxLayout(group_pattern)

        self.lbl_pattern = QtWidgets.QLabel("Бой будет показан здесь")
        self.lbl_pattern.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_pattern.setMinimumHeight(40)
        block_pattern.addWidget(self.lbl_pattern)

        row2 = QtWidgets.QHBoxLayout()
        block_pattern.addLayout(row2)

        self.btn_generate_pattern = QtWidgets.QPushButton("Сгенерировать бой")
        row2.addWidget(self.btn_generate_pattern)

        self.cmb_rhythm = QtWidgets.QComboBox()
        self.cmb_rhythm.addItems(['Down-Up','Rock','Ballad','Gallop','Shuffle','Palm Mute'])
        row2.addWidget(self.cmb_rhythm)

        self.spn_bpm = QtWidgets.QSpinBox()
        self.spn_bpm.setRange(40, 220)
        self.spn_bpm.setValue(100)
        self.spn_bpm.setMaximumWidth(70)
        row2.addWidget(self.spn_bpm)

        left_panel.addWidget(group_pattern)

        group_play = QtWidgets.QGroupBox("Проигрывание")
        block_play = QtWidgets.QHBoxLayout(group_play)

        self.btn_play = QtWidgets.QPushButton("Проиграть")
        block_play.addWidget(self.btn_play)

        self.btn_stop = QtWidgets.QPushButton("Остановить")
        block_play.addWidget(self.btn_stop)

        self.btn_save = QtWidgets.QPushButton("Сохранить")
        block_play.addWidget(self.btn_save)

        left_panel.addWidget(group_play)

        self.cmb_available = QtWidgets.QComboBox()
        left_panel.addWidget(self.cmb_available)

        right_panel = QtWidgets.QVBoxLayout()
        main_layout.addLayout(right_panel, 1)

        self.image_label = QtWidgets.QLabel()
        self.image_label.setFixedSize(360, 260)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setStyleSheet("background: #111; border: 1px solid #444;")
        right_panel.addWidget(self.image_label)

        self.lbl_info = QtWidgets.QLabel("Сэмплы: data/samples — имена: C.wav, Am.wav, G7.wav")
        self.lbl_info.setWordWrap(True)
        right_panel.addWidget(self.lbl_info)

        self.lbl_images = QtWidgets.QLabel("Изображения: data/images — имена: C.png, Am.png")
        self.lbl_images.setWordWrap(True)
        right_panel.addWidget(self.lbl_images)

        right_panel.addStretch()

        MainWindow.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-size: 14px;
            }
            QGroupBox {
                border: 1px solid #555;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton {
                background-color: #2d2d2d;
                border: 1px solid #555;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
            QLabel {
                font-size: 15px;
            }
            QComboBox {
                background-color: #2d2d2d;
                padding: 4px;
            }
            QSpinBox {
                background-color: #2d2d2d;
                padding: 4px;
            }
        """)