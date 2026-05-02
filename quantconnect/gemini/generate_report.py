import re
import os
import sys

raw_file = "gemini/batch_stats_raw.txt"

def generate_report_page(start_it, end_it, output_file, it_data):
    # --- Generate Markdown ---
    md = f"# QuantConnect Community Research Master Ledger ({start_it}-{end_it})\n\n"
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
            
        if cagr >= 30 and dd <= 58:
            status = "✅ Pass"
        elif cagr < 30 and dd > 58:
            status = "❌ Fail"
        elif cagr < 30:
            status = "❌ Low Return"
        else:
            status = "❌ High DD"
            
        if i == 41: status = "✅🏆 CHAMP"
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
        md += f"> PATH: \"vault://QuantConnect/gemini/algos/it_{i}.py\"\n"
        md += f"> ```\n\n"

    with open(output_file, "w") as f:
        f.write(md)

def main():
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
        yearly_matches = re.findall(r"(\d{4}):\s+[🟢🔴⚪]\s+([-]?\d+)%", block)
        stats['Yearly'] = {y: r for y, r in yearly_matches}
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

    # Generate Paginated Reports
    generate_report_page(1, 50, "gemini/qc_forum_1.md", it_data)
    generate_report_page(51, 100, "gemini/qc_forum_2.md", it_data)
    print("Reports generated: gemini/qc_forum_1.md, gemini/qc_forum_2.md")

if __name__ == "__main__":
    main()

