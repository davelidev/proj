import re
import os
import sys

def generate_qc_report(raw_file, output_file, start_it, end_it):
    if not os.path.exists(raw_file):
        print(f"Error: {raw_file} not found.")
        return

    with open(raw_file, "r") as f:
        content = f.read()

    iterations = content.split("--- IT ")

    def parse_stats(block):
        stats = {}
        stats['CAGR'] = re.search(r"Compounding Annual Return:\s+([\d\.-]+)%", block)
        stats['MaxDD'] = re.search(r"Drawdown:\s+([\d\.-]+)%", block)
        stats['Sharpe'] = re.search(r"Sharpe Ratio:\s+([\d\.-]+)", block)
        stats['WinRate'] = re.search(r"Win Rate:\s+([\d\.-]+)%", block)
        stats['LossRate'] = re.search(r"Loss Rate:\s+([\d\.-]+)%", block)
        stats['ProfitLoss'] = re.search(r"Profit-Loss Ratio:\s+([\d\.-]+)", block)
        stats['Orders'] = re.search(r"Total Orders:\s+(\d+)", block)
        
        # Extract yearly returns
        yearly_matches = re.findall(r"(\d{4}):\s+[🟢🔴⚪]\s+([-]?\d+)%", block)
        stats['Yearly'] = {y: r for y, r in yearly_matches}
        
        # Clean up values
        for k, v in stats.items():
            if k != 'Yearly' and v:
                stats[k] = v.group(1)
        return stats

    it_data = {}
    for it_block in iterations[1:]:
        lines = it_block.split("\n")
        if not lines: continue
        header = lines[0]
        it_num_match = re.search(r"(\d+)", header)
        if not it_num_match: continue
        it_num = it_num_match.group(1)
        it_data[it_num] = parse_stats(it_block)

    # --- Generate Markdown ---
    md = f"# QuantConnect Community Research Ledger ({start_it}-{end_it})\n\n"
    md += f"This document tracks iterations {start_it} through {end_it} of the strategy scouting loop.\n"
    md += "**Pass Criteria:** CAGR >= 28% and MaxDD <= 58%.\n\n"

    # 1. Summary Table
    md += "| # | CAGR | MaxDD | Sharpe | Win % | Orders | P/L Ratio | Status |\n"
    md += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    for i in range(start_it, end_it + 1):
        idx = str(i)
        d = it_data.get(idx, {})
        cagr_str = d.get('CAGR', '0')
        dd_str = d.get('MaxDD', '0')
        try:
            cagr = float(cagr_str)
            dd = float(dd_str)
        except:
            cagr = 0
            dd = 0
            
        if cagr >= 28 and dd <= 58:
            status = "✅ Pass"
        elif cagr < 28 and dd > 58:
            status = "❌ Fail"
        elif cagr < 28:
            status = "❌ Low Return"
        else:
            status = "❌ High DD"
            
        md += f"| [{i}](#strategy-{i}) | {cagr_str}% | -{dd_str}% | {d.get('Sharpe')} | {d.get('WinRate')}% | {d.get('Orders')} | {d.get('ProfitLoss')} | {status} |\n"

    md += "\n\n"

    # 2. Yearly Table
    years = [str(y)[2:] for y in range(2014, 2026)]
    md += "| # | " + " | ".join(years) + " |\n"
    md += "| :--- | " + " | ".join([":---" for _ in years]) + " |\n"
    for i in range(start_it, end_it + 1):
        idx = str(i)
        d = it_data.get(idx, {})
        yearly = d.get('Yearly', {})
        row = [f"[{i}](#strategy-{i})"]
        for y in range(2014, 2026):
            val = yearly.get(str(y), "0")
            try:
                val_int = int(val)
                color = "🟢" if val_int > 0 else ("🔴" if val_int < 0 else "⚪")
            except:
                color = "⚪"
            row.append(f"{color} {val}%")
        md += "| " + " | ".join(row) + " |\n"

    md += "\n\n---\n\n"

    # 3. Detail Sections
    for i in range(start_it, end_it + 1):
        idx = str(i)
        d = it_data.get(idx, {})
        md += f"## Strategy-{i}\n"
        md += f"**Iteration {i} Results**\n\n"
        
        md += "| CAGR | MaxDD | Sharpe | Win % | Loss % | P/L Ratio |\n"
        md += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        md += f"| {d.get('CAGR')}% | -{d.get('MaxDD')}% | {d.get('Sharpe')} | {d.get('WinRate')}% | {d.get('LossRate')}% | {d.get('ProfitLoss')} |\n\n"
        
        md += "| " + " | ".join(years) + " |\n"
        md += "| " + " | ".join([":---" for _ in years]) + " |\n"
        row = []
        yearly = d.get('Yearly', {})
        for y in range(2014, 2026):
            val = yearly.get(str(y), "0")
            try:
                val_int = int(val)
                color = "🟢" if val_int > 0 else ("🔴" if val_int < 0 else "⚪")
            except:
                color = "⚪"
            row.append(f"{color} {val}%")
        md += "| " + " | ".join(row) + " |\n\n"
        
        md += f"> [!code]- Click to view: it_{i}.py\n"
        md += f"> ```embed-python\n"
        md += f"> PATH: \"quantconnect/gemini/it_{i}.py\"\n"
        md += f"> ```\n\n"

    with open(output_file, "w") as f:
        f.write(md)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 generate_qc_report.py <raw_file> <output_file> <start_it> <end_it>")
    else:
        generate_qc_report(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
