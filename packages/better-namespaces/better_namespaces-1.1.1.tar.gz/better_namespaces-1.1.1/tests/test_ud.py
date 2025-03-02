#!/usr/bin/env python3

from better_namespaces import NamespaceGroup

def test_context_manager():
    with NamespaceGroup() as foo:
        class Bar:
            '''random class for testing'''
            def __init__(self, g):
                self.salutation = g
            
            def greet(self, name):
                return f'{self.salutation}! {name}'
        
        def bar(name):
            return f'Hi! {name}'

    assert f"{type(foo)}" == "<class 'better_namespaces.context_group.NamespaceGroup'>" 

    attrs = dir(foo) 
    assert 'Bar' in attrs
    assert 'bar' in attrs

    assert foo.Bar('Hi').greet('John') == 'Hi! John' 
    assert foo.bar('John') == 'Hi! John'

if __name__ == '__main__':
    test_context_manager()