from dscribe.descriptors import SOAP
import numpy as np
from tqdm import tqdm
import os
from typing import Dict, List, Tuple, Union
from collections import defaultdict 

try:
    from ase import Atoms
    from ase.cell import Cell
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing ASE: {str(e)}\n")
    del sys

class SOAP_analysis:
    def __init__(self, uniqueAtomLabels:list=None, 
            symbols:list=None, positions:list=None, cell:list=None,
            r_cut:float=None, n_max:float=None, l_max:float=None, sigma:float=None,verbose:bool=None):
        self.r_cut = r_cut
        self.n_max = n_max
        self.l_max = l_max
        self.sigma = sigma

        self.symbols    = symbols
        self.positions  = positions
        self.cell       = cell 

        self.uniqueAtomLabels = uniqueAtomLabels
        self.descriptors = None


    #achedir = './cache_dir'
    #memory = Memory(cachedir, verbose=0) 
    #@memory.cache   
    def calculate_soap_descriptors(self, 
                symbols:np.array=None, positions:np.array=None, cell:np.array=None, 
                r_cut: float = None, n_max: int = None, l_max: int = None, sigma: float = None):
        """
        Calculate Smooth Overlap of Atomic Positions (SOAP) descriptors for atomic structures.

        This method computes SOAP descriptors for each atom in the stored containers,
        organizing the results by atomic species.

        Args:
            r_cut (float, optional): Cutoff radius for atomic interactions. Defaults to 5.0.
            n_max (int, optional): Maximum number of radial basis functions. Defaults to 8.
            l_max (int, optional): Maximum degree of spherical harmonics. Defaults to 6.
            sigma (float, optional): The standard deviation of the Gaussian smearing function. Defaults to 0.03.

        Returns:
            tuple: A tuple containing two dictionaries:
                - descriptors_by_species: SOAP descriptors for each atomic species.
                - atom_info_by_species: Information about atom indices and container indices for each species.

        Note:
            This method assumes the existence of 'self.containers' and 'self.uniqueAtomLabels'.
        """
        # Set default values if None is provided
        r_cut = self.r_cut if r_cut is None else r_cut
        n_max = self.n_max if n_max is None else n_max
        l_max = self.l_max if l_max is None else l_max
        sigma = self.sigma if sigma is None else sigma

        symbols     = self.symbols      if symbols      is None else symbols
        positions   = self.positions    if positions    is None else positions
        cell        = self.cell         if cell         is None else cell

        # Initialize SOAP descriptor
        soap = SOAP(species=self.uniqueAtomLabels, periodic=True, r_cut=r_cut, 
                    n_max=n_max, l_max=l_max, sigma=sigma, sparse=False)

        # Initialize dictionaries to store results
        descriptors_by_species = defaultdict(list)
        atom_info_by_species = defaultdict(list)

        # Iterate through containers to calculate descriptors
        for idx, (s,p,c) in enumerate(zip(symbols, positions, cell)):

            # Create ASE Atoms object from container data
            atoms = Atoms(symbols=s, 
                          positions=p, 
                          cell=Cell(c),
                          pbc=True)

            # Calculate SOAP descriptors for the current structure 
            descriptors = soap.create(atoms) 
 
            # Organize descriptors and atom info by species
            for atom_idx, (specie, descriptor) in enumerate(zip(s, descriptors)):
                descriptors_by_species[specie].append(descriptor)
                atom_info_by_species[specie].append((idx, atom_idx))
        
        # Convert descriptor lists to numpy arrays for each species
        for species in descriptors_by_species:
            descriptors_by_species[species] = np.array(descriptors_by_species[species])
        
        self.descriptors_by_species, self.atom_info_by_species = descriptors_by_species, atom_info_by_species

        return descriptors_by_species, atom_info_by_species

    def save_descriptors(self, descriptors_by_species:list=None, atom_info_by_species:list=None, output_dir:str='./'):
        """
        Save SOAP descriptors and corresponding atom information to files.

        This method saves the calculated SOAP descriptors and associated atom information
        for each atomic species to separate files in the specified output directory.

        Args:
            descriptors_by_species (dict): A dictionary containing SOAP descriptors for each species.
                                           Key: atomic species, Value: numpy array of descriptors.
            atom_info_by_species (dict): A dictionary containing atom information for each species.
                                         Key: atomic species, Value: list of tuples (structure_index, atom_index).
            output_dir (str): Path to the directory where files will be saved.

        Returns:
            None

        Note:
            - Creates the output directory if it doesn't exist.
            - Saves descriptors as .npy files and atom information as .txt files.
            - Prints information about saved files to the console.
        """
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        descriptors_by_species = self.descriptors_by_species if not descriptors_by_species else descriptors_by_species
        atom_info_by_species = self.atom_info_by_species if not atom_info_by_species else atom_info_by_species

        # Iterate through each species and save its data
        for species, descriptors in descriptors_by_species.items():
            # Save descriptors as numpy array
            desc_filename = os.path.join(output_dir, f"descriptors_{species}.npy")
            np.save(desc_filename, descriptors)
            print(f"Descriptors for {species} saved to {desc_filename}")

            # Save atom information as text file
            info_filename = os.path.join(output_dir, f"atom_info_{species}.txt")
            with open(info_filename, 'w') as f:
                # Write header
                f.write("descriptor_index,structure_index,atom_index\n")
                # Write data for each atom
                for desc_idx, (struct_idx, atom_idx) in enumerate(atom_info_by_species[species]):
                    f.write(f"{desc_idx},{struct_idx},{atom_idx}\n")
            print(f"Atom information for {species} saved to {info_filename}")

    def verify_and_load_soap(self, uniqueAtomLabels:list=None, output_dir='SOAPs'):
        """
        Verify the existence of SOAP descriptor files and load them if they exist.

        This method checks for the presence of SOAP descriptor and atom information files
        for each atomic species in the specified directory. If all files exist, it loads
        the data and returns it. If any file is missing, it returns False.

        Args:
            output_dir (str): Path to the directory where SOAP files are stored. Default is 'SOAPs'.

        Returns:
            tuple or bool: If all files exist, returns a tuple containing:
                           (descriptors_by_species, atom_info_by_species)
                           If any file is missing, returns False.

        Note:
            - Assumes the file naming convention: 'descriptors_{species}.npy' and 'atom_info_{species}.txt'
            - Requires self.uniqueAtomLabels to be defined with the list of atomic species.
        """
        uniqueAtomLabels = self.uniqueAtomLabels if type(uniqueAtomLabels) == type(uniqueAtomLabels) else uniqueAtomLabels

        descriptors_by_species = {}
        atom_info_by_species = {}

        for species in tqdm(uniqueAtomLabels, desc="Verifying and loading soap"):
            desc_filename = os.path.join(output_dir, f"descriptors_{species}.npy")
            info_filename = os.path.join(output_dir, f"atom_info_{species}.txt")

            # Check if both files exist for the current species
            if not (os.path.exists(desc_filename) and os.path.exists(info_filename)):
                print(f"Missing SOAP files for species {species}")
                return False

            # Load descriptor data
            descriptors_by_species[species] = np.load(desc_filename)

            # Load atom information
            atom_info_by_species[species] = []
            with open(info_filename, 'r') as f:
                next(f)  # Skip header
                for line in f:
                    _, struct_idx, atom_idx = line.strip().split(',')
                    atom_info_by_species[species].append((int(struct_idx), int(atom_idx)))

        print("All SOAP files found and loaded successfully.")
        return descriptors_by_species, atom_info_by_species
