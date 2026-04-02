
import pandas as pd

def analyze_kirkland_hi_octane():
    # --- INPUTS ---
    purchase_price = 1_700_000
    construction_cost = 950_000 # Midpoint of 800k-1M
    construction_interest_rate = 0.10
    construction_months = 6
    perm_interest_rate = 0.055
    
    # Tax Rates
    fed_tax = 0.37
    niit = 0.038
    ordinary_rate = fed_tax + niit
    lt_cap_gain_rate = 0.20 + niit # 23.8%
    
    # Post-Construction Values
    val_main = 1_450_000
    val_dadus = 2_100_000 # 1.05M each
    total_val = val_main + val_dadus
    
    # Rents
    rent_main = 5_500 * 12
    rent_dadus = (3_800 * 2) * 12
    
    # --- 1. THE SUNK COST OF CONSTRUCTION ---
    # Avg balance of $950k draw over 6 months at 10%
    interest_carry_construction = (construction_cost / 2) * construction_interest_rate * (construction_months / 12)
    total_capital_outlay = construction_cost + interest_carry_construction
    
    # --- 2. OPTION: KEEP EVERYTHING (The "Compound" Strategy) ---
    # Annual Expenses (Property Tax, Ins, Maint @ 10%)
    prop_tax = total_val * 0.01
    insurance = 5000 # Main + 2 DADUs
    maint_vacancy = (rent_main + rent_dadus) * 0.10
    
    noi_pre_tax = (rent_main + rent_dadus) - prop_tax - insurance - maint_vacancy
    
    # Depreciation Shield (DADU structure only)
    depreciation_dadu = construction_cost / 27.5
    # Depreciation Main (Rental portion only - 0 if primary residence)
    # We assume you live in main for 2 years, so no depreciation there yet.
    
    taxable_income = (rent_dadus * 0.90) - (val_dadus * 0.01) - 2000 - depreciation_dadu
    tax_bill = max(0, taxable_income * ordinary_rate)
    
    after_tax_cf = noi_pre_tax - tax_bill
    annual_debt_service = (purchase_price + construction_cost) * perm_interest_rate # Assuming 100% LTV for math
    
    # --- 3. OPTION: SELL DADUS (The "De-Leverage" Strategy) ---
    selling_costs = val_dadus * 0.06
    basis_dadu = (purchase_price * 0.40) + total_capital_outlay # 40% land allocation
    gain_dadu = (val_dadus - selling_costs) - basis_dadu
    tax_on_dadu_sale = gain_dadu * lt_cap_gain_rate
    
    net_profit_dadu_sale = gain_dadu - tax_on_dadu_sale

    print(f"--- DETAILED PROJECT FINANICALS ---")
    print(f"Construction Interest Carry: ${interest_carry_construction:,.0f}")
    print(f"Total Cost Basis (All In): ${purchase_price + total_capital_outlay:,.0f}")
    print(f"Equity Created: ${total_val - (purchase_price + total_capital_outlay):,.0f}")
    
    print(f"\n--- IF YOU KEEP (Rental Phase) ---")
    print(f"Total Annual Rental NOI: ${noi_pre_tax:,.0f}")
    print(f"Annual Tax Bill (Top Bracket): ${tax_bill:,.0f}")
    print(f"After-Tax Cash Flow: ${after_tax_cf:,.0f}")
    print(f"Annual Interest (at 5.5%): ${annual_debt_service:,.0f}")
    print(f"Net Annual Spread: ${after_tax_cf - annual_debt_service:,.0f}")
    
    print(f"\n--- IF YOU SELL DADUs (Separate Sale) ---")
    print(f"Net Profit after Tax & Commission: ${net_profit_dadu_sale:,.0f}")

if __name__ == '__main__':
    analyze_kirkland_hi_octane()
    
if __name__ == '__main__':
    analyze_kirkland_dadu_project()
