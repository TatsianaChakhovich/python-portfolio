""""
Multi-Window GUI
by Tatsiana Chakhovich
May 20, 2026
"""

import sys
from enum import Enum
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QComboBox,
    QAction,
    QMessageBox,
    QLineEdit
)


# Enum class
class Shift(Enum):
    """ A class to represent Shift using enum """

    DAY = 1
    SWING = 2
    NIGHT = 3


# Employee class
class Employee:
    """ A class to represent an Employee """

    # class ("static") intended constants
    MIN_NUMBER = 100
    MAX_NUMBER = 999

    # initializer ("constructor") method
    def __init__(self, name='unidentified', number=999):
        """Constructs all the necessary attributes for the employee object."""
        if not self.set_name(name):
            self.name = 'unidentified'
        if not self.set_number(number):
            self.number = 999
        self.benefits = self.set_benefits(self.number)

    # mutators
    def set_name(self, name):
        """Set employee's name"""
        if not self.valid_name(name):
            return False
        # else
        self.name = name
        return True

    def set_number(self, number):
        """Set employee's number"""
        if not self.valid_number(number):
            return False
        # else
        self.number = number
        self.benefits = self.set_benefits(number)
        return True

    # accessors
    def get_name(self):
        """Get employee's name"""
        return self.name

    def get_number(self):
        """Get employee's number"""
        return self.number

    def get_benefits(self):
        """Get employee's benefits"""
        return self.benefits

    # class methods
    @classmethod
    def set_benefits(cls, number):
        """Determine benefits based on employee's number"""
        if number < 500:
            return True
        # else
        return False

    @classmethod
    def valid_name(cls, name):
        """Validate employee's name"""
        if not isinstance(name, str):
            return False
        # else
        return True

    @classmethod
    def valid_number(cls, number):
        """Validate the employee's number"""
        if not isinstance(number, int) or not (cls.MIN_NUMBER <= number <= cls.MAX_NUMBER):
            return False
        # else
        return True

    def __str__(self):
        """Return employee's info"""
        benefits_text = "Benefits" if self.benefits else "No benefits"
        return f"{self.name}  #{self.number} ({benefits_text})"


# Production Worker class (subclass of Employee)
class ProductionWorker(Employee):
    """An hourly production worker assigned to one shift."""

    # class ("static") intended constants
    MIN_RATE = 1
    MAX_RATE = 20
    MIN_HOURS = 0
    MAX_HOURS = 40

    def __init__(self, name='unidentified', number=999, shift=Shift.DAY, pay_rate=1, hours=0):
        """Constructs all the necessary attributes for the worker object."""
        super().__init__(name, number)
        if not self.set_shift(shift):
            self.shift = Shift.DAY
        if not self.set_pay_rate(pay_rate):
            self.pay_rate = 1.0
        if not self.set_hours(hours):
            self.hours = 0

    # mutators
    def set_shift(self, shift):
        """Set the worker's shift."""
        if not isinstance(shift, Shift):
            return False
        # else
        self.shift = shift
        return True

    def set_pay_rate(self, pay_rate):
        """Set the worker's hourly pay rate"""
        if not self.valid_pay_rate(pay_rate):
            return False
        # else
        self.pay_rate = pay_rate
        return True

    def set_hours(self, hours):
        """Set hours worked this week"""
        if not self.valid_hours(hours):
            return False
        # else
        self.hours = hours
        return True

    # accessors
    def get_shift(self):
        """Get worker's shift."""
        return self.shift

    def get_pay_rate(self):
        """Get worker's hourly pay rate."""
        return self.pay_rate

    def get_hours(self):
        """Get worker's hours worked this week."""
        return self.hours

    def gross_pay(self):
        """Return pay rate * hours worked."""
        return self.pay_rate * self.hours

    # class methods
    @classmethod
    def valid_pay_rate(cls, pay_rate):
        """Validate the pay rate."""
        if not isinstance(pay_rate, int):
            return False
        if not (cls.MIN_RATE <= pay_rate <= cls.MAX_RATE):
            return False
        # else
        return True

    @classmethod
    def valid_hours(cls, hours):
        """Validate the hours worked."""
        if not isinstance(hours, int):
            return False
        if not (cls.MIN_HOURS <= hours <= cls.MAX_HOURS):
            return False
        # else
        return True

    def __str__(self):
        """Return the worker's full info string."""
        return (f"WORKER: {super().__str__()}\n"
                f"Shift: {self.shift.name}\n"
                f"${self.pay_rate:.2f} per hour\n"
                f"{self.hours} hours this week\n"
                f"Gross pay: ${self.gross_pay():.0f}\n")


# Shift Supervisor class (subclass of Employee)
class ShiftSupervisor(Employee):
    """Supervisor of a single shift's production workers."""

    # class ("static") intended constants
    MIN_SALARY = 50000
    MAX_SALARY = 200000

    def __init__(self, name='unidentified', number=999, salary=50000, shift=Shift.DAY, max_workers=6):
        """Constructs all the necessary attributes for the supervisor."""
        super().__init__(name, number)
        if not self.set_salary(salary):
            self.salary = 50000
        if not self.set_shift(shift):
            self.shift = Shift.DAY
        self.max_workers = max_workers
        self.workers = []

    # mutators
    def set_salary(self, salary):
        """Set the supervisor's annual salary (50,000 - 200,000)."""
        if not self.valid_salary(salary):
            return False
        # else
        self.salary = salary
        return True

    def set_shift(self, shift):
        """Set the supervisor's shift."""
        if not isinstance(shift, Shift):
            return False
        # else
        self.shift = shift
        return True

    # accessors
    def get_salary(self):
        """Get the supervisor's annual salary."""
        return self.salary

    def get_shift(self):
        """Get the supervisor's shift."""
        return self.shift

    def get_num_workers(self):
        """Get the current count of workers reporting to this supervisor."""
        return len(self.workers)

    # class methods
    @classmethod
    def valid_salary(cls, salary):
        """Validate the salary range."""
        if not isinstance(salary, int):
            return False
        if not (cls.MIN_SALARY <= salary <= cls.MAX_SALARY):
            return False
        # else
        return True

    # helpers
    def shift_valid(self, worker):
        """Return True if the worker's shift matches this supervisor's."""
        return worker.get_shift() == self.get_shift()

    def add_worker(self, worker):
        """Add a worker to the list, with shift / capacity validation."""
        if not self.shift_valid(worker):
            QMessageBox.warning(None, "Error",
                                f"Worker shift ({worker.get_shift().name}) does not match "
                                f"supervisor shift ({self.shift.name}).")
            return False
        if len(self.workers) >= self.max_workers:
            QMessageBox.warning(None, "Error",
                                f"No spots available ({self.max_workers} max).")
            return False
        self.workers.append(worker)
        return True

    def remove_worker(self, worker):
        """Remove a ProductionWorker from this supervisor's worker list."""
        if worker in self.workers:
            self.workers.remove(worker)
            worker.supervisor_name = "No one"

    def bonus(self):
        """Award a $10,000 bonus when at least 5 workers report in."""
        if len(self.workers) >= 5:
            self.salary += 10000
            return True
        # else
        return False

    def __str__(self):
        """Return the supervisor's info string followed by each worker."""
        text = (f"SUPERVISOR: {super().__str__()}\n"
                f"Salary ${self.salary}\n"
                f"Shift: {self.shift.name}\n"
                f"{len(self.workers)} workers in their shift:\n")
        for w in self.workers:
            text += f"  - {w.get_name()}\n"
        return text


# UI class
class UI(QMainWindow):

    def __init__(self):
        """Initialize the main window, arrays, widgets, and signal connections."""
        super().__init__()
        uic.loadUi("mainwindow.ui", self)

        # fixed size array
        self.workers: list[ProductionWorker | None] = [None] * 5
        self.supervisors: list[ShiftSupervisor | None] = [None] * 3

        # array index counter
        self.w_i: int = 0
        self.s_i: int = 0

        # widgets
        self.label_disp = self.findChild(QLabel, "labelDisplay")
        self.box_sup = self.findChild(QComboBox, "comboBoxSup")
        self.box_work = self.findChild(QComboBox, "comboBoxWork")
        self.button_sup = self.findChild(QPushButton, "pushButtonDispSup")
        self.button_work = self.findChild(QPushButton, "pushButtonDispWork")
        self.action_sup_input = self.findChild(QAction, "actionSupervisorInput")
        self.action_work_input = self.findChild(QAction, "actionProduction_WorkerInput")
        self.action_sup_remove = self.findChild(QAction, "actionSupervisorRemove")
        self.action_work_remove = self.findChild(QAction, "actionProduction_WorkerRemove")

        # Connect signals
        self.action_sup_input.triggered.connect(self.click_supervisor_input)
        self.action_work_input.triggered.connect(self.click_worker_input)
        self.action_sup_remove.triggered.connect(self.click_supervisor_remove)
        self.action_work_remove.triggered.connect(self.click_worker_remove)
        self.button_sup.clicked.connect(self.display_supervisor)
        self.button_work.clicked.connect(self.display_worker)

        self.show()

    # open input windows
    def click_supervisor_input(self):
        """Open the supervisor input window if the supervisor array is not full."""
        if self.s_i >= 3:
            QMessageBox.warning(self, "Error", "Supervisor array is full (max 3).")
            return
        self.sup_window = SupervisorWindow(self)
        self.sup_window.show()

    def click_worker_input(self):
        """Open the worker input window if a supervisor exists and worker array is not full."""
        if self.s_i == 0:
            QMessageBox.warning(self, "Error", "Please add a supervisor first.")
            return
        if self.w_i >= 5:
            QMessageBox.warning(self, "Error", "Worker array is full (max 5).")
            return
        self.worker_window = WorkerWindow(self)
        self.worker_window.show()

    # display selected item
    def display_supervisor(self):
        """Display the selected supervisor's info in the display label."""
        index = self.box_sup.currentIndex()
        if index < 0 or self.supervisors[index] is None:
            return
        self.label_disp.setText(str(self.supervisors[index]))

    def display_worker(self):
        """Display the selected worker's info in the display label."""
        index = self.box_work.currentIndex()
        if index < 0 or self.workers[index] is None:
            return
        self.label_disp.setText(str(self.workers[index]))

    # remove selected item
    def click_supervisor_remove(self):
        """Remove the selected supervisor and detach their workers."""
        index = self.box_sup.currentIndex()
        if index < 0:
            QMessageBox.warning(self, "Error", "No supervisor selected.")
            return

        sup = self.supervisors[index]
        if sup is None:
            return

        # Detach workers — they stay in the system but lose their supervisor
        for worker in sup.workers:
            worker.supervisor_name = "No one"

        # Shift array left
        self.supervisors.pop(index)
        self.supervisors.append(None)
        self.s_i -= 1

        self.box_sup.removeItem(index)
        self.label_disp.clear()

    def click_worker_remove(self):
        """Remove the selected worker and unassign them from their supervisor."""
        index = self.box_work.currentIndex()
        if index < 0:
            QMessageBox.warning(self, "Error", "No worker selected.")
            return

        worker = self.workers[index]
        if worker is None:
            return

        # Remove worker from supervisor's list
        for sup in self.supervisors:
            if sup is not None and worker in sup.workers:
                sup.remove_worker(worker)
                break

        self.workers.pop(index)
        self.workers.append(None)
        self.w_i -= 1

        self.box_work.removeItem(index)
        self.label_disp.clear()

    # helpers
    def show_info(self, text):
        """Handle success popup"""
        QMessageBox.information(self, "Info", text)

    def show_error(self, text):
        """Handle error popup"""
        QMessageBox.critical(self, "Error", text)


# Supervisor Input Window
class SupervisorWindow(QMainWindow):

    def __init__(self, main_window):
        """Initialize the supervisor input window and connect the submit button."""
        super().__init__()
        uic.loadUi("supervisorinput.ui", self)
        self.main_window = main_window

        # widgets
        self.name_input = self.findChild(QLineEdit, "lineEditName")
        self.number_input = self.findChild(QLineEdit, "lineEditNumber")
        self.salary_input = self.findChild(QLineEdit, "lineEditSalary")
        self.max_input = self.findChild(QLineEdit, "lineEditMax")
        self.combo_shift = self.findChild(QComboBox, "comboBoxShift")
        self.submit_btn = self.findChild(QPushButton, "pushButtonSubmit")

        self.submit_btn.clicked.connect(self.submit_supervisor)

    def submit_supervisor(self):
        """Validate and submit supervisor data (Lab 5 rules applied)."""

        # Name
        name = self.name_input.text().strip()

        if not name:
            self.show_error("Supervisor name is required.")
            return

        # Number
        num_text = self.number_input.text().strip()

        if not num_text:
            self.show_error("Supervisor number is required.")
            return

        if not num_text.isdigit():
            self.show_error("Supervisor number must contain only digits.")
            return

        number = int(num_text)

        if not Employee.valid_number(number):
            self.show_error("Supervisor number must be between 100 and 999.")
            return

        # Salary
        salary_text = self.salary_input.text().strip()

        if not salary_text:
            self.show_error("Salary is required.")
            return

        if not salary_text.isdigit():
            self.show_error("Salary must be a whole number.")
            return

        salary = int(salary_text)

        if not ShiftSupervisor.valid_salary(salary):
            self.show_error("Salary must be between 50000 and 200000.")
            return

        # Max workers
        max_w_text = self.max_input.text().strip()

        if not max_w_text:
            self.show_error("Max workers is required.")
            return

        if not max_w_text.isdigit():
            self.show_error("Max workers must be a whole number.")
            return

        max_workers = int(max_w_text)

        # Shift
        shift = Shift[self.combo_shift.currentText()]

        # Create and store supervisor
        sup = ShiftSupervisor(name, number, salary, shift, max_workers)
        self.main_window.supervisors[self.main_window.s_i] = sup
        self.main_window.s_i += 1
        self.main_window.box_sup.addItem(sup.get_name())

        self.show_info(f"Supervisor '{name}' added successfully.")
        self.close()

    def show_error(self, text):
        """Handle error popup"""
        QMessageBox.critical(self, "Error", text)

    def show_info(self, text):
        """Handle success popup"""
        QMessageBox.information(self, "Success", text)


# Worker Input Window
class WorkerWindow(QMainWindow):

    def __init__(self, main_window):
        """Initialize the worker input window, populate the supervisor dropdown, and connect the submit button."""
        super().__init__()
        uic.loadUi("workerinput.ui", self)
        self.main_window = main_window

        # widgets
        self.name_input = self.findChild(QLineEdit, "lineEditWorkName")
        self.number_input = self.findChild(QLineEdit, "lineEditWorkNumber")
        self.rate_input = self.findChild(QLineEdit, "lineEditRate")
        self.hours_input = self.findChild(QLineEdit, "lineEditHours")
        self.combo_shift = self.findChild(QComboBox, "comboBoxWorkShift")
        self.combo_sup = self.findChild(QComboBox, "comboBoxSupervisor")

        self.submit_btn = self.findChild(QPushButton, "pushButtonSubmitWorker")

        # fill supervisor combo box
        for sup in self.main_window.supervisors:
            if sup is not None:
                self.combo_sup.addItem(sup.get_name())

        self.submit_btn.clicked.connect(self.submit_worker)

    def submit_worker(self):
        """Validate and submit worker data (Lab 5 rules applied)."""
        # Name
        name = self.name_input.text().strip()
        if not name:
            self.show_error("Worker name is required.")
            return

        # Number
        num_text = self.number_input.text().strip()
        if not num_text:
            self.show_error("Worker number is required.")
            return
        if not num_text.isdigit():
            self.show_error("Worker number must contain digits only.")
            return
        number = int(num_text)
        if not Employee.valid_number(number):
            self.show_error("Worker number must be between 100 and 999.")
            return

        # Pay rate
        rate_text = self.rate_input.text().strip()
        if not rate_text:
            self.show_error("Pay rate is required.")
            return
        if not rate_text.isdigit():
            self.show_error("Pay rate must be a whole number.")
            return
        pay_rate = int(rate_text)
        if not ProductionWorker.valid_pay_rate(pay_rate):
            self.show_error("Pay rate must be between 1 and 20.")
            return

        # Hours
        hours_text = self.hours_input.text().strip()
        if not hours_text:
            self.show_error("Hours is required.")
            return
        if not hours_text.isdigit():
            self.show_error("Hours must be a whole number.")
            return
        hours = int(hours_text)
        if not ProductionWorker.valid_hours(hours):
            self.show_error("Hours must be between 0 and 40.")
            return

        # Shift
        shift = Shift[self.combo_shift.currentText()]

        # Create worker
        worker = ProductionWorker(name, number, shift, pay_rate, hours)

        # Assign to supervisor
        sup_index = self.combo_sup.currentIndex()
        supervisor = self.main_window.supervisors[sup_index]
        if supervisor is not None:
            if not supervisor.add_worker(worker):
                return

        # Store in main array
        self.main_window.workers[self.main_window.w_i] = worker
        self.main_window.w_i += 1
        self.main_window.box_work.addItem(worker.get_name())

        self.show_info(f"Worker '{name}' added successfully.")
        self.close()

    def show_error(self, text):
        """Handle error popup"""
        QMessageBox.critical(self, "Error", text)

    def show_info(self, text):
        """Handle success popup"""
        QMessageBox.information(self, "Success", text)


def main():
    """Client program"""

    app = QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
