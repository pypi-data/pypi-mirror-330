import numpy as np
import re

try:
    from sage_lib.master.FileManager import FileManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing FileManager: {str(e)}\n")
    del sys


class DOSManager(FileManager):
    """
    Class to manage and analyze Density of States (DOS) data from VASP's DOSCAR file.

    Inherits from FileManager and provides methods to read and parse total and partial DOS data.
    """

    def __init__(self, file_location: str = None, name: str = None, **kwargs):
        """
        Initialize DOSManager with optional file location and descriptive name.

        Parameters:
            file_location (str): Path to the DOSCAR file.
            name (str): Descriptive name for the DOS data set.
            **kwargs: Additional keyword arguments for the base FileManager.
        """
        super().__init__(name=name, file_location=file_location)
        self._spin_polarized = None  # To be determined based on DOS data
        self._dos_total = None       # Total DOS data
        self._dos_ion = []           # Partial DOS data for each ion
        self._fermi_energy = None
        self._atom_count = None
        self._NEDOS = None
        self._system_name = None
        self._E_max = None
        self._E_min = None

    @property
    def fermi_energy(self):
        """Returns the Fermi energy."""
        return self._fermi_energy

    @property
    def spin_polarized(self):
        """Indicates whether the calculation is spin-polarized."""
        return self._spin_polarized

    @property
    def dos_total(self):
        """Returns the total DOS data."""
        return self._dos_total

    @property
    def dos_ion(self):
        """Returns the partial DOS data for each ion."""
        return self._dos_ion

    def _fix_number_format(self, line):
        """
        Fixes the number format in a line by inserting 'E' where necessary.

        Parameters:
            line (str): A line from the DOSCAR file.

        Returns:
            str: The corrected line.
        """
        # Use regex to find numbers missing 'E' before the exponent
        corrected_line = re.sub(
            r'(\d+\.\d+)([\+\-]\d+)',  # Matches numbers like '1.2345-103'
            r'\1E\2',                  # Inserts 'E' between the mantissa and exponent
            line.strip()
        )
        return corrected_line

    def _read_total_dos(self, lines):
        """
        Reads and parses the total DOS data from the given lines.

        Parameters:
            lines (list): List of lines containing the total DOS data.

        Returns:
            dict: Dictionary with total DOS and integrated DOS data.
        """
        energies = []
        dos_up = []
        dos_down = []
        integrated_dos_up = []
        integrated_dos_down = []

        for line_number, line in enumerate(lines, start=1):
            original_line = line.strip()
            corrected_line = self._fix_number_format(original_line)
            try:
                values = list(map(float, corrected_line.strip().split()))
            except ValueError as e:
                print(f"Error parsing line {line_number}: {corrected_line}")
                raise e

            num_values = len(values)

            if num_values == 5:
                # Spin-polarized data
                self._spin_polarized = True
                energies.append(values[0])
                dos_up.append(values[1])
                dos_down.append(values[2])
                integrated_dos_up.append(values[3])
                integrated_dos_down.append(values[4])
            elif num_values == 3:
                # Non-spin-polarized data
                self._spin_polarized = False
                energies.append(values[0])
                dos_up.append(values[1])  # Using dos_up for total DOS
                integrated_dos_up.append(values[2])  # Using integrated_dos_up for integrated DOS
            else:
                # Unexpected format
                raise ValueError(f"Unexpected number of columns in total DOS: {num_values}")

        # Convert lists to NumPy arrays for efficiency
        dos_total = {
            'energies': np.array(energies),
            'dos_up': np.array(dos_up),
            'integrated_dos_up': np.array(integrated_dos_up)
        }

        if self._spin_polarized:
            dos_total['dos_down'] = np.array(dos_down)
            dos_total['integrated_dos_down'] = np.array(integrated_dos_down)

        return dos_total

    def _read_ion_dos(self, lines):
        """
        Reads and parses the partial DOS data for an individual ion.

        Parameters:
            lines (list): Lines containing the partial DOS data for an ion.

        Returns:
            dict: Dictionary with partial DOS data for an ion.
        """
        # The first line contains header information
        header = lines[0].strip()
        _, _, NEDOS, _, _ = map(float, header.split())
        NEDOS = int(NEDOS)

        # Initialize arrays for efficiency
        energies = []
        orbitals = {}

        # Determine orbitals based on spin polarization
        if self.spin_polarized:
            orbital_labels = [
                's_up', 's_down',
                'p_y_up', 'p_y_down',
                'p_z_up', 'p_z_down',
                'p_x_up', 'p_x_down',
                'd_xy_up', 'd_xy_down',
                'd_yz_up', 'd_yz_down',
                'd_z2r2_up', 'd_z2r2_down',
                'd_xz_up', 'd_xz_down',
                'd_x2y2_up', 'd_x2y2_down'
            ]
        else:
            orbital_labels = [
                's',
                'p_y', 'p_z', 'p_x',
                'd_xy', 'd_yz', 'd_z2r2', 'd_xz', 'd_x2y2'
            ]

        for label in orbital_labels:
            orbitals[label] = []

        for line in lines[1:]:
            line = self._fix_number_format(line)
            values = list(map(float, line.strip().split()))
            energies.append(values[0])

            for idx, label in enumerate(orbital_labels):
                orbitals[label].append(values[idx + 1])

        # Convert lists to NumPy arrays
        dos_ion = {'energies': np.array(energies)}
        for label in orbital_labels:
            dos_ion[label] = np.array(orbitals[label])

        return dos_ion

    def _read_ions_dos(self, lines):
        """
        Reads and parses the partial DOS data for all ions.

        Parameters:
            lines (list): Lines containing the partial DOS data for all ions.
        """
        # Each ion has NEDOS + 1 lines (header + data)
        ion_block_size = self._NEDOS + 1
        num_ions = self._atom_count

        for n in range(num_ions):
            start = ion_block_size * n
            end = start + ion_block_size
            ion_lines = lines[start:end]
            dos_ion = self._read_ion_dos(ion_lines)
            self._dos_ion.append(dos_ion)

    def _read_header(self, lines):
        """
        Reads and parses the header information from the DOSCAR file.

        Parameters:
            lines (list): First six lines of the file containing header information.
        """
        # First line: atom counts and flags
        tokens = lines[0].split()
        self._atom_count = int(tokens[1])
        self._partial_DOS = int(tokens[2])

        # Fifth line: system name
        self._system_name = lines[4].strip()

        # Sixth line: Emax, Emin, NEDOS, E_fermi, weight
        tokens = lines[5].split()
        self._E_max = float(tokens[0])
        self._E_min = float(tokens[1])
        self._NEDOS = int(float(tokens[2]))
        self._fermi_energy = float(tokens[3])

    def read_DOSCAR(self, file_location: str = None):
        """
        Loads the DOS data from a DOSCAR file.

        Reads the file, extracting header information, total DOS,
        and, if available, partial DOS for each ion.

        Parameters:
            file_location (str): Path to the DOSCAR file. Defaults to the initialized file location.

        Returns:
            bool: True if loading succeeds, False otherwise.
        """
        file_location = file_location if isinstance(file_location, str) else self._file_location
        if not file_location:
            raise ValueError("No file location provided for DOSCAR.")

        # Read all lines from the file
        with open(file_location, 'r') as f:
            lines = f.readlines()

        # Read header information
        self._read_header(lines[:6])

        # Read total DOS data
        total_dos_start = 6
        total_dos_end = total_dos_start + self._NEDOS
        self._dos_total = self._read_total_dos(lines[total_dos_start:total_dos_end])

        # Check if partial DOS is available
        if len(lines) > total_dos_end and self._partial_DOS == 1:
            # Read partial DOS for ions
            ion_dos_lines = lines[total_dos_end:]
            self._read_ions_dos(ion_dos_lines)

        return True

    # Additional methods for analysis and visualization can be added here

