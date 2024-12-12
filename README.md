# Invoice-IQ
Invoice IQ project for invoice data recognition using ML

# Steps to run the project

# Step 1: Create virtual environment for the project

On cmd : python -m venv your_venv_name

To activate the environment : your_venv_name/Scripts/activate (if windows)

your_venv_name\bin\activate (if linux/ubuntu)

# Step 2: Install the neccessary libraries and requirements

# NOTE: Make sure your environment is activated before installing and project dependencies

Go inside src/python using CMD

Run the below command to install the required libraries to rn the project

python -m pip install -r requirements.txt

After installation of libraries 

Go inside invoice_iq directory

Again run : python -m pip install -r requirements.txt 
and run : python -m pip install -e .
To install package dependendies

# Step 3: For development or training

Download and load the transformer model of spacy

python -m spacy download en_core_web_trf

# Step 4: Project UI 

Go inside directory : src\python\invoice_iq\invoice_iq

run : python invoice_app.py

To upload a testing pdf go to docs folder. Inside docs folder you will get testing pdfs 
