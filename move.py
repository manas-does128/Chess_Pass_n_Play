class Move:
    def __init__(self, start, end):

        self.start_row = start[0]
        self.start_col = start[1]

        self.end_row = end[0]
        self.end_col = end[1]

    def __eq__(self, other):
        return (
            self.start_row == other.start_row
            and self.start_col == other.start_col
            and self.end_row == other.end_row
            and self.end_col == other.end_col
        )

    def __repr__(self):
        return f"({self.start_row},{self.start_col}) -> ({self.end_row},{self.end_col})"