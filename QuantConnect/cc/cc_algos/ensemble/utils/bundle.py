import os
import re
import sys
import warnings

# Suppress urllib3 NotOpenSSLWarning
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")

# ---------------------------------------------------------------------------
# Configurations
# ---------------------------------------------------------------------------

BASE_FILE = "/Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/utils/base.py"
ORCHESTRATOR_FILE = "/Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/utils/ultAlgo.py"
ALGOS_DIR = "/Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble"
OUTPUT_DIR = "/Users/daveli/Desktop/proj/QuantConnect/cc/cc_algos/ensemble/merged"

def detect_ensemble_files():
    """Finds NNN.py sub-algo files (those subclassing BaseSubAlgo) in ALGOS_DIR."""
    algo_files = []
    for fn in sorted(os.listdir(ALGOS_DIR)):
        if not re.fullmatch(r"\d{3}\.py", fn):
            continue
        fpath = os.path.join(ALGOS_DIR, fn)
        with open(fpath) as f:
            if re.search(r"class \w+\(BaseSubAlgo\)", f.read()):
                algo_files.append(fpath)
    return [BASE_FILE] + algo_files + [ORCHESTRATOR_FILE]

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
    #   python3 bundle.py                -> Bundles all NNN.py sub-algos + ultAlgo.py
    #   python3 bundle.py path/to/NNN.py -> Bundles base.py + NNN.py (Standalone)

    if len(sys.argv) > 1:
        # Mini-Bundle (Standalone) mode
        target_file = sys.argv[1]
        output_name = os.path.join(OUTPUT_DIR, "standalone.py")
        bundle([BASE_FILE, target_file], output_name)
    else:
        # Full Ensemble mode
        ensemble_files = detect_ensemble_files()
        output_name = os.path.join(OUTPUT_DIR, "ensemble.py")
        bundle(ensemble_files, output_name, ensemble=True)

if __name__ == "__main__":
    main()
