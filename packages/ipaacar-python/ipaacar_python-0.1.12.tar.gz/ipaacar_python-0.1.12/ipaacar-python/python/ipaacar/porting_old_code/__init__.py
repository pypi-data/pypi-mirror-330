"""
Porting old code to the neq version is quite a hassle, due to the domain shift into an async architecture.
An Interface that orients itself on the old IpaacaInterface is provided under`ipaacar.legacy.IpaacaInterface`.

This interface has several drawbacks, do <b>not</b> use it for new projects.

* It forces linear programming execution
* Each method is also provided as an async variant, that is just handed to the event loop by the sync variant.
The actual program logic happens inside the async variants.
    * Overwriting the sync variant can cause problems
    * You, most of the time, want to overwrite the async methods.
    * This means however, that you need to adjust your legacy code.
* There is no compatibility between old and new IUs. This is not possible with the api changes.
    * If you still want to use old IUs, you can just (de-)serialize them as a string and send them as messages.
IU updates are broken in the old interface anyway, and it will still be faster.
* This interface is mostly untested and probably has bugs.

Here is an Example ion how to use it, with the ExampleComponent from the old architecture.



## Dummy Perception

```python
.. include:: ../../../examples/legacy/port/dummyPerception.py
```


## Dummy Receiver

```python
.. include:: ../../../examples/legacy/port/dummyReceiver.py
```

This example overwrites the async version of `incoming_msg_handler`.
In this case it would have also be fine to use the sync version of it,
since we don't need to access any async resources, that are managed by the rust code.

"""