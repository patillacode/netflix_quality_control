#! /bin/bash

echo "Creating a virtual environemnt under ./venv folder ..."
python3 -m venv venv
echo "Activating venv ..."
source venv/bin/activate
echo "Installing requirements..."
pip install -r requirements.txt

touch secrets.py

echo "Please enter your QC_EMAIL: "
read QC_EMAIL
echo "Please enter your QC_PASSWORD: "
read QC_PASSWORD
echo "Please enter your QC_URL: "
read QC_URL

echo "QC_EMAIL = $QC_EMAIL" >> secrets.py
echo "QC_PASSWORD = $QC_PASSWORD" >> secrets.py
echo "QC_URL = $QC_URL" >> secrets.py

echo "Configuration completed!"

echo "You can now run the bot with: python bot.py"
