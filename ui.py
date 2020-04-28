from PyQt4.QtCore import *
from PyQt4.QtGui import *

class App(QApplication):
    def __init__(self, argv):
        super(App, self).__init__(argv)
        self.msg = QLabel("Hello, World!")
        self.msg.show()

if __name__ == "__main__":
    import sys
    app = App(sys.argv)
    sys.exit(app.exec_())