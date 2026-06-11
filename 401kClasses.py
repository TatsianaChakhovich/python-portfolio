"""
PW401k and S401k classes
by Tatsiana Chakhovich
May 27, 2026
"""

import random
from enum import Enum


class Shift(Enum):
    """ A class to represent Shift using enum """
    DAY = 1
    SWING = 2
    NIGHT = 3


class Employee:
    """ A class to represent an Employee """

    # class ("static") intended constants
    MIN_NUMBER = 100
    MAX_NUMBER = 999

    @staticmethod
    def _generate_account(number):
        """Generate account number as three random lowercase letters
        followed by the employee number (e.g. 'xkq573')."""
        letters = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(3))
        return letters + str(number)

    # initializer ("constructor") method
    def __init__(self, name='unidentified', number=999, **kwargs):
        """Constructs all the necessary attributes for the employee object."""
        super().__init__(**kwargs)
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
        """Return employee's info."""
        if type(self) is not Employee:
            return ""
        benefits_text = "Benefits" if self.benefits else "No benefits"
        return f"{self.name}  #{self.number} ({benefits_text})"


# ProductionWorker (subclass of Employee)
class ProductionWorker(Employee):
    """An hourly production worker assigned to one shift."""

    # class ("static") intended constants
    MIN_RATE = 1
    MAX_RATE = 20
    MIN_HOURS = 0
    MAX_HOURS = 40

    def __init__(self, name='unidentified', number=999, shift=Shift.DAY, pay_rate=1, hours=0, **kwargs):
        """Constructs all the necessary attributes for the worker object."""
        super().__init__(name=name, number=number, **kwargs)
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
        """Set the worker's hourly pay rate (1-20)."""
        if not self.valid_pay_rate(pay_rate):
            return False
        # else
        self.pay_rate = float(pay_rate)
        return True

    def set_hours(self, hours):
        """Set hours worked this week (0-40)."""
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
        if not isinstance(pay_rate, (int, float)):
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
        if type(self) is not ProductionWorker:
            return ""
        return (f"WORKER: {self.name}  #{self.number}\n"
                f"Shift: {self.shift.name}\n"
                f"${self.pay_rate:.2f} per hour\n"
                f"{self.hours} hours this week\n"
                f"Gross pay: ${self.gross_pay():.2f}\n")


# ShiftSupervisor (subclass of Employee)
class ShiftSupervisor(Employee):
    """Supervisor of a single shift's production workers."""

    # class ("static") intended constants
    MIN_SALARY = 50000
    MAX_SALARY = 200000

    def __init__(self, name='unidentified', number=999, salary=50000, shift=Shift.DAY, max_workers=6, **kwargs):
        """Constructs all the necessary attributes for the supervisor."""
        super().__init__(name=name, number=number, **kwargs)
        if not self.set_salary(salary):
            self.salary = 50000
        if not self.set_shift(shift):
            self.shift = Shift.DAY
        self.max_workers = max_workers
        self.workers = []  # list of ProductionWorker objects

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
        if not isinstance(salary, (int, float)):
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
        try:
            if not self.shift_valid(worker):
                raise ValueError
            if len(self.workers) >= self.max_workers:
                raise IndexError
            self.workers.append(worker)
        except ValueError:
            print(f"  Cannot add {worker.get_name()}: shift "
                  f"{worker.get_shift().name} does not match supervisor "
                  f"shift {self.shift.name}")
        except IndexError:
            print(f"  Cannot add {worker.get_name()}: no spots available "
                  f"({self.max_workers} spots already filled)")

    def bonus(self):
        """Award a $10,000 bonus when at least 5 workers report in."""
        if len(self.workers) >= 5:
            self.salary += 10000
            return True
        # else
        return False

    def __str__(self):
        """Return the supervisor's info string followed by each worker."""
        if type(self) is not ShiftSupervisor:
            return ""
        text = (f"SUPERVISOR: {self.name}  #{self.number}\n"
                f"Salary: ${self.salary:,.2f}\n"
                f"Shift: {self.shift.name}\n")
        return text


class PW401k(ProductionWorker):
    """401k retirement plan for a Production Worker."""

    # class ("static") intended constants
    MIN_CONTRIBUTION = 0
    MAX_CONTRIBUTION = 5000

    def __init__(self, name='unidentified', number=999,
                 shift=Shift.DAY, pay_rate=1, hours=0,
                 _account='qqq999', contribution=0, **kwargs):
        """Constructs all the necessary attributes for PW401k object."""
        super().__init__(name=name, number=number,
                         shift=shift, pay_rate=pay_rate,
                         hours=hours, **kwargs)

        self._account = self._generate_account(self.number)
        self._max_match = 0.0
        self._actual_match = 0.0
        self._contribution = None
        self.set_contribution(contribution)

    # mutators
    def set_contribution(self, amount):
        """Validate, store contribution, then recalc both matches."""
        if not isinstance(amount, (int, float)):
            return False
        if not (self.MIN_CONTRIBUTION <= amount <= self.MAX_CONTRIBUTION):
            return False
        self._contribution = float(amount)
        self.calc_max_match()
        self.calc_actual_match()
        return True

    def set_account(self, account):
        """Set the worker's account number."""
        self._account = account

    # accessors
    def get_contribution(self):
        """Return the worker's monthly contribution amount."""
        return self._contribution

    def get_account(self):
        """Return the worker's 401k account number."""
        return self._account

    def get_max_match(self):
        """Return the maximum worker match (5% of monthly pay)."""
        return self._max_match

    def get_actual_match(self):
        """Return the actual worker match."""
        return self._actual_match

    # helpers
    def calc_max_match(self):
        """Max match = 5% of monthly pay (weekly gross * 4)."""
        monthly_pay = self.gross_pay() * 4
        self._max_match = monthly_pay * 0.05

    def calc_actual_match(self):
        """Actual match = lesser of contribution or max match."""
        self._actual_match = min(self._contribution, self._max_match)

    def monthly_pay(self):
        """Return monthly pay."""
        return self.gross_pay() * 4

    def __str__(self):
        """Return a formatted string with the worker's 401k info,
        including account number, monthly pay, contribution, and match amounts."""
        if type(self) is not PW401k:
            return ""
        return (
            f"{self.name}  #{self.number}\n"
            f"Account #{self._account}\n"
            f"Monthly pay: ${self.monthly_pay():,.2f}\n"
            f"Amount contributed: ${self._contribution:,.2f}\n"
            f"Max match: ${self._max_match:,.2f}\n"
            f"Actual match: ${self._actual_match:,.2f}\n"
        )


class S401k(ShiftSupervisor):
    """401k retirement plan for a Shift Supervisor."""

    # class ("static") intended constants
    MIN_CONTRIBUTION = 0
    MAX_CONTRIBUTION = 5000

    def __init__(self, name='unidentified', number=999,
                 salary=50000, shift=Shift.DAY, max_workers=6,
                 _account='qqq999', contribution=0, **kwargs):
        """Constructs all the necessary attributes for S401k object."""
        super().__init__(name=name, number=number,
                         salary=salary, shift=shift,
                         max_workers=max_workers, **kwargs)

        self._account = self._generate_account(self.number)
        self._max_match = 0.0
        self._actual_match = 0.0
        self._contribution = None
        self.set_contribution(contribution)

    # mutators
    def set_contribution(self, amount):
        """Validate, store contribution, then recalc both matches."""
        if not isinstance(amount, (int, float)):
            return False
        if not (self.MIN_CONTRIBUTION <= amount <= self.MAX_CONTRIBUTION):
            return False
        self._contribution = float(amount)
        self.calc_max_match()
        self.calc_actual_match()
        return True

    def set_account(self, account):
        """Set the supervisor's account number."""
        self._account = account

    # accessors
    def get_contribution(self):
        """Return the supervisor's monthly contribution amount."""
        return self._contribution

    def get_account(self):
        """Return the supervisor's 401k account number."""
        return self._account

    def get_max_match(self):
        """Return the maximum supervisor match (5% of monthly pay)."""
        return self._max_match

    def get_actual_match(self):
        """Return the actual supervisor match."""
        return self._actual_match

    # helpers
    def calc_max_match(self):
        """Max match = 5% of monthly salary (annual / 12)."""
        monthly_pay = self.salary / 12
        self._max_match = monthly_pay * 0.05

    def calc_actual_match(self):
        """Actual match = lesser of contribution or max match."""
        self._actual_match = min(self._contribution, self._max_match)

    def monthly_pay(self):
        """Return monthly pay."""
        return self.salary / 12

    def __str__(self):
        """Return a formatted string with the supervisor's 401k info,
        including account number, monthly pay, contribution, and match amounts."""
        if type(self) is not S401k:
            return ""
        return (
            f"{self.name}  #{self.number}\n"
            f"Account #{self._account}\n"
            f"Monthly pay: ${self.monthly_pay():,.2f}\n"
            f"Amount contributed: ${self._contribution:,.2f}\n"
            f"Max match: ${self._max_match:,.2f}\n"
            f"Actual match: ${self._actual_match:,.2f}\n"
        )


def main():

    pw1 = PW401k(name='John Smith', number=578,
                 shift=Shift.DAY, pay_rate=15, hours=35,
                 contribution=500)  # max

    pw2 = PW401k(name='Maria Brown', number=501,
                 shift=Shift.NIGHT, pay_rate=14, hours=40,
                 contribution=400)  # max

    pw3 = PW401k(name='Jim Stone', number=399,
                 shift=Shift.SWING, pay_rate=10, hours=38,
                 contribution=50)  # under max

    s1 = S401k(name='Tom Linn', number=133,
               salary=96000, shift=Shift.DAY,
               contribution=590)  # max

    s2 = S401k(name='Sam Winter', number=651,
               salary=72000, shift=Shift.NIGHT,
               contribution=100)  # under max

    employees = [pw1, pw2, pw3, s1, s2]

    # first display
    print("Initial contributions")
    print("pw1, pw2, s1 maxed out; pw3, s2 under max")
    print("=" * 60)
    for emp in employees:
        print(emp)
        print("-" * 40)

    # update the two under-max employees so they hit the max
    print("Updating pw3 and s2 so they now hit their max match")

    pw3.set_contribution(pw3.get_max_match())
    print(f"{pw3.get_name()}: contribution set to "
          f"${pw3.get_contribution():.2f} "
          f"(max match = ${pw3.get_max_match():.2f})")

    s2.set_contribution(s2.get_max_match())
    print(f"{s2.get_name()}: contribution set to "
          f"${s2.get_contribution():.2f} "
          f"(max match = ${s2.get_max_match():.2f})")
    print("\n" + "=" * 60)

    # second display
    for emp in employees:
        print(emp)
        print("-" * 40)


if __name__ == "__main__":
    main()

r"""C:\Users\tania\AppData\Local\Python\bin\python.exe C:\Users\tania\PycharmProjects\pythonProject2\Lab_Assignment_7.py 
Initial contributions
pw1, pw2, s1 maxed out; pw3, s2 under max
============================================================
John Smith  #578
Account #dkw578
Monthly pay: $2,100.00
Amount contributed: $500.00
Max match: $105.00
Actual match: $105.00

----------------------------------------
Maria Brown  #501
Account #soq501
Monthly pay: $2,240.00
Amount contributed: $400.00
Max match: $112.00
Actual match: $112.00

----------------------------------------
Jim Stone  #399
Account #zek399
Monthly pay: $1,520.00
Amount contributed: $50.00
Max match: $76.00
Actual match: $50.00

----------------------------------------
Tom Linn  #133
Account #jgr133
Monthly pay: $8,000.00
Amount contributed: $590.00
Max match: $400.00
Actual match: $400.00

----------------------------------------
Sam Winter  #651
Account #qwd651
Monthly pay: $6,000.00
Amount contributed: $100.00
Max match: $300.00
Actual match: $100.00

----------------------------------------
Updating pw3 and s2 so they now hit their max match
Jim Stone: contribution set to $76.00 (max match = $76.00)
Sam Winter: contribution set to $300.00 (max match = $300.00)

============================================================
John Smith  #578
Account #dkw578
Monthly pay: $2,100.00
Amount contributed: $500.00
Max match: $105.00
Actual match: $105.00

----------------------------------------
Maria Brown  #501
Account #soq501
Monthly pay: $2,240.00
Amount contributed: $400.00
Max match: $112.00
Actual match: $112.00

----------------------------------------
Jim Stone  #399
Account #zek399
Monthly pay: $1,520.00
Amount contributed: $76.00
Max match: $76.00
Actual match: $76.00

----------------------------------------
Tom Linn  #133
Account #jgr133
Monthly pay: $8,000.00
Amount contributed: $590.00
Max match: $400.00
Actual match: $400.00

----------------------------------------
Sam Winter  #651
Account #qwd651
Monthly pay: $6,000.00
Amount contributed: $300.00
Max match: $300.00
Actual match: $300.00

----------------------------------------

Process finished with exit code 0
"""