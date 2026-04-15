#!/usr/bin/env python
"""Simplified Morphology + Spectroscopy Analysis

Usage:
    python simplified_morphology_analysis.py --input <file_or_directory> [--output results.csv]

This script finds a .dmt file, loads hyperspectral IR data, segments particles using
threshold = mean + 2 * std, performs PCA-based spectrum reduction, matches each
particle to the OS cluster library, and writes results to CSV.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from skimage.measure import label, regionprops

from agilent_ir_file import AgilentIRFile
import agilent_to_python as a2p
from calc_pca import cpca
import spec_process as spec_p
import library_OS_fit as lib_OS

# ===== CONFIGURATION =====
# Set your default directory path here (change this to your local drive path)
DEFAULT_DATA_PATH = r"C:\Users\Stephanie.Wang\Downloads"  # Modify this path to your data folder
# ========================


def find_dmt_files(root_path: Path) -> list[Path]:
    """Find all .dmt files in subdirectories of the given root path."""
    dmt_files = []
    for dmt_file in root_path.rglob('*.dmt'):
        dmt_files.append(dmt_file)
    return sorted(dmt_files)


def find_dmt_file(path: Path) -> Path:
    if path.is_file() and path.suffix.lower() == '.dmt':
        return path
    if not path.is_dir():
        raise FileNotFoundError(f'Path not found: {path}')

    dmt_files = sorted(path.glob('*.dmt'))
    if not dmt_files:
        raise FileNotFoundError(f'No .dmt files found in {path}')
    if len(dmt_files) > 1:
        print(f'Found {len(dmt_files)} .dmt files in {path}. Using: {dmt_files[0]}')
    return dmt_files[0]


def load_agilent_data(filename: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    reader = AgilentIRFile()
    reader.read(str(filename))

    wavenumbers = a2p.data_wns(reader).astype(np.float32)
    intensities = reader.intensities.astype(np.float32)
    total_image = reader.total_image.astype(np.float32)
    metadata = reader.metadata if isinstance(reader.metadata, dict) else {}
    return wavenumbers, intensities, total_image, metadata


def match_library(spectrum: np.ndarray, library_spectra: np.ndarray) -> tuple[int, float]:
    spectrum = (spectrum - np.mean(spectrum)) / (np.std(spectrum) + 1e-8)
    library_norm = (
        library_spectra - np.mean(library_spectra, axis=1, keepdims=True)
    ) / (np.std(library_spectra, axis=1, keepdims=True) + 1e-8)

    correlations = np.dot(library_norm, spectrum) / spectrum.shape[0]
    if not np.isfinite(correlations).any():
        return -1, 0.0

    best_ix = int(np.nanargmax(correlations))
    return best_ix, float(correlations[best_ix])


def analyze_particle(
    prop,
    intensities: np.ndarray,
    wavenumbers: np.ndarray,
    library_wavenos: np.ndarray,
    library_spectra: np.ndarray,
) -> dict:
    coords = prop.coords
    spectra = np.asarray([intensities[int(row), int(col)] for row, col in coords], dtype=np.float32)

    if spectra.size == 0 or spectra.shape[1] == 0:
        return {
            'label': prop.label,
            'polymer': 'small particle',
            'best_pr': 0.0,
            'pixel_count': 0,
            'error': 'empty spectrum',
        }

    if spectra.shape[0] < 5:
        return {
            'label': prop.label,
            'polymer': 'small particle',
            'best_pr': 0.0,
            'pixel_count': spectra.shape[0],
        }

    try:
        pca_components = cpca(spectra, range(1))
        if len(pca_components) == 0 or pca_components[0].size == 0:
            raise ValueError('PCA returned no components')
        representative = pca_components[0].astype(np.float32)
    except Exception as exc:
        return {
            'label': prop.label,
            'polymer': 'error',
            'best_pr': 0.0,
            'pixel_count': spectra.shape[0],
            'error': f'PCA failure: {exc}',
        }

    if representative.shape[0] != wavenumbers.shape[0]:
        representative = np.interp(
            wavenumbers,
            np.linspace(wavenumbers[0], wavenumbers[-1], representative.shape[0]),
            representative,
        ).astype(np.float32)

    try:
        processed = spec_p.proc(representative, 5, 2, wavenumbers, library_wavenos)
        if processed.size == 0:
            raise ValueError('processed spectrum is empty')
        best_ix, best_pr = match_library(processed, library_spectra)
    except Exception as exc:
        return {
            'label': prop.label,
            'polymer': 'error',
            'best_pr': 0.0,
            'pixel_count': spectra.shape[0],
            'error': f'processing failure: {exc}',
        }

    try:
        polymer_name = lib_OS.catID(best_ix)
    except Exception:
        polymer_name = 'unknown polymer'
        best_pr = 0.0

    if best_pr < 0.3:
        polymer_name = f'{polymer_name} (low confidence)'

    return {
        'label': prop.label,
        'polymer': polymer_name,
        'best_pr': best_pr,
        'pixel_count': spectra.shape[0],
    }


def build_analysis(
    dmt_file: Path,
    output_path: Path,
    csv_library: Path | None = None,
    min_pixels: int = 5,
) -> pd.DataFrame:
    print(f'Using .dmt file: {dmt_file}')

    wavenumbers, intensities, total_image, metadata = load_agilent_data(dmt_file)
    print(f'Loaded data: intensities={intensities.shape}, total_image={total_image.shape}')

    threshold = float(total_image.mean() + 2 * total_image.std())
    print(f'Using threshold = mean + 2*std = {threshold:.2f}')

    mask = total_image > threshold
    lbls, num_particles = label(mask, return_num=True)
    props = regionprops(lbls)
    print(f'Found {num_particles} particle candidates')

    if csv_library is None:
        csv_library = Path('OS_clusters_derint.csv')
    library_spectra = pd.read_csv(csv_library).values.T.astype(np.float32)
    library_wavenos = lib_OS.get_lib_wns().astype(np.float32)

    results = []
    for i, prop in enumerate(props, start=1):
        if prop.area < min_pixels:
            results.append({
                'fileID': dmt_file.name,
                'label': prop.label,
                'polymer': 'small particle',
                'best_pr': 0.0,
                'pixel_count': prop.area,
            })
            continue

        result = analyze_particle(prop, intensities, wavenumbers, library_wavenos, library_spectra)
        result['fileID'] = dmt_file.name
        results.append(result)
        if i % 50 == 0 or i == len(props):
            print(f'Processed {i}/{len(props)} particles')

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(['fileID', 'label']).reset_index(drop=True)

    pixel_size_microns = float(metadata.get('fpasize', 64))
    results_df['area_um2'] = results_df['pixel_count'] * (pixel_size_microns ** 2)
    results_df['area_mm2'] = results_df['area_um2'] / 1_000_000

    return results_df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Simplified Morphology + Spectroscopy Analysis')
    parser.add_argument('--input', '-i', help='Path to .dmt file or directory containing .dmt files')
    parser.add_argument('--output', '-o', default='simplified_particle_results.csv', help='Output CSV path')
    parser.add_argument('--library', '-l', default='OS_clusters_derint.csv', help='Library CSV file path')
    parser.add_argument('--min-pixels', type=int, default=5, help='Minimum pixels for a valid particle')
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # Prompt for directory if not provided
    if args.input is None:
        print(f'Default data path: {DEFAULT_DATA_PATH}')
        input_path_str = input('Enter the directory path to search for .dmt files (or press Enter for default): ').strip(' "\'')
        if not input_path_str:
            input_path = Path(DEFAULT_DATA_PATH)
            print(f'Using default path: {input_path}')
        else:
            input_path = Path(input_path_str)
    else:
        input_path = Path(args.input)

    while not input_path.exists():
        print(f'Path does not exist: {input_path}', file=sys.stderr)
        create_dir = input('Create the directory? (y/n): ').strip().lower()
        if create_dir == 'y':
            try:
                input_path.mkdir(parents=True, exist_ok=True)
                print(f'Created directory: {input_path}')
                break
            except Exception as e:
                print(f'Failed to create directory: {e}', file=sys.stderr)
                return 1
        else:
            input_path_str = input('Enter a new directory path: ').strip(' "\'')
            if not input_path_str:
                input_path = Path(DEFAULT_DATA_PATH)
            else:
                input_path = Path(input_path_str)

    # Set output path to input directory if using default output filename
    if args.output == 'simplified_particle_results.csv':
        args.output = str(input_path / 'simplified_particle_results.csv')
        print(f'Output will be saved to: {args.output}')

    # Find all .dmt files
    if input_path.is_file() and input_path.suffix.lower() == '.dmt':
        dmt_files = [input_path]
    else:
        dmt_files = find_dmt_files(input_path)
        if not dmt_files:
            print(f'No .dmt files found in {input_path}', file=sys.stderr)
            return 1

    print(f'Found {len(dmt_files)} .dmt file(s) to process:')
    for dmt_file in dmt_files:
        print(f'  - {dmt_file}')

    # Process all .dmt files
    all_results = []
    for dmt_file in dmt_files:
        try:
            results_df = build_analysis(
                dmt_file=dmt_file,
                output_path=Path(args.output),
                csv_library=Path(args.library),
                min_pixels=args.min_pixels,
            )
            all_results.append(results_df)
        except Exception as exc:
            print(f'Error processing {dmt_file}: {exc}', file=sys.stderr)
            continue

    if not all_results:
        print('No results to save.', file=sys.stderr)
        return 1

    # Combine all results
    combined_results = pd.concat(all_results, ignore_index=True)
    combined_results = combined_results[
        ['fileID', 'label', 'polymer', 'best_pr', 'pixel_count', 'area_mm2']
    ]
    combined_results.to_csv(args.output, index=False)
    print(f'\nWrote combined results to {args.output}')
    print(f'Total particles analyzed: {len(combined_results)}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())