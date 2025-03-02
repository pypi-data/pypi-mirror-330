#!/usr/bin/env python3

from better_namespaces import NamespaceGroup

def test_context_manager():
    with NamespaceGroup() as foo:
        import pandas as pd
        from matplotlib import pyplot as plt

    assert f"{type(foo)}" == "<class 'better_namespaces.context_group.NamespaceGroup'>" 

    attrs = dir(foo) 
    assert 'pd' in attrs
    assert 'plt' in attrs


if __name__ == '__main__':
    test_context_manager()