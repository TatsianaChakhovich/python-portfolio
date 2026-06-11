"""
Factor Breakout game
by Tatsiana Chakhovich
April 28, 2026
"""
import numpy as np


class Breakout:
    """A class that implements the Factor Breakout game.
    The game consists of a grid (NumPy array) of random integers.
    Players select a column and a factor to "break" numbers that are divisible
    by the factor. Broken positions are tracked using binary encoding."""

    def __init__(self, x=3, y=4, seed=None):
        """
        Initialize the playing field.

        Parameters:
            x (int): Number of rows.
            y (int): Number of columns.
            seed (int or None): Seed for random number generator.

        Creates:
            self.field  : NumPy array of size (x, y) with values 2–99.
            self.broken : List of length x storing binary row states.
        """

        if seed is not None:
            np.random.seed(seed)

        self.field = np.random.randint(2, 100, size=(x, y))
        self.broken = [0] * x

    def see_broken(self, j, factor):
        """Start breaking from the bottom row and calculate score.

        Parameters:
            j (int): Column selected by the user.
            factor (int): Factor used to break numbers.

        Returns:
            int: Total score for this round (including multiplier).
        """

        start_row = 0
        total = self.see_broken_rec(start_row, j, factor, 1)
        multiplier = self.check_rows()
        return total * multiplier

    def see_broken_rec(self, i, j, factor, depth):
        """
        Recursive breaking logic starting from bottom row.

        Parameters:
            i (int): Row index.
            j (int): Column index.
            factor (int): Factor used for breaking.
            depth (int): Depth of recursion (used for scoring).

        Returns:
            int: Score gained from this position and recursive calls.
        """

        if i < 0 or i >= self.field.shape[0] or j < 0 or j >= self.field.shape[1]:
            return 0

        if factor < 2 or factor > 99:
            return 0

        value = self.field[i][j]

        if value % factor != 0:
            return 0

        if self.broken[i] & (1 << j):
            return 0

        self.broken[i] |= (1 << j)

        score = factor * depth

        score += self.see_broken_rec(i + 1, j - 1, factor, depth + 1)
        score += self.see_broken_rec(i + 1, j, factor, depth + 1)
        score += self.see_broken_rec(i + 1, j + 1, factor, depth + 1)

        return score

    def check_rows(self):
        """
        Check if any rows are fully broken and remove them.

        Returns:
            int: Multiplier based on number of rows removed.
        """

        multiplier = 1
        if self.field.size == 0:
            return 1
        cols = self.field.shape[1]

        full_mask = (1 << cols) - 1

        i = 0
        while i < len(self.broken):
            if self.broken[i] == full_mask:
                self.field = np.delete(self.field, i, axis=0)
                self.broken.pop(i)
                multiplier += 1
            else:
                i += 1

        return multiplier

    def still_playing(self):
        """Check if the game should continue.

        Returns:
            bool: True if there are still numbers left, False otherwise."""

        return self.field.size > 0

    def print_field(self):
        """Print the playing field.

        Broken positions are shown as 'XX'."""

        if self.field.size == 0:
            print("(empty field)")
            return

        rows = self.field.shape[0]
        cols = self.field.shape[1]

        for i in range(rows - 1, -1, -1):
            for j in range(cols):
                if self.broken[i] & (1 << j):
                    print(f"{'XX':>3}", end=" ")
                else:
                    print(f"{self.field[i][j]:>3}", end=" ")
            print()


def main():
    """Run the Breakout game loop."""

    print("Let's play!")
    my_field = Breakout(4, 5)
    score = 0
    while my_field.still_playing():
        my_field.print_field()
        col = input("Select the column: ")
        factor = input("Which factor do you want to use? ")
        new_score = (my_field.see_broken(int(col), int(factor)))
        score += new_score
        print("You got", new_score, "points this round for a total of", score, "points!")
    print("Thank you for playing!")


if __name__ == "__main__":
    main()

r"""
C:\Users\tania\AppData\Local\Python\bin\python.exe C:\Users\tania\PycharmProjects\pythonProject2\Lab_Assignment_3.py 
Let's play!
 28  31  18  68  57 
  3  27  33  69  48 
  5  96  90  96  85 
 12  79  29  22  16 
Select the column: 3
Which factor do you want to use? 2
You got 24 points this round for a total of 24 points!
 28  31  18  XX  57 
  3  27  33  69  XX 
  5  96  XX  XX  85 
 12  79  29  XX  16 
Select the column: 0
Which factor do you want to use? 6
You got 18 points this round for a total of 42 points!
 28  31  18  XX  57 
  3  27  33  69  XX 
  5  XX  XX  XX  85 
 XX  79  29  XX  16 
Select the column: 2
Which factor do you want to use? 9
You got 0 points this round for a total of 42 points!
 28  31  18  XX  57 
  3  27  33  69  XX 
  5  XX  XX  XX  85 
 XX  79  29  XX  16 
Select the column: 2
Which factor do you want to use? 29
You got 29 points this round for a total of 71 points!
 28  31  18  XX  57 
  3  27  33  69  XX 
  5  XX  XX  XX  85 
 XX  79  XX  XX  16 
Select the column: 1
Which factor do you want to use? 79
You got 79 points this round for a total of 150 points!
 28  31  18  XX  57 
  3  27  33  69  XX 
  5  XX  XX  XX  85 
 XX  XX  XX  XX  16 
Select the column: 4
Which factor do you want to use? 16
You got 32 points this round for a total of 182 points!
 28  31  18  XX  57 
  3  27  33  69  XX 
  5  XX  XX  XX  85 
Select the column: 4
Which factor do you want to use? 85
You got 85 points this round for a total of 267 points!
 28  31  18  XX  57 
  3  27  33  69  XX 
  5  XX  XX  XX  XX 
Select the column: 0
Which factor do you want to use? 1
You got 0 points this round for a total of 267 points!
 28  31  18  XX  57 
  3  27  33  69  XX 
  5  XX  XX  XX  XX 
Select the column: 0
Which factor do you want to use? 5
You got 10 points this round for a total of 277 points!
 28  31  18  XX  57 
  3  27  33  69  XX 
Select the column: 0
Which factor do you want to use? 3
You got 3 points this round for a total of 280 points!
 28  31  18  XX  57 
 XX  27  33  69  XX 
Select the column: 1
Which factor do you want to use? 3
You got 9 points this round for a total of 289 points!
 28  31  XX  XX  57 
 XX  XX  33  69  XX 
Select the column: 2
Which factor do you want to use? 3
You got 3 points this round for a total of 292 points!
 28  31  XX  XX  57 
 XX  XX  XX  69  XX 
Select the column: 3
Which factor do you want to use? 69
You got 138 points this round for a total of 430 points!
 28  31  XX  XX  57 
Select the column: 1
Which factor do you want to use? 31
You got 31 points this round for a total of 461 points!
 28  XX  XX  XX  57 
Select the column: 0
Which factor do you want to use? 28
You got 28 points this round for a total of 489 points!
 XX  XX  XX  XX  57 
Select the column: 4
Which factor do you want to use? 57
You got 114 points this round for a total of 603 points!
Thank you for playing!

Process finished with exit code 0

"""
