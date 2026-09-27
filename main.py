"""
main.py - Interactive Terminal Application for Electricity Bill Calculator.

This program guides the user through entering consumer details,
validating inputs without exception handling (using loops and membership checks),
calculating progressive slab rates, tracking sessions with an array data structure,
and presenting formatted receipts.
"""

from array import array
from bill import (
    ElectricityBill,
    SLAB_RATES,
    VALID_CATEGORIES,
    VALID_PHASES,
    FLAG_ONLINE_PAYMENT,
    FLAG_EARLY_PAYMENT,
)


def is_valid_positive_number(text):
    """
    Validate whether a string represents a valid non-negative float.
    Uses only membership operators ('in', 'not in'), relational operators,
    and control flow statements. Strictly avoids try/except.
    """
    clean_text = text.strip()
    if len(clean_text) == 0:
        return False

    decimal_count = 0
    digit_count = 0

    for char in clean_text:
        if char == ".":
            decimal_count += 1
        elif char in "0123456789":
            digit_count += 1
        else:
            # Character is neither a digit nor a decimal point
            return False

    # A valid positive number must have at least one digit and at most one decimal point
    if decimal_count > 1 or digit_count == 0:
        return False

    return True


def input_non_empty_string(prompt):
    """
    Prompt the user repeatedly until a non-empty string is provided.
    """
    is_valid = False
    result = ""

    while not is_valid:
        raw_val = input(prompt).strip()
        if len(raw_val) > 0:
            result = raw_val
            is_valid = True
        else:
            print("  [!] Input cannot be empty. Please try again.")

    return result


def input_positive_float(prompt):
    """
    Prompt the user repeatedly until a valid positive float number is provided.
    """
    is_valid = False
    result = 0.0

    while not is_valid:
        user_text = input(prompt).strip()
        if is_valid_positive_number(user_text):
            result = float(user_text)  # Safe type conversion
            is_valid = True
        else:
            print("  [!] Invalid number. Please enter a positive numerical value.")

    return result


def input_category():
    """
    Prompt user for category and validate using membership in VALID_CATEGORIES set.
    """
    print("\n  Select Connection Category:")
    print("  1. DOMESTIC")
    print("  2. COMMERCIAL")

    is_valid = False
    chosen_category = ""

    while not is_valid:
        choice = input("  Enter category option (1 or 2): ").strip()
        if choice == "1":
            chosen_category = "DOMESTIC"
        elif choice == "2":
            chosen_category = "COMMERCIAL"
        else:
            print("  [!] Invalid selection. Please enter 1 or 2.")
            continue

        # Membership operator check on set
        if chosen_category in VALID_CATEGORIES:
            is_valid = True

    return chosen_category


def input_phase():
    """
    Prompt user for phase and validate using membership in VALID_PHASES frozenset.
    """
    print("\n  Select Connection Phase:")
    print("  1. 1-PHASE (Standard residential)")
    print("  2. 3-PHASE (High load / Commercial)")

    is_valid = False
    chosen_phase = ""

    while not is_valid:
        choice = input("  Enter phase option (1 or 2): ").strip()
        if choice == "1":
            chosen_phase = "1-PHASE"
        elif choice == "2":
            chosen_phase = "3-PHASE"
        else:
            print("  [!] Invalid selection. Please enter 1 or 2.")
            continue

        # Membership operator check on frozenset
        if chosen_phase in VALID_PHASES:
            is_valid = True

    return chosen_phase


def input_rebates():
    """
    Prompt user for payment rebates and combine flags using bitwise OR (|).
    """
    flags = 0  # 00 in binary

    print("\n  Rebate & Discount Options:")

    # Online payment prompt
    online_ans = input("  Is this payment being made online? (y/n): ").strip().lower()
    if online_ans == "y" or online_ans == "yes":
        # Bitwise OR assignment to set the online payment bit
        flags = flags | FLAG_ONLINE_PAYMENT

    # Early payment prompt
    early_ans = input("  Is the payment made before the due date? (y/n): ").strip().lower()
    if early_ans == "y" or early_ans == "yes":
        # Bitwise OR assignment to set the early payment bit
        flags = flags | FLAG_EARLY_PAYMENT

    return flags


def display_bill_receipt(summary):
    """
    Display a formatted bill receipt from a dictionary.
    Demonstrates floor division (//), modulo (%), and type() function.
    """
    total = summary["total_bill"]

    # Floor division and modulo to break down rupees and paise
    rupees_part = int(total // 1)
    paise_part = int(round((total % 1) * 100))

    print("\n" + "=" * 50)
    print("         ELECTRICITY BILL RECEIPT")
    print("=" * 50)
    print("  Consumer Name   : " + str(summary["consumer_name"]))
    print("  Consumer ID     : " + str(summary["consumer_id"]))
    print("  Category        : " + str(summary["category"]))
    print("  Supply Phase    : " + str(summary["phase"]))
    print("  Units Consumed  : " + str(summary["units"]) + " kWh")
    print("-" * 50)
    print("  Energy Charge   : Rs. " + str(round(summary["energy_charge"], 2)))
    print("  Fixed Charge    : Rs. " + str(round(summary["fixed_charge"], 2)))
    print("  Rebate Discount : Rs. -" + str(round(summary["rebate_amount"], 2)))
    print("-" * 50)
    print("  TOTAL PAYABLE   : Rs. " + str(round(total, 2)))
    print("  (Breakdown      : " + str(rupees_part) + " Rupees and " + str(paise_part) + " Paise)")
    print("=" * 50)


def display_slab_table():
    """
    Display the active tariff slab rates to inform the user.
    Iterates over the SLAB_RATES tuple.
    """
    print("\n--- Current Tariff Slab Rates ---")
    for slab in SLAB_RATES:
        lower = slab[0]
        upper = slab[1]
        rate = slab[2]
        if upper is None:
            print("  Above " + str(lower) + " units: Rs. " + str(rate) + " per unit")
        else:
            print("  " + str(lower) + " - " + str(upper) + " units: Rs. " + str(rate) + " per unit")
    print("---------------------------------")


def display_session_summary(bills_list, units_array):
    """
    Display end-of-session statistics using the list of bills
    and the array of unit consumptions.
    Demonstrates mixed-type division and type() inspection.
    """
    total_bills_count = len(bills_list)

    if total_bills_count == 0:
        print("\n  [i] No bills have been calculated in this session yet.")
        return

    # Calculate total units using the array
    total_units_consumed = 0.0
    for u in units_array:
        total_units_consumed += u

    # Mixed data type division: float total divided by integer count
    average_units = total_units_consumed / total_bills_count

    total_revenue = 0.0
    for bill in bills_list:
        total_revenue += bill.total_bill

    print("\n" + "=" * 55)
    print("              SESSION SUMMARY REPORT")
    print("=" * 55)
    print("  Total Bills Calculated  : " + str(total_bills_count))
    print("  Total Units Billed      : " + str(round(total_units_consumed, 2)) + " kWh")
    print("  Average Consumption     : " + str(round(average_units, 2)) + " kWh")
    print("  Total Billed Revenue    : Rs. " + str(round(total_revenue, 2)))
    print("-" * 55)
    print("  [Academic Note on Data Types & Structures]")
    print("  • Bills Container Type  : " + type(bills_list).__name__)
    print("  • Units Container Type  : " + type(units_array).__name__ + " ('d' double float)")
    print("  • Total Bill Data Type  : " + type(total_revenue).__name__)
    print("=" * 55)


def main():
    """
    Main application loop for Electricity Bill Calculator.
    """
    print("==================================================")
    print("     WELCOME TO ELECTRICITY BILL CALCULATOR       ")
    print("         Academic Python Essentials Project       ")
    print("==================================================")

    # Core data structures for tracking the current session
    bills_history = []  # List of ElectricityBill objects
    units_history = array("d", [])  # Array storing float consumption numbers

    keep_running = True

    while keep_running:
        print("\nMain Menu:")
        print("1. Calculate New Electricity Bill")
        print("2. View Tariff Slab Information")
        print("3. View Session Summary & History")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            print("\n--- Enter Consumer Details ---")
            name = input_non_empty_string("  Enter Consumer Name: ")
            consumer_id = input_non_empty_string("  Enter Consumer ID (e.g., EB-1001): ")
            category = input_category()
            phase = input_phase()
            units = input_positive_float("  Enter Units Consumed (kWh): ")
            rebate_flags = input_rebates()

            # Create an instance of ElectricityBill (OOP)
            bill = ElectricityBill(
                consumer_name=name,
                consumer_id=consumer_id,
                category=category,
                phase=phase,
                units=units,
                rebate_flags=rebate_flags,
            )

            # Perform calculation
            bill.calculate()

            # Record in session data structures
            bills_history.append(bill)
            units_history.append(units)

            # Display generated bill
            summary = bill.get_summary_dict()
            display_bill_receipt(summary)

        elif choice == "2":
            display_slab_table()

        elif choice == "3":
            display_session_summary(bills_history, units_history)

        elif choice == "4":
            keep_running = False
            print("\nThank you for using Electricity Bill Calculator. Goodbye!")

        else:
            print("  [!] Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
