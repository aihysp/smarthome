import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from button_functions import send_command, call_light_service
import asyncio



websocket_url = "ws://10.0.1.20:8123/api/websocket"
auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjNGNmMDNmNzcxNzU0ZDY1ODlkZDgxOGNjNDQ4NDQ3ZCIsImlhdCI6MTY5MjgyMDA1NiwiZXhwIjoyMDA4MTgwMDU2fQ.yGR3oRgzLxlEeSWrBv5jLF5g85YcajoiONfzqBIwRZY"

class ReactStyleApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.on_button_stylesheet = "QPushButton { background-color: #2663a4; color: white; border-radius: 15px; padding: 10px; }"
        self.off_button_stylesheet = "QPushButton { background-color: #c0392b; color: white; border-radius: 15px; padding: 10px; }"

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowTitle("No Title Bar Window with Move")
        self.setGeometry(100, 100, 300, 150)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.title_label = QLabel("Light Control", self)
        self.title_label.setFont(QFont("Arial", 18))
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignTop)

        self.on_button = QPushButton("Turn On", self)
        self.on_button.setFont(QFont("Arial", 12))
        self.on_button.setStyleSheet(self.on_button_stylesheet)
        layout.addWidget(self.on_button)

        self.off_button = QPushButton("Turn Off", self)
        self.off_button.setFont(QFont("Arial", 12))
        self.off_button.setStyleSheet(self.off_button_stylesheet)
        layout.addWidget(self.off_button)

        self.on_button.pressed.connect(self.on_button_pressed)
        self.on_button.released.connect(self.on_button_released)
        self.off_button.pressed.connect(self.off_button_pressed)
        self.off_button.released.connect(self.off_button_released)

        self.show()

        self.close_timer = QTimer(self)
        self.close_timer.timeout.connect(self.close)
        self.close_timer.start(10000)

    def mousePressEvent(self, event):
        self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)

    def turn_on_light(self):
        service_call_json = call_light_service("turn_on", "light.yeelight_ceiling5_0x0000000007cbc767")
        asyncio.get_event_loop().run_until_complete(send_command(websocket_url, auth_token, service_call_json))

    def turn_off_light(self):
        service_call_json = call_light_service("turn_off", "light.yeelight_ceiling5_0x0000000007cbc767")
        asyncio.get_event_loop().run_until_complete(send_command(websocket_url, auth_token, service_call_json))

    # Button pressed and released event handlers
    def on_button_pressed(self):
        self.on_button.setStyleSheet("QPushButton { background-color: #2663a4; color: white; border-radius: 15px; padding: 10px; }")

    def on_button_released(self):
        self.on_button.setStyleSheet(self.on_button_stylesheet)
        self.turn_on_light()

    def off_button_pressed(self):
        self.off_button.setStyleSheet("QPushButton { background-color: #c0392b; color: white; border-radius: 15px; padding: 10px; }")

    def off_button_released(self):
        self.off_button.setStyleSheet(self.off_button_stylesheet)
        self.turn_off_light()

    # Function to create a JSON service call
    def call_light_service(self, service, entity_id):
        service_call = {
            "id": 24,
            "type": "call_service",
            "domain": "light",
            "service": service,
            "target": {
                "entity_id": entity_id
            }
        }
        service_call_json = json.dumps(service_call)
        return service_call_json

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReactStyleApp()
    sys.exit(app.exec_())