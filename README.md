# Face Generator
Face Generation Tool for Memory Experimentation

### Set up

Install virtualenv to keep all your dependencies in one place.
```bash
sudo apt-get install virtualenv
```

After that, create a virtual environment
```bash
virtualenv venv --python=python3.8
```
This should create a venv folder. Activate it by running
```bash
source venv/bin/activate
```
Install the dependencies
```bash
pip install -r requirements.txt
```

Finally, you are ready to go!! Run the face generator
```bash
python main_window.py
```

Once you are all done, get out of the virtual environment by running
```bash
deactivate
```
