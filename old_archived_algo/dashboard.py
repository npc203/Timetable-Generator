# Mandatory imports
import sys

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dashboard(object):
    def setupUi(self, Dashboard):
        """Initialize the UI elements before rendering"""

        # Setting "Dashboard" as the Object name
        Dashboard.setObjectName("Dashboard")

        # Setting the dialog dimensions
        Dashboard.resize(570, 562)

        # Creating a Table to render the Time Table
        self.timeTable = QtWidgets.QTableWidget(Dashboard)

        # Setting the position for the Time Table Element
        self.timeTable.setGeometry(QtCore.QRect(0, 120, 561, 192))

        # Setting the Column Count
        self.timeTable.setColumnCount(8)

        # Setting the Row Count
        self.timeTable.setRowCount(5)

        # Creating columns
        for col in range(8):
            item = QtWidgets.QTableWidgetItem()
            self.timeTable.setHorizontalHeaderItem(col, item)

        # Creating rows
        for row in range(5):
            item = QtWidgets.QTableWidgetItem()
            self.timeTable.setVerticalHeaderItem(row, item)

        # Translate and Render the Time Table Element
        self.retranslateUi(Dashboard)
        QtCore.QMetaObject.connectSlotsByName(Dashboard)

    def retranslateUi(self, Dashboard):

        """Adding Labels to all QT objects"""
        _translate = QtCore.QCoreApplication.translate

        item = self.timeTable.horizontalHeaderItem(0)
        item.setText(_translate("Dashboard", "Day/Time"))

        Dashboard.setWindowTitle(_translate("Dashboard", "Dashboard"))

        # Adding row names
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        for dayIndex, day in enumerate(days):
            item = self.timeTable.verticalHeaderItem(dayIndex)
            item.setText(_translate("Dashboard", day))

        # Adding column names
        daysWithTimingLabel = [
            "9-10",
            "10-11",
            "11-11.15",
            "11.15-12.15",
            "12.15-1",
            "1-2",
            "2-3",
            "3-4",
        ]
        for colIndex, col in enumerate(daysWithTimingLabel):
            item = self.timeTable.horizontalHeaderItem(colIndex)
            item.setText(_translate("Dashboard", col))


if __name__ == "__main__":
    """ " Driver function that triggers the Dashboard dialog"""

    # Initializing the QT application
    app = QtWidgets.QApplication(sys.argv)
    Dashboard = QtWidgets.QDialog()
    ui = Ui_Dashboard()

    # Initialize the UI elements before rendering the actual Dialog
    ui.setupUi(Dashboard)

    # Renders the Dashboard dialog
    Dashboard.show()

    # Terminating the Python interpreter
    sys.exit(app.exec_())
