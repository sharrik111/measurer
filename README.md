[![PyPI version](https://badge.fury.io/py/measurer.svg)](https://badge.fury.io/py/measurer)

# Measurer
Easily measure Python function performance

## Install
`$ pip install measurer`

## Usage
```python
import measure

@measure.time(repeats=100, copy=False, gc_off=True)
def a():
    pass  # Your logic here
print(a())  # 6.700000000005313e-06

def b():
    pass  # Your logic here
print(measure.time(b, repeats=100, copy=False, gc_off=True)())  # 6.199999999997874e-06
```

## Goal
Currently, this module contains only one decorator measuring function execution time. The goal was to make performance evaluation extremely easy for non-experienced programmers, who wants to check how much resources their programs/solutions take.
As a subject for future development, other types of measurers could be implemented (e.g. memory, recursive function calls etc.)

## Details
#### Why not *&quot;timeit&quot;* ?
Timeit is not suitable for function calls with arguments. Thus, one has to wrap a tested function with another function (without arguments) and evaluate redundant function calls (which sometimes causes big overhead).
#### We still perform redundant calls...
Yes. Ideally, we have to analyze syntactic tree and create some sort of &quot;inline&quot; method call. However, this is a hobby module, so we don&apos;t push towards ideal implementation.
#### Why do  we dump parameters with Pickle?
Packages like &quot;msgpack&quot; or &quot;marshal&quot; show comparable performance (and time to time they are faster), but the difference is not significant. So we use pickle, cause it&apos;s a built-in package (we try to leave the module simple).