# Reading Agilent FTIR files

The `AgilentIRFile` class reads single-tile (`*.seq`) and multi-tile mosaic (`*.dmt`) hyperspectral images from Agilent FTIR instruments with a focal plane array.

## Install

```bash
pip install -e .
```

## Example — inspect a file

```python
from pprint import pprint
from agilentirformats import AgilentIRFile

filename = "inputs/my_project/myfile.dmt"

reader = AgilentIRFile()
reader.read(filename)

xvalues = reader.xvalues          # wavenumbers
intensities = reader.intensities  # (height, width, datapoints)
metadata = reader.metadata

print(xvalues.shape)
print(intensities.shape)
pprint(metadata)
```

## Example — export HDF5

```python
from agilentirformats import AgilentIRFile

AgilentIRFile("inputs/my_project/myfile.dmt").export_hdf5()
```

## Properties and methods

| Member | Description |
|--------|-------------|
| `wavenumbers` / `xvalues` | Spectral axis |
| `data` / `intensities` | Hyperspectral cube |
| `total_spectrum` | Sum of intensity vs wavenumber |
| `total_image` | Sum of intensity vs position |
| `metadata` | Acquisition / geometry metadata |
| `hdf5_metadata` | Hierarchy suited to HDF5 export |
| `read()` | Open and parse a file |
| `export_hdf5()` | Write an HDF5 representation |

Static helpers: `filetype()`, `filefilter()`, `isreadable()`, `version()`.

## Dependencies

- `python >= 3.10`
- `numpy`, `h5py`

Upstream author: Alex Henderson (University of Manchester). See root README and CITATION.cff.
