import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://daisseur.github.io/'))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        navbar = QToolBar()
        self.addToolBar(navbar)

        self.code = str()

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # input_code = QAction("Code", self)
        # input_ = QLineEdit()
        # input_code.hovered.connect(lambda:navbar.addWidget(input_))
        # input_code.triggered.connect(lambda:navbar.removeAction())
        # navbar.addAction(input_code)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)


    def navigate_home(self):
        self.browser.setUrl(QUrl('http://daisseur.github.io/'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())



app = QApplication(sys.argv)
QApplication.setApplicationName('My browser')
window = MainWindow()
app.exec_()


class App:

    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.browser = QWebEngineView()
        self.menuBar = QMenuBar()
        self.menuBar.move(10, 10)

        self.url = 'http://daisseur.github.io/'

        self._createMenuBar()
        self.menu()
        self.run()

    def click_button(self, txt, action):
        btn = QPushButton(txt)
        btn.clicked.connect(action)
        return btn

    def _createMenuBar(self):

        # Creating menus using a QMenu object
        self.menuBar.addMenu("&File")

        self.menuBar.addMenu("&Edit")
        self.menuBar.addMenu("&Help")
        self.menuBar.addAction("&help", lambda:self.browser)
        self.layout.addWidget(self.menuBar)

    def menu(self):
        self.browser.setUrl(QUrl(self.url))
        self.layout.addWidget(self.browser)

    def run(self):
        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec()

