import dataclasses
from dataclasses import dataclass, asdict
import numpy as np


@dataclass
class SpectralIndex:
    """
    Class for keeping track of processing parameters.
    
    Parameters
    ---------
    index_name: str
        name of index
    index_type: str
        one of 'Ratio', 'RABD', 'RABA', 'RMean', 'RABDnorm'
    index_description: str
        description of index
    left_band: int
        left band to compute index
    right_band: int
        right band to compute index
    trough_band: int
        trough band to compute index
    numerator_band: int
        numerator band to compute ratio index
    denominator_band: int
        denominator band to compute ratio index
    left_band_default: int
        default left band to compute index
    right_band_default: int
        default right band to compute index
    trough_band_default: int
        default trough band to compute index
    numerator_band_default: int
        default numerator band to compute ratio index
    denominator_band_default: int
        default denominator band to compute ratio index
    index_map: np.ndarray
        index map
    index_proj: np.ndarray
        index projection
    index_map_range: nd.array
        range of index map for plotting
    colormap: str
        colormap for index map
    smooth_proj_window: int
        window for smoothing index projection
    
    """

    index_name: str = None
    index_type: str = None
    index_description: str = None
    left_band: int = None
    right_band: int = None
    middle_band: int = None
    left_band_default: int = None
    right_band_default: int = None
    middle_band_default: int = None
    index_map: np.ndarray = None
    index_proj: np.ndarray = None
    index_map_range: np.ndarray = None
    colormap: str = 'viridis'
    smooth_proj_window: int = None
    
    def __post_init__(self):
        """Use defaults for bands."""

        if self.left_band is None:
            self.left_band = self.left_band_default
        if self.right_band is None:
            self.right_band = self.right_band_default
        if self.middle_band is None:
            self.middle_band = self.middle_band_default

        if self.index_description is None:
            self.index_description = self.index_name

        if self.index_map_range is None:
            self.index_map_range = [0,1]

    def dict_spectral_index(self):
        """Return dataclass as dict and exclude large numpy arrays."""


        dict_to_save = dataclasses.asdict(self)
        del dict_to_save['index_map']
        del dict_to_save['index_proj']
        for key in dict_to_save:
            if isinstance(dict_to_save[key], np.generic):
                dict_to_save[key] = dict_to_save[key].item()
            if isinstance(dict_to_save[key],(list, np.ndarray)):
                if isinstance(dict_to_save[key][0], np.generic):
                    dict_to_save[key] = [i.item() for i in dict_to_save[key]]
        return dict_to_save
    