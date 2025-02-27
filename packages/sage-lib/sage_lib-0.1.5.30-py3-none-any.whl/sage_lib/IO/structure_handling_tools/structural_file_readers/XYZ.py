try:
    from sage_lib.master.FileManager import FileManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing FileManager: {str(e)}\n")
    del sys

try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

try:
    import re
    from typing import Optional, List, Dict, Any
    import mmap

except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing re: {str(e)}\n")
    del sys

class XYZ(FileManager):
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        super().__init__(name=name, file_location=file_location)
        self.property_info = None

    def export_as_xyz(self, file_location:str=None, save_to_file:str='w', verbose:bool=False,
                            species:bool=True, position:bool=True, energy:bool=True, forces:bool=True, charge:bool=True, magnetization:bool=True, 
                            lattice:bool=True, pbc:bool=True, time:bool=True, fixed:bool=True, class_ID:bool=True,
                            position_tag:str='pos', forces_tag:str='forces', charge_tag:str='charge', magnetization_tag:str='magnetization', energy_tag:str='energy', fixed_tag:str='fixed',
                            time_tag:str='time', pbc_tag:str='pbc', classID_tag:str='class_ID') -> str:
        """
        Export atomistic information in the XYZ format.

        Parameters:
            file_location (str): The location where the XYZ file will be saved. Ignored if save_to_file is False.
            save_to_file (bool): Flag to control whether to save the XYZ content to a file.
            verbose (bool): Flag to print additional information, if True.

        Returns:
            str: The generated XYZ content.
        """
        file_location  = file_location  if not file_location  is None else self.file_location+'config.xyz' if self.file_location is str else self.file_location
        self.group_elements_and_positions()
        
        # Dynamically determine which properties to include based on their presence and non-None status
        include_lattice = hasattr(self, 'latticeVectors') and self.latticeVectors is not None and lattice
        include_species = hasattr(self, 'atomLabelsList' ) and self.atomLabelsList is not None and species 
        include_position = hasattr(self, 'atomPositions') and self.atomPositions is not None and position
        include_forces = hasattr(self, 'total_force') and self.total_force is not None and forces
        include_charge = hasattr(self, 'charge') and self.charge is not None and charge
        
        include_magnetization = hasattr(self, 'magnetization') and self.magnetization is not None and magnetization
        include_energy = hasattr(self, 'E') and energy and self.E is not None and energy
        include_pbc = hasattr(self, 'latticeVectors') and self.latticeVectors is not None and pbc
        include_time = hasattr(self, 'time') and self.time is not None and time 
        include_fixed = hasattr(self, 'selectiveDynamics') and self.selectiveDynamics and fixed 

        include_classID = hasattr(self, 'class_ID') and self.class_ID is not None and class_ID

        # Constructing the header information dynamically
        properties_list = [
            f'Lattice="{ " ".join(map(str, self.latticeVectors.flatten())) }"' if include_lattice else '', 
            f'Properties={":".join(filter(None, [f"species:S:1" if include_species else "",  f"{position_tag}:R:3" if include_position else "", f"{forces_tag}:R:3" if include_forces else "", f"{charge_tag}:R:1" if include_charge and hasattr(self.charge, "shape") and len(self.charge.shape) > 1 else "", f"{magnetization_tag}:R:1" if include_magnetization and hasattr(self.magnetization, "shape") and len(self.magnetization.shape) > 1 else "", f"{fixed_tag}:I:3" if include_fixed else "",                f"{classID_tag}:I:1" if include_classID else "", ]))}',
            f'{energy_tag}={self.E}' if include_energy else '',
            f'{pbc_tag}="T T T"' if include_pbc else '',
            f'{time_tag}={self.time}' if include_time else ''
        ]
        properties_str = ' '.join(filter(None, properties_list))
        #            f'Properties={":".join(filter(None, [ f"species:S:1" if include_species else "",   f"{position_tag}:R:3" if include_position else "",f"{forces_tag}:R:3" if include_forces else "",f"{charge_tag}:R:1" if include_charge and hasattr(self.charge, "shape") and len(self.charge.shape) > 1 else "",f"{magnetization_tag}:R:1" if include_magnetization and hasattr(self.magnetization, "shape") and len(self.magnetization.shape) > 1 else "",f"{fixed_tag}:I:3" if include_fixed else "",                f"{classID_tag}:I:1" if include_classID else "",                ]))}',
        # Preparing atom data lines
        atom_lines = [
            f"{self.atomLabelsList[i]} {' '.join(map('{:13.10f}'.format, self.atomPositions[i])) if include_position else ''} \
              {' '.join(map('{:14.10f}'.format, self.total_force[i])) if include_forces else ''} \
              {' '.join(map('{:14.10f}'.format, self.charge[i] if np.ndim(self.charge) == 1 else [self.charge[i, -1]])) if include_charge else ''} \
              {' '.join(map('{:14.10f}'.format, self.magnetization[i] if np.ndim(self.magnetization) == 1 else [self.magnetization[i, -1]])) if include_magnetization else ''} \
              {' '.join(map('{:2d}'.format, np.array(self.atomicConstraints[i], dtype=np.int32) )) if include_fixed else ''} \
              {np.array(self.class_ID[i],dtype=np.int32) if include_classID and i < len(self.class_ID) else '-1'} "
            for i in range(self.atomCount)
        ]

        # Combining header and atom data
        xyz_content = f"{self.atomCount}\n{properties_str}\n" + "\n".join(atom_lines)+ "\n"

        # Saving to file if required
        if file_location and save_to_file != 'none':
            with open(file_location, save_to_file) as f:
                f.write(xyz_content)
            if verbose:
                print(f"XYZ content saved to {file_location}")

        return xyz_content

    def read_XYZ(self, file_location: Optional[str] = None, lines: Optional[List[str]] = None, 
                 verbose: bool = False, tags: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Reads and parses data from an extended XYZ configuration file.

        Parameters:
            file_location (str, optional): Location of the XYZ file.
            lines (list, optional): List of lines from the file to be read directly if provided.
            verbose (bool, optional): Enables detailed logging if set to True.
            tags (dict, optional): Dictionary of tags for backward compatibility (not used in this implementation).
            **kwargs: Additional keyword arguments for backward compatibility.

        Returns:
            dict: Parsed data including position, atomCount, species, and other available properties.
        """
        file_location = file_location or self.file_location
        if not lines and not file_location:
            raise ValueError("Either 'lines' or 'file_location' must be provided.")

        lines = lines or self.read_file(file_location)
        
        if len(lines) < 2:
            raise ValueError("File must contain at least 2 lines.")

        self.atomCount = int(lines[0].strip())
        if self.atomCount <= 0:
            raise ValueError(f"Invalid number of atoms: {self.atomCount}")

        self._parse_header(lines[1])
        self._parse_atom_data(lines[2:])

        return {
            'position': self.atomPositions,
            'atomCount': self.atomCount,
            'species': self.atomLabelsList,
            'forces': self.total_force,
            'charge': self.charge,
            'magnetization': self.magnetization,
            'latticeVectors': self.latticeVectors,
            'energy': self.E,
            'pbc': self.pbc,
        }

    def _parse_header(self, header_line: str) -> None:
        """Parses the header line of the extended XYZ format."""
        header_parts = re.findall(r'(\w+)=("[^"]+"|[^\s]+)', header_line)
        
        for key, value in header_parts:
            if key == 'Lattice':
                self.latticeVectors = np.array(list(map(float, value.strip('"').split()))).reshape(3, 3)
            elif key == 'Properties':
                self._parse_properties(value.strip('"'))
            elif key == 'energy':
                self.E = float(value)
            elif key == 'pbc':
                self.pbc = [v.lower() == 't' for v in value.strip('"').split()]
            else:
                self.info_system[key] = value

    def _parse_properties(self, properties_str: str) -> None:
        """Parses the Properties string to determine the structure of atom data."""
        self.property_info = []
        parts = properties_str.split(':')
        for i in range(0, len(parts), 3):
            name, dtype, ncols = parts[i:i+3]
            self.property_info.append((name, dtype, int(ncols)))

    def _parse_atom_data(self, atom_lines: List[str]) -> None:
        """Parses the atom data based on the Properties specification."""
        data = np.array([line.split() for line in atom_lines if line.strip()])
        
        if len(data) != self.atomCount:
            raise ValueError(f"Number of atom lines ({len(data)}) does not match atom count ({self.atomCount})")

        col_index = 0
        for name, dtype, ncols in self.property_info:
            end_index = col_index + ncols
            if end_index > data.shape[1]:
                raise ValueError(f"Not enough columns in data for property {name}")

            if dtype == 'S':
                setattr(self, name, data[:, col_index])
            elif dtype == 'R':
                setattr(self, name, data[:, col_index:end_index].astype(float) )


            elif dtype == 'I':

                if ncols == 1:
                    setattr(self, name, data[:, col_index].astype(int))
                else:
                    setattr(self, name, data[:, col_index:end_index].astype(int))


            col_index = end_index

        # Assign specific properties to class attributes
        self.atomLabelsList = getattr(self, 'species', None)
        self.atomPositions = getattr(self, 'pos', None)
        self.total_force = getattr(self, 'forces', None)
        self.charge = getattr(self, 'charge', None)
        self.magnetization = getattr(self, 'magnetization', None)

    @staticmethod
    def read_file(file_location: str) -> List[str]:
        with open(file_location, 'r') as f:
            return f.readlines()

    def read_file(self, file_location, strip=True):
        """
        Reads the content of a file.

        Parameters:
            file_location (str): The location of the file to read.
            strip (bool, optional): Determines if lines should be stripped of whitespace.

        Yields:
            str: Lines from the file.
        """
        with open(file_location, 'r') as f:
            for line in f:
                yield line.strip() if strip else line



