import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QFileDialog
from PyQt5.QtGui import QIcon
from tango_script import tprint, tadd


class TangoIDE(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tango Script IDE")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: white; color: black;")

        icon_path = "icon/icon.ico"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: #f5f5f5; border: 1px solid #ddd;")
        layout.addWidget(self.output_text)

        self.input_text = QLineEdit(self)
        self.input_text.setPlaceholderText("Enter your code here...")
        self.input_text.setStyleSheet("background-color: white; border: 1px solid #ddd; padding: 5px;")
        layout.addWidget(self.input_text)

        self.run_button = self.create_button("Run", self.run_code)
        layout.addWidget(self.run_button)

        self.save_button = self.create_button("Save", self.save_file)
        layout.addWidget(self.save_button)

        self.load_button = self.create_button("Load", self.load_file)
        layout.addWidget(self.load_button)

        self.clear_button = self.create_button("Clear", self.clear_all)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)

    def create_button(self, text, callback):
        button = QPushButton(text, self)
        button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 5px;
                transition: background-color 0.3s, transform 0.1s;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
                transform: translateY(2px);
            }
        """)
        button.clicked.connect(callback)
        return button

    def run_code(self):
        code = self.input_text.text()
        try:
            if code.startswith("tprint"):
                text = code[6:].strip()
                result = tprint(text)
                self.output_text.append(str(result))
            elif "tadd" in code:
                expression = code[5:].strip()
                result = tadd(expression)
                self.output_text.append(str(result))
            else:
                self.output_text.append("Unknown command")
        except Exception as e:
            self.output_text.append(f"Error: {e}")

    def save_file(self):
        if not os.path.exists('scripts'):
            os.makedirs('scripts')

        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "scripts/", "Tango Script Files (*.tgs)")
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(self.input_text.text())
            except Exception as e:
                self.output_text.append(f"Error saving file: {e}")

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "scripts/", "Tango Script Files (*.tgs)")
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    code = file.read()
                    self.input_text.setText(code)
            except Exception as e:
                self.output_text.append(f"Error loading file: {e}")

    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()


def run_tango_ide():
    app = QApplication(sys.argv)
    window = TangoIDE()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_tango_ide()
