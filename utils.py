import random
from faker import Faker
from models import (
    Employee,
    FixedSalaryEmployee,
    FopEmployee,
    HourlyEmployee,
    SelfEmployedContractor,
)

fake = Faker('uk_UA')


def generate_employees(count: int = 20) -> list[Employee]:
  employees = []
  for i in range(count):
    emp_id = f'EMP{i+1:03d}'
    first_name = fake.first_name()
    last_name = fake.last_name()
    emp_type = random.choice(['hourly', 'fixed', 'fop', 'self_employed'])

    if emp_type == 'hourly':
      emp = HourlyEmployee(
          emp_id, first_name, last_name, round(random.uniform(10, 50), 2)
      )
    elif emp_type == 'fixed':
      emp = FixedSalaryEmployee(
          emp_id, first_name, last_name, round(random.uniform(20000, 80000), 2)
      )
    elif emp_type == 'fop':
      emp = FopEmployee(
          emp_id,
          first_name,
          last_name,
          round(random.uniform(15, 60), 2),
          group=random.choice([2, 3]),
      )
    else:
      emp = SelfEmployedContractor(
          emp_id,
          first_name,
          last_name,
          round(random.uniform(1, 5), 2),
          random.randint(2000, 10000),
      )

    employees.append(emp)
  return employees


def get_sorted_employees(employees: list[Employee]) -> list[Employee]:
  return sorted(employees, key=lambda e: (-e.calculate_salary(), e.last_name))