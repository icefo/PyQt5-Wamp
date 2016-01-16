import sys
import functools
import asyncio

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLineEdit, QGridLayout

from autobahn.asyncio.wamp import ApplicationRunner
from autobahn.asyncio.wamp import ApplicationSession

from quamash import QEventLoop
from PyQt5.QtGui import QFont

def wrap_in_future(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        asyncio.async(func(*args, **kw))
    return wrapper


class MainWindow(ApplicationSession, QMainWindow):

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        QMainWindow.__init__(self)

        self.the_widget = MainWidget()
        self.statusBar()
        self.main_window_init()

    def time_event_handler(self, time):
        self.statusBar().showMessage("Time: " + time, msecs=2000)

    @asyncio.coroutine
    def onJoin(self, details):
        print("session ready")
        yield from self.subscribe(self.time_event_handler, 'com.myapp.the_time')

    @wrap_in_future  # PyQT5 can't call a coroutine directly so we wrap it in a future
    @asyncio.coroutine
    def the_widget_add_numbers(self, list_of_number=None):
        print("call it baby !")

        result = yield from self.call('com.myapp.add', list_of_number)

        print("I called baby ! ", result)
        self.the_widget.addition_result_signal.emit(str(result))

    def main_window_init(self):
        self.the_widget.add_the_numbers_signal.connect(self.the_widget_add_numbers)
        self.setCentralWidget(self.the_widget)

        #                 x    y  x_size y_size
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('PyQt5-Wamp')
        self.show()


class MainWidget(QWidget):

    add_the_numbers_signal = pyqtSignal([list])
    addition_result_signal = pyqtSignal([str])

    def __init__(self):
        super().__init__()

        self.number_1 = QLineEdit()
        self.number_2 = QLineEdit()

        self.addition_button = QPushButton("push to add !")
        self.addition_result = QLineEdit()

        self.widget_init()

    def widget_init(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.addition_button.clicked.connect(self.collect_numbers)
        self.addition_result_signal.connect(self.addition_result.setText)

        grid.addWidget(self.number_1, 0, 0)
        grid.addWidget(self.number_2, 0, 3)
        grid.addWidget(self.addition_button, 1, 2)
        grid.addWidget(self.addition_result, 2, 2)

    def collect_numbers(self):
        number_1 = self.number_1.displayText()
        number_2 = self.number_2.displayText()
        print("numbers to add: ", [number_1, number_2])
        self.add_the_numbers_signal.emit([number_1, number_2])


if __name__ == "__main__":
    # the quamash lib create an asyncio_driven loop that is used by PyQt5 and autobahn

    QT_app = QApplication(sys.argv)

    asyncio_loop = QEventLoop(QT_app)
    asyncio.set_event_loop(asyncio_loop)

    runner = ApplicationRunner(url="ws://127.0.0.1:8080/ws", realm="realm1")
    runner.run(MainWindow)
