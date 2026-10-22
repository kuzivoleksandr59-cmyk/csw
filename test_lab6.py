from click.testing import CliRunner
from lab6 import cli
from models import FixedSalaryEmployee, FopEmployee, HourlyEmployee
import pytest


def test_hourly_employee():
  emp = HourlyEmployee('E01', 'Іван', 'Петренко', 10.0)
  assert emp.calculate_salary() == 1664.0
  assert pytest.approx(emp.calculate_taxes(), 0.01) == 324.48


def test_fixed_salary_employee():
  emp = FixedSalaryEmployee('E02', 'Марія', 'Коваль', 20000.0)
  assert emp.calculate_salary() == 20000.0
  assert pytest.approx(emp.calculate_taxes(), 0.01) == 3900.0


def test_fop_employee():
  emp = FopEmployee('E03', 'Олег', 'Сидоренко', 10.0, group=3)
  assert pytest.approx(emp.calculate_salary(), 0.01) == 1830.4
  assert pytest.approx(emp.calculate_taxes(), 0.01) == 1851.52


def test_cli_list_all():
  runner = CliRunner()
  result = runner.invoke(cli, ['list-all', '--count', '5'])
  assert result.exit_code == 0
  assert 'ID' in result.output


def test_cli_filter_fop():
  runner = CliRunner()
  result = runner.invoke(cli, ['filter-fop', '--group', '3'])
  assert result.exit_code == 0