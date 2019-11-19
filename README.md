# Automated Fibrosis Analysis Toolkit (AFAT)
## Setup
### Windows
1. Python 3.7 will need to be installed prior to seting up AFAT. Python 3.7 can be 
    downloaded from python.org. The x86-64 executable installer is reccommended,
    as the default install configuration will set python to open .py files by 
    double clicking. If it is installed correctly opening a cmd or powershell 
    window and typing py should start a python prompt.
    ![](./images/command_prompt_py.png)
2. From a terminal window navigate to the folder where AFAT has been downloaded. 
    This can also be achieved by opening the AFAT folder in File Explorer,
    Right Clicking + Shift, and selecting 'Open Powershell here' or 'Open 
    Command Prompt here'.
    ![](./images/file_explorer_open_cmd.png)
3.  From the prompt window, to install the dependancies run the command 
    `py -m pip install -r requirments.txt`. Alternatively install these 
    dependancies: matplotlib, scipy, scikit-image, scikit-learn, xlrd, xlsxwriter,
    numpy, PyQt5, pillow.
    ![](./images/command_prompt_install.png)
4. To run AFAT either open the command prompt/powershell as directed in (3) and
   run `py 'Automated Fibrosis Analysis Toolkit.py'` or double-click on 
   *Automated Fibrosis Analysis Toolkit.py* from the file explorer.

### Mac/Linux
1. Python 3 will need to be installed prior to seting up AFAT. Python 3 can be 
    installed via your package manager in linux. If it is installed correctly
    opening a terminal and typing python (in some distributions such as Ubuntu
    the command is python3) should start a python prompt.
2. From a terminal window navigate to the folder where AFAT has been downloaded. 
    From there run the command `pip install -r requirments.txt`. Alternatively 
    install these dependancies: matplotlib, scipy, numpy, scikit-image, scikit-learn,
    Tkinter.
3. To run MAT either use the command `python 'Automated Fibrosis Analysis Toolkit.py'` or
    double-click on *Automated Fibrosis Analysis Toolkit.py* from the file explorer.

## Setup
1. Python 3 will need to be installed prior to seting up AFAT. Python 3 can be 
    downloaded from python.org, or installed via your package manager in linux. 
    If it is installed correctly opening a terminal(cmd/powershell in windows)
    and typing python (in some distributions such as Ubuntu the command is 
    python3) should start a python prompt.
2. From a terminal window navigate to the folder where AFAT has been downloaded. 
    From there run the setup.py to ensure all dependancies are installed. Run
    with the command `python setup.py install`. Alternatively install these 
    dependancies: matplotlib, scipy, numpy, scikit-image, scikit-learn, Tkinter.
3. To run AFAT either use the command `python 'Automated Fibrosis Analysis Toolkit.py'`
    or double-click on *Automated Fibrosis Analysis Toolkit.py* from the file
    explorer.
