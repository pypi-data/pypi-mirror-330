# Brian2Lava

[Brian](https://briansimulator.org/) is an open-source Python package developed and used by the computational neuroscience community to simulate spiking neural networks. The goal of the **Brian2Lava** open-source project is to develop a Brian device interface for the neuromorphic computing framework [Lava](https://lava-nc.org/), in order to facilitate deployment of brain-inspired algorithms on 
Lava-supported hardware and emulator backends. 

For more information, please see our [website](https://brian2lava.gitlab.io/) and the [documentation](https://brian2lava.gitlab.io/docs).

For a rundown of the new features and bugfixes addressed in the latest version, see the [Release Notes](https://gitlab.com/brian2lava/brian2lava/-/blob/main/RELEASES.md).

## Getting started

Below you'll find information on how to quickly get Brian2Lava to run. For further information, please visit the [documentation](https://brian2lava.gitlab.io/docs).

> **Note:** Brian2Lava is still in its testing phase. Please feel free to [report issues or feature requests](https://gitlab.com/brian2lava/brian2lava/-/issues).

> **Note:** At the moment, due to legal restrictions, models for the `Loihi2` backend may just be provided to members of the [Intel Neuromorphic Research Community](https://intel-ncl.atlassian.net/wiki/spaces/INRC/pages/1784807425/Join+the+INRC). Thus, the public version of Brian2Lava currently contains models for the `CPU` backend only.

### Installation

Brian2Lava can be easily installed via the Python Package Index (`pip`):

```
python3 -m pip install brian2lava
```

Note: `conda` support may be added at a later point.

For the latest source code, please visit [gitlab.com/brian2lava/brian2lava](https:/gitlab.com/brian2lava/brian2lava/). If you run from source code, make sure that you have added your path to the source code to `PYTHONPATH`, for example, via:

```
export PYTHONPATH=~/brian2lava
```

### Prerequisites

Make sure that you have installed [Brian 2](https://github.com/brian-team/brian2) (recommended >= 2.7.1) and [Lava](https://github.com/lava-nc/lava) (recommended >= 0.10.0, or lava_loihi-0.7.0).

### Import package and set device

Using Brian2Lava within Brian 2 only requires two steps.

First, import the package:

```
import brian2lava
```

Second, set the `lava` device with the desired hardware backend and mode:

```
set_device('lava', hardware='CPU', mode = 'preset')
```

In principle, this can already run your Brian simulation on the Lava engine. However, you may have to use a few additional settings to 
specify how the code for the simulation is generated and executed. Please see the [documentation](https://brian2lava.gitlab.io/docs/user_guide/import_set_device.html) for more information.

You may want to continue by considering the example code provided [here](https://brian2lava.gitlab.io/docs/introduction/examples.html).

## Dependencies

Brian2Lava currently includes the library of preset models as an external dependency. To make sure that you have the latest version
of the library in your installation, navigate to the Brian2Lava package folder and run
```
source update_submodules.sh
```
or manually execute
```
git init
git submodule foreach 'git pull origin main'
```
This will pull the latest version of the public library of preset models from a [GitHub repository](https://github.com/brian2lava/model_library_public) into your local Brian2Lava installation.

Further dependencies can be found in `setup.py`.
