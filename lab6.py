import click
from models import FopEmployee
from utils import generate_employees, get_sorted_employees


@click.group()
def cli():
  pass


@cli.command()
@click.option(
    '--count', default=15, help='Кількість робітників для генерації'
)
def list_all(count):
  employees = generate_employees(count)
  sorted_employees = get_sorted_employees(employees)

  header = f"{'ID':<8} | {'Прізвище':<15} | {'Зарплата (грн)':<15} | {'Податок (грн)':<15}"
  click.echo(header)
  click.echo('-' * 65)

  for e in sorted_employees:
    salary = round(e.calculate_salary(), 2)
    tax = round(e.calculate_taxes(), 2)
    click.echo(
        f'{e.emp_id:<8} | {e.last_name:<15} | {salary:<15.2f} | {tax:<15.2f}'
    )


@cli.command()
@click.option('--group', type=int, help='Фільтр за групою ФОП (2 або 3)')
@click.option('--min-income', type=float, help='Мінімальний рівень доходу')
@click.option('--max-tax', type=float, help='Максимальний розмір податку')
def filter_fop(group, min_income, max_tax):
  employees = generate_employees(30)
  fops = [e for e in employees if isinstance(e, FopEmployee)]

  if group is not None:
    fops = [e for e in fops if e.group == group]
  if min_income is not None:
    fops = [e for e in fops if e.calculate_salary() >= min_income]
  if max_tax is not None:
    fops = [e for e in fops if e.calculate_taxes() <= max_tax]

  if not fops:
    click.echo('ФОПів за вказаними критеріями не знайдено.')
    return

  header = f"{'ID':<8} | {'Прізвище':<12} | {'Група':<6} | {'ЗП (грн)':<12} | {'Податок (грн)':<12}"
  click.echo(header)
  click.echo('-' * 60)

  for f in fops:
    salary = round(f.calculate_salary(), 2)
    tax = round(f.calculate_taxes(), 2)
    click.echo(
        f'{f.emp_id:<8} | {f.last_name:<12} | {f.group:<6} | {salary:<12.2f} |'
        f' {tax:<12.2f}'
    )


if __name__ == '__main__':
  cli()