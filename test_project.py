"""
test_project.py - Pure Python assert-based verification for Electricity Bill Calculator.

Zero external frameworks (no unittest, no pytest).
Run command:
    python tests/test_project.py
"""

import os
import sys

# Add parent directory to path to allow importing bill and main
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from bill import (
    calculate_energy_charge,
    calculate_fixed_charge,
    calculate_rebate,
    ElectricityBill,
    FLAG_ONLINE_PAYMENT,
    FLAG_EARLY_PAYMENT,
    VALID_CATEGORIES,
    VALID_PHASES,
)
from main import is_valid_positive_number


def test_slab_calculations():
    print("Testing slab rate calculations...")

    # Boundary 0 units
    assert calculate_energy_charge(0) == 0.0, "Charge for 0 units must be 0.0"

    # Within Slab 1 (0-100 @ Rs 2/unit)
    assert calculate_energy_charge(50) == 100.0, "50 units @ Rs 2 = 100.0"
    assert calculate_energy_charge(100) == 200.0, "100 units @ Rs 2 = 200.0"

    # Within Slab 2 (101-200 @ Rs 3/unit)
    # 150 units: 100*2 + 50*3 = 200 + 150 = 350.0
    assert calculate_energy_charge(150) == 350.0, "150 units must equal 350.0"
    # 200 units: 100*2 + 100*3 = 200 + 300 = 500.0
    assert calculate_energy_charge(200) == 500.0, "200 units must equal 500.0"

    # Within Slab 3 (201-300 @ Rs 5/unit)
    # 250 units: 200 + 300 + 50*5 = 750.0
    assert calculate_energy_charge(250) == 750.0, "250 units must equal 750.0"
    # 300 units: 200 + 300 + 100*5 = 1000.0
    assert calculate_energy_charge(300) == 1000.0, "300 units must equal 1000.0"

    # Within Slab 4 (Above 300 @ Rs 7/unit)
    # 350 units: 1000 + 50*7 = 1350.0
    assert calculate_energy_charge(350) == 1350.0, "350 units must equal 1350.0"

    print("  [PASS] Slab rate tests passed.")


def test_fixed_charges():
    print("Testing fixed charges lookup...")
    assert calculate_fixed_charge("DOMESTIC") == 50.0, "Domestic charge should be 50.0"
    assert calculate_fixed_charge("COMMERCIAL") == 100.0, "Commercial charge should be 100.0"
    assert calculate_fixed_charge("OTHER") == 0.0, "Unknown category should be 0.0"
    print("  [PASS] Fixed charges tests passed.")


def test_bitwise_rebates():
    print("Testing bitwise rebate calculations...")
    # No rebate
    assert calculate_rebate(0) == 0.0, "Flags = 0 should give 0.0 rebate"

    # Online payment only (bit 0 = 1) -> Rs 15
    assert calculate_rebate(FLAG_ONLINE_PAYMENT) == 15.0, "Online rebate should be 15.0"

    # Early payment only (bit 1 = 2) -> Rs 20
    assert calculate_rebate(FLAG_EARLY_PAYMENT) == 20.0, "Early payment rebate should be 20.0"

    # Combined using bitwise OR (1 | 2 = 3) -> Rs 35
    combined_flags = FLAG_ONLINE_PAYMENT | FLAG_EARLY_PAYMENT
    assert calculate_rebate(combined_flags) == 35.0, "Combined rebate should be 35.0"

    print("  [PASS] Bitwise rebate tests passed.")


def test_electricity_bill_class():
    print("Testing ElectricityBill class...")
    # Domestic consumer with 150 units, online payment rebate (Rs 15)
    bill1 = ElectricityBill("Alice", "EB-101", "DOMESTIC", "1-PHASE", 150.0, FLAG_ONLINE_PAYMENT)
    bill1.calculate()

    # Energy: 350.0, Fixed: 50.0, Rebate: 15.0 -> Total: 385.0
    assert bill1.energy_charge == 350.0, "Energy charge mismatch"
    assert bill1.fixed_charge == 50.0, "Fixed charge mismatch"
    assert bill1.rebate_amount == 15.0, "Rebate amount mismatch"
    assert bill1.total_bill == 385.0, "Total bill mismatch: expected 385.0"

    summary = bill1.get_summary_dict()
    assert summary["consumer_name"] == "Alice"
    assert summary["total_bill"] == 385.0

    # Commercial consumer with 350 units, early payment rebate (Rs 20)
    bill2 = ElectricityBill("Apex Corp", "EB-501", "COMMERCIAL", "3-PHASE", 350.0, FLAG_EARLY_PAYMENT)
    bill2.calculate()

    # Energy: 1350.0, Fixed: 100.0, Rebate: 20.0 -> Total: 1430.0
    assert bill2.energy_charge == 1350.0, "Energy charge mismatch"
    assert bill2.fixed_charge == 100.0, "Fixed charge mismatch"
    assert bill2.rebate_amount == 20.0, "Rebate amount mismatch"
    assert bill2.total_bill == 1430.0, "Total bill mismatch: expected 1430.0"

    print("  [PASS] ElectricityBill class tests passed.")


def test_input_validation():
    print("Testing input validation helper (without try/except)...")
    # Valid positive numbers
    assert is_valid_positive_number("100") is True
    assert is_valid_positive_number("120.50") is True
    assert is_valid_positive_number("0") is True
    assert is_valid_positive_number("0.75") is True

    # Invalid cases
    assert is_valid_positive_number("-10") is False
    assert is_valid_positive_number("abc") is False
    assert is_valid_positive_number("12.34.56") is False
    assert is_valid_positive_number("") is False
    assert is_valid_positive_number("   ") is False
    assert is_valid_positive_number(".") is False

    print("  [PASS] Input validation helper tests passed.")


def test_membership_and_data_structures():
    print("Testing membership and set/frozenset definitions...")
    assert "DOMESTIC" in VALID_CATEGORIES
    assert "COMMERCIAL" in VALID_CATEGORIES
    assert "INVALID" not in VALID_CATEGORIES

    assert "1-PHASE" in VALID_PHASES
    assert "3-PHASE" in VALID_PHASES
    assert "2-PHASE" not in VALID_PHASES

    print("  [PASS] Membership and constants tests passed.")


def run_all_tests():
    print("==================================================")
    print("    RUNNING PURE ASSERT-BASED TESTS FOR BILLING   ")
    print("==================================================")

    test_slab_calculations()
    test_fixed_charges()
    test_bitwise_rebates()
    test_electricity_bill_class()
    test_input_validation()
    test_membership_and_data_structures()

    print("==================================================")
    print("    ALL TESTS PASSED SUCCESSFULLY! (100% OK)     ")
    print("==================================================")


if __name__ == "__main__":
    run_all_tests()
