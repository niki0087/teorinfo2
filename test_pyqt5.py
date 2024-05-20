from PyQt5.QtWidgets import QApplication, QWidget

def main():
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("Test QWidget")
    window.setGeometry(100, 100, 280, 80)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
