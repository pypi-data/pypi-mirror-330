
def calculate_roi(initial: int, final: int) -> float:
    return (final - initial) / initial

def project_growth(initial, growth_rate, years):
    return initial * (1 + growth_rate) ** years


if __name__ == "__main__":
    initial_investment = 1000
    final_value = 1500

    roi = calculate_roi(initial_investment, final_value)
    print(f"ROI: {roi:.2%}")

    growth_rate = 0.05
    years = 10
    projected_value = project_growth(initial_investment, growth_rate, years)
    print(f"Projected Growth: {projected_value:.2f}")