"""
    Created at 04/04/2018
    Created by Vinod M P
    Created for KERALA UNIVERSITY
    Created under MASSIVE DATA ANALYTICS
"""


from PyQt4.QtGui import *
from PyQt4.QtCore import *

class arrow(QWidget):
    def __init__(self,direction):
        super(arrow,self).__init__()
        self.direction=direction
        self.color=QColor(255,0,0)
        self.setMinimumSize(30,30)
        self.setMaximumSize(30,30)
        self.repaint()

    def paintEvent(self,e):
        canvas = QPainter()
        canvas.begin(self)
        self.drawarrow(canvas)
        canvas.setRenderHint(QPainter.Antialiasing)
        canvas.end()
        
    def drawarrow(self,canvas):
        font = QFont('Serif',10,QFont.Light)
        canvas.setFont(font)
        size = self.size()
        width = size.width()
        height = size.height()
        canvas.setPen(QColor(169,171,197))
        grad=QLinearGradient(QPointF(int(width/2),0),QPointF(int(width/2),height))
        grad.setColorAt(0,QColor(169,171,197))
        grad.setColorAt(1, QColor(69,71,97))
        canvas.setBrush(QBrush(grad))
        canvas.drawRect(int(width/4),int(height/4),width-(int(width/2)),height-(int(height/2)))
        if self.direction == "up":
            points = [QPoint(0,int(height/2)),QPoint(width,int(height/2)),QPoint(int(width/2),0)]
        elif self.direction == "down":
            points = [QPoint(0,(height-(int(height/2)))),QPoint(width,(height-(int(height/2)))),QPoint(int(width/2),height)]
        elif self.direction == "left":
            points = [QPoint(int(width/2),0),QPoint(int(width/2),height),QPoint(0,int(height/2))]
        elif self.direction == "right":
            points = [QPoint((width-(int(width/2))),0),QPoint((width-(int(width/2))),height),QPoint(width,int(height/2))]
        else:
            points = [QPoint((width-(int(width/2))),0),QPoint((width-(int(width/4)*2)),height),QPoint(width,int(height/2))]
        triangle =QPolygon(points)
        canvas.drawPolygon(triangle)
