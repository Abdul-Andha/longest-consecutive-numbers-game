import sys
from PyQt6.QtCore import Qt, QPoint, QRect, QSize
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout, QMainWindow,
     QVBoxLayout, QSizePolicy, QWidget, QGridLayout, QBoxLayout, QPushButton)

class MainWindow(QMainWindow):
    def __init__(self, matrix, solution):
        super().__init__()
        self.solution = solution
        self.setWindowTitle('Longest Sequence')
        self.resize(500, 525)

        #central widget
        widget = QWidget()
        central = QVBoxLayout()
        central.setSpacing(1)
        central.setContentsMargins(0,0,0,0)
        widget.setLayout(central)
        self.setCentralWidget(widget)

        #add grid
        self.grid = QGridLayout()
        central.addLayout(self.grid)
        self.grid.setContentsMargins(25,25,25,25)
        central.addStretch()

        #setup grid
        numRows = len(matrix)
        numCols = len(matrix[0])
        for i in range(numRows):
            for j in range(numCols):
                button = QPushButton(matrix[i][j])
                button.setFixedSize(500//numRows, 500//numCols)
                button.setStyleSheet("border: 2px solid black; background: white; color: black; font-size:25px; font-weight: bold");
                self.grid.addWidget(button,i,j)

        #add solve button
        solveBut = QPushButton("Solve")
        solveBut.setStyleSheet('color: #000000;background:white;'
                                    'font-family: Arial; font-size: 32px; margin-bottom: 10px')
        central.addWidget(solveBut)
        solveBut.clicked.connect(self.colorSolution)

    def colorSolution(self):
        iChange, jChange = 0, 0
        i = self.solution[0]
        j = self.solution[1]
        
        if self.solution[3] == "LEFT_DIAGONAL":
            iChange = -1
            jChange = -1
        elif self.solution[3] == "RIGHT_DIAGONAL":
            iChange = -1
            jChange = 1
        elif self.solution[3] == "UP":
            iChange = -1
        elif self.solution[3] == "LEFT":
            jChange = -1

        for x in range(self.solution[2] + 1):
            self.grid.itemAtPosition(i, j).widget().setStyleSheet("border: 2px solid black; background: yellow; color: black; font-size:25px; font-weight: bold")
            i += iChange
            j += jChange

#returns solution arr [i, j, length, direction]
def solve(matrix):
    #setup length matrices
    leftSeqSize = []
    topSeqSize = []
    leftDiagSeqSize = []
    rightDiagSeqSize = []
    for i in range(len(matrix)):
        temp1 = []
        temp2 = []
        temp3 = []
        temp4 = []
        for j in range(len(matrix[i])):
            temp1.append(0)
            temp2.append(0)
            temp3.append(0)
            temp4.append(0)
        leftSeqSize.append(temp1)
        topSeqSize.append(temp2)
        leftDiagSeqSize.append(temp3)
        rightDiagSeqSize.append(temp4)

    #fill length matrices and track max
    maxSeen = [-1 ,-1, 0, "NULL"]
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            
            if (matrix[i - 1][j] == matrix[i][j]): #vertical match found
                newSize = topSeqSize[i - 1][j] + 1
                if newSize > topSeqSize[i][j]:
                    topSeqSize[i][j] = newSize
                    if newSize > maxSeen[2]:
                        maxSeen = [i, j, newSize, "UP"]

            if (matrix[i][j - 1] == matrix[i][j]): #horizontal match found
                newSize = leftSeqSize[i][j - 1] + 1
                if newSize > leftSeqSize[i][j]:
                    leftSeqSize[i][j] = newSize
                    if newSize > maxSeen[2]:
                        maxSeen = [i, j, newSize, "LEFT"]

            if (matrix[i - 1][j - 1] == matrix[i][j]): #left diagonal match found
                newSize = leftDiagSeqSize[i - 1][j - 1] + 1
                if newSize > leftDiagSeqSize[i][j]:
                    leftDiagSeqSize[i][j] = newSize
                    if newSize > maxSeen[2]:
                        maxSeen = [i, j, newSize, "LEFT_DIAGONAL"]

            if (j + 1 < len(matrix[i]) and matrix[i - 1][j + 1] == matrix[i][j]): #right diagonal match found
                newSize = rightDiagSeqSize[i - 1][j + 1] + 1
                if newSize > rightDiagSeqSize[i][j]:
                    rightDiagSeqSize[i][j] = newSize
                    if newSize > maxSeen[2]:
                        maxSeen = [i, j, newSize, "RIGHT_DIAGONAL"]
    return maxSeen

def main():
    #setup matrix
    matrix = []
    with open(sys.argv[1], 'r') as fi:
        for line in fi:
            line = line.strip().split(",")
            row = []
            for num in line:
                row.append(num)
            
            matrix.append(row)

    #get solution
    solution = solve(matrix)
    
    #init gui
    app = QApplication(sys.argv)
    window = MainWindow(matrix, solution)
    window.show()
    app.exec()

main()
