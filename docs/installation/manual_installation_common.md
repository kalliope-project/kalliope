> **Note:** Python 2 is not supported anymore

### Method 1 - User install using the PIP package

You can install kalliope on your system by using Pypi:

```bash
sudo pip3 install kalliope
```

### Method 2 - Manual setup using sources

Clone the project:

```bash
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope
```

Install the project:

```bash
sudo python3 setup.py install
```

### Method 3 - Developer install using Virtualenv

Install the `python-virtualenv` package:

```bash
sudo pip3 install virtualenv
```

Clone the project:

```bash
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope
```

Generate a local python3 virtual environment:

```bash
virtualenv venv -p /usr/bin/python3
```

Activate the local environment:

```bash
source venv/bin/activate
```

Install Kalliope

```bash
python3 setup.py install
```

### Method 4 - Developer, dependencies install only

Clone the project:

```bash
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope
```

Install the python dependencies directly:

```bash
sudo pip3 install -r install/files/python_requirements.txt
```
