# pyrfuniverse

[![Pypi](https://img.shields.io/pypi/v/pyrfuniverse.svg?style=for-the-badge)](https://pypi.org/project/pyrfuniverse/)

`pyrfuniverse` is a python package used to interact with `RFUniverse` simulation environment. It is developed with reference to [ML-Agents](https://github.com/Unity-Technologies/ml-agents) and produce new features.

Please go to the [RFUniverse](https://github.com/robotflow-initiative/rfuniverse) repository to view the documentation

## Local Installation

### 1. Create a new conda virtual environment and activate it.

```shell
conda create -n rfuniverse python=3.10 -y
conda activate rfuniverse
```

### 2. Clone this repository and move here in command line.

```shell
git clone https://github.com/mvig-robotflow/pyrfuniverse.git
cd pyrfuniverse
```

### 3. Install the python requirements.

```shell
pip install -r requirements.txt
```

For users in China, please remember to change mirror by the following command. This can significantly accelerate
downloading speed.

```shell
pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
```

### 4. Install

If you want to use `pyrfuniverse` without modifying source code, run the following commands to copy source code to your conda directory.

```shell
python setup.py install
```

Otherwise, you may want to modify source code, then run the following command to construct the link in your conda directory.

```shell
pip install -e .
```

## Headless mode

If you want to run `RFUniverse` on ubuntu server, you will need **headless** mode so that no GUI window will be
generated. To fix this, we use `virtual display` to render on virtual devices, inspired by
[furniture](https://github.com/clvrai/furniture/blob/master/docs/installation.md#virtual-display-on-headless-machines).
You will need the following commands to configure your ubuntu server

```shell
sudo apt-get install xserver-xorg libglu1-mesa-dev freeglut3-dev mesa-common-dev libxmu-dev libxi-dev
```

Then, restart your server and connect your server to a screen. The screen won't render anything, but there must be a
display device connecting to your server.

```shell
# Configure nvidia-x
sudo nvidia-xconfig -a --use-display-device=None --virtual=1280x1024

# Configure environment variable
export DISPLAY=:1

# Launch a virtual display
sudo /usr/bin/X :1 &
```

Here's a [demo](./docs/headless_mode_demo.md). I strongly recommend you run this demo first to test your virtual display
configuration.

After this, you can use `RFUniverse` on ubuntu server freely!
