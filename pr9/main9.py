"""_summary_
"""
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QMessageBox, QInputDialog, QListWidget
from database9 import hash_password, change_password, DB_PATH

class MainWindow(QMainWindow):
    """_summary_

    Args:
        QMainWindow (_type_): _description_
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management System")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.login_input = QLineEdit(self)
        self.login_input.setPlaceholderText("Login")
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.add_user_button = QPushButton("Add User", self)
        self.add_user_button.clicked.connect(self.add_user)
        layout.addWidget(self.add_user_button)

        self.change_password_button = QPushButton("Change Password", self)
        self.change_password_button.clicked.connect(self.change_password)
        layout.addWidget(self.change_password_button)

        self.show_users_button = QPushButton("Show All Users", self)
        self.show_users_button.clicked.connect(self.show_all_users)
        layout.addWidget(self.show_users_button)

        self.users_list = QListWidget(self)
        layout.addWidget(self.users_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_user(self):
        login = self.login_input.text()
        password = self.password_input.text()
        if login and password:
            hashed_password = hash_password(password)
            user_type, ok = QInputDialog.getInt(self, "User Type", "Enter user type (1 - admin, 2 - user):")
            if ok and user_type in [1, 2]:
                try:
                    connection = sqlite3.connect(DB_PATH)
                    cursor = connection.cursor()
                    cursor.execute('INSERT INTO Users (login, password, utype_id) VALUES (?, ?, ?)', (login, hashed_password, user_type))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    QMessageBox.information(self, "Success", "User added successfully!")
                except sqlite3.Error as error:
                    QMessageBox.critical(self, "Error", f"Failed to add user: {error}")
            else:
                QMessageBox.warning(self, "Warning", "Invalid user type entered.")
        else:
            QMessageBox.warning(self, "Warning", "Login and password fields cannot be empty.")

    def change_password(self):
        login = self.login_input.text()
        new_password, ok = QInputDialog.getText(self, "Change Password", "Enter new password:")
        if ok and new_password:
            change_password(login, new_password)
            QMessageBox.information(self, "Success", "Password changed successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Password cannot be empty.")

    def show_all_users(self):
        self.users_list.clear()
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute('SELECT login FROM Users')
            users = cursor.fetchall()
            cursor.close()
            connection.close()
            for user in users:
                self.users_list.addItem(user[0])
        except sqlite3.Error as error:
            QMessageBox.critical(self, "Error", f"Failed to retrieve users: {error}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
