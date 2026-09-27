"""
bill.py - Core calculation logic and data definitions for Electricity Bill Calculator.

This module defines:
1. Tariff slabs (tuple)
2. Fixed charges (dict)
3. Connection categories (set)
4. Phase options (frozenset)
5. Bitwise rebate flags and functions
6. ElectricityBill class (OOP)
"""

# Tuple of tariff slabs: (lower_limit, upper_limit, rate_per_unit)
# Note: upper_limit is None for the highest open-ended slab (above 300 units)
SLAB_RATES = (
    (0, 100, 2.0),
    (100, 200, 3.0),
    (200, 300, 5.0),
    (300, None, 7.0),
)

# Dictionary mapping connection category to fixed service charge
FIXED_CHARGES = {
    "DOMESTIC": 50.0,
    "COMMERCIAL": 100.0,
}

# Set of allowed connection categories for fast membership checking
VALID_CATEGORIES = {"DOMESTIC", "COMMERCIAL"}

# Frozenset of immutable phase connection options
VALID_PHASES = frozenset({"1-PHASE", "3-PHASE"})

# Bitwise flags for optional billing discounts
# FLAG_ONLINE_PAYMENT: bit 0 (value 1 = 0b01)
# FLAG_EARLY_PAYMENT:  bit 1 (value 2 = 0b10)
FLAG_ONLINE_PAYMENT = 1
FLAG_EARLY_PAYMENT = 2

# Discount amounts in Rupees corresponding to flags
REBATE_ONLINE = 15.0
REBATE_EARLY = 20.0


def calculate_energy_charge(units):
    """
    Calculate the tiered energy charge according to progressive slabs.
    Units are charged progressively across each tier.
    """
    charge = 0.0
    remaining_units = units

    for slab in SLAB_RATES:
        lower_limit = slab[0]
        upper_limit = slab[1]
        rate = slab[2]

        # Use identity operator 'is' to check for the final open slab (None)
        if upper_limit is None:
            if remaining_units > 0:
                slab_units = remaining_units
                charge += slab_units * rate
                remaining_units -= slab_units
        else:
            slab_capacity = upper_limit - lower_limit
            if remaining_units > 0:
                if remaining_units >= slab_capacity:
                    slab_units = slab_capacity
                else:
                    slab_units = remaining_units

                # Precedence: multiplication takes place before addition assignment
                charge += slab_units * rate
                remaining_units -= slab_units

    return charge


def calculate_fixed_charge(category):
    """
    Retrieve the fixed meter charge using dictionary lookup.
    """
    if category in FIXED_CHARGES:
        return FIXED_CHARGES[category]
    return 0.0


def calculate_rebate(rebate_flags):
    """
    Calculate total rebate using bitwise AND (&) to inspect rebate flags.
    Demonstrates legitimate bitwise flag masking.
    """
    total_rebate = 0.0

    # Check if online payment bit is set
    if (rebate_flags & FLAG_ONLINE_PAYMENT) != 0:
        total_rebate += REBATE_ONLINE

    # Check if early payment bit is set
    if (rebate_flags & FLAG_EARLY_PAYMENT) != 0:
        total_rebate += REBATE_EARLY

    return total_rebate


class ElectricityBill:
    """
    Beginner-level class representing an electricity consumer bill.
    Contains standard attributes and simple methods.
    Strictly avoids __str__ or advanced magic methods.
    """

    def __init__(self, consumer_name, consumer_id, category, phase, units, rebate_flags=0):
        # Plain attributes
        self.consumer_name = consumer_name
        self.consumer_id = consumer_id
        self.category = category
        self.phase = phase
        self.units = units
        self.rebate_flags = rebate_flags

        # Calculation result attributes
        self.energy_charge = 0.0
        self.fixed_charge = 0.0
        self.rebate_amount = 0.0
        self.total_bill = 0.0

    def calculate(self):
        """
        Perform all calculations for the electricity bill.
        Demonstrates arithmetic operator precedence and assignment operators.
        """
        self.energy_charge = calculate_energy_charge(self.units)
        self.fixed_charge = calculate_fixed_charge(self.category)
        self.rebate_amount = calculate_rebate(self.rebate_flags)

        # Precedence: addition within parentheses, then subtraction
        gross_amount = self.energy_charge + self.fixed_charge
        self.total_bill = gross_amount - self.rebate_amount

        # Guard: bill should not be negative
        if self.total_bill < 0.0:
            self.total_bill = 0.0

    def get_summary_dict(self):
        """
        Return bill details in a standard dictionary for reporting and display.
        """
        summary = {
            "consumer_name": self.consumer_name,
            "consumer_id": self.consumer_id,
            "category": self.category,
            "phase": self.phase,
            "units": self.units,
            "energy_charge": self.energy_charge,
            "fixed_charge": self.fixed_charge,
            "rebate_amount": self.rebate_amount,
            "total_bill": self.total_bill,
        }
        return summary
