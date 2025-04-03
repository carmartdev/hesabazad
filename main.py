from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem
)
import sqlite3
conn = sqlite3.connect("main.db")
cur = conn.cursor()
try:
    cur.execute("""CREATE TABLE accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, phone INTEGER, category TEXT)""")
except:
    print("Database is already created")
try:
    accounts = cur.execute("""SELECT * FROM accounts""")
    accounts = accounts.fetchall()
except:
    dialog = QMessageBox()
    dialog.setMinimumSize(800, 640)
    dialog.setWindowTitle("خطا")
    dialog.setText("خطایی رخ داد")
    dialog.setInformativeText("نمیتوانیم به پایگاه داده متصل شویم")
    ret = dialog.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("سیستم حسابداری حساب آزاد")
        self.title = QLabel("حساب آزاد")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.font()
        font.setFamily("Lalehzar")
        self.title.setFont(font)
        self.setCentralWidget(self.title)

        toolbar = QToolBar("منوی اصلی")
        #toolbar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addToolBar(toolbar)
        
        accounts_action = QAction("حساب ها و اشخاص", self)
        accounts_action.setStatusTip("این دکمه به بخش حساب ها و اشخاص میرود که میتوان در آنجا نام اشخاص و حساب ها را وارد کنید.")
        accounts_action.triggered.connect(self.accountsAndPeople)
        toolbar.addAction(accounts_action)
        
        buy_action = QAction("خرید", self)
        buy_action.setStatusTip("خرید")
        buy_action.triggered.connect(self.buy)
        toolbar.addAction(buy_action)

        sell_action = QAction("فروش", self)
        sell_action.setStatusTip("فروش")
        sell_action.triggered.connect(self.sell)
        toolbar.addAction(sell_action)

        payment_action = QAction("پرداخت", self)
        payment_action.setStatusTip("پرداخت")
        payment_action.triggered.connect(self.payment)
        toolbar.addAction(payment_action)
        self.setStatusBar(QStatusBar(self))

        payment_action = QAction("گزارشات", self)
        payment_action.setStatusTip("گزارشات")
        payment_action.triggered.connect(self.logs)
        toolbar.addAction(payment_action)
        self.setStatusBar(QStatusBar(self))
        
    def accountsAndPeople(self, s):
        layout = QVBoxLayout()
        self.title = QLabel("حساب ها و اشخاص")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.title)

        add_accounts_btn = QPushButton(
            text = "افزودن حساب",
            parent = self
        )
        add_accounts_btn.clicked.connect(self.addAccountsPage)
        
        show_accounts_btn = QPushButton(
            text = "نمایش حساب ها",
            parent = self
        )
        show_accounts_btn.clicked.connect(self.showAccountsPage)
        
        
        layout.addWidget(self.title)
        layout.addWidget(add_accounts_btn)
        layout.addWidget(show_accounts_btn)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)        

    def addAccountsPage(self, s):
        # TODO: Add back buttons
        # TODO: Make form act on key press
        layout = QVBoxLayout()
        
        self.title = QLabel("افزودن حساب")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.title)
        
        self.name = QLineEdit()
        self.name.setMaxLength(10)
        self.name.setPlaceholderText("نام: (مثل: حسن حسنی٫ حساب فروش و ...)")

        self.cat = QLineEdit()
        self.cat.setMaxLength(10)
        self.cat.setPlaceholderText("دسته بندی")
        
        self.phone = QLineEdit()
        self.phone.setMaxLength(10)
        self.phone.setPlaceholderText("تلفن")

        submit = QPushButton(
            text = "افزودن",
            parent = self
        )
        submit.clicked.connect(self.addAccount)
        
        layout.addWidget(self.title)
        layout.addWidget(self.name)
        layout.addWidget(self.cat)
        layout.addWidget(self.phone)
        layout.addWidget(submit)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)        

    def showAccountsPage(self, s):
        layout = QVBoxLayout()
        
        self.title = QLabel("حساب ها")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.title)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("جستجو...")
        self.search_field.textChanged.connect(self.filter_table)
        layout.addWidget(self.search_field)


         # Create table widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['شناسه', 'نام', 'شماره تلفن', 'دسته بندی'])
        
        # Enable sorting
        self.table.setSortingEnabled(True)
        
        # Adjust column widths
        self.table.horizontalHeader().setStretchLastSection(True)

        # Set row count
        self.table.setRowCount(len(accounts))
        
        # Populate the table
        for row_idx, row_data in enumerate(accounts):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table.setItem(row_idx, col_idx, item)

        self.save_button = QPushButton("ذخیره ی تغییرات")
        self.save_button.clicked.connect(self.save_changes)
        
        
        layout.addWidget(self.title)
        layout.addWidget(self.table)
        layout.addWidget(self.save_button)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)        

    def filter_table(self, text):
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if text.lower() in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def save_changes(self):
        for row in range(self.table.rowCount()):
            record_id = self.table.item(row, 0).text()
            name = self.table.item(row, 1).text()
            phone = self.table.item(row, 2).text()
            category = self.table.item(row, 3).text()
        
            cur.execute("""
            UPDATE accounts 
            SET name=?, phone=?, category=?
            WHERE id=?
            """, (name, phone, category, record_id))
        
        conn.commit()
    
    def addAccount(self):
        if self.phone.text().isdigit() and self.name.text() and self.name.text():
            print(self.name.text(), self.phone.text(), self.cat.text())
            account = (self.name.text(), self.phone.text(), self.cat.text())
            sql = ("INSERT INTO accounts(name, phone, category) VALUES(?, ?, ?)")
            try:
                cur.execute(sql, account)
                conn.commit()
            except:
                # TODO: Make it suggest a new name
                dialog = QMessageBox()
                dialog.setMinimumSize(800, 640)
                dialog.setWindowTitle("خطا")
                dialog.setText("خطایی رخ داد")
                dialog.setInformativeText("نمیتوانیم این مشتری/حساب را اضافه کنیم لطفا چک کنید که تکراری یا غلط نباشد")
                ret = dialog.exec()
            
            accounts = cur.execute("""SELECT * FROM accounts""")
            accounts = accounts.fetchall()
            print(accounts)
        else:
            print("ERR: Wrong Format")
    def buy(self, s):
        self.title = QLabel("خرید")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.title)

    def sell(self, s):
        self.title = QLabel("فروش")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.title)

    def payment(self, s):
        self.title = QLabel("پرداخت")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.title)

    def logs(self, s):
        self.title = QLabel("گزارشات")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.title)
        
app = QApplication([])
window = MainWindow()
window.show()
app.exec()

conn.close()
