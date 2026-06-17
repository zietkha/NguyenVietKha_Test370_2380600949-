import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton, QMessageBox

class RailFenceCipher:
    def encrypt(self, plain_text, key):
        try:
            key = int(key)
        except ValueError:
            return plain_text
        if key <= 1 or key >= len(plain_text):
            return plain_text
        rails = [[] for _ in range(key)]
        row = 0
        direction = 1
        for char in plain_text:
            rails[row].append(char)
            if row == 0:
                direction = 1
            elif row == key - 1:
                direction = -1
            row += direction
        result = []
        for r in rails:
            result.extend(r)
        return "".join(result)

    def decrypt(self, cipher_text, key):
        try:
            key = int(key)
        except ValueError:
            return cipher_text
        if key <= 1 or key >= len(cipher_text):
            return cipher_text
        grid = [['\n' for _ in range(len(cipher_text))] for _ in range(key)]
        row = 0
        direction = 1
        for col in range(len(cipher_text)):
            grid[row][col] = '*'
            if row == 0:
                direction = 1
            elif row == key - 1:
                direction = -1
            row += direction
        idx = 0
        for r in range(key):
            for c in range(len(cipher_text)):
                if grid[r][c] == '*' and idx < len(cipher_text):
                    grid[r][c] = cipher_text[idx]
                    idx += 1
        plain_text = []
        row = 0
        direction = 1
        for col in range(len(cipher_text)):
            plain_text.append(grid[row][col])
            if row == 0:
                direction = 1
            elif row == key - 1:
                direction = -1
            row += direction
        return "".join(plain_text)

class RailFenceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cipher = RailFenceCipher()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Rail Fence Cipher GUI")
        self.setGeometry(100, 100, 500, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        layout.addWidget(QLabel("Văn bản đầu vào (Plain text / Cipher text):"))
        self.txtInput = QTextEdit()
        layout.addWidget(self.txtInput)
        
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("Khoá (Số đường ray - Key):"))
        self.txtKey = QLineEdit()
        self.txtKey.setPlaceholderText("Nhập số nguyên...")
        key_layout.addWidget(self.txtKey)
        layout.addLayout(key_layout)
        
        btn_layout = QHBoxLayout()
        self.btnEncrypt = QPushButton("Mã hoá (Encrypt)")
        self.btnEncrypt.clicked.connect(self.encrypt)
        btn_layout.addWidget(self.btnEncrypt)
        
        self.btnDecrypt = QPushButton("Giải mã (Decrypt)")
        self.btnDecrypt.clicked.connect(self.decrypt)
        btn_layout.addWidget(self.btnDecrypt)
        layout.addLayout(btn_layout)
        
        layout.addWidget(QLabel("Kết quả (Output):"))
        self.txtOutput = QTextEdit()
        self.txtOutput.setReadOnly(True)
        layout.addWidget(self.txtOutput)
        
    def encrypt(self):
        text = self.txtInput.toPlainText()
        key = self.txtKey.text()
        if not text or not key:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản và khoá!")
            return
        try:
            key_val = int(key)
            if key_val <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Khoá phải là một số nguyên dương!")
            return
            
        result = self.cipher.encrypt(text, key_val)
        self.txtOutput.setPlainText(result)
        
    def decrypt(self):
        text = self.txtInput.toPlainText()
        key = self.txtKey.text()
        if not text or not key:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản và khoá!")
            return
        try:
            key_val = int(key)
            if key_val <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Khoá phải là một số nguyên dương!")
            return
            
        result = self.cipher.decrypt(text, key_val)
        self.txtOutput.setPlainText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RailFenceApp()
    window.show()
    sys.exit(app.exec_())
