# agilent-ir-formats

## Agilent File Format Handling for Infrared Spectroscopy
Author: Alex Henderson <[alex.henderson@manchester.ac.uk](alex.henderson@manchester.ac.uk)>              
Version: 0.2.0  
Copyright: (c) 2018-2023 Alex Henderson   

## About ##
Python package to read hyperspectral image files produced by infrared spectroscopy instrumentation from Agilent Technologies, Inc.
  
Currently, the code reads single or multi-tile images (*.seq files or *.dmt files) 

## Help information
``` python
Class to open, read and export the contents of an Agilent Fourier Transform Infrared (FTIR) microscopy file.

FTIR instruments from Agilent Technologies Inc., that use a focal plane array detector, can store hyperspectral
images in single 'tile' or multi-tile 'mosaic' file formats. This class can read both single and multi-tile images.
Files with a filename extension of *.seq or *.dmt are compatible.

The class has properties and methods allowing the user to explore the numeric values in the file. In addition, some
metadata values are also accessible.

Properties:
    wavenumbers     x-axis values of the spectral dimension.
    data            spectral intensities of the hyperspectral data as a 3D object (height, width, datapoints).
    total_spectrum  sum of intensity in all pixels, as a function of wavenumber.
    total_image     sum of intensity in all pixels as a function of position (height, width).
    metadata        simple metadata relating to these data.
    hdf5_metadata   metadata arranged into a hierarchy for use in HDF5 export of these data.

Methods:
    read()          open and parse a file.
    export_hdf5()   create a representation on disc of the file in the HDF5 file format.

Static methods:
    filetype()      string identifying the type of files this class reads.
    filefilter()    string identifying the Windows file extensions for files this class can read.
    isreadable()    whether this class is capable of reading a given file.
    version()       the version number of this code.
```

## Simplified Morphology + Spectroscopy Analysis

This repository includes a batch processing script for automated microplastic particle analysis from Agilent IR hyperspectral data.

### Features

- **Batch Processing**: Automatically finds and processes all .dmt files in a directory
- **Smart Thresholding**: Uses `mean + 2*std` for robust particle segmentation
- **Spectral Analysis**: PCA-based spectrum reduction and polymer identification
- **Physical Measurements**: Converts pixel counts to actual area (μm² and mm²)
- **Multi-file Support**: Processes multiple .dmt files and combines results

### Configuration

Edit the `DEFAULT_DATA_PATH` variable at the top of `batch_simplified_morphology_analysis.py`:

```python
# Set your default directory path here (change this to your local drive path)
DEFAULT_DATA_PATH = r"C:\Users\Stephanie.Wang\Downloads"  # Modify this path
```

### Quick Start

#### Option 1: Double-click launcher (Windows)
1. Double-click `run_analysis.bat`
2. Press Enter to use the default path, or enter a custom directory path
3. Wait for processing to complete

#### Option 2: Command line
```bash
# Use default path (press Enter when prompted)
python batch_simplified_morphology_analysis.py

# Process all .dmt files in a directory (output saved to that directory)
python batch_simplified_morphology_analysis.py --input "C:\path\to\directory"

# Process a single file
python batch_simplified_morphology_analysis.py --input "C:\path\to\file.dmt"

# Custom output location
python batch_simplified_morphology_analysis.py --input "C:\data" --output "C:\results\my_results.csv"
```

### Output Format

The CSV output includes:
- `dmt_file`: Name of the source .dmt file
- `label`: Particle ID within that file
- `polymer`: Identified polymer type
- `best_pr`: Confidence score (0-1)
- `pixel_count`: Number of pixels in the particle
- `area_um2`: Physical area in square microns
- `area_mm2`: Physical area in square millimeters

### Algorithm Details

1. **Data Loading**: Extracts hyperspectral cube and total absorbance image
2. **Thresholding**: `threshold = mean(image) + 2 * std(image)`
3. **Segmentation**: Connected component analysis to identify particles
4. **Spectral Processing**: PCA reduction to representative spectrum per particle
5. **Identification**: Correlation matching against polymer library
6. **Area Calculation**: Pixel count × (pixel_size)² where pixel_size = 64 μm

## Usage ##
### Example 1 ###
Open a file and display simple metadata. 

``` python
from pprint import pprint   # only for this example

from agilentirformats import AgilentIRFile

filename = r"C:\mydata\myfile\myfile.dmt"

reader = AgilentIRFile()
reader.read(filename)

xvalues = reader.xvalues
intensities = reader.intensities
metadata = reader.metadata

print(xvalues.shape)
print(intensities.shape)
pprint(metadata)

# output...

(728,)
(128, 256, 728)
{'acqdatetime': '2023-05-11T14:37:02',
 'filename': WindowsPath('C:/mydata/myfile/myfile.dmt'),
 'firstwavenumber': 898.6699159145355,
 'fpasize': 128,
 'lastwavenumber': 3702.674331665039,
 'numpts': 728,
 'xlabel': 'wavenumbers (cm-1)',
 'xpixels': 256,
 'xtiles': 2,
 'ylabel': 'absorbance',
 'ypixels': 128,
 'ytiles': 1}
```    
### Example 2 ###
Convert a file to HDF5 format in the same location.

``` python
from agilentirformats import AgilentIRFile

filename = r"C:\mydata\myfile\myfile.dmt"

AgilentIRFile(filename).export_hdf5()
```

## Requirements ##
* python >= 3.10  
* h5py
* numpy

## Licence conditions ##
Copyright (c) 2018-2023 Alex Henderson (alex.henderson@manchester.ac.uk)   
Licensed under the MIT License. See https://opensource.org/licenses/MIT      
SPDX-License-Identifier: MIT   
Visit https://github.com/AlexHenderson/agilent-ir-formats/ for the most recent version  

---
### See also:  
* MATLAB code available here: [https://bitbucket.org/AlexHenderson/agilent-file-formats/](https://bitbucket.org/AlexHenderson/agilent-file-formats/)
