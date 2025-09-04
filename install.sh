python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
pip uninstall numpy
pip install "numpy<2.0"