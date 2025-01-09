#!/bin/env python3

from PyQt5 import QtWidgets as qt
from PyQt5.QtNetwork import QNetworkAccessManager as qNet, QNetworkRequest as qReq
from PyQt5.QtCore import  QUrl as qLink, QByteArray as qBytes
from PyQt5.QtGui import QPixmap


class HeroWid(qt.QMainWindow):
    url = qLink('http://127.0.0.1:8001')
    def __init__(self) -> None:
        super().__init__()
        self.initUi()
        self.manager = qNet()
        self.manager.finished.connect(self.handle_reply)

    def initUi(self):
        self.setWindowTitle('Stream')
        # main layout
        
        self.layout_ = qt.QVBoxLayout()
        self.image_label = qt.QLabel('Loading...') 
        self.field = qt.QLineEdit(self)
        self.field.setPlaceholderText('Type IP of the stream')
        self.field.textChanged.connect(self.input_url)
        self.text_field = qt.QLabel('127.0.0.1:8001')
        self.layout_.addWidget(self.text_field)
        # IP input field layout
        
        input_layout = qt.QHBoxLayout()
        self.stream_button = qt.QPushButton()
        self.stream_button.setText('Start Stream')
        self.stream_button.clicked.connect(self.start_stream)
        input_layout.addWidget(self.field)
        input_layout.addSpacing(8)
        input_layout.addWidget(self.stream_button)
        # importing layouts
        self.layout_.addLayout(input_layout)
        self.layout_.addSpacing(8)
        self.layout_.addWidget(self.image_label)
        self.window_ = qt.QWidget()
        self.window_.setLayout(self.layout_)
        self.setCentralWidget(self.window_)

    def input_url(self, text: str):
        self.url = qLink(f'http://{text}')
        self.text_field.setText(text)

    def display_image(self, data):
        pixmap = QPixmap()
        pixmap.loadFromData(qBytes(data))
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
    def start_stream(self):
        req = qReq(self.url)
        self.reply = self.manager.get(req)
        if self.reply:
            self.reply.readyRead.connect(self.read_stream)
    def read_stream(self):
        if self.reply:
            # Filtering JPEG bytes to display
            data = self.reply.readAll()
            start_id = data.indexOf(b'\xff\xd8')
            end_id = data.indexOf(b'\xff\xd9')
            if start_id != -1 and end_id != -1 and start_id < end_id:
                img = data[start_id:end_id+2]
                self.display_image(img)

    def handle_reply(self, reply):
        if reply.error():
            self.image_label.setText(f'Error: {reply.errorString()}')
        
def run_app():
    app = qt.QApplication([]) 
    window = HeroWid()
    window.show()
    app.exec()
exit(run_app())
