import hou
from PySide2 import QtWidgets
from PySide2 import QtWidgets, QtCore, QtGui

from ciohoudini.validation_tab import ValidationTab

from ciohoudini.progress_tab import ProgressTab
from ciohoudini.response_tab import ResponseTab
from ciohoudini import validation
import time

class SubmissionDialog(QtWidgets.QDialog):

    def __init__(self, nodes, parent=None):
        super(SubmissionDialog, self).__init__(parent)
        # super(SubmissionDialog, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Conductor Submission")
        self.setStyleSheet(hou.qt.styleSheet())
        self.layout = QtWidgets.QVBoxLayout()
        self.tab_widget = QtWidgets.QTabWidget()
        self.setLayout(self.layout)
        self.layout.addWidget(self.tab_widget)

        self.validation_tab = ValidationTab(self)
        self.tab_widget.addTab(self.validation_tab, "Validation")

        self.progress_tab = ProgressTab(self)
        self.tab_widget.addTab(self.progress_tab, "Progress")

        self.response_tab = ResponseTab(self)
        self.tab_widget.addTab(self.response_tab, "Response")

        #self.setGeometry(200, 200, 1100, 756)
        # self.setMinimumSize(900, 556)  # Set minimum window size
        self.setMinimumSize(1200, 742)  # Set minimum window size

        self.tab_widget.setTabEnabled(1, False)
        self.tab_widget.setTabEnabled(2, False)

        self.nodes = nodes
 
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.run()

    def show_validation_tab(self):
        pass


    def show_progress_tab(self):
        self.tab_widget.setTabEnabled(1, True)
        self.tab_widget.setCurrentWidget(self.progress_tab)
        # self.tab_widget.setTabEnabled(0, False)
        # self.tab_widget.setTabEnabled(2, False)
        QtCore.QCoreApplication.processEvents()
        time.sleep(1)

    def show_response_tab(self):
        self.tab_widget.setTabEnabled(2, True)
        self.tab_widget.setCurrentWidget(self.response_tab)
        self.tab_widget.setTabEnabled(0, False)
        # self.tab_widget.setTabEnabled(1, False)
        QtCore.QCoreApplication.processEvents()
        time.sleep(1)

    def run(self):
        errors, warnings, notices = validation.run(*(self.nodes))
        self.validation_tab.populate(errors, warnings, notices)

    def on_close(self):
        self.accept()


