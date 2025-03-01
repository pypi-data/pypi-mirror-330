"""マインスイーパー"""

import time
from enum import IntEnum
from typing import ClassVar, assert_never

import numpy as np
from nicegui import ui


class State(IntEnum):
    """マスの状態"""

    UnRevealed = 0
    Flag = 1
    Revealed = 2


class Square(ui.button):
    """マス"""

    def __init__(self, game: "Game", y: int, x: int) -> None:
        """初期化"""
        super().__init__()
        self.game = game
        self.y = y
        self.x = x
        self.on("contextmenu", self.toggle_revealed)
        self.on("click", lambda: self.game.reveal_cell(y, x))
        self.classes("w-10 h-10")
        self.build()

    def build(self) -> None:
        """構築"""
        self.text = self.icon = None
        self.props("text-color=white")
        state: State = self.game.revealed[self.y, self.x]
        match state:
            case State.UnRevealed:
                self.props("color=grey")
            case State.Flag:
                self.icon = "flag"
                self.props("text-color=red")
            case State.Revealed:
                if self.game.grid[self.y, self.x] == -1:
                    self.text = "X"
                    self.props("color=red")
                else:
                    self.text = str(self.game.grid[self.y, self.x])
                    self.props("color=green")
            case _:
                assert_never(state)

    def toggle_revealed(self) -> None:
        """Toggle revealed"""
        if self.game.revealed[self.y, self.x] != State.Revealed:
            if self.game.revealed[self.y, self.x] == State.UnRevealed:
                self.game.revealed[self.y, self.x] = State.Flag
            elif self.game.revealed[self.y, self.x] == State.Flag:
                self.game.revealed[self.y, self.x] = State.UnRevealed
            self.game.refresh()


class Game:
    """ゲーム"""

    rng: ClassVar[np.random.Generator] = np.random.default_rng()

    def __init__(self, *, grid_size: int, num_mines: int) -> None:
        """初期化"""
        self.grid_size = grid_size
        self.num_mines = num_mines
        self.grid = np.zeros((grid_size, grid_size), dtype=int)
        self.revealed = np.full_like(self.grid, State.UnRevealed, dtype=State)
        self.timer_start_time = 0.0
        with ui.row():
            ui.button("Restart", on_click=self.restart)
            label = ui.label()
            self.timer = ui.timer(
                1.0, lambda: label.set_text(f"Time: {int(time.time() - self.timer_start_time)} seconds")
            )
        with ui.grid(columns=grid_size).classes("gap-0"):
            self.squares = [Square(self, y, x) for y in range(grid_size) for x in range(grid_size)]
        self.restart()

    def restart(self) -> None:
        """再ゲーム"""
        self.grid.fill(0)
        self.revealed.fill(State.UnRevealed)
        self.timer_start_time = time.time()
        self.timer.activate()
        # Set mines
        for _ in range(self.num_mines):
            while True:
                y, x = self.rng.integers(0, self.grid_size, 2)
                if self.grid[y, x] != -1:
                    self.grid[y, x] = -1
                    break
        self.set_grid_numbers()
        self.refresh()

    def set_grid_numbers(self) -> None:
        """周りのmineの数をgridに設定"""
        mine = np.zeros((self.grid_size + 2, self.grid_size + 2), dtype=int)
        mine[1:-1, 1:-1] = self.grid == -1
        count = (
            mine[:-2, :-2]
            + mine[1:-1, :-2]
            + mine[2:, :-2]
            + mine[:-2, 1:-1]
            + mine[2:, 1:-1]
            + mine[:-2, 2:]
            + mine[1:-1, 2:]
            + mine[2:, 2:]
        )
        self.grid = np.where(self.grid == -1, self.grid, count)

    def refresh(self) -> None:
        """再描画"""
        for square in self.squares:
            square.build()

    def reveal_cell(self, y: int, x: int) -> None:
        """マスを開ける"""
        if not self.is_over:
            self._reveal_cell_sub(y, x)
            self.judge()
            self.refresh()

    def _reveal_cell_sub(self, y: int, x: int) -> None:
        if self.revealed[y, x] == State.Revealed:
            return
        self.revealed[y, x] = State.Revealed
        if self.grid[y, x] == -1:
            self.timer.deactivate()
            self.show_banner("You lost!")
        elif self.grid[y, x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < self.grid_size and 0 <= nx < self.grid_size:
                        self._reveal_cell_sub(ny, nx)

    def judge(self) -> None:
        """判定"""
        if ((self.grid == -1) | (self.revealed == State.Revealed)).all():
            self.timer.deactivate()
            self.show_banner("You won!")

    @property
    def is_over(self) -> bool:
        """ゲームオーバーかどうか"""
        return not self.timer.active

    @staticmethod
    def show_banner(message: str) -> None:
        """メッセージ表示"""
        ui.notify(message, type="positive")


def run_game(*, port: int | None = None) -> None:
    """ゲーム実行"""
    Game(grid_size=10, num_mines=10)
    s = "document.addEventListener('contextmenu', event => event.preventDefault())"
    ui.timer(0.5, lambda: ui.run_javascript(s), once=True)  # 右クリック禁止
    ui.run(title="Minesweeper", reload=False, port=port)
