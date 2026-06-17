import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class RSAApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.private_key = None
        self.public_key = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("RSA Cipher & Signature GUI")
        self.setGeometry(100, 100, 750, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        lblTitle = QLabel("RSA Cipher & Digital Signature")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        lblTitle.setFont(font)
        lblTitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(lblTitle)
        
        # Grid layout for panels
        grid = QGridLayout()
        layout.addLayout(grid)
        
        # Left side: Cryptography (Mã hoá/Giải mã)
        grid.addWidget(QLabel("Plain text:"), 0, 0)
        self.txt_info = QTextEdit()
        grid.addWidget(self.txt_info, 1, 0)
        
        grid.addWidget(QLabel("Cipher text (Hex):"), 2, 0)
        self.txt_cipher = QTextEdit()
        grid.addWidget(self.txt_cipher, 3, 0)
        
        btn_crypto_layout = QHBoxLayout()
        self.btnEncrypt = QPushButton("Mã hoá (Encrypt)")
        self.btnEncrypt.clicked.connect(self.encrypt)
        btn_crypto_layout.addWidget(self.btnEncrypt)
        
        self.btnDecrypt = QPushButton("Giải mã (Decrypt)")
        self.btnDecrypt.clicked.connect(self.decrypt)
        btn_crypto_layout.addWidget(self.btnDecrypt)
        grid.addLayout(btn_crypto_layout, 4, 0)
        
        # Right side: Digital Signature (Ký/Xác minh)
        grid.addWidget(QLabel("Sign (Chữ ký Hex):"), 0, 1)
        self.txt_sign = QTextEdit()
        grid.addWidget(self.txt_sign, 1, 1)
        
        grid.addWidget(QLabel("Verify (Chữ ký để xác minh):"), 2, 1)
        self.txt_verify = QTextEdit()
        grid.addWidget(self.txt_verify, 3, 1)
        
        btn_sig_layout = QHBoxLayout()
        self.btnSign = QPushButton("Ký (Sign)")
        self.btnSign.clicked.connect(self.sign)
        btn_sig_layout.addWidget(self.btnSign)
        
        self.btnVerify = QPushButton("Xác minh (Verify)")
        self.btnVerify.clicked.connect(self.verify)
        btn_sig_layout.addWidget(self.btnVerify)
        grid.addLayout(btn_sig_layout, 4, 1)
        
        # Bottom: Key Generation
        btn_key_layout = QHBoxLayout()
        self.btnGenerate = QPushButton("Tạo khoá (Generate RSA Keys)")
        self.btnGenerate.clicked.connect(self.generate_keys)
        btn_key_layout.addWidget(self.btnGenerate)
        layout.addLayout(btn_key_layout)
        
    def generate_keys(self):
        try:
            key = RSA.generate(2048)
            self.private_key = key
            self.public_key = key.publickey()
            
            # Export and save keys locally
            private_pem = self.private_key.export_key()
            public_pem = self.public_key.export_key()
            
            with open("privateKey.pem", "wb") as f:
                f.write(private_pem)
            with open("publicKey.pem", "wb") as f:
                f.write(public_pem)
                
            QMessageBox.information(self, "Thành công", "Đã tạo cặp khoá và lưu vào file privateKey.pem, publicKey.pem thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tạo khoá: {e}")
            
    def load_keys_if_needed(self):
        if not self.private_key or not self.public_key:
            if os.path.exists("privateKey.pem") and os.path.exists("publicKey.pem"):
                try:
                    with open("privateKey.pem", "rb") as f:
                        self.private_key = RSA.import_key(f.read())
                    with open("publicKey.pem", "rb") as f:
                        self.public_key = RSA.import_key(f.read())
                except Exception as e:
                    QMessageBox.warning(self, "Cảnh báo", f"Lỗi đọc file khoá hiện có: {e}")
            else:
                QMessageBox.warning(self, "Lỗi", "Vui lòng bấm nút 'Tạo khoá' trước!")
                return False
        return True
        
    def encrypt(self):
        if not self.load_keys_if_needed():
            return
        text = self.txt_info.toPlainText()
        if not text:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản cần mã hoá vào ô Plain text!")
            return
        try:
            cipher = PKCS1_OAEP.new(self.public_key)
            ciphertext = cipher.encrypt(text.encode('utf-8'))
            self.txt_cipher.setPlainText(ciphertext.hex())
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Mã hoá thất bại: {e}")
            
    def decrypt(self):
        if not self.load_keys_if_needed():
            return
        ciphertext_hex = self.txt_cipher.toPlainText()
        if not ciphertext_hex:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ciphertext hex cần giải mã!")
            return
        try:
            cipher = PKCS1_OAEP.new(self.private_key)
            decrypted = cipher.decrypt(bytes.fromhex(ciphertext_hex))
            self.txt_info.setPlainText(decrypted.decode('utf-8'))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Giải mã thất bại: {e}")
            
    def sign(self):
        if not self.load_keys_if_needed():
            return
        text = self.txt_info.toPlainText()
        if not text:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản cần ký vào ô Plain text!")
            return
        try:
            h = SHA256.new(text.encode('utf-8'))
            signature = pkcs1_15.new(self.private_key).sign(h)
            self.txt_sign.setPlainText(signature.hex())
            # Auto-fill verify box for convenience
            self.txt_verify.setPlainText(signature.hex())
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Ký thất bại: {e}")
            
    def verify(self):
        if not self.load_keys_if_needed():
            return
        text = self.txt_info.toPlainText()
        signature_hex = self.txt_verify.toPlainText()
        if not text or not signature_hex:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản ở Plain text và chữ ký ở Verify!")
            return
        try:
            h = SHA256.new(text.encode('utf-8'))
            pkcs1_15.new(self.public_key).verify(h, bytes.fromhex(signature_hex))
            QMessageBox.information(self, "Kết quả", "Chữ ký HỢP LỆ!")
        except Exception as e:
            QMessageBox.warning(self, "Kết quả", f"Chữ ký KHÔNG hợp lệ! Chi tiết: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec_())
