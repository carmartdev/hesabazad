from PyQt6.QtCore import QSize, Qt, QDate
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
    QTableWidgetItem,
    QDateEdit
)
import sqlite3
conn = sqlite3.connect("main.db")
cur = conn.cursor()
try:
    cur.execute("""CREATE TABLE accounts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, phone INTEGER, category TEXT, debt INTEGER, credit INTEGER)""")
except:
    print("Database is already created")

try:
    cur.execute('''CREATE TABLE events
                 (id INTEGER PRIMARY KEY, name TEXT, date TEXT, category TEXT, descryption TEXT, debt INTEGER, credit INTEGER)''')
except:
    print("Database is already created")
    
try:
    events = cur.execute("""SELECT * FROM events""")
    events = events.fetchall()
    
except:
    print("Couldn't connect to Database")

try:
    accounts = cur.execute("""SELECT * FROM accounts""")
    accounts = accounts.fetchall()
except:
    print("Couldn't connect to database")

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
        
        accounts_action = QAction("راهنما", self)
        accounts_action.setStatusTip("برای اضافه٫ تغییر٫ حذف و یا مشاهده ی حساب ها و اشخاص")
        accounts_action.triggered.connect(self.accountsAndPeople)
        toolbar.addAction(accounts_action)

        events_action = QAction("روزنامه", self)
        events_action.setStatusTip("حساب روزانه")
        events_action.triggered.connect(self.events)
        toolbar.addAction(events_action)
        
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

    def events(self):
        layout = QVBoxLayout()
        self.title = QLabel("روزنامه")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.title)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("جستجو...")
        self.search_field.textChanged.connect(self.filter_table)
        layout.addWidget(self.search_field)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['شناسه', 'نام','تاریخ', 'دسته بندی', 'توضیحات', 'بدهکاری', 'بستانکاری'])

        self.table.setSortingEnabled(True)
        
        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.setRowCount(len(events))
        
        for row_idx, row_data in enumerate(events):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table.setItem(row_idx, col_idx, item)

        self.save_button = QPushButton("ذخیره ی تغییرات")
        self.save_button.clicked.connect(self.save_changes_for_events)

        add_events_btn = QPushButton(
            text = "افزودن حساب روزانه",
            parent = self
        )
        add_events_btn.clicked.connect(self.addEvents)
        
        layout.addWidget(self.title)
        layout.addWidget(self.table)
        layout.addWidget(self.save_button)
        layout.addWidget(add_events_btn)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
               
        conn.commit()
        
    def addEvents(self):
        # TODO: Add back buttons
        # TODO: Make form act on key press
        layout = QVBoxLayout()
        
        self.title = QLabel("افزودن حساب")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.title)
        
        self.name = QLineEdit()
        self.name.setMaxLength(20)
        self.name.setPlaceholderText("نام: (مثل: حسن حسنی٫ حساب فروش و ...)")
        # date
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)  # Enable calendar popup
        self.date.setDate(QDate.currentDate())  # Set default to today
        
        self.cat = QLineEdit()
        self.cat.setMaxLength(20)
        self.cat.setPlaceholderText("دسته بندی")
        
        self.descrypt = QLineEdit()
        self.descrypt.setMaxLength(11)
        self.descrypt.setPlaceholderText("توضیحات")

        self.debt = QLineEdit()
        self.debt.setMaxLength(13)
        self.debt.setPlaceholderText("بدهکاری")

        self.credit = QLineEdit()
        self.credit.setMaxLength(13)
        self.credit.setPlaceholderText("بستانکاری")
        
        submit = QPushButton(
            text = "افزودن",
            parent = self
        )
        submit.clicked.connect(self.addEvent)
        
        layout.addWidget(self.title)
        layout.addWidget(self.name)
        layout.addWidget(self.cat)
        layout.addWidget(self.date)
        layout.addWidget(self.debt)
        layout.addWidget(self.credit)
        layout.addWidget(submit)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def addEvent(self):
        if self.date and self.name.text():
            datestr = self.date.date().toString('yyyy-MM-dd')
            event = (self.name.text(), datestr, self.cat.text(), self.debt.text(), self.credit.text())
            sql = ("INSERT INTO events(name, date, category, debt, credit) VALUES(?, ?, ?, ?, ?)")
            try:
                cur.execute(sql, event)
                conn.commit()
            except:
                # TODO: Make it suggest a new name
                dialog = QMessageBox()
                dialog.setMinimumSize(800, 640)
                dialog.setWindowTitle("خطا")
                dialog.setText("خطایی رخ داد")
                dialog.setInformativeText("نمیتوانیم این مشتری/حساب را اضافه کنیم لطفا چک کنید که تکراری یا غلط نباشد")
                ret = dialog.exec()
            
            events = cur.execute("""SELECT * FROM events""")
            events = events.fetchall()
            print(events)
        else:
            print("ERR: Wrong Format")
            dialog = QMessageBox()
            dialog.setMinimumSize(800, 640)
            dialog.setWindowTitle("خطا")
            dialog.setText("خطایی رخ داد")
            dialog.setInformativeText("نمیتوانیم این مشتری/حساب را اضافه کنیم لطفا چک کنید که تکراری یا غلط نباشد")
            ret = dialog.exec()

    def save_changes_for_events(self):
        for row in range(self.table.rowCount()):
            record_id = self.table.item(row, 0).text()
            name = self.table.item(row, 1).text()
            date = self.table.item(row, 2).text()
            descrypt= self.table.item(row, 3).text()
            category = self.table.item(row, 4).text()
            debt = self.table.item(row, 5).text()
            credit = self.table.item(row, 6).text()

            cur.execute("""
            UPDATE events 
            SET name=?, date=?, , descryption=?, category=?,
            WHERE id=?, debt=?, credit=?
            """, (name, date, descrypt, category, record_id, debt, credit))
            
    def accountsAndPeople(self, s):
        layout = QVBoxLayout()
        self.title = QLabel("راهنما")
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
        self.name.setMaxLength(20)
        self.name.setPlaceholderText("نام: (مثل: حسن حسنی٫ حساب فروش و ...)")

        self.cat = QLineEdit()
        self.cat.setMaxLength(20)
        self.cat.setPlaceholderText("دسته بندی")
        
        self.phone = QLineEdit()
        self.phone.setMaxLength(11)
        self.phone.setPlaceholderText("تلفن")

        self.debt = QLineEdit()
        self.debt.setMaxLength(13)
        self.debt.setPlaceholderText("بدهکاری")

        self.credit = QLineEdit()
        self.credit.setMaxLength(13)
        self.credit.setPlaceholderText("بستانکاری")
        
        submit = QPushButton(
            text = "افزودن",
            parent = self
        )
        submit.clicked.connect(self.addAccount)
        
        layout.addWidget(self.title)
        layout.addWidget(self.name)
        layout.addWidget(self.cat)
        layout.addWidget(self.phone)
        layout.addWidget(self.debt)
        layout.addWidget(self.credit)
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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['شناسه', 'نام', 'شماره تلفن', 'دسته بندی', 'بدهکاری', 'بستانکاری'])
        
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
            debt = self.table.item(row, 4).text()
            credit = self.table.item(row, 5).text()
        
            cur.execute("""
            UPDATE accounts 
            SET name=?, phone=?, category=?
            WHERE id=?, debt=?, credit
            """, (name, phone, category, record_id, debt, credit))
        
        conn.commit()
    
    def addAccount(self):
        if self.phone.text().isdigit() and self.name.text() and self.name.text():
            account = (self.name.text(), self.phone.text(), self.cat.text(), self.debt.text(), self.credit.text())
            sql = ("INSERT INTO accounts(name, phone, category, debt, credit) VALUES(?, ?, ?, ?, ?)")
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
            dialog = QMessageBox()
            dialog.setMinimumSize(800, 640)
            dialog.setWindowTitle("خطا")
            dialog.setText("خطایی رخ داد")
            dialog.setInformativeText("نمیتوانیم این مشتری/حساب را اضافه کنیم لطفا چک کنید که تکراری یا غلط نباشد")
            ret = dialog.exec()
            
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
