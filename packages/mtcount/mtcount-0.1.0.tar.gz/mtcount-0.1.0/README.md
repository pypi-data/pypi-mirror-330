# MTC 

## Overview  
A light weight python tool for detecting and counting metastatic cells in cancerous tissue image samples utilising a unique combination of image transformation techniques. Can be integrated with ML/DL algorithms for predicting cancer by simplifying learning data complexity.

##  Local Installation  
```bash
git clone https://github.com/abd-ur/MTC_Count.git
cd MTC_Count
pip install .
```
##  PyPi Module Installation  
```bash
pip install mcount
```
## Install Dependencies
```bash
pip install -r requirements.txt
```

##  Usage 
```bash
import mcount
detected_cells = mcount.circle("input_image","output_image", alpha, beta)
```
## Note
Output path if not provided, results will be saved at the default path.  
**Alpha** and **Beta** by default is set to 190 and 550, but can be changed by argument 'alpha' and 'beta' while function call.  
Gradient intensity below Alpha is ignored as not an edge, higher Alpha removes more weak edges.  
Gradient intensity above Beta is considered strong edge, lower Beta makes it more sensitive to edges.  
Function returns coordinates of detected cells along with radius.  

## Contributing 
Improvements, bug fixes, and new features are welcomed. Feel free to contribute.

**Fork the Repository** – Click the "Fork" button on GitHub.  
**Clone Your Fork** – Download the code to your local machine:

## Contact  
For any issues, questions, or feature requests, feel free to reach out:

**Email:** theabdur10@gmail.com  
**Portfolio:** https://abd-ur.github.io  
