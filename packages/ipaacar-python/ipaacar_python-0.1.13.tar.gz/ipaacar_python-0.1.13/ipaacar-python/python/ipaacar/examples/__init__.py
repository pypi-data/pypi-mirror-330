"""
This page shows some example use cases


# Ping-Pong

A simple example of two IUs, that incrementally update a counter together.

```mermaid
flowchart TD
    A[Ping Creation] -->|Init Counter + Update| B(Ping)
    B -->|Increment Counter + update| C(Pong)
    C -->|Increment Counter + update| B(Ping)
    D[Pong Creation] -->|Create + wait for update| C(Pong)
```

## ping.py

This code triggers the update loop.
```python
.. include:: ../../../examples/pingpong/ping.py
```

## pong.py
Most of it works just like in ping.py (with Ping and Pong swapped).
The only notable difference is, that the dummy update, that triggers the
update circle is commented out.
```python
.. include:: ../../../examples/pingpong/pong.py
```


# Messages

Ipaacar also offers the possibility to send Strings efficiently around the network, without the use of IUs.

## Simple Use Case
```python
.. include:: ../../../examples/messages/simple.py
```

# Sequential vs. Concurrent



"""