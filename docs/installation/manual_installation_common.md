
### Method 1 - User install using the PIP package

You can install kalliope on your system by using Pypi:
```bash
sudo pip install kalliope
```

### Method 2 - Manual setup using sources

Clone the project:
```bash
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope
```

Install the project:
```bash
sudo python setup.py install
```

### Method 3 - Developer install using Virtualenv

Install the `python-virtualenv` package:
```bash
sudo apt-get install python-virtualenv
```

Clone the project:
```bash
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope
```

Generate a local python environment:
```bash
virtualenv venv
```

Install the project using the local environment:
```bash
venv/bin/pip install --editable .
```

Activate the local environment:
```bash
source venv/bin/activate
```

### Method 4 - Developer, dependencies install only

Clone the project:
```bash
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope
```

Install the python dependencies directly:
```bash
sudo pip install -r install/files/python_requirements.txt
```
