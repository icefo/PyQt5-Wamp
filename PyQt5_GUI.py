import sys
import functools
import asyncio

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLineEdit, QGridLayout

from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession
from autobahn import wamp

from quamash import QEventLoop


def wrap_in_future(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        asyncio.async(func(*args, **kw))
    return wrapper


class MainWindow(ApplicationSession, QMainWindow):

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        QMainWindow.__init__(self)
        self.bla = "hh"

        self.the_widget = MainWidget(parent=self)
        self.statusBar()
        self.main_window_init()

    @wamp.subscribe('com.myapp.the_time')
    def time_event_handler(self, time):
        self.statusBar().showMessage("Time: " + time, msecs=2000)

    @asyncio.coroutine
    def onJoin(self, details):
        print("session ready")
        try:
            res = yield from self.subscribe(self)
            print("Subscribed to {0} procedure(s)".format(len(res)))
        except Exception as e:
            print("could not subscribe to procedure: {0}".format(e))

    def main_window_init(self):
        self.setCentralWidget(self.the_widget)

        #                 x    y  x_size y_size
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('PyQt5-Wamp')
        self.show()


class MainWidget(QWidget):

    def __init__(self, parent):
        # this allow the use of the parent's methods when needed
        super(MainWidget, self).__init__(parent=parent)

        self.number_1 = QLineEdit()
        self.number_2 = QLineEdit()

        self.addition_button = QPushButton("push to add !")
        self.addition_result = QLineEdit()

        self.widget_init()

    def widget_init(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.addition_button.clicked.connect(self.collect_numbers)

        grid.addWidget(self.number_1, 0, 0)
        grid.addWidget(self.number_2, 0, 3)
        grid.addWidget(self.addition_button, 1, 2)
        grid.addWidget(self.addition_result, 2, 2)

    @wrap_in_future  # PyQT5 can't call a coroutine directly so we wrap it in a future
    @asyncio.coroutine
    # the function is called with a second positional argument that is False
    # I haven't figured out why
    def collect_numbers(self, dummy=False):
        number_1 = self.number_1.displayText()
        number_2 = self.number_2.displayText()
        print("numbers to add: ", [number_1, number_2])

        # make the wamp call using the call method instantiated in the MainWindows class
        result = yield from self.parent().call('com.myapp.add', [number_1, number_2])
        self.addition_result.setText(str(result))


if __name__ == "__main__":
    # the quamash lib create an asyncio_driven loop that is used by PyQt5 and autobahn

    QT_app = QApplication(sys.argv)

    asyncio_loop = QEventLoop(QT_app)
    asyncio.set_event_loop(asyncio_loop)

    runner = ApplicationRunner(url="ws://127.0.0.1:8080/ws", realm="realm1")
    runner.run(MainWindow)
