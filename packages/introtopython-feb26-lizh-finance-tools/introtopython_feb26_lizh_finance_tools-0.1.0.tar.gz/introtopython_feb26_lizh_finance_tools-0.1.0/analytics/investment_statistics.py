import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from investments import calculate_roi, project_growth
from .statistics import moving_average

def investment_statistics(initial_investment, final_value, growth_rate, years):
    roi = calculate_roi(initial_investment, final_value)
    projected_growth = project_growth(initial_investment, growth_rate, years)
    return roi, projected_growth


if __name__ == "__main__":
    initial_investment = 1000
    final_value = 1500
    growth_rate = 0.05
    years = 10

    roi, projected_growth = investment_statistics(initial_investment, final_value, growth_rate, years)
    print(f"ROI: {roi:.2%}")
    print(f"Projected Growth: {projected_growth:.2f}")