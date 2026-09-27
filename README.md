# Electricity Bill Calculator

A beginner-friendly, modular command-line application built in Python to calculate electricity bills using progressive slab tariffs, fixed connection charges, and payment rebates.

---

## 1. Project Title
**Electricity Bill Calculator (Console Edition)**

## 2. Project Description
The Electricity Bill Calculator is an academic Python project developed for the *Python Essentials* curriculum. It simulates the billing engine of an electric utility company. The application prompts for consumer information (name, consumer ID, connection category, supply phase, units consumed, and payment rebate options), validates user inputs without using exception handling, applies progressive tiered tariffs, and prints a formatted bill receipt. It also maintains a session history using core Python data structures and calculates session statistics such as average consumption.

## 3. Objective
- To implement a practical, real-world utility problem using core Python fundamentals.
- To demonstrate progressive tariff slab logic using arithmetic operators and loops.
- To showcase clean coding, proper function modularity, and beginner-level Object-Oriented Programming (OOP).
- To adhere strictly to syllabus topics while avoiding advanced frameworks, databases, or external libraries.

## 4. Features
- **Progressive Slab Rate Calculation:** Units are charged across tiered slabs rather than a single flat rate.
- **Connection Category Support:** Supports Domestic and Commercial tariff profiles with corresponding fixed charges.
- **Legitimate Bitwise Payment Rebates:** Uses bitwise flags (`&`, `|`) to calculate discounts for online and early bill payments.
- **Input Validation Without Exception Handling:** Validates numeric strings and menu selections using loops, relational checks, and membership operators (`in`, `not in`).
- **Session History & Analytics:** Tracks total bills in a `list` and numerical consumptions in an `array` (`array('d')`) to report session averages and total revenue.
- **Pure Assert-Based Test Suite:** Verified using plain Python `assert` statements without external test runners.

## 5. Technologies Used
- **Language:** Python 3.8+
- **Environment:** Terminal / Command Prompt / PowerShell
- **Libraries:** Python Standard Library only (`array`, `sys`, `os`)
- **External Dependencies:** None (Zero third-party packages)

## 6. Python Concepts Used
This project specifically applies topics from the *Python Essentials* course:
1. **Python Fundamentals:** Standard variable naming, comments, script execution.
2. **Membership Operators (`in`, `not in`):** Validating category choices in `VALID_CATEGORIES` and inspecting numeric characters in input strings.
3. **Assignment Operators (`=`, `+=`, `-=`):** Accumulating progressive slab costs and deducting rebates.
4. **Bitwise Operators (`&`, `|`):** Combining rebate options (`|`) and checking discount entitlement (`&`).
5. **`type()` Function:** Inspecting and demonstrating data types of containers and numeric totals.
6. **Identity Operators (`is`, `is not`):** Checking for `None` in the open-ended slab definition (`slab[1] is None`).
7. **Arithmetic Operators (`+`, `-`, `*`, `/`, `//`, `%`):** Tiered rate multiplication, floor division `//` and modulo `%` for Rupees/Paise split, and float division `/` for average usage.
8. **Logical Operators (`and`, `or`, `not`):** Loop guards (`while not is_valid:`) and slab range evaluations.
9. **Relational Operators (`<`, `>`, `<=`, `>=`, `==`, `!=`):** Comparing units against slab thresholds.
10. **Division of Mixed Data Types:** Demonstrating integer vs. float division behavior.
11. **Input/Output Operations:** `input()` prompts and formatted `print()` receipt generation.
12. **Precedence and Associativity:** Calculating net amounts: `(energy_charge + fixed_charge) - rebate_amount`.
13. **Type Conversion:** Converting validated strings with `float()` and `int()`.
14. **Core Data Structures:**
    - `tuple`: Fixed tariff slabs.
    - `dict`: Fixed service charges and receipt summaries.
    - `set`: Fast membership validation for consumer categories.
    - `frozenset`: Immutable phase choices (`{"1-PHASE", "3-PHASE"}`).
    - `list`: Storing session bill objects.
15. **Array Data Structure (`array('d')`):** Storing numerical unit consumption values for session reporting.
16. **Control Flow:** `while` loops for input loops/menus, `for` loops for slabs, and `if/elif/else` branches.
17. **Functions:** Modular functions with distinct parameters and return values.
18. **Modules:** Separation of calculation logic (`bill.py`) from user interaction (`main.py`).
19. **Object-Oriented Programming (OOP):** `ElectricityBill` class with ordinary attributes and methods, strictly avoiding magic methods beyond `__init__`.

## 7. Project Structure
```text
electricity_bill_calculator/
│
├── main.py                  # User interface, input loops, session summary
├── bill.py                  # Slab definitions, calculation functions, ElectricityBill class
├── tests/
│   └── test_project.py      # Plain assert-based unit tests
├── requirements.txt         # Standard library declaration (no external dependencies)
└── README.md                # Comprehensive documentation
```

## 8. Requirements
- Python 3.8 or newer installed on Windows, macOS, or Linux.
- No external packages needed (`pip install` is not required).

## 9. Installation & Setup Instructions
1. Clone or copy the project files to your local system:
   ```bash
   cd electricity_bill_calculator
   ```
2. Verify Python is installed:
   ```bash
   python --version
   ```

## 10. How to Run from Terminal
To start the interactive program:
```bash
python main.py
```

To run the verification test suite:
```bash
python tests/test_project.py
```

## 11. Sample Input
When running Option 1 (*Calculate New Electricity Bill*):
- **Consumer Name:** Rahul Sharma
- **Consumer ID:** EB-2041
- **Category:** 1 (Domestic)
- **Phase:** 1 (1-PHASE)
- **Units Consumed (kWh):** 175
- **Online Payment? (y/n):** y
- **Early Payment? (y/n):** y

## 12. Sample Output
```text
==================================================
         ELECTRICITY BILL RECEIPT
==================================================
  Consumer Name   : Rahul Sharma
  Consumer ID     : EB-2041
  Category        : DOMESTIC
  Supply Phase    : 1-PHASE
  Units Consumed  : 175.0 kWh
--------------------------------------------------
  Energy Charge   : Rs. 425.0
  Fixed Charge    : Rs. 50.0
  Rebate Discount : Rs. -35.0
--------------------------------------------------
  TOTAL PAYABLE   : Rs. 440.0
  (Breakdown      : 440 Rupees and 0 Paise)
==================================================
```

## 13. How the Bill is Calculated
For a consumer using **175 units** under Domestic category:
1. **Tiered Energy Charge:**
   - **First 100 units** (0 to 100) @ ₹2.00/unit:
     $$100 \times 2.00 = ₹200.00$$
   - **Next 75 units** (101 to 175) @ ₹3.00/unit:
     $$75 \times 3.00 = ₹225.00$$
   - **Subtotal Energy Charge:** $200.00 + 225.00 = ₹425.00$
2. **Fixed Service Charge:**
   - Domestic connection fixed charge = ₹50.00
3. **Rebates (Bitwise Flags):**
   - Online Payment Rebate = ₹15.00 (Bit 1)
   - Early Payment Rebate = ₹20.00 (Bit 2)
   - Total Rebate = $15.00 + 20.00 = ₹35.00$
4. **Net Total Bill:**
   $$\text{Total} = (425.00 + 50.00) - 35.00 = ₹440.00$$

## 14. Limitations
- Runs in a single console session; data is stored in memory and is not saved to disk after the program exits.
- Supports linear progressive slabs without time-of-day (peak/off-peak) metering.
- Input validation relies purely on character inspections and loop checks rather than regex or exception handling.

## 15. Future Improvements
- Add persistent storage using simple text or CSV files.
- Support commercial time-of-day tariffs and commercial power-factor surcharges.
- Add multi-language receipt printing.
