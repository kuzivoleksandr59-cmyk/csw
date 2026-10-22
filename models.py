from abc import ABC, abstractmethod


class Employee(ABC):

  def __init__(self, emp_id: str, first_name: str, last_name: str):
    self.emp_id = emp_id
    self.first_name = first_name
    self.last_name = last_name

  @abstractmethod
  def calculate_salary(self) -> float:
    pass

  @abstractmethod
  def calculate_taxes(self) -> float:
    pass


class HourlyEmployee(Employee):

  def __init__(
      self, emp_id: str, first_name: str, last_name: str, hourly_rate: float
  ):
    super().__init__(emp_id, first_name, last_name)
    self.hourly_rate = hourly_rate

  def calculate_salary(self) -> float:
    return 20.8 * 8 * self.hourly_rate

  def calculate_taxes(self) -> float:
    return self.calculate_salary() * (0.18 + 0.015)


class FixedSalaryEmployee(Employee):

  def __init__(
      self, emp_id: str, first_name: str, last_name: str, monthly_salary: float
  ):
    super().__init__(emp_id, first_name, last_name)
    self.monthly_salary = monthly_salary

  def calculate_salary(self) -> float:
    return self.monthly_salary

  def calculate_taxes(self) -> float:
    return self.monthly_salary * (0.18 + 0.015)


class FopEmployee(Employee):

  def __init__(
      self,
      emp_id: str,
      first_name: str,
      last_name: str,
      hourly_rate: float,
      group: int = 3,
  ):
    super().__init__(emp_id, first_name, last_name)
    self.hourly_rate = hourly_rate
    self.group = group

  def calculate_salary(self) -> float:
    return (20.8 * 8 * self.hourly_rate) * 1.10

  def calculate_taxes(self) -> float:
    return (
        self.calculate_salary() * 0.05
    ) + 1760


class SelfEmployedContractor(Employee):

  def __init__(
      self,
      emp_id: str,
      first_name: str,
      last_name: str,
      price_per_line: float,
      lines_written: int,
  ):
    super().__init__(emp_id, first_name, last_name)
    self.price_per_line = price_per_line
    self.lines_written = lines_written

  def calculate_salary(self) -> float:
    return self.price_per_line * self.lines_written

  def calculate_taxes(self) -> float:
    return (
        self.calculate_salary() * (0.18 + 0.015)
    ) + 1760