# Employee Management GUI

A multi-window desktop application built with Python and PyQt5 for managing production workers and shift supervisors. Features a menu-driven interface, dynamic dropdowns, real-time display, and full input validation across multiple linked windows.

---

## Overview

This application extends the Employee/ProductionWorker/ShiftSupervisor class hierarchy into a fully interactive GUI. Users can add, view, and remove employees through separate input windows, with shift-matching enforcement and supervisor roster management handled under the hood.

---

## Features

- **Multi-window architecture** — main window plus dedicated input windows for supervisors and workers, each loaded from `.ui` files via `uic.loadUi()`
- **Menu bar navigation** — four menu actions open input/remove flows for both employee types
- **Dynamic ComboBoxes** — supervisor and worker dropdowns populate in real time as records are added
- **Live display panel** — click any entry in a dropdown to render its full formatted info string
- **Shift enforcement** — workers can only be assigned to a supervisor whose shift matches
- **Capacity enforcement** — supervisors have a configurable `max_workers` limit; adding beyond it raises a warning dialog
- **Graceful removal** — removing a supervisor detaches their workers (workers stay in the system); removing a worker unassigns them from their supervisor
- **Input validation** — every field is validated before object creation: type checks, range checks, required-field checks, and digit-only checks with descriptive error dialogs

---

## Application Structure

```
Main Window (UI)
├── Menu Bar
│   ├── Supervisor Input  →  SupervisorWindow
│   ├── Worker Input      →  WorkerWindow
│   ├── Supervisor Remove
│   └── Worker Remove
├── ComboBox — Supervisors
├── ComboBox — Workers
├── Display Label (shows selected employee's info)
└── Display Buttons
```

---

## Validation Rules

| Field | Rule |
|---|---|
| Name | Required, non-empty string |
| Employee Number | Digits only, 100–999 |
| Salary (Supervisor) | Integer, 50,000–200,000 |
| Pay Rate (Worker) | Integer, 1–20 |
| Hours (Worker) | Integer, 0–40 |
| Max Workers | Integer, required |
| Shift assignment | Worker shift must match supervisor shift |
| Array capacity | Max 3 supervisors, max 5 workers |

---

## Getting Started

**Requirements:** Python 3.7+, PyQt5

```bash
# Install dependency
pip install PyQt5

# Clone and run
git clone https://github.com/your-username/employee-management-gui.git
cd employee-management-gui
python Lab_Assignment_6.py
```

The project requires three `.ui` files in the same directory:

```
employee-management-gui/
│
├── Lab_Assignment_6.py     # All classes + GUI logic
├── mainwindow.ui           # Main window layout
├── supervisorinput.ui      # Supervisor input form
├── workerinput.ui          # Worker input form
└── README.md
```

---

## Class Overview

| Class | Role |
|---|---|
| `Employee` | Base class — name, number, benefits eligibility |
| `ProductionWorker` | Subclass — shift, pay rate, hours, gross pay |
| `ShiftSupervisor` | Subclass — salary, shift, worker roster, bonus |
| `UI` | Main window — state management, routing, display |
| `SupervisorWindow` | Input form for creating `ShiftSupervisor` objects |
| `WorkerWindow` | Input form for creating `ProductionWorker` objects and assigning to supervisors |

---

## Concepts Demonstrated

- PyQt5 multi-window GUI with `QMainWindow` and `uic.loadUi()`
- Signal/slot connections (`clicked`, `triggered`) for event-driven interaction
- `QMessageBox` for user-facing error and success feedback
- Fixed-size arrays with index counters for predictable state management
- Cross-window communication via parent window reference (`main_window`)
- OOP inheritance integrated directly into a GUI application layer
- Defensive input validation with early-return guard clauses

---

## Author

**Tatsiana Chakhovich** — QA Automation Engineer  
