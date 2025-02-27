try:
    from sage_lib.partition.PartitionManager import PartitionManager
    from sage_lib.miscellaneous.data_mining import *
    

except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PartitionManager: {str(e)}\n")
    del sys

try:
    import numpy as np

    from sklearn.manifold import TSNE
    from sklearn.decomposition import PCA

except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sklearn.manifold: {str(e)}\n")
    del sys

try:
    import os
    import copy
    from tqdm import tqdm
    from typing import Dict, List, Tuple, Union
    from collections import defaultdict
    from joblib import Memory

except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing os: {str(e)}\n")
    del sys
    
try:
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    import seaborn as sns
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while matplotlib || seaborn: {str(e)}\n")
    del sys

class AbInitioThermodynamics_builder(PartitionManager):
    """
    A class for performing Ab Initio Thermodynamics analysis on atomic structures.

    This class extends PartitionManager to handle composition data, energy data, and perform
    various analyses such as phase diagram generation, local linear regression, and global linear prediction.

    Attributes:
        composition_data (np.ndarray): Array containing composition data for each structure.
        energy_data (np.ndarray): Array containing energy data for each structure.
        area_data (np.ndarray): Array containing area data for each structure.
    """

    def __init__(self, file_location: str = None, name: str = None, **kwargs):
        """
        Initialize the AbInitioThermodynamics_builder.

        Args:
            file_location (str, optional): Location of input files.
            name (str, optional): Name of the analysis.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(name=name, file_location=file_location)
        
        self.composition_data = None
        self.energy_data = None 
        self.area_data = None

    def plot_phase_diagram(self, diagram_data: np.ndarray, mu_max: float, mu_min: float, 
                           output_path: str = None, window_size: Tuple[int, int] = (12, 8), 
                           save: bool = True, verbose: bool = True) -> None:
        """
        Plot a phase diagram with extrapolated lines and highlight the lower envelope.

        Args:
            diagram_data (np.ndarray): An Nx2 array with each row being [y-intercept, slope] for a line.
            mu_max (float): Maximum chemical potential value.
            mu_min (float): Minimum chemical potential value.
            output_path (str, optional): Path to save the plot image.
            window_size (Tuple[int, int]): Size of the plotting window.
            save (bool): Whether to save the plot to a file.
            verbose (bool): Whether to print additional information.
        """
        print("Generating phase diagram plot...")

        plt.figure(figsize=window_size)

        x_values = np.linspace(mu_min, mu_max, 100)
        lower_envelope = np.inf * np.ones_like(x_values)
        optimal_structures = []

        for index, (x, y) in enumerate(diagram_data):
            m = (y - x) / (1 - 0)
            b = y - m * 1
            y_values = m * x_values + b
            
            plt.plot(x_values, y_values, alpha=0.5, label=f'Structure {index}')

            # Update lower envelope
            mask = y_values < lower_envelope
            lower_envelope[mask] = y_values[mask]
            optimal_structures.append(index)

        # Plot lower envelope
        plt.plot(x_values, lower_envelope, 'k-', linewidth=2, label='Lower Envelope')

        plt.xlabel('Chemical Potential (μ)')
        plt.ylabel('Formation Energy (γ)')
        plt.title('Phase Diagram with Lower Envelope')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)

        if save:
            if not output_path:
                output_path = '.'
            plt.savefig(f'{output_path}/phase_diagram_plot.png', dpi=300, bbox_inches='tight')
            if verbose:
                print(f"Phase diagram plot saved to {output_path}/phase_diagram_plot.png")
        else:
            plt.show()

        if verbose:
            print(f"Optimal structures: {optimal_structures}")

    def calculate_ensemble_properties(self, energies: np.ndarray, volumes: np.ndarray, 
                                      temperatures: np.ndarray, particles: np.ndarray,
                                      ensemble: str = 'canonical', mass: float = 1.0,
                                      output_path: str = None, save: bool = True, 
                                      verbose: bool = True) -> Dict[str, np.ndarray]:
        """
        Calculate partition function and thermodynamic parameters for different ensembles.

        Args:
            energies (np.ndarray): Energy levels of the system.
            volumes (np.ndarray): Volumes of the system.
            temperatures (np.ndarray): Array of temperatures to analyze.
            particles (np.ndarray): Array of particle numbers (for grand canonical ensemble).
            ensemble (str): Type of ensemble ('canonical', 'microcanonical', 'grand_canonical').
            mass (float): Mass of the particles (used in some calculations).
            output_path (str, optional): Path to save the plots.
            save (bool): Whether to save the plots to files.
            verbose (bool): Whether to print additional information.

        Returns:
            Dict[str, np.ndarray]: Dictionary of calculated thermodynamic properties.
        """
        print(f"Calculating ensemble properties for {ensemble} ensemble...")

        k_B = Boltzmann
        h = hbar * 2 * pi
        properties = {}

        if ensemble == 'canonical':
            # Canonical ensemble calculations
            Z = np.sum(np.exp(-energies[:, np.newaxis] / (k_B * temperatures)), axis=0)
            properties['partition_function'] = Z
            
            # Free energy
            F = -k_B * temperatures * np.log(Z)
            properties['free_energy'] = F
            
            # Internal energy
            U = np.sum(energies[:, np.newaxis] * np.exp(-energies[:, np.newaxis] / (k_B * temperatures)), axis=0) / Z
            properties['internal_energy'] = U
            
            # Entropy
            S = k_B * np.log(Z) + U / temperatures
            properties['entropy'] = S
            
            # Heat capacity
            C_V = k_B * (np.sum(energies[:, np.newaxis]**2 * np.exp(-energies[:, np.newaxis] / (k_B * temperatures)), axis=0) / Z
                         - (np.sum(energies[:, np.newaxis] * np.exp(-energies[:, np.newaxis] / (k_B * temperatures)), axis=0) / Z)**2) / temperatures**2
            properties['heat_capacity'] = C_V

        elif ensemble == 'microcanonical':
            # Microcanonical ensemble calculations
            # Assuming a simple model where Ω(E) ~ E^(3N/2-1) for an ideal gas
            N = len(particles)  # Number of particles
            Omega = energies**(3*N/2 - 1)
            properties['density_of_states'] = Omega
            
            # Entropy
            S = k_B * np.log(Omega)
            properties['entropy'] = S
            
            # Temperature (derived from entropy)
            T = 1 / (np.gradient(S, energies))
            properties['temperature'] = T
            
            # Heat capacity
            C_V = 1 / (np.gradient(1/T, energies))
            properties['heat_capacity'] = C_V

        elif ensemble == 'grand_canonical':
            # Grand Canonical ensemble calculations
            mu = np.linspace(np.min(energies), np.max(energies), 100)  # Chemical potential range
            Z_grand = np.sum(np.exp((mu[:, np.newaxis, np.newaxis] - energies[:, np.newaxis]) / (k_B * temperatures)), axis=0)
            properties['grand_partition_function'] = Z_grand
            
            # Grand potential
            Omega = -k_B * temperatures * np.log(Z_grand)
            properties['grand_potential'] = Omega
            
            # Average number of particles
            N_avg = np.sum(particles[:, np.newaxis, np.newaxis] * np.exp((mu[:, np.newaxis, np.newaxis] - energies[:, np.newaxis]) / (k_B * temperatures)), axis=0) / Z_grand
            properties['average_particles'] = N_avg
            
            # Internal energy
            U = np.sum(energies[:, np.newaxis, np.newaxis] * np.exp((mu[:, np.newaxis, np.newaxis] - energies[:, np.newaxis]) / (k_B * temperatures)), axis=0) / Z_grand
            properties['internal_energy'] = U

        # Plotting
        fig, axs = plt.subplots(2, 2, figsize=(16, 16))
        
        if ensemble == 'canonical':
            axs[0, 0].plot(temperatures, properties['free_energy'])
            axs[0, 0].set_xlabel('Temperature (K)')
            axs[0, 0].set_ylabel('Free Energy (J)')
            axs[0, 0].set_title('Free Energy vs Temperature')

            axs[0, 1].plot(temperatures, properties['internal_energy'])
            axs[0, 1].set_xlabel('Temperature (K)')
            axs[0, 1].set_ylabel('Internal Energy (J)')
            axs[0, 1].set_title('Internal Energy vs Temperature')

            axs[1, 0].plot(temperatures, properties['entropy'])
            axs[1, 0].set_xlabel('Temperature (K)')
            axs[1, 0].set_ylabel('Entropy (J/K)')
            axs[1, 0].set_title('Entropy vs Temperature')

            axs[1, 1].plot(temperatures, properties['heat_capacity'])
            axs[1, 1].set_xlabel('Temperature (K)')
            axs[1, 1].set_ylabel('Heat Capacity (J/K)')
            axs[1, 1].set_title('Heat Capacity vs Temperature')

        elif ensemble == 'microcanonical':
            axs[0, 0].plot(energies, properties['density_of_states'])
            axs[0, 0].set_xlabel('Energy (J)')
            axs[0, 0].set_ylabel('Density of States')
            axs[0, 0].set_title('Density of States vs Energy')

            axs[0, 1].plot(energies, properties['entropy'])
            axs[0, 1].set_xlabel('Energy (J)')
            axs[0, 1].set_ylabel('Entropy (J/K)')
            axs[0, 1].set_title('Entropy vs Energy')

            axs[1, 0].plot(energies, properties['temperature'])
            axs[1, 0].set_xlabel('Energy (J)')
            axs[1, 0].set_ylabel('Temperature (K)')
            axs[1, 0].set_title('Temperature vs Energy')

            axs[1, 1].plot(energies, properties['heat_capacity'])
            axs[1, 1].set_xlabel('Energy (J)')
            axs[1, 1].set_ylabel('Heat Capacity (J/K)')
            axs[1, 1].set_title('Heat Capacity vs Energy')

        elif ensemble == 'grand_canonical':
            axs[0, 0].pcolormesh(temperatures, mu, properties['grand_potential'])
            axs[0, 0].set_xlabel('Temperature (K)')
            axs[0, 0].set_ylabel('Chemical Potential (J)')
            axs[0, 0].set_title('Grand Potential')

            axs[0, 1].pcolormesh(temperatures, mu, properties['average_particles'])
            axs[0, 1].set_xlabel('Temperature (K)')
            axs[0, 1].set_ylabel('Chemical Potential (J)')
            axs[0, 1].set_title('Average Number of Particles')

            axs[1, 0].pcolormesh(temperatures, mu, properties['internal_energy'])
            axs[1, 0].set_xlabel('Temperature (K)')
            axs[1, 0].set_ylabel('Chemical Potential (J)')
            axs[1, 0].set_title('Internal Energy')

        plt.tight_layout()

        if save:
            if not output_path:
                output_path = '.'
            plt.savefig(f'{output_path}/{ensemble}_ensemble_properties.png', dpi=300)
            if verbose:
                print(f"{ensemble.capitalize()} ensemble properties plot saved to {output_path}/{ensemble}_ensemble_properties.png")
        else:
            plt.show()

        if verbose:
            print(f"Calculation of {ensemble} ensemble properties completed.")

        return properties

    '''
    def get_composition_data(self) -> Dict[str, np.ndarray]:
        """
        Extract composition, energy, and area data from containers.

        Returns:
            Dict[str, np.ndarray]: Dictionary containing composition_data, energy_data, and area_data.
        """
        print("Extracting composition, energy, and area data from containers...")
        
        composition_data = np.zeros((len(self.containers), len(self.uniqueAtomLabels)), dtype=np.float64)
        energy_data = np.zeros(len(self.containers), dtype=np.float64)
        area_data = np.zeros(len(self.containers), dtype=np.float64)
        
        for c_i, c in enumerate(self.containers):  
            comp = np.zeros_like(self.uniqueAtomLabels, dtype=np.int64)
            for ual, ac in zip(c.AtomPositionManager.uniqueAtomLabels, c.AtomPositionManager.atomCountByType):
                comp[self.uniqueAtomLabels_order[ual]] = ac 

            composition_data[c_i,:] = comp
            energy_data[c_i] = c.AtomPositionManager.E
            area_data[c_i] = c.AtomPositionManager.get_area('z')

        self.composition_data, self.energy_data, self.area_data = composition_data, energy_data, area_data

        print(f"Extracted data for {len(self.containers)} structures.")
        return {'composition_data': composition_data, 'energy_data': energy_data, 'area_data': area_data, 'uniqueAtomLabels':self.uniqueAtomLabels}
    '''
    
    def get_diagram_data(self, ID_reference: List[int], composition_data: np.ndarray, 
                         energy_data: np.ndarray, area_data: np.ndarray, especie: str) -> np.ndarray:
        """
        Calculate diagram data for phase diagram generation.

        Args:
            ID_reference (List[int]): List of reference structure IDs.
            composition_data (np.ndarray): Array of composition data.
            energy_data (np.ndarray): Array of energy data.
            area_data (np.ndarray): Array of area data.
            especie (str): Chemical species to focus on.

        Returns:
            np.ndarray: Array containing diagram data for phase diagram plotting.
        """
        print(f"Calculating diagram data for phase diagram generation, focusing on species: {especie}")
        
        composition_reference = composition_data[ID_reference, :] 
        energy_reference = energy_data[ID_reference] 

        reference_mu_index = next(cr_i for cr_i, cr in enumerate(composition_reference) 
                                  if np.sum(cr) == cr[self.uniqueAtomLabels_order[especie]])

        mask = np.ones(len(energy_data), dtype=bool)
        mask[ID_reference] = False

        composition_relevant = composition_data[mask,:]
        energy_relevant = energy_data[mask]
        area_relevant = area_data[mask]

        diagram_data = np.zeros((energy_relevant.shape[0], 2))

        for mu in [0, 1]:
            for i, (E, C, A) in enumerate(zip(energy_relevant, composition_relevant, area_relevant)):
                E_ref_mask = np.zeros_like(energy_reference)
                E_ref_mask[reference_mu_index] = mu

                mu_value = np.linalg.solve(composition_reference, energy_reference + E_ref_mask)
                gamma = 1/A * (E - np.sum(mu_value * C))

                diagram_data[i, mu] = gamma

        print(f"Diagram data calculated for {energy_relevant.shape[0]} structures.")
        return diagram_data

    def generate_atom_labels_and_cluster_counts(
        self,
        atom_clusters: Dict[str, Union[List[int], np.ndarray]],
        atom_structures: Dict[str, Union[List[Union[List[int], np.ndarray]], np.ndarray]]
    ) -> Tuple[List[np.ndarray], np.ndarray, List[str]]:
        """
        Generate atom labels for each structure, count clusters across structures, and create class labels.

        Args:
            atom_clusters: Dictionary mapping element symbols to cluster labels for each atom.
            atom_structures: Dictionary mapping element symbols to structure and atom IDs.

        Returns:
            A tuple containing:
            - List of numpy arrays with cluster labels for atoms in each structure.
            - 2D numpy array of cluster counts for each structure.
            - List of class labels in the format "Element_ClusterNumber".
        """
        # Get the number of structures
        num_structures = len(self.containers)

        # Initialize variables for cluster mapping and class labels
        total_clusters = 0
        cluster_mapping = {}
        class_labels = []

        # Process each unique element
        for element in self.uniqueAtomLabels:
            clusters = atom_clusters[element]
            unique_clusters = sorted(set(clusters))
            
            # Create mapping for cluster indices and generate class labels
            cluster_mapping[element] = {c: i + total_clusters for i, c in enumerate(unique_clusters)}
            class_labels.extend([f"{element}_{c}" for c in unique_clusters])
            total_clusters += len(unique_clusters)

        # Initialize output structures
        structure_labels = [np.zeros(c.AtomPositionManager.atomCount, dtype=np.int64) for c in self.containers]
        cluster_counts = np.zeros((num_structures, total_clusters), dtype=int)

        # Process atom clusters for each element
        for element, clusters in atom_clusters.items():
            structures = atom_structures[element]
            element_mapping = cluster_mapping[element]

            # Extract structure IDs and atom IDs
            struct_ids, atom_ids = structures if isinstance(structures, list) else structures.T

            # Assign cluster labels and count clusters
            for struct_id, atom_id, cluster in zip(struct_ids, atom_ids, clusters):
                mapped_cluster = element_mapping[int(cluster)]
                structure_labels[int(struct_id)][int(atom_id)] = mapped_cluster
                cluster_counts[int(struct_id), mapped_cluster] += 1

        return structure_labels, cluster_counts, class_labels

    def handleABITAnalysis(self, values: Dict[str, Dict], file_location: str = None) -> None:
        """
        Handle Ab Initio Thermodynamics analysis based on specified values.

        Args:
            values (Dict[str, Dict]): Dictionary of analysis types and their parameters.
            file_location (str, optional): File location for output data.
        """
        print("Starting Ab Initio Thermodynamics analysis...")

        composition_data = self.get_composition_data()
        uniqueAtomLabels = composition_data['uniqueAtomLabels']
        compositions = composition_data['composition_data']
        energies = composition_data['energy_data']

        for abit, params in values.items():

            if abit.upper() == 'PHASE_DIAGRAM':
                print(f"Performing Phase Diagram analysis. Reference : {params.get('reference', ['GLOBAL'])[0].upper()},")

                if params.get('reference', ['GLOBAL'])[0].upper() == 'GLOBAL':

                    linear_analysis = LinearAnalysis(X=compositions, y=energies, X_labels=self.uniqueAtomLabels )
                    coefficients, predictions, residuals = linear_analysis.linear_predict(
                                            regularization = params.get('regularization', 1e-5), verbose = params.get('verbose', True), 
                                            zero_intercept = True, force_negative = False)
                    linear_analysis.save_output(output_dir='linear')
                    linear_analysis.analysis(output_dir='linear')

                elif params.get('reference', ['GLOBAL'])[0].upper() == 'LOCAL':
                    if params.get('opt', True):
                        print("Optimizing k value for local linear regression...")
                        params['k'], initial_errors, refined_errors, coeffs = self.find_optimal_k(
                            composition_data=composition_data,
                            verbose=params.get('verbose', False)
                            )

                else:
                    diagram_data = self.get_diagram_data(
                        ID_reference=params.get('reference', [0]),
                        composition_data=composition_data['composition_data'],
                        energy_data=composition_data['energy_data'],
                        area_data=composition_data['area_data'],
                        especie=params.get('especie', None)
                    )

                    self.plot_phase_diagram(
                        diagram_data,
                        output_path=params.get('output_path', '.'),
                        save=True,
                        verbose=params.get('verbose', True),
                        mu_max=params.get('mu_max', 1),
                        mu_min=params.get('mu_min', 0)
                        )

            if abit.upper() == 'ENSEMBLE_ANALYSIS':
                print("Performing Ensemble Analysis...")
                ensemble_type = params.get('ensemble', 'canonical')
                temperatures = params.get('temperatures', np.linspace(100, 1000, 100))
                volumes = params.get('volumes', np.ones_like(energies))  # Assuming unit volume if not provided
                particles = params.get('particles', np.arange(1, len(energies) + 1))
                mass = params.get('mass', 1.0)

                ensemble_properties = self.calculate_ensemble_properties(
                    volumes=volumes,
                    temperatures=temperatures,
                    particles=particles,
                    ensemble=ensemble_type,
                    mass=mass,
                    output_path=params.get('output_path', '.'),
                    save=params.get('save', True),
                    verbose=params.get('verbose', True)
                )

            if abit.upper() == 'COMPOSITION_ANALYSIS':
                '''
                COMPOSITION Analysis Process:

                1. Linear Analysis:
                   - Perform initial linear analysis on compositions and energies
                   - Save output and perform analysis

                2. SOAP (Smooth Overlap of Atomic Positions):
                   - Set up SOAP parameters (r_cut, n_max, l_max, sigma)
                   - Calculate or load SOAP descriptors for each atomic species
                   - Save descriptors if newly calculated

                3. Dimensionality Reduction:
                   - Compress SOAP descriptors using UMAP or another specified method
                   - Reduce to a specified number of components

                4. Clustering:
                   - Perform clustering analysis on compressed data
                   - Use specified clustering model (e.g., DBSCAN)
                   - Apply clustering for each atomic species

                5. Linear Model in Cluster Space:
                   - Generate atom labels and cluster counts
                   - Perform linear analysis on cluster counts
                   - Save output and perform analysis
                   - Plot distribution of chemical potentials

                6. RBF Interpretation:
                   - Plot RBF (Radial Basis Function) cluster

                7. Export Files:
                   - Export analysis results and processed data

                This script combines various analysis techniques to provide insights into the 
                composition-energy relationship and atomic structure characteristics.
                '''
                print("Performing COMPOSITION analysis...")
                print(" >> Linear model.") 

                # save raw data #
                np.savetxt('composition_counts.dat', compositions, header= ','.join(self.uniqueAtomLabels), comments='', delimiter='\t', fmt='%.6i')
                np.savetxt('energy.dat', energies, header='E', comments='', delimiter='\t', fmt='%.6f')

                metadata_colector = compositions # add to metadata_colector #
                metadata_colector_header = ','.join(self.uniqueAtomLabels)
                metadata_colector = np.hstack(( metadata_colector, energies.reshape(-1, 1) )) # add to metadata_colector #
                metadata_colector_header += ',E'

                linear_analysis = LinearAnalysis(X=compositions, y=energies, X_labels=self.uniqueAtomLabels )
                coefficients, predictions, residuals = linear_analysis.linear_predict(
                                        regularization = params.get('regularization', 1e-5), verbose = params.get('verbose', True), 
                                        zero_intercept = True, force_negative = False)
                linear_analysis.save_output(output_dir='linear')
                linear_analysis.analysis(output_dir='linear')

                #metadata_colector = np.hstack(( metadata_colector, coefficients.reshape(-1, 1) )) # add to metadata_colector #
                metadata_colector = np.hstack(( metadata_colector, predictions.reshape(-1, 1) )) # add to metadata_colector #
                metadata_colector_header += ',e_l'
                metadata_colector = np.hstack(( metadata_colector, residuals.reshape(-1, 1) )) # add to metadata_colector #
                metadata_colector_header += ',r_l'

                print(f'Coefficients', {u:c for u,c in zip(uniqueAtomLabels,coefficients[1:])})

                # =========== =========== =========== =========== #
                r_cut = params.get('r_cut', 4.0)
                n_max, l_max = params.get('n_max', 12), params.get('l_max', 12)
                sigma = params.get('sigma', 0.01)
                cache = params.get('cache', True)
                descriptors_by_species, atom_info_by_species = self.get_SOAP( 
                        r_cut=r_cut, 
                        n_max=n_max, 
                        l_max=l_max, 
                        sigma=sigma, 
                        save=True,
                        cache=cache )

                # =========== =========== =========== =========== #
                
                n_components = params.get('components', 10) 
                compress_model = params.get('compress_model', 'umap') 
                print(f" >< Compress model {compress_model} ({n_components}).")
                compressor = Compress(unique_labels=self.uniqueAtomLabels)
                compressed_data = compressor.verify_and_load_or_compress(descriptors_by_species, method=compress_model, n_components= {k:n_components for k, d in descriptors_by_species.items()} )

                # =========== =========== =========== =========== #
                cluster_model = params.get('cluster_model', 'dbscan')
                eps, min_samples = params.get('eps', 0.7), params.get('min_samples', 2) 
                print(f" >< Cluster model {cluster_model} (eps:{eps}, samples:{min_samples}).")
                cluster_analysis_results = {}
                for species_idx, species in enumerate(self.uniqueAtomLabels):
                    analyzer = ClusteringAnalysis()
                    cluster_analysis_results[species] = analyzer.cluster_analysis(compressed_data[species], params={'eps':eps, 'min_samples':min_samples}, 
                                                    output_dir=f'./cluster_results/{species}', use_cache=True, methods=[cluster_model])
                    print( f' Especie: {species} {cluster_model} clusters: { len(set(cluster_analysis_results[species][cluster_model]))}')


                # =========== =========== =========== =========== #
                print(" >< Linear model in cluster space.")
                structure_labels, cluster_counts, class_labels = self.generate_atom_labels_and_cluster_counts( 
                                        atom_clusters   = {key:cluster_analysis_results[key][cluster_model] for key, item in cluster_analysis_results.items()},
                                        atom_structures = {key:np.array(atom_info_by_species[key]) for key, item in atom_info_by_species.items()},
                                      )

                # save raw data #
                np.savetxt('cluster_counts.dat', cluster_counts, header=','.join(class_labels), comments='', delimiter='\t', fmt='%.6i')

                for specie, cluster_data in cluster_analysis_results.items():
                    for cluster_idx, (structure_idx, atom_idx) in enumerate(np.array(atom_info_by_species[specie])):
                        if type(self.containers[ structure_idx ].AtomPositionManager.class_ID) == type(None):
                            self.containers[ structure_idx ].AtomPositionManager.class_ID = np.zeros(self.containers[ structure_idx ].AtomPositionManager.atomCount)
                        self.containers[ structure_idx ].AtomPositionManager.class_ID[atom_idx] = cluster_data[cluster_model][cluster_idx]

                linear_analysis = LinearAnalysis(X=cluster_counts, y=energies, X_labels=class_labels )
                coefficients_cluster, predictions_cluster, residuals_cluster = linear_analysis.linear_predict(
                                        regularization = params.get('regularization', 1e-5), verbose = params.get('verbose', True), 
                                        zero_intercept = True, force_negative = False)
                linear_analysis.save_output(output_dir='linear_cluster')
                linear_analysis.analysis(output_dir='linear_cluster')

                metadata_colector = np.hstack(( metadata_colector, cluster_counts )) # add to metadata_colector #
                metadata_colector_header += ','+','.join(class_labels)
                #metadata_colector = np.hstack(( metadata_colector, coefficients_cluster.reshape(-1, 1) )) # add to metadata_colector #
                metadata_colector = np.hstack(( metadata_colector, predictions_cluster.reshape(-1, 1) )) # add to metadata_colector #
                metadata_colector_header += ',e_cl'
                metadata_colector = np.hstack(( metadata_colector, residuals_cluster.reshape(-1, 1) )) # add to metadata_colector #
                metadata_colector_header += ',r_cl'

                np.savetxt('metadata_colector.dat', metadata_colector, header=metadata_colector_header, comments='', delimiter='\t', fmt='%.6f')

                self.plot_value_distribution_by_group(
                                values=coefficients_cluster[1:],
                                labels=class_labels,
                                reference_values={u:c for u,c in zip(uniqueAtomLabels, coefficients)},
                                output_filename="chemical_potential_distribution.png" )

                # =========== =========== =========== =========== #
                print(" >< RBF interpretation.")
                self.plot_RBF(cutoff=r_cut, number_of_bins=100, output_path='rbf/', A_class=True, )
                
                print(" >> Export files.")
                self.export_files(file_location=params.get('output_path', '.'), source='xyz', label='enumerate', verbose=params.get('verbose', True))

                print(" >< RBF cluster interpretation.")
                rbf = self.plot_RBF(cutoff=r_cut, number_of_bins=100, output_path='rbf_cluster/', A_class=True, B_class=True)
                self.plot_RBF_correlation(cutoff=r_cut, number_of_bins=100, output_path='rbf_cluster/', A_class=True, B_class=True)
                
                #compressor = Compress(unique_labels=['A'])
                #optimal_factors = compressor.determine_optimal_factors( {'A':cluster_counts} )
                #print(f' >> Optimalnumber of factors {optimal_factors}')
                #compressed_data = compressor.verify_and_load_or_compress(data={'A':cluster_counts}, 
                #                        method='factor_analysis', n_components=optimal_factors, load=False)
                #compressor.plot_compression({'A':cluster_counts}, 'factor_analysis', output_file='fa_projection.png')
                #compressor.plot_factor_analysis_results(data={'A':cluster_counts}, optimal_factors=optimal_factors, output_dir='factor_analysis')


            elif abit.upper() == 'LINEAR':
                print("Performing Local Linear Regression analysis...")

                linear_analysis = LinearAnalysis(X=compositions, y=energies, X_labels=self.uniqueAtomLabels )
                coefficients, predictions, residuals = linear_analysis.linear_predict(
                                        regularization = params.get('regularization', 1e-5), verbose = params.get('verbose', True), 
                                        zero_intercept = True, force_negative = False)
                linear_analysis.save_output(output_dir='linear')
                linear_analysis.analysis(output_dir='linear')

        print("Ab Initio Thermodynamics analysis completed.")




