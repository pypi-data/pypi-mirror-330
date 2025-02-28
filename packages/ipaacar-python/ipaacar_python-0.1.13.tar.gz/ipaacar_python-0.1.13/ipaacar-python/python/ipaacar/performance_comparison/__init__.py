"""

# Experiment

This section compares the performance of different Ipaacar solutions to the same problem: Count to 10,000.

Ipaacar is compiled in with the `--release` flag and installed into a Python 3.11 Venv.
The old Ipaaca version is installed after the instructions from the gitlab page.
[NanoMQ](https://nanomq.io/) is used as the MQTT broker.

# Ipaacar Python Version

## Simple Message

Here we store the counter as a string and send it as a Message.
For message Handling we simply parse the counter, increment it, put it into a String and send it again.
```python
.. include:: ../../../examples/performance_tests/comp_msg_value.py
```

## JSON Message

This piece of code is similar to the first one. We just have the counter in a dict and parse it as json.

```python
.. include:: ../../../examples/performance_tests/comp_msg_json.py
```

## Updating IU

Here we create a IU and safe the dict from the sample before as the payload.
The IU the updates itself, each time it receives an update.

```python
.. include:: ../../../examples/performance_tests/comp_iu.py
```

## Creating New IU

This version creates a new IU, each time a new IU is received (and increments the counter).

```python
.. include:: ../../../examples/performance_tests/comp_new_iu.py
```

## Multiple IUs

This test spreads the Workload on multiple IUs.
We use 20 IUs that count to 500 (20 * 500 = 10,000).

```python
.. include:: ../../../examples/performance_tests/parallel_ius.py
```

## Multiple OutputBuffer

Since all IUs in the Same Buffer share the same Backend connection, we can also try to use multiple Buffer.
This test does 5 Buffers, 20 IUs, that count to 100 (5 * 20 * 100 = 10,000).

```python
.. include:: ../../../examples/performance_tests/multiple_buffer.py
```

## Results

Each Test ran 5 times. Result times are provided in seconds.

| Test Version        | Run 1              | Run 2              | Run 3              | Run 4              | Run 5              |
|---------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| Simple Message      | 1.861              | 1.957              | 1.917              | 1.874              | 1.920              |
| Json Message        | 2.009              | 2.040              | 2.046              | 2.080              | 2.007              |
| Update IU           | 3.185              | 3.158              | 3.118              | 3.142              | 3.113              |
| New IU              | 182.323            | 180.266            | 181.680            | 180.970            | 249.860            |
| Multiple IUs        | 1.610              | 1.609              | 1.612              | 1.609              | 1.612              |
| Multiple Buffer     | 1.513              | 1.422              | 1.514              | 1.414              | 1.511              |


# Ipaaca (old Version)

## Sending Messages

Here we send Messages over the IpaacaInterface.

```python
.. include:: ../../../examples/legacy/msg_perf.py
```

## Creating new IU

This creates new IUs on each callback. This is in essence the same as sending messages,
because Messages are IUs in the old version.

```python
.. include:: ../../../examples/legacy/iu_new_perf.py
```

## Updating IU

This code updates the IU. Testing this code is not necessary, due to a bug in the Interface. It doesn't recognize the iu
type correctly and silently creates a new one instead.

```python
.. include:: ../../../examples/legacy/iu_update_perf.py
```

## Results

| Test Version        | Run 1              | Run 2              | Run 3              | Run 4              | Run 5              |
|---------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| Legacy Message      | 680.621            | 674.467            | 679.411            | 673.410            | 676.491            |
| New IU              | 2047.316           | no termination     | no termination     | 2218.546           | no termination     |
| Update IU           | -                  | -                  | -                  | -                  | -                  |

## Evaluation
The new Implementation reliably outperforms the old interface in every test.
Testing the old interface with multiple buffer wouldn't make any sense, since they still run on the same thread.

The Benchmarks also show that using multiple Buffer also brings performance benefits.
The big bottleneck in these is the Python GIL. By using multiple Callbacks that run in parallel
(with multiple Buffers),
the Rust Coroutines can reduce the time between GIL acquisitions.

There is also a clear difference in execution times, where
sending messages < updating IUs << creating a new IU each time

The new Interface beats the old one in terms of speed by an order of magnitude.
I highly recommend new users to use the new interface.
Users of the old version have to decide on their own,
if the performance benefits are worth migrating their legacy codebase and swapping to a stricter interface
that uses a different architecture.
"""
