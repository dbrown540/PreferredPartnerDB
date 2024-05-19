from .scripts.indeedbot import SalaryFinder
from .utils.net_worth_analysis import NetWorthCalculator

def main():
    """salary_finder = SalaryFinder()
    salary_finder.access_indeed_salaries()"""

    net_worth_calc = NetWorthCalculator()
    net_worth_calc.wrapper()

if __name__ == "__main__":
    main()