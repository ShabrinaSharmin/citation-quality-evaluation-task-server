# Citation Quality Evaluation Task Server
A citation quality evalutor task submission server.
The server is based on the python flask package


## Setup
```bash
# create a conda environment with python 3.x
conda create --name citation-quality-evaluation-task-server
conda activate citation-quality-evaluation-task-server

#git clone and install packages
git clone https://github.com/ShabrinaSharmin/citation-quality-evaluation-task-server.git
cd citation-quality-evaluation-task-server
pip install requirements.txt
```

## Running the weserver (http mode)
```bash
python cqets.py
```

Make sure that you have the port 5000 open for HTTP traffic

Note: The server is currently running HTTP which is not secure over the wire.
