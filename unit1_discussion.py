"""
===========================================================
Unit 1 DISCUSSION: Python OOP, Namespaces, and Copying
===========================================================

INSTRUCTIONS:
In this assignment, you will build and explore object-oriented programming (OOP) concepts in Python.
You are provided with starter code containing TODO sections. Your task is to complete, modify, and
analyze the code to demonstrate understanding of inheritance, namespaces, and object copying.
"""

from copy import copy, deepcopy


# TODO 1:
# Create a parent class.
#
# Requirements:
# - Include at least one class variable.
# - Include at least two instance variables.
# - Include a constructor (__init__).
# - Include a method that returns or displays information about the object.
#
# Replace the pass statement with your implementation.

class CalibrationStandard:
    """Parent class representing a metrology reference standard."""

    # Class variable: Shared facility location across all reference standards
    facility_location = "ETI Precision Standards Lab - Frederick, MD"
    standards_count = 0

    def __init__(self, asset_tag: str, model: str, tolerance_ppm: float):
        """Initialize core attributes with defensive boundary validation."""
        if not asset_tag or not isinstance(asset_tag, str):
            raise ValueError("Asset tag must be a non-empty string identifier.")
        if tolerance_ppm <= 0:
            raise ValueError("Measurement tolerance must be a positive non-zero value.")

        self.asset_tag = asset_tag
        self.model = model
        self.tolerance_ppm = tolerance_ppm
        # Nested mutable structure tracking calibration history
        self.calibration_history = ["Initial Baseline NIST Traceability Verification"]

        CalibrationStandard.standards_count += 1

    def log_verification(self, verification_note: str):
        """Append a verification record to the history log with validation."""
        if not verification_note or not isinstance(verification_note, str):
            raise ValueError("Verification note cannot be empty or invalid.")
        self.calibration_history.append(verification_note)

    def describe(self) -> str:
        """Display formatted telemetry describing the calibration standard."""
        return (
            f"[Standard] Asset: {self.asset_tag} | Model: {self.model} | "
            f"Tolerance: {self.tolerance_ppm} ppm | Log Count: {len(self.calibration_history)}"
        )


# TODO 2:
# Create a child class that inherits from the parent class.
#
# Requirements:
# - Use inheritance.
# - Add at least one new class variable.
# - Add at least two new instance variables.
# - Add at least one new method.
# - Override a method from the parent class.
#
# Replace the pass statement with your implementation.

class MultifunctionCalibrator(CalibrationStandard):
    """Child class inheriting from CalibrationStandard, modeling multifunction calibrators."""

    # New child class variable
    primary_domain = "Electrical & Temperature Calibration"

    def __init__(
        self,
        asset_tag: str,
        model: str,
        tolerance_ppm: float,
        max_voltage_output: float,
        firmware_version: str = "v4.2.1",
    ):
        """Initialize child attributes and delegate core setup to super().__init__()."""
        super().__init__(asset_tag, model, tolerance_ppm)

        if max_voltage_output <= 0:
            raise ValueError("Maximum voltage output must be a positive number.")

        # Two new instance variables
        self.max_voltage_output = max_voltage_output
        self.firmware_version = firmware_version

    def describe(self) -> str:
        """Override parent method to extend summary with hardware output limits."""
        base_summary = super().describe()
        return (
            f"{base_summary} | Max Voltage: {self.max_voltage_output}V | "
            f"Firmware: {self.firmware_version}"
        )

    def trigger_safety_interlock(self, target_voltage: float) -> bool:
        """New child method: Validate voltage request against hardware safety interlocks."""
        if target_voltage > self.max_voltage_output:
            raise ValueError(
                f"Safety Interlock Trip: Requested output ({target_voltage}V) exceeds "
                f"rated hardware limit ({self.max_voltage_output}V)!"
            )
        return True

    # Student-created extension (README Requirement 6)
    def export_telemetry_packet(self) -> dict:
        """Student Extension: Compile and return a telemetry packet dictionary."""
        return {
            "asset_tag": self.asset_tag,
            "model": self.model,
            "rated_tolerance": f"{self.tolerance_ppm} ppm",
            "max_voltage": f"{self.max_voltage_output}V",
            "firmware": self.firmware_version,
            "total_verifications": len(self.calibration_history),
            "latest_log": self.calibration_history[-1],
        }


# TODO 3:
# Create a function that demonstrates class namespaces and instance namespaces.
#
# Your function should:
# - Create at least two objects of the child class.
# - Access a class variable through the class itself.
# - Access the same class variable through an object.
# - Add a new attribute to only one object after it is created.
# - Display each object's namespace using __dict__.
# - Display information about the class namespace.

def demonstrate_namespaces():
    print("\n=== Namespace Demonstration ===")

    # Create two child objects
    cal_unit_a = MultifunctionCalibrator("CAL-5522A", "Fluke 5522A", 6.0, 1020.0)
    cal_unit_b = MultifunctionCalibrator("CAL-5730A", "Fluke 5730A", 3.5, 1100.0)

    # Access class variable through class and through an object
    print(f"Class variable accessed via Class:  {CalibrationStandard.facility_location}")
    print(f"Class variable accessed via Object: {cal_unit_a.facility_location}")

    # Add a new attribute to ONLY one object after creation
    cal_unit_a.bench_assignment = "RF & Low-Frequency Bench 02"

    print("\nObject cal_unit_a Namespace (__dict__):")
    print(f"  Includes dynamic 'bench_assignment': {cal_unit_a.__dict__}")

    print("\nObject cal_unit_b Namespace (__dict__):")
    print(f"  Unaffected by cal_unit_a's new attribute: {cal_unit_b.__dict__}")

    print("\nParent Class Namespace (Subset of CalibrationStandard.__dict__):")
    parent_ns = {k: v for k, v in CalibrationStandard.__dict__.items() if not k.startswith("__")}
    print(f"  {parent_ns}")


# TODO 4:
# Create a function that demonstrates shallow copying and deep copying.
#
# Requirements:
# - Create an object that contains nested mutable data.
# - Create a shallow copy.
# - Create a deep copy.
# - Modify the original object's nested data.
# - Display the original object, shallow copy, and deep copy.
# - Use comments to explain the difference between shallow and deep copying.

def demonstrate_copying():
    print("\n=== Copy Demonstration ===")

    # Original object containing nested mutable list: calibration_history
    primary_calibrator = MultifunctionCalibrator("CAL-PRIMARY", "Fluke 8508A", 2.0, 1000.0)
    primary_calibrator.log_verification("Q1 Laboratory Audit Passed")

    # Shallow Copy: Duplicates top-level object only.
    # The nested list 'calibration_history' is copied as a REFERENCE pointing to the same memory.
    shallow_clone = copy(primary_calibrator)

    # Deep Copy: Recursively duplicates top-level object AND all nested mutable objects.
    # The nested list 'calibration_history' receives its own completely independent memory space.
    deep_clone = deepcopy(primary_calibrator)

    # Modify the original object's nested data
    primary_calibrator.log_verification("CRITICAL: Out-of-Tolerance Voltage Spike Detected")

    print("\nPost-Mutation Inspection of Nested History Lists:")
    print(f"Original Object History:    {primary_calibrator.calibration_history}")
    print(f"Shallow Copy History:       {shallow_clone.calibration_history}")
    print(f"Deep Copy History:          {deep_clone.calibration_history}")

    # Identity check to verify memory references
    print("\nMemory Reference Verification ('is' operator):")
    is_shallow_same = primary_calibrator.calibration_history is shallow_clone.calibration_history
    is_deep_same = primary_calibrator.calibration_history is deep_clone.calibration_history
    print(f"Original list IS Shallow list reference? {is_shallow_same} (Shared mutable memory)")
    print(f"Original list IS Deep list reference?    {is_deep_same} (Isolated independent memory)")


# TODO 5:
# Complete the main function.
#
# Requirements:
# - Create at least one object from the parent class.
# - Create at least one object from the child class.
# - Demonstrate inheritance by calling methods.
# - Call your namespace demonstration function.
# - Call your copy demonstration function.

def main():
    print("=== Unit 1 OOP Assignment ===")

    print("\n--- 1. Testing Parent Class ---")
    base_standard = CalibrationStandard("STD-RES-10K", "IET HARS-X Standard Resistor", 1.5)
    print(base_standard.describe())

    print("\n--- 2. Testing Child Class & Inheritance ---")
    lab_calibrator = MultifunctionCalibrator(
        "CAL-MULTI-01", "Fluke 5522A Multi-Product", 6.0, 1020.0, "v5.0.2"
    )
    # Demonstrating overridden describe() method combining parent + child fields
    print(lab_calibrator.describe())

    # Demonstrating child-specific method
    print("\nTesting Hardware Safety Check (Valid: 500V):")
    if lab_calibrator.trigger_safety_interlock(500.0):
        print("  Safety Interlock: Request verified within operating limits.")

    # Demonstrating student-created extension (README Requirement 6)
    print("\nTesting Student Extension: export_telemetry_packet():")
    telemetry = lab_calibrator.export_telemetry_packet()
    for key, value in telemetry.items():
        print(f"  {key}: {value}")

    print("\n--- 3. Testing Edge Cases & Error Handling ---")
    # Edge Case 1: Interlock threshold violation
    try:
        print("Edge Case 1: Requesting 1500V (Exceeds 1020V limit)...")
        lab_calibrator.trigger_safety_interlock(1500.0)
    except ValueError as err:
        print(f"  [Handled Gracefully] {err}")

    # Edge Case 2: Blank asset tag initialization
    try:
        print("Edge Case 2: Instantiating standard with blank asset tag...")
        CalibrationStandard("", "Fluke 8846A", 10.0)
    except ValueError as err:
        print(f"  [Handled Gracefully] {err}")

    # Execute namespace and copying demonstrations
    demonstrate_namespaces()
    demonstrate_copying()


if __name__ == "__main__":
    main()
