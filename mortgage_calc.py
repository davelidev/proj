# --- USER INPUT SCENARIOS ---
# Note: This list is processed in the execution block at the bottom
SCENARIOS = [
    # Optional fields use defaults: appreciation=0, tax=1%, term=30yr, hold=5yr
    {
        "property_value": 1_500_000,
        "down_payment_percent": 20,
        "annual_interest_rate_percent": 5,
        "monthly_rent": 5500
    },
    {
        "property_value": 1_500_000,
        "down_payment_percent": 30,
        "annual_interest_rate_percent": 5,
        "monthly_rent": 5500
    },
    {
        "property_value": 1_150_000,
        "down_payment_percent": 20,
        "annual_interest_rate_percent": 5,
        "monthly_rent": 3500
    },
    {
        "property_value": 1_150_000,
        "down_payment_percent": 30,
        "annual_interest_rate_percent": 5,
        "monthly_rent": 3500
    },
]

# --- CONSTANTS ---
MONTHS_IN_YEAR = 12

def calculate_investment_metrics(inputs) -> dict:
    """
    Calculates key real estate investment metrics based on provided inputs.
    Returns a dictionary containing all calculated values.
    """
    # --- INITIAL CALCULATIONS ---
    down_payment = inputs.property_value * (inputs.down_payment_percent / 100)
    loan_amount = inputs.property_value - down_payment
    monthly_interest_rate = (inputs.annual_interest_rate_percent / 100) / MONTHS_IN_YEAR
    num_payments = inputs.loan_term_years * MONTHS_IN_YEAR

    # Monthly P&I (Principal + Interest)
    if monthly_interest_rate > 0:
        monthly_pi = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**num_payments) / \
                     ((1 + monthly_interest_rate)**num_payments - 1)
    else: # Handle 0% interest case
        monthly_pi = loan_amount / num_payments if num_payments > 0 else 0

    # --- CAP RATE CALCULATION (Year 1) ---
    annual_rent = inputs.monthly_rent * MONTHS_IN_YEAR
    annual_property_tax_y1 = inputs.property_value * (inputs.annual_property_tax_percent / 100)
    annual_op_ex = (inputs.monthly_rent * (inputs.op_ex_vacancy_percent_of_rent / 100)) * MONTHS_IN_YEAR
    annual_noi = annual_rent - annual_property_tax_y1 - annual_op_ex
    cap_rate = (annual_noi / inputs.property_value) * 100 if inputs.property_value > 0 else 0

    # --- DYNAMIC PROJECTIONS over hold period ---
    current_balance = loan_amount
    total_principal_paid = 0
    total_interest_paid = 0
    total_cash_flow = 0
    total_property_tax_paid = 0
    monthly_op_expenses = inputs.monthly_rent * (inputs.op_ex_vacancy_percent_of_rent / 100)

    for month in range(1, (inputs.hold_period_years * MONTHS_IN_YEAR) + 1):
        if (month - 1) % MONTHS_IN_YEAR == 0:
            year_index = (month - 1) // MONTHS_IN_YEAR
            current_year_property_value = inputs.property_value * (1 + (inputs.annual_appreciation_percent / 100))**year_index
            monthly_tax = (current_year_property_value * (inputs.annual_property_tax_percent / 100)) / MONTHS_IN_YEAR

        total_property_tax_paid += monthly_tax
        monthly_cash_flow = inputs.monthly_rent - monthly_pi - monthly_tax - monthly_op_expenses
        total_cash_flow += monthly_cash_flow

        interest_payment = current_balance * monthly_interest_rate
        principal_payment = monthly_pi - interest_payment
        total_interest_paid += interest_payment
        total_principal_paid += principal_payment
        current_balance -= principal_payment

    appreciation_rate = inputs.annual_appreciation_percent / 100
    future_property_value = inputs.property_value * (1 + appreciation_rate)**inputs.hold_period_years
    appreciation_gain = future_property_value - inputs.property_value
    total_profit = total_cash_flow + total_principal_paid + appreciation_gain

    first_year_monthly_tax = (inputs.property_value * (inputs.annual_property_tax_percent / 100)) / MONTHS_IN_YEAR
    first_year_monthly_op_ex = inputs.monthly_rent * (inputs.op_ex_vacancy_percent_of_rent / 100)
    monthly_cash_flow_for_summary = inputs.monthly_rent - monthly_pi - first_year_monthly_tax - first_year_monthly_op_ex

    ending_equity = down_payment + total_profit
    if down_payment > 0:
        cagr = ((ending_equity / down_payment)**(1/inputs.hold_period_years) - 1) * 100
    else:
        cagr = float('inf') if ending_equity > 0 else 0

    return {
        "inputs": inputs,
        "down_payment_amount": down_payment,
        "principal_paid_amount": total_principal_paid,
        "total_interest_paid": total_interest_paid,
        "total_property_tax_paid": total_property_tax_paid,
        "total_cash_flow": total_cash_flow,
        "monthly_cash_flow": monthly_cash_flow_for_summary,
        "total_profit": total_profit,
        "cagr_percent": cagr,
        "cap_rate_percent": cap_rate,
        "ending_equity": ending_equity,
    }

def print_summary(results: dict, index: int):
    inputs = results["inputs"]
    input_data = [
        ("Property Value", f"${inputs.property_value:,.0f}"),
        ("Down Payment", f"{inputs.down_payment_percent:.1f}%"),
        ("Interest Rate", f"{inputs.annual_interest_rate_percent:.2f}%"),
        ("Monthly Rent", f"${inputs.monthly_rent:,.0f}"),
        ("Appreciation /yr", f"{inputs.annual_appreciation_percent:.2f}%"),
        ("Hold Period", f"{inputs.hold_period_years} years"),
    ]
    analysis_data = [
        ("Pre-Equity (Down Pay)", f"${results['down_payment_amount']:,.0f}"),
        ("Monthly Cash Flow (Y1)", f"${results['monthly_cash_flow']:,.2f}"),
        ("Cap Rate (Y1)", f"{results['cap_rate_percent']:.2f}%"),
        ("", ""),
        (f"--- PROJECTION: {inputs.hold_period_years} YEARS ---", ""),
        ("Total Interest Paid", f"${results['total_interest_paid']:,.0f}"),
        ("Total Property Tax Paid", f"${results['total_property_tax_paid']:,.0f}"),
        ("Total Cash Flow", f"${results['total_cash_flow']:,.0f}"),
        ("Principal Paid", f"${results['principal_paid_amount']:,.0f}"),
        ("Total Profit", f"${results['total_profit']:,.2f}"),
        ("Post-Equity", f"${results['ending_equity']:,.0f}"),
        ("", ""),
        ("Equity (CAGR)", f"{results['cagr_percent']:.2f}%"),
    ]

    input_width, analysis_width = 36, 43
    table_gap = "   "
    full_width = input_width + len(table_gap) + analysis_width

    print(f'\n{"=" * full_width}')

    print(f'\n{"--- INPUTS ---":^{input_width}}{table_gap}{"--- ANALYSIS ---":^{analysis_width}}')
    print(f'{"=" * input_width}{table_gap}{"=" * analysis_width}')
    for i in range(max(len(input_data), len(analysis_data))):
        left_row = f"{input_data[i][0]:<18} | {input_data[i][1]:>15}" if i < len(input_data) else ' ' * input_width
        right_row = f"{analysis_data[i][0]:<25} | {analysis_data[i][1]:>15}" if i < len(analysis_data) and analysis_data[i][1] else (analysis_data[i][0] if i < len(analysis_data) else ' ')
        print(f'{left_row}{table_gap}{right_row}')
    print(f'{"-" * input_width}{table_gap}{"-" * analysis_width}')

from dataclasses import dataclass

@dataclass
class InvestmentInputs:
    """A class to hold all input parameters for the investment calculation."""
    property_value: float
    down_payment_percent: float
    annual_interest_rate_percent: float
    monthly_rent: float
    # Optional fields with default values
    annual_appreciation_percent: float = 0.0
    op_ex_vacancy_percent_of_rent: float = 0.0
    annual_property_tax_percent: float = 1.0
    loan_term_years: int = 30
    hold_period_years: int = 5

if __name__ == "__main__":
    for idx, scenario_dict in enumerate(SCENARIOS, 1):
        scenario = InvestmentInputs(**scenario_dict)
        analysis_results = calculate_investment_metrics(scenario)
        print_summary(analysis_results, idx)