try:
    from sage_lib.partition.partition_builder.BandStructure_builder import BandStructure_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing BandStructure_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.Config_builder import Config_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Config_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.Crystal_builder import Crystal_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Crystal_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.CrystalDefect_builder import CrystalDefect_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing CrystalDefect_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.Molecule_builder import Molecule_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Molecule_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.PositionEditor_builder import PositionEditor_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PositionEditor_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.SurfaceStates_builder import SurfaceStates_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing SurfaceStates_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.VacuumStates_builder import VacuumStates_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing VacuumStates_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.Filter_builder import Filter_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Filter_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.MoleculeCluster_builder import MoleculeCluster_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing MoleculeCluster_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.MolecularDynamic_builder import MolecularDynamic_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing MolecularDynamic_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.AbInitioThermodynamics_builder import AbInitioThermodynamics_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing AbInitioThermodynamics_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.Blender_builder import Blender_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Blender_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.Extract_builder import Extract_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Extract_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.Conductivity_builder import Conductivity_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Conductivity_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.Plot_builder import Plot_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Plot_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.partition_builder.Metadata_builder import Metadata_builder
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing Metadata_builder: {str(e)}\n")
    del sys

try:
    from sage_lib.partition.PartitionManager import PartitionManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PartitionManager: {str(e)}\n")
    del sys

try:
    import numpy as np
    from typing import List, Tuple, Optional, Dict
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

try:
    from scipy.interpolate import interp1d
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

from sage_lib.miscellaneous.SOAP_tools import *

class Partition(BandStructure_builder, Config_builder, Crystal_builder, CrystalDefect_builder, 
                 Molecule_builder, PositionEditor_builder, SurfaceStates_builder, VacuumStates_builder, Filter_builder, 
                  MoleculeCluster_builder,MolecularDynamic_builder,AbInitioThermodynamics_builder,
                 Blender_builder, Extract_builder, Conductivity_builder, Plot_builder, Metadata_builder):
    """
    The Partition class is designed to handle various operations related to different types
    of crystal structure manipulations. It inherits from multiple builder classes, each
    specialized in a specific aspect of crystal structure and simulation setup.
    """

    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        """
        Initializes the Partition class with the provided file location and name.

        Args:
            file_location (str, optional): The path to the file or directory where the data is stored.
            name (str, optional): The name associated with this instance of the Partition class.
            kwargs: Additional keyword arguments.
        """
        #super().__init__(name=name, file_location=file_location)

        # BandStructure_builder: Likely involved in constructing or analyzing the band structure of materials. 

        # This could include calculations related to the electronic properties of solids, such as band gaps, 
        # electronic density of states, etc.
        BandStructure_builder.__init__(self, name=name, file_location=file_location, **kwargs)
        # Config_builder: Potentially used for setting up or managing configuration settings. This could 
        # be related to simulation parameters, computational settings, or environment configurations.
        Config_builder.__init__(self, name=name, file_location=file_location, **kwargs)
        # Crystal_builder: Likely used for creating or manipulating crystal structures. This class might 
        # handle tasks like generating crystal lattices, defining unit cells, or applying crystallographic transformations.
        Crystal_builder.__init__(self, name=name, file_location=file_location, **kwargs)
        # CrystalDefect_builder: Probably focused on introducing and managing defects within crystal structures, 
        # such as vacancies, interstitials, or dislocations. Useful in studies of material properties influenced by imperfections.
        CrystalDefect_builder.__init__(self, name=name, file_location=file_location, **kwargs)

        # Molecule_builder: Presumably used for creating and manipulating molecular structures. This may include 
        # tasks like building molecular models, adding or removing atoms or groups, and setting molecular geometries.
        Molecule_builder.__init__(self, name=name, file_location=file_location, **kwargs)
        # PositionEditor_builder: Probably designed for editing and manipulating atomic positions. This could 
        # involve tasks like translating, rotating, or scaling atomic structures.
        PositionEditor_builder.__init__(self, name=name, file_location=file_location, **kwargs)
        # SurfaceStates_builder: Likely focuses on the properties and states of material surfaces. This might include 
        # surface energy calculations, adsorption studies, or surface reconstruction analyses.
        SurfaceStates_builder.__init__(self, name=name, file_location=file_location, **kwargs)
        # VacuumStates_builder: Potentially involved in simulating or analyzing states in a vacuum environment. 
        # This could be relevant in studies of isolated molecules or atoms, free from interactions with a surrounding medium.
        VacuumStates_builder.__init__(self, name=name, file_location=file_location, **kwargs)
        # Filter_builder: Possibly used for creating filters or criteria for selecting specific atoms, molecules, 
        # or structures based on certain properties or conditions.
        Filter_builder.__init__(self, name=name, file_location=file_location, **kwargs)
        # SupercellEmbedding_builder: Likely used in the context of supercell models in crystallography or materials science. 
        # This class might handle the creation or manipulation of supercells for periodic boundary condition simulations.
        MoleculeCluster_builder.__init__(self, name=name, file_location=file_location, **kwargs)
        #
        #
        MolecularDynamic_builder.__init__(self, name=name, file_location=file_location, **kwargs)
        #
        #
        AbInitioThermodynamics_builder.__init__(self, name=name, file_location=file_location, **kwargs)

        Conductivity_builder.__init__(self, name=name, file_location=file_location, **kwargs)

    def get_composition_data(self, verbose: bool = True) -> Dict[str, np.ndarray]:
        """
        Extract composition, energy, and area data from containers.

        This function iterates through all containers and extracts relevant information such as the composition data,
        energy values, surface area, and lattice vectors. The extracted data is stored as numpy arrays for efficient
        numerical operations.

        Parameters:
            verbose (bool): If True, prints progress messages.

        Returns:
            Dict[str, np.ndarray]: A dictionary containing:
                - composition_data: Array with composition counts for each container.
                - energy_data: Array with energy values for each container.
                - area_data: Array with surface area values for each container.
                - uniqueAtomLabels: Unique atom labels used in the containers.
                - lattice_data: Array with lattice vector information for each container.
        """
        if verbose:
            print("Extracting composition, energy, and area data from containers...")

        # Initialize arrays to store the data extracted from containers
        num_containers = len(self.containers)
        num_labels = len(self.uniqueAtomLabels)

        composition_data = np.zeros((num_containers, num_labels), dtype=np.float64)
        energy_data = np.zeros(num_containers, dtype=np.float64)
        area_data = np.zeros(num_containers, dtype=np.float64)
        lattice_data = np.zeros((num_containers, 9), dtype=np.float64)

        # Extract data for each container
        for c_i, c in enumerate(self.containers):  
            comp = np.zeros_like(self.uniqueAtomLabels, dtype=np.float64)
            for ual, ac in zip(c.AtomPositionManager.uniqueAtomLabels, c.AtomPositionManager.atomCountByType):
                comp[self.uniqueAtomLabels_order[ual]] = ac

            # Store extracted data in the corresponding arrays
            composition_data[c_i, :] = comp
            energy_data[c_i] = c.AtomPositionManager.E
            area_data[c_i] = c.AtomPositionManager.get_area('z')
            lattice_data[c_i, :] = np.ravel( c.AtomPositionManager.latticeVectors )

        # Store data in instance attributes for future use
        self.composition_data = composition_data
        self.energy_data = energy_data
        self.area_data = area_data
        self.lattice_data = lattice_data

        if verbose:
            print(f"Extracted data for {num_containers} structures.")

        # Return the extracted data as a dictionary
        return {
            'composition_data': composition_data,
            'energy_data': energy_data,
            'area_data': area_data,
            'uniqueAtomLabels': self.uniqueAtomLabels,
            'lattice_data': lattice_data,
        }

    def generate_variants(self, parameter: str, values:np.array=None, file_location: str = None) -> bool:
        """
        Generates variants of the current container set based on the specified parameter and its range of values.

        This method iterates over the existing containers and applies different modifications
        according to the specified parameter (e.g., KPOINTS, VACANCY). The result is a new set
        of containers with the applied variations.

        Args:
            parameter (str): The parameter based on which the variants are to be generated.
            values (np.array, optional): The range of values to be applied for the parameter.
            file_location (str, optional): The location where the generated data should be stored.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        containers = []
        directories = ['' for _ in self.containers]
        parameter = parameter.upper().strip()

        for container_index, container in enumerate(self.containers):

            if parameter.upper() == 'KPOINTS':
                containers += self.handleKPoints(container, values, container_index,  file_location) 
                directories[container_index] = 'KPOINTConvergence'

            elif container.InputFileManager and parameter.upper() in container.InputFileManager.parameters_data:
                containers += self.handleInputFile(container, values, parameter,  container_index, file_location)
                directories[container_index] = f'{parameter}_analysis'

            elif parameter.upper() == 'DEFECTS':
                containers += self.handleDefect(container, values, container_index, file_location)
                directories[container_index] = 'Vacancy'

            elif parameter.upper() == 'BAND_STRUCTURE':
                containers += self.handleBandStruture(container, values, container_index, file_location)
                directories[container_index] = 'band_structure'

            elif parameter.upper() == 'CHANGE_ATOM_ID':
                containers += self.handleAtomIDChange(container, values, container_index, file_location)
                directories[container_index] = 'changeID'

            elif parameter.upper() == 'SOLVENT':
                containers += self.handleCLUSTER(container, values, container_index, file_location)
                directories[container_index] = 'solvent'

        self.containers = containers
        #self.generate_master_script_for_all_containers(directories, file_location if not file_location is None else container.file_location )

    @staticmethod
    def _compute_lag_msd(pos: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute the MSD using lag time differences, returning total MSD and MSD by dimension.
        
        pos shape: (n_particles, n_time, n_dim)
        Returns:
         Dt_r: (n_time-1,)
         MSD_total: (n_time-1,) averaged total MSD over particles
         MSD_by_dim: (n_particles, n_time-1, n_dim)
        """
        n_particles, n_time, n_dim = pos.shape
        Dt_r = np.arange(1, n_time)
        MSD_by_dim = np.zeros((n_particles, len(Dt_r), n_dim))

        for i, Dt in enumerate(Dt_r):
            diffs = pos[:, Dt:, :] - pos[:, :-Dt, :]
            diffs_sq = diffs**2
            MSD_by_dim[:, i, :] = np.mean(diffs_sq, axis=1)  # mean over time

        # MSD_total is the sum over dimensions, averaged over particles
        MSD_total = np.mean(np.sum(MSD_by_dim, axis=-1), axis=0)

        return Dt_r, MSD_total, MSD_by_dim

    @staticmethod
    def _compute_initial_msd(pos: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute the MSD relative to the initial position, returning total MSD and MSD by dimension.
        
        pos shape: (n_particles, n_time, n_dim)
        """
        n_particles, n_time, n_dim = pos.shape
        Dt_r = np.arange(1, n_time)

        diffs = pos - pos[:, 0:1, :]
        diffs_sq = diffs**2

        # MSD_by_dim: promedio sobre partículas ya que en _compute_lag_msd no lo hacíamos,
        # aquí lo haremos similarmente:
        # Queremos (n_particles, n_time-1, n_dim)
        MSD_by_dim = diffs_sq[:, 1:, :]  # sacamos el primer punto (Dt=0)
        
        # MSD_total: sum sobre dim y promedio sobre partículas
        MSD_total = np.mean(np.sum(MSD_by_dim, axis=-1), axis=0)

        return Dt_r, MSD_total, MSD_by_dim

    @staticmethod
    def _compute_fft_msd(pos: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute the Mean Squared Displacement (MSD) using the Fast Fourier Transform (FFT) method,
        returning total MSD and MSD by dimension.

        Parameters:
            pos (np.ndarray): Particle positions with shape (n_particles, n_time, n_dim).

        Returns:
            Dt_r (np.ndarray): Array of lag times (of length n_time-2).
            MSD_total (np.ndarray): The averaged total MSD over all particles and summed across all dimensions.
                                   Shape (n_time-2,).
            MSD_by_dim (np.ndarray): MSD values for each particle and dimension.
                                     Shape (n_particles, n_time-2, n_dim).

        Method:
        -------
        1. Decompose the calculation by dimension. For each dimension, use FFT to compute the MSD.
        2. For each dimension, we obtain a (n_particles, n_time-2) MSD array.
        3. Stack these results across the dimension axis to form MSD_by_dim.
        4. Compute MSD_total by summing over dimensions and averaging over particles.
        
        Note:
        -----
        The logic for handling arrays (e.g., D_pad, D_flip_pad) ensures that the shapes match 
        before summation, preventing broadcasting errors. This follows the Wiener-Khinchin theorem
        for MSD calculation via FFT.
        """

        n_particles, n_time, n_dim = pos.shape
        Dt_r = np.arange(1, n_time - 1)

        MSD_dimensional_list = []
        for d in range(n_dim):
            # Extract one dimension
            pos_d = pos[:, :, d]  # (n_particles, n_time)

            # FFT-based computations
            f_pos = np.fft.fft(pos_d, n=2*n_time, axis=-1)
            S2 = np.fft.ifft(np.abs(f_pos)**2, axis=-1).real[:, :n_time]
            S2 /= (n_time - np.arange(n_time))[None, :]

            D = pos_d**2
            D = np.append(D, np.zeros((n_particles, 1)), axis=-1)  # (n_particles, n_time+1)

            # Prepare arrays for S1 calculation
            D_pad = np.insert(D[:, :-1], 0, 0, axis=-1)      # (n_particles, n_time+1)
            D_flip = np.flip(D[:, :-1], axis=-1)             # (n_particles, n_time)
            D_flip_pad = np.insert(D_flip, 0, 0, axis=-1)    # (n_particles, n_time+1)

            S1 = (2 * np.sum(D, axis=-1)[:, None] - np.cumsum(D_pad + D_flip_pad, axis=-1))
            # Reduce back to n_time columns
            S1 = S1[:, :-1] / (n_time - np.arange(n_time))[None, :]

            # MSD for this dimension
            MSD_d = S1 - 2 * S2
            MSD_d = MSD_d[:, Dt_r]  # keep only lags 1 to n_time-2
            MSD_dimensional_list.append(MSD_d)

        # Combine all dimensions
        MSD_by_dim = np.stack(MSD_dimensional_list, axis=-1)  #  (particles, frames-2, dimentions)  (n_particles, n_time-2, n_dim)
        MSD_total = np.mean(np.sum(MSD_by_dim, axis=-1), axis=0)  # (frames,) average over particles, sum over dim

        return Dt_r, MSD_total, MSD_by_dim



    def MSD(self, pos: np.ndarray, lag: bool = True, fft: bool = True) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate the MSD (total and by dimension) for given particle positions.
        
        Returns:
         Dt_r (np.ndarray): time differences
         MSD_total (np.ndarray): average MSD total over particles (sum of all dimensions)
         MSD_by_dim (np.ndarray): MSD for each particle and dimension (n_particles, n_times, n_dim)
        """
        if fft:
            return self._compute_fft_msd(pos)
        elif lag:
            return self._compute_lag_msd(pos)
        else:
            return self._compute_initial_msd(pos)

    def rmse(self, y_true: np.array, y_pred: np.array) -> float:
        """
        Calculate the Root Mean Square Error (RMSE).

        Parameters
        ----------
        y_true : np.array
            The ground truth target values.
        y_pred : np.array
            The predicted values by the model.

        Returns
        -------
        float
            The RMSE metric as a float.
        """
        # Compute RMSE using the square root of the mean squared error.
        return np.sqrt(np.mean((y_true - y_pred) ** 2))

    def nrmse(self, y_true: np.array, y_pred: np.array) -> float:
        """
        Calculate the Normalized Root Mean Square Error (NRMSE).

        Parameters
        ----------
        y_true : np.array
            The ground truth target values.
        y_pred : np.array
            The predicted values by the model.

        Returns
        -------
        float
            The NRMSE metric as a float. Normalization is done using the range of y_true.
        """
        # Ensure the RMSE function is accessed correctly within the class.
        return self.rmse(y_true, y_pred) / (y_true.max() - y_true.min())

    def mae(self, y_true: np.array, y_pred: np.array) -> float:
        """
        Calculate the Mean Absolute Error (MAE).

        Parameters
        ----------
        y_true : np.array
            The ground truth target values.
        y_pred : np.array
            The predicted values by the model.

        Returns
        -------
        float
            The MAE metric as a float.
        """
        # Compute MAE as the mean of absolute differences between true and predicted values.
        return np.mean(np.abs(y_true - y_pred))

    def mape(self, y_true: np.array, y_pred: np.array) -> float:
        """
        Calculate the Mean Absolute Percentage Error (MAPE).

        Parameters
        ----------
        y_true : np.array
            The ground truth target values.
        y_pred : np.array
            The predicted values by the model.

        Returns
        -------
        float
            The MAPE metric as a float, expressed in percentage terms.
        """
        # Compute MAPE, avoiding division by zero by adding a small constant to y_true if necessary.
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    def r_squared(self, y_true: np.array, y_pred: np.array) -> float:
        """
        Calculate the coefficient of determination, R^2 score.

        Parameters
        ----------
        y_true : np.array
            The ground truth target values.
        y_pred : np.array
            The predicted values by the model.

        Returns
        -------
        float
            The R^2 score as a float.
        """
        # Compute R^2 score, indicating the proportion of variance in the dependent variable predictable from the independent variable(s).
        return 1 - (np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2))

    def str_to_connectivity(self, input_string:str) -> dict:
        # Initialize variables
        elements = {}  # To store parsed elements and their indexes
        i = 0  # Index to iterate through the string
        element_id_map = {}

        # Iterate through the string to parse elements and indexes
        while i < len(input_string):
            # Detect element (considering elements can have 2 characters, e.g., 'Ni')
            if i < len(input_string) - 1 and input_string[i:i+2] in self.atomic_numbers.keys() :
                element = input_string[i:i+2]
                i += 2

            elif input_string[i:i+1] in self.atomic_numbers.keys() or input_string[i:i+1] == '*':
                element = input_string[i]
                i += 1

            # If next character is a digit, it's an index for self-connection, skip it
            if i < len(input_string) and input_string[i].isdigit():
                if not input_string[i] in element_id_map: element_id_map[input_string[i]] = len(elements)
                element_id = element_id_map[input_string[i]]
                i += 1
            
            else:
                element_id = len(elements)
            
            # Add element to list
            elements[len(elements)] = [element, element_id] 

        return elements

    def interpolate_with_splines(self, data:np.array, M:int, degree='cubic'):
        """
        Interpolates using splines or polynomials between each pair of subsequent images.
        
        Parameters:
        - data: A NumPy array of shape (N, 3, I).
        - M: Number of points to interpolate between each pair of images.
        - degree: Type of spline or polynomial for interpolation ('linear', 'cubic', 'quadratic', etc.).
        
        Returns:
        - A new array with interpolations.
        """
        N, _, I = data.shape
        # Original "x" positions (indices of the images)
        x_orig = np.arange(I)
        # New "x" positions where we want to interpolate
        x_new = np.linspace(0, I - 1, I + (I - 1) * M)
        
        # Prepare the new array
        new_array = np.empty((N, 3, len(x_new)))
        
        # Iterate over each atom and each spatial dimension
        for n in range(N):
            for dim in range(3):
                # Create an interpolation function for each atom and dimension
                f_interp = interp1d(x_orig, data[n, dim, :], kind=degree)
                # Compute interpolated values and assign them to the new array
                new_array[n, dim, :] = f_interp(x_new)
        
        return new_array

    def get_SOAP(self, r_cut, n_max, l_max, sigma, save, cache):
        symbols     = [c.AtomPositionManager.atomLabelsList for c in self.containers] 
        positions   = [c.AtomPositionManager.atomPositions  for c in self.containers]
        cell        = [c.AtomPositionManager.latticeVectors for c in self.containers]

        print(f" >< Making SOAP (r_cut={r_cut}, n_max={n_max}, l_max={l_max}, sigma={sigma}).")
        soap = SOAP_analysis(uniqueAtomLabels=self.uniqueAtomLabels,
                             r_cut=r_cut,
                             n_max=n_max,  
                             l_max=l_max,
                             sigma=sigma,
                            )

        if cache:
            soap_data = soap.verify_and_load_soap()
            if soap_data:
                descriptors_by_species, atom_info_by_species = soap_data
                print("Loaded existing SOAP data.")

            else:
                print("Some SOAP files are missing. Recalculating...")
                descriptors_by_species, atom_info_by_species = soap.calculate_soap_descriptors(
                                        symbols=symbols, 
                                        positions=positions, 
                                        cell=cell,)
                soap.save_descriptors(  descriptors_by_species=descriptors_by_species, 
                                        atom_info_by_species=atom_info_by_species, 
                                        output_dir='SOAPs')
        else:
            print("Cache disabled. Calculating SOAP descriptors...")
            descriptors_by_species, atom_info_by_species = soap.calculate_soap_descriptors(
                                        symbols=symbols, 
                                        positions=positions, 
                                        cell=cell,)
            soap.save_descriptors(  descriptors_by_species=descriptors_by_species, 
                                    atom_info_by_species=atom_info_by_species, 
                                    output_dir='SOAPs')

        return descriptors_by_species, atom_info_by_species

    def get_positions(self, fractional: bool = False, wrap: bool = False):
        """
        Retrieve atomic positions from all containers.

        Depending on the flags, returns either Cartesian or fractional coordinates.
        Optionally, periodic boundary conditions can be enforced.

        Parameters
        ----------
        fractional : bool, optional
            Return positions in fractional coordinates relative to the unit cell if True.
        wrap : bool, optional
            Apply periodic boundary conditions if True.

        Returns
        -------
        np.ndarray
            Array of atomic positions.
        """
        if wrap:
            for container in self.containers:
                container.AtomPositionManager.wrap()

        if fractional:
            return np.array([
                container.AtomPositionManager.atomPositions_fractional
                for container in self.containers
            ], dtype=np.float64)
        else:
            return np.array([
                container.AtomPositionManager.atomPositions
                for container in self.containers
            ], dtype=np.float64)

    def get_msd_data(self, chemical_ID: List[str] = None) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Extract the atom positions and labels from the loaded simulation containers.
        Also returns the simulation cell volume.

        Parameters
        ----------
        chemical_ID : list of str, optional
            If provided, can be used to filter atoms by their chemical labels.

        Returns
        -------
        atoms_positions : np.ndarray
            Atomic positions with shape (n_atoms, n_steps, 3).
        atom_labels : np.ndarray
            Atomic labels corresponding to each atom.
        volume : float
            The simulation cell volume.

        Notes
        -----
        The raw data is reorganized so that the resulting array has
        dimensions (n_atoms, n_steps, 3).
        """

        volume = self.containers[0].AtomPositionManager.get_volume()
        atom_labels = self.containers[0].AtomPositionManager.get_atomic_labels()

        num_steps = len(self.containers)
        num_atoms = self.containers[0].AtomPositionManager.atomPositions.shape[0]
        atoms_positions = np.zeros((num_steps, num_atoms, 3))

        for c_i in tqdm(range(num_steps), desc="Extracting MSD Data", unit="step"):
            atoms_positions[c_i, :, :] = self.containers[c_i].AtomPositionManager.atomPositions

        # Rearranging into (n_atoms, n_steps, 3)
        atoms_positions = np.transpose(atoms_positions, (1, 0, 2))

        return atoms_positions, atom_labels, volume


