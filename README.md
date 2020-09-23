

**Downloading venv**

```
sudo apt inatall python3-venv
```

**Creating virtual environment**

```
python3 -m venv python_blockchain_env
```

**Checking if the virtual environment has been created**

```
echo $VIRTUAL_ENV
```

**Activating the virtual environment**

```
source python_blockchain_env/bin/activate
```

**Inastalling required packages**

```
pip3 install -r requirements.txt
```

**Deactivating virtual environment**

```
deactivate
```

**__init__.py**

```
Used to set up files as modules
```

**Running a single file**

```
python3 -m backend.blockchain.block
```

**Testing the application**

Ensure that the virtual environment is active

```
python3 -m pythest backend/tests
```

**Running the blockchain application**

Ensure that the virtual environment is active

```
python3 -m backend.app
```

**Running a peer instance of the application**

Ensure that the virtual environment is active

```
export PEER=True && python3 -m backend.app
```
