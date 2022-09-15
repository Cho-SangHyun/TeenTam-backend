# python version check

    $ python -V
    >> Python 3.10.7

# install virtual environment

    $ python -m venv venv_name
    $ cd venv_name      # go to your venv dir
    $ Scripts\activate.bat

# if you can see venv_name on cmd, venv activated successfully
(venv_name) C:.....\venv_name>
# you have to set your interpreter as venv python.exe

#install packages using requirements.txt 

    $ python -m pip install -r requirements.txt

# check intalled packages on venv

    $ python -m pip freeze

# extracting packages as requirements.txt 

    $ python -m pip feeze > requirements.txt
