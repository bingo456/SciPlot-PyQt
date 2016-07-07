# -*- coding: utf-8 -*-
"""
Create generic MPL canvas, toolbar, figure, axis.

Heavily borrowed from:
    matplotlib.org/examples/user_interfaces/embedding_in_qt5.html

Created on Thu Jun 30 15:41:35 2016

@author: chc
"""

import sys as _sys
import os as _os
import matplotlib as _mpl
import matplotlib.style as _mpl_sty

from PyQt5 import QtWidgets as _QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as \
    FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as \
    _NavigationToolbar

from matplotlib.figure import Figure as _Figure

# Make sure that we are using QT5
_mpl.use('Qt5Agg')


class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100, style=None):
        if style is None:
            pass
        else:
            _mpl.style.use(style)

        # Create figure and axes
        self.fig = _Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        # Not really used, but could be used to have some sort of initial plot
        self.compute_initial_figure()

        # Initialize the canvas
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        # Set canvas size policies and geometry
        FigureCanvas.setSizePolicy(self, _QtWidgets.QSizePolicy.Expanding,
                                   _QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # Create the toolbar and connect to canvas (self)
        self.toolbar = _NavigationToolbar(self, None)

    def compute_initial_figure(self):
        pass


if __name__ == '__main__':

    from PyQt5 import QtCore as _QtCore

    class ApplicationWindow(_QtWidgets.QMainWindow):
        def __init__(self, style=None):
            _QtWidgets.QMainWindow.__init__(self)
            self.setAttribute(_QtCore.Qt.WA_DeleteOnClose)

            self.main_widget = _QtWidgets.QWidget(self)

            self.mpl_layout = _QtWidgets.QVBoxLayout(self.main_widget)
            self.mpl_widget = MplCanvas(self.main_widget, width=5, height=4,
                                        dpi=100, style=style)
            self.mpl_layout.addWidget(self.mpl_widget.toolbar)
            self.mpl_layout.addWidget(self.mpl_widget)

            self.main_widget.setFocus()
            self.setCentralWidget(self.main_widget)

            self.setSizePolicy(_QtWidgets.QSizePolicy.Expanding,
                               _QtWidgets.QSizePolicy.Expanding)

    qApp = _QtWidgets.QApplication(_sys.argv)

    aw = ApplicationWindow('seaborn-deep')
    aw.mpl_widget.axes.plot((2,3),(4,-1), label='a')
    aw.mpl_widget.axes.hold(True)
    aw.mpl_widget.axes.plot((2,3),(4,-2), label='b')
    aw.mpl_widget.axes.set_xlabel('X')
    aw.mpl_widget.axes.set_ylabel('Y')
    aw.mpl_widget.axes.set_title('Title')
    aw.mpl_widget.axes.legend()
    aw.mpl_widget.fig.tight_layout()

    aw.show()

    qApp.exec_()
