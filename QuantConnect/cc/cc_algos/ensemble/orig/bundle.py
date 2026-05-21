import os
import re
import sys
import warnings

# Suppress urllib3 NotOpenSSLWarning
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")

# ---------------------------------------------------------------------------
# Configurations
# ---------------------------------------------------------------------------

BASE_FILE = "strategies/base.py"
ORCHESTRATOR_FILE = "strategies/ultAlgo.py"
ALGOS_DIR = "strategies/algos"
OUTPUT_DIR = "strategies/embedded"

def detect_ensemble_files():
    """Parses ultAlgo.py to find imported sub-algos and builds the file list."""
    if not os.path.exists(ORCHESTRATOR_FILE):
        print(f"Error: Orchestrator {ORCHESTRATOR_FILE} not found.")
        return [BASE_FILE, ORCHESTRATOR_FILE]

    with open(ORCHESTRATOR_FILE, "r") as f:
        content = f.read()

    # Find patterns like "from vol_breakout import ..."
    # We assume these files live in strategies/algos/
    imports = re.findall(r"^from\s+([\w_]+)\s+import", content, re.MULTILINE)
    
    # Filter out 'base' as it's handled separately
    sub_algos = [i for i in imports if i != "base" and i != "AlgorithmImports"]
    
    file_list = [BASE_FILE]
    for sa in sub_algos:
        sa_path = os.path.join(ALGOS_DIR, f"{sa}.py")
        if os.path.exists(sa_path):
            file_list.append(sa_path)
        else:
            print(f"Warning: Detected import '{sa}' but file not found at {sa_path}")
            
    file_list.append(ORCHESTRATOR_FILE)
    return file_list

def bundle(files, output_path, ensemble=False):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Bundling {len(files)} files into {output_path}...")
    bundled_content = "from AlgorithmImports import *\n\n"

    seen_files = set() # Prevent duplicates

    for fpath in files:
        if fpath in seen_files: continue
        if not os.path.exists(fpath):
            print(f"Warning: File not found {fpath}")
            continue

        seen_files.add(fpath)
        with open(fpath, "r") as f:
            content = f.read()
            content = re.sub(r"^from\s+.*?import\s+.*$", "", content, flags=re.MULTILINE)
            content = re.sub(r"^import\s+.*$", "", content, flags=re.MULTILINE)

            if ensemble:
                # Strip _make_standalone and standalone assignments — they create extra
                # QCAlgorithm subclasses that cause QC to run the wrong class.
                content = re.sub(
                    r"\n# -{10,}\n# Standalone mixin factory\n# -{10,}\n\ndef _make_standalone\b.*?\n    return Algo\n",
                    "\n", content, flags=re.DOTALL)
                content = re.sub(r"^\w+Algo\s*=\s*_make_standalone\(\w+\)\s*$", "", content, flags=re.MULTILINE)

            bundled_content += f"\n# --- Content from {fpath} ---\n"
            bundled_content += content + "\n"

    with open(output_path, "w") as f:
        f.write(bundled_content)
    print("Bundle complete.")

def main():
    # Usage: 
    #   python3 bundle.py                -> Dynamically bundles ensemble based on ultAlgo.py imports
    #   python3 bundle.py strategies/X.py -> Bundles base.py + X.py (Standalone)
    
    if len(sys.argv) > 1:
        # Mini-Bundle (Standalone) mode
        target_file = sys.argv[1]
        output_name = os.path.join(OUTPUT_DIR, "standalone.py")
        bundle([BASE_FILE, target_file], output_name)
    else:
        # Full Ensemble mode with Dynamic Detection
        ensemble_files = detect_ensemble_files()
        output_name = os.path.join(OUTPUT_DIR, "ensemble.py")
        bundle(ensemble_files, output_name, ensemble=True)

if __name__ == "__main__":
    main()
