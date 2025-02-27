import os
import numpy as np
import pandas as pd
from scipy import ndimage
from nilearn import image
from nilearn.image import resample_to_img


def get_region_phenotypes(
    phenotype_nii_path,
    atlas_nii_path,
    info_df,
    label_column='Atlas Index',
    region_column='Anatomical Name',
    method='mean',
    resample = True
):
    """
    Calculate region-wise phenotypes based on an input NIfTI file and an atlas NIfTI file.

    Parameters:
        phenotype_nii_path (str): Path to the phenotype NIfTI file.
        atlas_nii_path (str): Path to the atlas NIfTI file.
        info_df (pd.DataFrame): DataFrame containing atlas region information.
        label_column (str): Column in info_df that represents the label values in the atlas. 
        region_column (str): Column in info_df that represents the region names. 
        statistic (str): Statistic to calculate for each region. Options: 'mean', 'sum'. Default is 'mean'.
        resample(bool): Whether to resample the phenotype image to match the atlas image. Default is True.

    Returns:
        pd.DataFrame: A DataFrame containing region-wise statistics, sorted by the order in info_df.
    """
    # Load the phenotype and atlas NIfTI files
    phenotype_img = image.load_img(phenotype_nii_path)
    atlas_img = image.load_img(atlas_nii_path)

    if resample and phenotype_img.shape != atlas_img.shape:
        print("Resampling phenotype image to match atlas image resolution...")
        phenotype_img = resample_to_img(phenotype_img, atlas_img)

    phenotype_data = np.asarray(phenotype_img.dataobj)
    atlas_data = np.asarray(atlas_img.dataobj)

    if phenotype_data.shape != atlas_data.shape:
        raise ValueError("The phenotype and atlas NIfTI files must have the same shape after resampling.")

    # Extract labels from the info DataFrame
    labels = info_df[label_column].values

    # Calculate the region phenotype for each label
    if method == 'mean':
        region_values = ndimage.mean(phenotype_data, labels=atlas_data, index=labels)
    elif method == 'sum':
        region_values = ndimage.sum(phenotype_data, labels=atlas_data, index=labels)
    else:
        raise ValueError(f"Unsupported statistic method: {method}. Choose from 'mean', 'sum'.")

    # Create a DataFrame for the results
    result_df = info_df.copy()
    result_df['Phenotype'] = region_values

    # Sort the DataFrame by the order in info_df
    result_df = result_df[[region_column,label_column,'Phenotype']]
    result_df.columns = ['Region name','Region label','Phenotype']
    result_df = result_df.set_index('Region name')
    result_df.reindex(info_df[region_column].to_list())
    result_df = result_df.reset_index()

    return result_df

