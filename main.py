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
    QLineEdit
)

accounts = []

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("سیستم حسابداری حساب آزاد")
        self.title = QLabel("حساب آزاد")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.font()
        font.setFamily("lalehzar")
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
        payment_action.triggered.connect(self.payment)
        toolbar.addAction(payment_action)
        self.setStatusBar(QStatusBar(self))

        
    def accountsAndPeople(self, s):
        layout = QVBoxLayout()
        
        self.title = QLabel("حساب ها و اشخاص")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.title)
        
        name = QLineEdit()
        name.setMaxLength(10)
        name.setPlaceholderText("نام: (مثل: حسن حسنی٫ حساب فروش و ...)")

        cat = QLineEdit()
        cat.setMaxLength(10)
        cat.setPlaceholderText("دسته بندی")
        
        phone = QLineEdit()
        phone.setMaxLength(10)
        phone.setPlaceholderText("تلفن")
        
        layout.addWidget(self.title)
        layout.addWidget(name)
        layout.addWidget(cat)
        layout.addWidget(phone)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)        
        
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
