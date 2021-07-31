class ScoreAgent:
    def __init__(self, id):
        self.id = id

    def make_move(self, game):
        return game.board.random_free()

    def __str__(self):
        return f'Player {self.id} (BaseAgent)'
