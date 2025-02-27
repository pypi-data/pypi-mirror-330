from pathlib import Path
import numpy as np
from .io import get_data_background_path
from .sediproc import correct_save_to_zarr
from ..data_structures.imchannels import ImChannels
from ..data_structures.parameters import Param

def batch_preprocessing(folder_to_analyze, export_folder, background_text='_WR_',
                        min_max_band=None, downsample_bands=1, background_correction=True, destripe=True,
                        use_dask=True, chunk_size=1000, use_float=True):

    export_folder = Path(export_folder)
    _, _, white_file_path, dark_for_white_file_path, dark_for_im_file_path, imhdr_path = get_data_background_path(folder_to_analyze, background_text=background_text)
    folder_to_analyze_name = folder_to_analyze.name
    export_folder = export_folder.joinpath(folder_to_analyze_name)

    if not export_folder.is_dir():
        export_folder.mkdir()

    param = Param(
        project_path=export_folder,
        file_path=imhdr_path,
        white_path=white_file_path,
        dark_for_im_path=dark_for_im_file_path,
        dark_for_white_path=dark_for_white_file_path,
        main_roi=[],
        rois=[])
    
    correct_save_to_zarr(
        imhdr_path=imhdr_path,
        white_file_path=white_file_path,
        dark_for_im_file_path=dark_for_im_file_path,
        dark_for_white_file_path=dark_for_white_file_path,
        zarr_path=export_folder.joinpath('corrected.zarr'),
        band_indices=None,
        min_max_bands=min_max_band,
        downsample_bands=downsample_bands,
        background_correction=background_correction,
        destripe=destripe,
        use_dask=use_dask,
        chunk_size=chunk_size,
        use_float=use_float
        )
    imchannels = ImChannels(export_folder.joinpath('corrected.zarr'))
    
    # add a main roi
    param.main_roi = [[
        0, 0,
        imchannels.nrows, 0,
        imchannels.nrows, imchannels.ncols,
        0, imchannels.ncols
        ]]
    
    # add sub-rois
    min_half_width = np.max([2, imchannels.ncols // 20])
    param.rois = np.array([
        [[
        0, imchannels.ncols // 2 - min_half_width,
        imchannels.nrows, imchannels.ncols // 2 - min_half_width,
        imchannels.nrows, imchannels.ncols // 2 + min_half_width,
        0, imchannels.ncols // 2 + min_half_width
        ]]
        ]).astype(int)
    param.rois = [[[z.item() for z in x] for x in y] for y in param.rois]
    param.save_parameters()