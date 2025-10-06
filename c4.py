import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QMessageBox,
    QGridLayout,
)
from PyQt6.QtGui import QColor, QPainter, QBrush
from PyQt6.QtCore import Qt

ROWS = 6
COLS = 7
EMPTY = 0
RED = 1
YELLOW = 2


class CellButton(QPushButton):
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.state = EMPTY
        self.setFixedSize(80, 80)
        self.setStyleSheet("background-color: #0066CC; border: none;")

    def set_state(self, state):
        self.state = state
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        radius = min(self.width(), self.height()) // 2 - 5
        center = self.rect().center()
        painter.setBrush(QBrush(Qt.GlobalColor.white))
        painter.drawEllipse(center, radius, radius)
        if self.state != EMPTY:
            color = QColor("#FF4136") if self.state == RED else QColor("#FFDC00")
            painter.setBrush(QBrush(color))
            painter.drawEllipse(center, radius - 2, radius - 2)


class Connect4(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connect 4 – PyQt6")
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = RED
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.setLayout(self.grid)
        self.column_buttons = []
        for c in range(COLS):
            btn = QPushButton("↓")
            btn.setFixedSize(80, 30)
            btn.clicked.connect(lambda _, col=c: self.handle_drop(col))
            self.column_buttons.append(btn)
            self.grid.addWidget(btn, 0, c)
        self.cells = [[CellButton(r, c) for c in range(COLS)] for r in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                self.grid.addWidget(self.cells[r][c], r + 1, c)

    def handle_drop(self, col):
        row = self._available_row(col)
        if row is None:
            QMessageBox.warning(self, "Column full", "That column is already full.")
            return
        self.board[row][col] = self.current_player
        self.cells[row][col].set_state(self.current_player)
        if self._check_winner(row, col):
            winner = "Red" if self.current_player == RED else "Yellow"
            QMessageBox.information(self, "Game Over", f"{winner} wins!")
            self._reset_game()
            return
        elif all(self.board[0][c] != EMPTY for c in range(COLS)):
            QMessageBox.information(self, "Game Over", "It’s a draw!")
            self._reset_game()
            return
        self.current_player = YELLOW if self.current_player == RED else RED

    def _available_row(self, col):
        for r in reversed(range(ROWS)):
            if self.board[r][col] == EMPTY:
                return r
        return None

    def _check_winner(self, last_row, last_col):
        player = self.board[last_row][last_col]

        def count(dr, dc):
            r, c = last_row + dr, last_col + dc
            cnt = 0
            while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == player:
                cnt += 1
                r += dr
                c += dc
            return cnt

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            total = 1 + count(dr, dc) + count(-dr, -dc)
            if total >= 4:
                return True
        return False

    def _reset_game(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                self.cells[r][c].set_state(EMPTY)
        self.current_player = RED


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Connect4()
    window.show()
    sys.exit(app.exec())
