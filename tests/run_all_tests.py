import subprocess
import sys

test_scripts = [
    "tests/verify_project.py",
    "tests/verify_practical_6.py",
    "tests/verify_phase_3.py",
    "tests/verify_phase_4.py",
    "tests/verify_phase_5.py",
    "tests/verify_ui_ux.py",
    "tests/verify_product_redesign.py",
    "tests/verify_phase_remedy.py",
    "tests/verify_responsive_layout.py",
    "tests/verify_marksheet_and_event_fixes.py"
]

all_passed = True
print("=" * 70)
print("RUNNING ALL 10 TEST SUITES (PRACTICALS 1-12, REMEDY, LAYOUT & FIXES)")
print("=" * 70)

for script in test_scripts:
    res = subprocess.run([sys.executable, script], capture_output=True, text=True)
    status = "PASS" if res.returncode == 0 else "FAIL"
    print(f"[{status}] {script}")
    if res.returncode != 0:
        all_passed = False
        print("--- OUTPUT ---")
        print(res.stdout[-500:] if len(res.stdout) > 500 else res.stdout)
        print(res.stderr)
        print("--------------")

print("=" * 70)
if all_passed:
    print("ALL 10 TEST SUITES PASSED (100% SUCCESS)!")
    sys.exit(0)
else:
    print("SOME TEST SUITES FAILED.")
    sys.exit(1)
