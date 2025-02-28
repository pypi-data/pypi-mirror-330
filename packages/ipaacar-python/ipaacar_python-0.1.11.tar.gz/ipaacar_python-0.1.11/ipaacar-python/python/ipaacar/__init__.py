"""

For the API documentation, head over to `ipaacar.components`.

# About this library
## Introduction
Welcome to Ipaacar,
a powerful implementation of the Incremental Processing Architecture for Artificial Conversational Agents (IPAACA) in Rust.
Ipaacar harnesses the performance and safety benefits of the Rust programming language,
providing a reliable and efficient platform for building conversational agents.
With its asynchronous model,
Ipaacar allows you to build responsive conversational agents that can handle real-time interactions efficiently.

## Key Concepts

1. **Incremental Units (IUs):**
   - IUs are the fundamental units of information in Ipaacar.
   - Each IU is identified by a globally unique identifier (UID).
   - IUs are categorized based on the type of data they represent, such as "asrresults" for Automatic Speech Recognition results.
   - An IU's owner is responsible for its initial creation and can mark it as committed to indicate its validity and finality.
   - The IU's payload contains the actual data stored as a map of key-value pairs, allowing flexible and structured representation using JSON objects.
   - IUs can establish links, representing dependency networks between different IUs.

2. **Messages:**
   - Messages provide a lightweight, non-persistent, and read-only form of IUs.
   - They are designed for efficient message-passing, allowing the transmission of current information without modification.
   - Messages exist only temporarily during their reception and do not consume additional system resources.

3. **Buffers:**
   - Buffers serve as containers for managing IUs in Ipaacar.
   - Output buffers handle the publication of newly created IUs, while input buffers express interests in specific IU categories.
   - When an IU of interest is published or modified, the corresponding input buffers receive notifications for efficient information exchange.
   - IUs can be modified from either end of the communication pipeline, offering flexibility and seamless data manipulation.

# Getting started

This section is dedicated to the installation and setup of ipaacar.

## Installation

## Backend

Ipaacar requires a server as a backend for synchronization. A MQTT backend is already implemented in the Rust codebase.
The library was developed and is tested with [Nanomq](https://nanomq.io/), which is a lightweight and fast.

If you wish to use a different Backend, you can implement it in Rust without much effort. Just implement the `Backend`
trait for a struct.


### Python

#### Installing prebuild wheels (recommended)

You can grab a precompiled version from the
[CI/Jobs Page of this repo](https://gitlab.ub.uni-bielefeld.de/davidschwab/ipaacar/-/jobs/).
The artifact with a job name corresponding to your Python version
(e.g. pick `wheels: [3.11.3]` for any Python 3.11 version).
Extract the zip and install the whl file with `pip install FILENAME.whl` from within a venv.

The wheels are build and tested on linux. Building from source might be required for Windows or MacOS.

#### Building from source

 * Install Rust and Cargo using [rustup](https://rustup.rs/):

```curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh```

 * Install [Python](https://www.python.org/) (currently 3.11 is the latest tested version),
 create and use a [virtual environment](https://docs.python.org/3/library/venv.html)
 * Install [Maturin](https://www.maturin.rs/): ```pip install maturin```
 * Build the wheel package inside the `ipaacar-python` folder: ```maturin build --release```
 * Install the wheel: ```pip install ../target/wheels/*.whl```



### Rust

The project architecture is chosen in such a way, that the Python Library is just a wrapper around a Rust Library.
If you want to take advantage of parallel processing of callbacks, using the Rust Library might be a better choice.


#### Usage over ssh (recommended)

You can use the library by linking it over git using ssh.
This will provide you with the newest version automatically on build.
You can also pin a version with the commit version.

```toml
[dependencies]
ipaacar-core = { git = "ssh://git@gitlab.ub.uni-bielefeld.de/davidschwab/ipaacar.git"}
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






# Sources
## IPAACA - Incremental processing architecture for artificial conversational agents

 * Schlangen, D. & Skantze, G. (2009). A general, abstract model of incremental dialogue processing. In Proceedings of the 12th Conference of the European Chapter of the Association for Computational Linguistics, pp. 710–718, Athens, Greece. [PDF](http://www.aclweb.org/anthology/E/E09/E09-1081.pdf)
 * Schlangen, D. & Skantze, G. (2011). A general, abstract model of incremental dialogue processing. Dialogue and Discourse, 2, 83–111. [doi:10.5087/dad.2011.105](https://doi.org/10.5087/dad.2011.105), [PDF](https://search.iczhiku.com/paper/SWkajux5ZBLernr2.pdf)

## Asynchronous Programming

Understanding asynchronous programming is essential for reaping the benefits of this library.
You should at least take a look at Coroutines and Asyncio.

 * Python [Coroutines](https://docs.python.org/3/library/asyncio-task.html)
 * Python [Asyncio](https://docs.python.org/3/library/asyncio.html)
 * Rust [Tokio](https://tokio.rs/tokio/tutorial)
 * Asyncio <-> Tokio [Interface](https://github.com/awestlake87/pyo3-asyncio)

"""

from ipaacar import components
from ipaacar import handler
from ipaacar import legacy
