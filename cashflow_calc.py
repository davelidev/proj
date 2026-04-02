import pandas as pd

def run_dadu_amortization_model():
    # ==========================================
    # INPUTS: Tweak these for different scenarios
    # ==========================================
    main_house_cost = 800_000
    construction_cost = 350000 * 2
    property_tax_rate = 0.01
    total_monthly_rent = 8000
    
    down_payment_pct = 0.20
    interest_rate = 0.07
    loan_term_years = 30
    
    
    # Extra payment strategy
    extra_pmt_frequency = 3    # 3 = Quarterly, 1 = Monthly, 12 = Yearly

    # ==========================================

    # 1. Calculate Initial Loan Balances
    total_project_cost = main_house_cost + construction_cost
    down_payment_amount = total_project_cost * down_payment_pct
    total_starting_loan = total_project_cost - down_payment_amount
    monthly_property_tax = (total_project_cost * property_tax_rate) / 12
    
    # 2. Calculate Standard Minimum Monthly Payment
    monthly_rate = interest_rate / 12
    term_months = loan_term_years * 12
    
    if monthly_rate > 0:
        standard_pmt = total_starting_loan * (monthly_rate * (1 + monthly_rate)**term_months) / ((1 + monthly_rate)**term_months - 1)
    else:
        standard_pmt = total_starting_loan / term_months

    # Calculate cash flow and determine extra payment strategy
    # A more detailed model would also subtract taxes, insurance, maintenance, etc.
    monthly_cash_flow = total_monthly_rent - standard_pmt - monthly_property_tax
    # For this model, we assume all positive cash flow is used as an extra payment
    extra_principal_pmt = total_monthly_rent

    print(f"Total Project Cost: ${total_project_cost:,.2f}")
    print(f"Down Payment ({down_payment_pct:.2%}): ${down_payment_amount:,.2f}")
    print(f"Total Starting Loan: ${total_starting_loan:,.2f}")
    print(f"Standard Monthly Payment (P&I): ${standard_pmt:,.2f}")
    print(f"Monthly Property Tax: ${monthly_property_tax:,.2f}")
    print(f"Monthly Cash Flow (Rent - P&I - Tax): ${monthly_cash_flow:,.2f}")

    # 3. Run the Amortization Loop
    balance = total_starting_loan
    cumulative_principal = 0
    total_interest_paid = 0
    yearly_data = []

    for year in range(1, loan_term_years + 1):
        principal_this_year = 0
        interest_this_year = 0
        
        for month in range(1, 13):
            if balance <= 0:
                break
            
            # Standard amortization math
            interest_charge = balance * monthly_rate
            principal_pay = standard_pmt - interest_charge
            
            # Apply the extra principal payment based on frequency
            m_total = (year - 1) * 12 + month
            if extra_pmt_frequency > 0 and m_total % extra_pmt_frequency == 0:
                principal_pay += extra_principal_pmt
                
            # Prevent overpaying on the final month
            if principal_pay > balance:
                principal_pay = balance
                
            balance -= principal_pay
            principal_this_year += principal_pay
            interest_this_year += interest_charge
            
            cumulative_principal += principal_pay
            total_interest_paid += interest_charge
            
        # Record data at the end of each year
        if principal_this_year > 0:
            yearly_data.append({
                "Year": year,
                "Principal Paid ($)": round(principal_this_year, 2),
                "Interest Paid ($)": round(interest_this_year, 2),
                "Cumulative Equity ($)": round(cumulative_principal, 2),
                "Remaining Balance ($)": round(balance, 2)
            })
            
        if balance <= 0:
            payoff_year = year - 1 + (month / 12)
            break

    # 4. Output the Results
    df = pd.DataFrame(yearly_data)
    
    # Format columns for readability
    for col in df.columns:
        if col != "Year":
            df[col] = df[col].apply(lambda x: f"${x:,.0f}")
            
    print(df.to_string(index=False))
    print("-" * 50)
    print(f"Total Interest Paid: ${total_interest_paid:,.2f}")

    if balance <= 0:
        print(f"Fully Paid Off In: ~{payoff_year:.1f} Years")
    else:
        print("Loan finishes exactly on schedule (30 Years).")

    # 5. Calculate Down Payment for Positive Cash Flow
    print("\n" + "="*50)
    print("ANALYSIS: Down Payment for Positive Cash Flow")
    print("="*50)

    found_breakeven = False
    # Iterate from 0% to 100% down payment
    for dp_pct_int in range(0, 101):
        dp_pct = dp_pct_int / 100.0
        loan_for_calc = total_project_cost * (1 - dp_pct)

        if monthly_rate > 0:
            pmt_for_calc = loan_for_calc * (monthly_rate * (1 + monthly_rate)**term_months) / ((1 + monthly_rate)**term_months - 1)
        else:
            pmt_for_calc = loan_for_calc / term_months if term_months > 0 else 0

        if total_monthly_rent - pmt_for_calc - monthly_property_tax >= 0:
            down_payment_amount = total_project_cost * dp_pct
            print(f"To achieve positive cash flow (where rent covers P&I and Tax), you need a down payment of at least: {dp_pct:.1%}")
            print(f"This equates to an initial investment of: ${down_payment_amount:,.2f}")
            found_breakeven = True
            break
    if not found_breakeven:
        print("Positive cash flow is not achievable with the current rent and interest rate, even with 100% down.")

if __name__ == "__main__":
    run_dadu_amortization_model()