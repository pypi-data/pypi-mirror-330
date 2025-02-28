"""
sage_lib - A Python package for advanced scientific simulations and data processing in computational physics and materials science.

This package provides functionalities for managing and automating computational tasks in physics and materials science simulations, particularly focusing on density functional theory (DFT) and force-field based calculations. It aids in the setup, execution, and analysis of simulation results.

Modules and Their Functions:
1. output: Handles the output data from simulations, including processing and visualization tools. Contains modules like EigenvalueFileManager for managing eigenvalue data, DOSManager for density of states calculations, and WaveFileManager and ChargeFileManager for managing wavefunction and charge density data respectively.

2. single_run: Manages individual simulation runs. Includes SingleRun for handling single instance simulations, SingleRunDFT for specific DFT calculations, and SingleRunManager for orchestrating these simulations.

3. input: Responsible for setting up simulation parameters and input files. Includes KPointsManager for k-point sampling setup, PotentialManager for potential energy configurations, and various tools for handling different input file types (InputDFT, InputClassic, etc.).

4. ensemble: Manages ensemble simulations, providing tools for running multiple simulations in parallel or in sequence. Includes FFEnsembleManager for force-field based ensemble simulations and DFTEnsemble for DFT-based ones.

5. partition: Offers functionalities for dividing simulations into smaller, manageable parts or for running specific types of simulations (e.g., VacuumStates_builder, Crystal_builder).

6. master: Contains core functionalities and utilities used across the package, like FileManager for general file management and AtomicProperties for handling atomic-level properties.

7. miscellaneous: A collection of various tools and utilities that support the main functionalities of the package.

8. build: Contains the compiled Python files ready for distribution and installation.

Each module is designed to work independently or in conjunction with others, providing a comprehensive toolkit for conducting and managing complex scientific simulations.
"""


"""
Examples:
    # Generate XYZ from OUTCAR
    generate_from_outcar("/path/to/OUTCAR", source='VASP', subfolders=True, verbose=True)

    # Generate configurations with vacancies
    generate_vacancy("/path/to/VASP_files")

    # Generate configurations for disassembling a surface
    generate_disassemble_surface("/path/to/VASP_files", steps=5, final_distance=10.0)

    # Generate dimer configurations
    generate_dimers("/path/to/VASP_files", labels=['C', 'O'], steps=10, vacuum=15.0)

    # Generate VASP partition and execution script
    generate_config("/path/to/VASP_files", config_path="/path/to/config", output_path="/path/to/output")

    # Generate band calculation files
    generate_band_calculation("/path/to/VASP_files", points=100, special_points='GMMLLXXG')

Note:
    - The 'sage_lib' package is primarily designed for use with VASP simulation data.
    - It is recommended to have a thorough understanding of DFT and materials simulation before using this package.
    - Ensure all paths provided to the functions are absolute paths.

Attributes:
    - Comprehensive support for various stages of simulation: setup, execution, and analysis.
    - Integration with VASP for efficient management of simulation data.
    - Versatile tools for creating, modifying, and analyzing simulation data.

Todo:
    - Expand support for other simulation software beyond VASP.
    - Implement more advanced data analysis tools for post-simulation analysis.
    - Enhance the user interface for ease of use in an interactive environment.

Authors:
    Dr. Juan Manuel Lombardi
    Fritz-Haber-Institut der Max-Planck-Gesellschaft
    Contact: lombardi@fhi-berlin.mpg.de
"""

# ==== Import statements for key modules ==== # 
"""
sage_lib - Advanced Scientific Simulations and Data Processing

This package provides tools for setting up, executing, and analyzing simulations in computational physics and materials science, focusing on DFT and force-field methods.

Modules:
- `partition`: Core functionalities for managing simulation partitions and configurations.
- `IO`: Tools for handling input/output files, including atomic positions, eigenvalues, and DOS data.
- `single_run`: Manage individual simulation runs.
- `ensemble`: Tools for ensemble simulations.
- `miscellaneous`: General-purpose utilities and tools.
- `test`: Testing tools for validating implementations.
"""

# === Metadata ===
__version__ = "0.1.5.26"
__author__ = "Dr. Juan Manuel Lombardi"
__license__ = "MIT"

# === Key Imports ===
#from .partition.Partition import Partition
#from .IO.structure_handling_tools.AtomPosition import AtomPosition
#from .IO.EigenvalueFileManager import EigenvalueFileManager
#from .IO.DOSManager import DOSManager
#from .IO.OutFileManager import OutFileManager

# === High-Level API Functions ===
# Import main script functionality for ease of use
'''
from .main import (
    generate_test,
    generate_export_files,
    generate_plot,
    generate_AbInitioThermodynamics,
    generate_BLENDER,
    generate_config,
    generate_edit_positions,
    generate_MD,
    generate_defects,
    generate_disassemble_surface,
    generate_dimers,
    generate_band_calculation,
    generate_json_from_bands,
    generate_edit_configuration,
    generate_filter,
    generate_dataset,
    generate_solvent,
    generate_conductivity,
)
'''

# === Simplified Access to Common Tools ===
# Alias commonly used classes or tools for convenience
'''
PartitionManager = Partition
AtomHandler = AtomPosition
EigenvalueHandler = EigenvalueFileManager
DOSHandler = DOSManager
OutFileHandler = OutFileManager
'''

# === Initialization Function ===
def initialize_sage_lib(verbose: bool = False):
    """
    Initialize the Sage library with optional configurations.

    Parameters:
    - verbose (bool): If True, prints initialization details.
    """
    if verbose:
        print(f"Initializing Sage Library (v{__version__}) - Advanced tools for materials science simulations.")

# === Define Public API ===
__all__ = [
    # High-level functions
    "generate_test",
    "generate_export_files",
    "generate_plot",
    "generate_AbInitioThermodynamics",
    "generate_BLENDER",
    "generate_config",
    "generate_edit_positions",
    "generate_MD",
    "generate_defects",
    "generate_disassemble_surface",
    "generate_dimers",
    "generate_band_calculation",
    "generate_json_from_bands",
    "generate_edit_configuration",
    "generate_filter",
    "generate_dataset",
    "generate_solvent",
    "generate_conductivity",

    # Common tools
    "PartitionManager",
    "AtomHandler",
    "EigenvalueHandler",
    "DOSHandler",
    "OutFileHandler",

    # Initialization
    "initialize_sage_lib",
]


# Any initialization code your package requires 
global_seed = 42

# Si desea controlar qué se importa con "from sage_lib import *"
#__all__ = ["Partition", "OutFileManager", "DFTSingleRun", "CrystalDefectGenerator"]

# Código de inicialización, si es necesario
def initialize_sage_lib():
    print("Inicializando sage_lib...")


# Version of the sage_lib package
__version__ = "0.1.2.3"

# Author of the package
__author__ = "[Your Name]"

# License of the package
__license__ = "[License Type]"

# End of __init__.py
