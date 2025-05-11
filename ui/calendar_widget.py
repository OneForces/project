from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate


class CalendarWidget(QtWidgets.QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.current_stage_date = None
        
    def setup_ui(self):
        self.setGridVisible(True)
        self.setVerticalHeaderFormat(
            QtWidgets.QCalendarWidget.NoVerticalHeader)
        
    def highlight_stage_date(self, date):
        """Выделение даты текущего этапа"""
        self.current_stage_date = date
        self.updateCells()
        
    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        
        if date == self.current_stage_date:
            painter.save()
            painter.setPen(QtCore.Qt.red)
            painter.drawRect(rect)
            painter.restore()