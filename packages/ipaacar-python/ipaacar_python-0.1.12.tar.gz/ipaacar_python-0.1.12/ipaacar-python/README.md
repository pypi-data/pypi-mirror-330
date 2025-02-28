# ipaacar - Incremental Processing Architecture for Artificial Conversational Agents, implemented in Rust

![pipeline](https://gitlab.ub.uni-bielefeld.de/scs/ipaacar/badges/main/pipeline.svg)
![PyPI - Version](https://img.shields.io/pypi/v/ipaacar-python)
![PyPI - License](https://img.shields.io/pypi/l/ipaacar-python)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ipaacar-python)

Implementation of IPAACA in Rust. For a theoretical background, see [ipaaca wiki entry](https://scs.techfak.uni-bielefeld.de/wiki/public/ipaaca/start). IPAACA is developed by the Social Cognitive Systems Group at Bielefeld University. Many thanks to David Schwab for his contribution to the initial rust implementation.

IPAACA is a framework for incremental processing via "incremental units" (IUs) processed by buffers (in and out). It uses a MQTT broker for message passing. Therefore, a MQTT broker must be installed and running to use ipaaca(r) ([mosquitto](https://mosquitto.org/download/), [nanomq](https://nanomq.io/downloads?os=Linux)). Simple messaging is possible via "messages". IUs can be updated, linked, committed, and retracted, allowing incremental processing, e.g. for conversational agents.


## Installation
### Python
#### Installing from PyPI

You can grab a precompiled versions from [PyPI](https://pypi.org/project/ipaacar-python/) and install it via pip:
```
pip install ipaacar-python
```
Currtently, the precompiled versions support [manylinux_x_y](https://github.com/pypa/manylinux) (e.g., Ubuntu >= 21.04, etc.) and Python 3.8 to 3.11.

#### Building from source

If the precompiled versions do not suit your needs, build ipaacar-python from source.

 * Install Rust and Cargo using [rustup](https://rustup.rs/):
```curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh```

 * Install [Python](https://www.python.org/) (3.11 recommended), create and use a [virtual environment](https://docs.python.org/3/library/venv.html)
 * Install [Maturin](https://www.maturin.rs/): ```pip install maturin```
 * Build the wheel package inside the `ipaacar-python` folder: ```maturin build --release```
 * Install the wheel: ```pip install ../target/wheels/FILENAME.whl```

### Rust

#### Usage over ssh (recommended)

You can use the library by linking it over git ssh. You will always use the newest version like this.

```toml
[dependencies]
ipaacar-core = { git = "ssh://git@gitlab.ub.uni-bielefeld.de:scs/ipaacar.git"}
```

If the project is still hosted on the uni gitlab, setup ssh authentication and create `.cargo/config.toml` with this content:

```toml
[net]
git-fetch-with-cli = true
```

#### Downloading source files

Download the ipaaca-core folder and place it into your project directory. You can use the library by linking it in your `Cargo.toml` like this:

```toml
[dependencies]
ipaacar-core = { path = "/ipaacar-core" }
```

Depending on your folder structure you might need to adjust the path.

## Documentation

Documentation is available for:

#### [Python](https://scs.pages.ub.uni-bielefeld.de/ipaacar/ipaacar-python)

Documentation of the Python API. Build with pdoc.

#### [Rust](https://scs.pages.ub.uni-bielefeld.de/ipaacar/ipaacar-core/doc/ipaacar_core/)

Documentation of the Rust library. Build with standard rust docs.

