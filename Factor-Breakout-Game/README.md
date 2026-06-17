# Factor Breakout

A terminal-based number puzzle game built in Python using NumPy. Players break numbers on a grid by selecting a column and a divisible factor — chain reactions, row clears, and score multipliers make every move count.

---

## Gameplay

The playing field is a grid of random integers (2–99). Each turn, you pick a **column** and a **factor**. Any number in that column divisible by your factor gets broken — and the break cascades downward through adjacent cells. Clear a full row to earn a score multiplier.

```
 28  31  18  68  57
  3  27  33  69  48
  5  96  90  96  85
 12  79  29  22  16

Select the column: 3
Which factor do you want to use? 2
You got 24 points this round for a total of 24 points!
```

Broken positions are displayed as `XX`. The game ends when the entire field is cleared.

---

## Scoring

| Event | Points |
|---|---|
| Breaking a number | `factor × depth` |
| Cascade (each level deeper) | depth increases by 1 |
| Full row cleared | +1 to multiplier per row |
| Round score | `raw score × multiplier` |

**Depth** starts at 1 for the selected cell and increases for each cascading break downward. Breaking a number at depth 3 with factor 7 = 21 points for that cell alone.

---

## How It Works

### Binary Row Encoding

Broken cell positions are tracked using **bitwise encoding** — each row's state is stored as a single integer where each bit represents one column. This makes row-clear detection O(1):

```python
# Mark column j as broken in row i
self.broken[i] |= (1 << j)

# Check if the entire row is cleared
full_mask = (1 << cols) - 1
if self.broken[i] == full_mask:
    # row is fully broken — remove it
```

### Recursive Cascade

`see_broken_rec()` uses depth-first recursion to propagate breaks downward into three adjacent cells (left-diagonal, straight down, right-diagonal):

```python
score += self.see_broken_rec(i + 1, j - 1, factor, depth + 1)
score += self.see_broken_rec(i + 1, j,     factor, depth + 1)
score += self.see_broken_rec(i + 1, j + 1, factor, depth + 1)
```

Base cases: out-of-bounds, factor out of range (2–99), number not divisible, or cell already broken.

---

## Features

- **NumPy grid** — field built and managed as a 2D `np.ndarray`; rows deleted with `np.delete()`
- **Recursive cascade** — breaks propagate downward through divisible neighbors
- **Bitwise state tracking** — broken cells encoded as binary integers per row
- **Row-clear multiplier** — clearing multiple rows in one move stacks the multiplier
- **Reproducible games** — optional `seed` parameter for testing and demos
- **Guard clauses** — invalid column, factor out of range, and already-broken cells handled gracefully

---

## Getting Started

**Requirements:** Python 3.7+, NumPy

```bash
# Install dependency
pip install numpy

# Clone and run
git clone https://github.com/your-username/factor-breakout.git
cd factor-breakout
python Lab_Assignment_3.py
```

---

## Sample Usage (Programmatic)

```python
from Lab_Assignment_3 import Breakout

# Reproducible game with seed
game = Breakout(x=4, y=5, seed=42)

game.print_field()
score = game.see_broken(col=2, factor=3)
print(f"Score this round: {score}")
print(f"Still playing: {game.still_playing()}")
```

---

## Project Structure

```
factor-breakout/
│
├── Lab_Assignment_3.py   # Breakout class + main() game loop
└── README.md
```

---

## Concepts Demonstrated

- Object-oriented design with a single well-encapsulated class
- Recursive algorithms with depth tracking
- Bitwise operations for compact state representation
- NumPy array manipulation (random generation, row deletion, shape queries)
- Separation of game logic (`see_broken_rec`, `check_rows`) from display (`print_field`)
- Reproducible randomness via seeded `np.random`

---

## Author

**Tatsiana Chakhovich** — QA Automation Engineer  
