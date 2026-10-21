from pathlib import Path
import subprocess, sys
ROOT = Path(__file__).resolve().parent
for script in [ROOT/"Component_A"/"run_component_a.py", ROOT/"Component_B"/"run_component_b.py"]:
    print(f"\n=== Running {script.relative_to(ROOT)} ===")
    subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)
print("\nFinished. See results/ and report/final_report.pdf.")
