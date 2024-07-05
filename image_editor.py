import cv2
import numpy as np
from PyQt5.QtWidgets import (QMainWindow,
                             QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QComboBox, QMessageBox, QLineEdit, QFormLayout)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image Editor')
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image = None
        self.original_image = None

        self.load_button = QPushButton('Загрузить изображение', self)
        self.load_button.clicked.connect(self.load_image)

        self.capture_button = QPushButton('Сделать снимок с вебкамеры', self)
        self.capture_button.clicked.connect(self.capture_image)

        self.draw_line_button = QPushButton('Нарисовать линию', self)
        self.draw_line_button.clicked.connect(self.draw_line)

        self.sharpen_button = QPushButton('Изменить резкость', self)
        self.sharpen_button.clicked.connect(self.sharpen_image)

        self.rotate_button = QPushButton('Вращать изображение', self)
        self.rotate_button.clicked.connect(self.rotate_image)

        self.clear_lines_button = QPushButton('Очистить линии', self)
        self.clear_lines_button.clicked.connect(self.clear_lines)

        self.reset_rotation_button = QPushButton('Сбросить вращение', self)
        self.reset_rotation_button.clicked.connect(self.reset_rotation)

        self.angle_input = QLineEdit(self)
        self.angle_input.setPlaceholderText('Введите угол вращения')

        self.start_x_input = QLineEdit(self)
        self.start_x_input.setPlaceholderText('X начальной точки')
        self.start_y_input = QLineEdit(self)
        self.start_y_input.setPlaceholderText('Y начальной точки')
        self.end_x_input = QLineEdit(self)
        self.end_x_input.setPlaceholderText('X конечной точки')
        self.end_y_input = QLineEdit(self)
        self.end_y_input.setPlaceholderText('Y конечной точки')
        self.thickness_input = QLineEdit(self)
        self.thickness_input.setPlaceholderText('Толщина линии')

        self.channel_selector = QComboBox(self)
        self.channel_selector.addItem("Полное изображение")
        self.channel_selector.addItem("Красный канал")
        self.channel_selector.addItem("Зелёный канал")
        self.channel_selector.addItem("Синий канал")
        self.channel_selector.currentIndexChanged.connect(self.change_channel)

        # Layout for buttons and combo box
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.capture_button)
        button_layout.addWidget(self.draw_line_button)
        button_layout.addWidget(self.sharpen_button)
        button_layout.addWidget(self.clear_lines_button)
        button_layout.addWidget(self.channel_selector)

        # Layout for rotation controls
        rotation_layout = QHBoxLayout()
        rotation_layout.addWidget(self.angle_input)
        rotation_layout.addWidget(self.rotate_button)
        rotation_layout.addWidget(self.reset_rotation_button)

        # Layout for line controls
        line_layout = QFormLayout()
        line_layout.addRow('Начало X:', self.start_x_input)
        line_layout.addRow('Начало Y:', self.start_y_input)
        line_layout.addRow('Конец X:', self.end_x_input)
        line_layout.addRow('Конец Y:', self.end_y_input)
        line_layout.addRow('Толщина:', self.thickness_input)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(rotation_layout)
        main_layout.addLayout(line_layout)
        main_layout.addWidget(self.image_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Загрузить изображение", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            try:
                self.image = cv2.imread(file_name)
                self.original_image = self.image.copy()
                if self.image is None:
                    raise ValueError("Не удалось загрузить изображение")
                self.display_image()
            except Exception as e:
                self.show_error_message(str(e))

    def capture_image(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise ValueError("Не удалось открыть веб-камеру")
            ret, frame = cap.read()
            if not ret:
                raise ValueError("Не удалось сделать снимок")
            self.image = frame
            self.original_image = self.image.copy()
            self.display_image()
            cap.release()
        except Exception as e:
            self.show_error_message(str(e))

    def draw_line(self):
        if self.image is not None:
            try:
                start_x = int(self.start_x_input.text())
                start_y = int(self.start_y_input.text())
                end_x = int(self.end_x_input.text())
                end_y = int(self.end_y_input.text())
                thickness = int(self.thickness_input.text())
                color = (0, 255, 0)
                self.image = cv2.line(self.image, (start_x, start_y), (end_x, end_y), color, thickness)
                self.display_image()
            except ValueError:
                self.show_error_message("Координаты и толщина должны быть числами")

    def sharpen_image(self):
        if self.image is not None:
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
            self.image = cv2.filter2D(self.image, -1, kernel)
            self.display_image()

    def rotate_image(self):
        if self.image is not None:
            try:
                angle = float(self.angle_input.text())
                height, width = self.image.shape[:2]
                center = (width // 2, height // 2)
                matrix = cv2.getRotationMatrix2D(center, angle, 1)
                self.image = cv2.warpAffine(self.image, matrix, (width, height))
                self.display_image()
            except ValueError:
                self.show_error_message("Угол вращения должен быть числом")

    def clear_lines(self):
        if self.image is not None:
            self.image = self.original_image.copy()  # Restore original image
            self.display_image()

    def reset_rotation(self):
        if self.image is not None and self.original_image is not None:
            self.image = self.original_image.copy()
            self.angle_input.clear()
            self.display_image()

    def change_channel(self):
        if self.image is not None:
            index = self.channel_selector.currentIndex()
            if index == 0:
                self.display_image()
            else:
                r, g, b = cv2.split(self.image)
                blank = np.zeros_like(b)
                if index == 1:
                    channel_img = cv2.merge([blank, blank, r])  # Red channel
                elif index == 2:
                    channel_img = cv2.merge([blank, g, blank])  # Green channel
                elif index == 3:
                    channel_img = cv2.merge([b, blank, blank])  # Blue channel
                self.display_image(channel_img)

    def display_image(self, img=None):
        if img is None:
            img = self.image

        qformat = QImage.Format_RGB888
        if len(img.shape) == 2:  # grayscale
            qformat = QImage.Format_Grayscale8
        elif img.shape[2] == 4:  # RGBA
            qformat = QImage.Format_RGBA8888

        qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], qformat)
        qimg = qimg.rgbSwapped()
        self.image_label.setPixmap(QPixmap.fromImage(qimg))
        self.image_label.setScaledContents(True)


    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Ошибка")
        msg_box.exec_()