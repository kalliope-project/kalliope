# Contributing: core

The community can contribute to the Core of Kalliope by providing some new features.

**How to contribute**

1. Fork it!
1. Checkout the dev branch `git checkout dev`
1. Create your feature branch: `git checkout -b my-new-feature`
1. Commit your changes: `git commit -am 'Add some feature'`
1. Push to the branch: `git push origin my-new-feature`
1. Submit a pull request in the **dev** branch

## Constraints

1. Respect [PEP 257](https://www.python.org/dev/peps/pep-0257/) -- Docstring conventions. For each class or method add a description with summary, input parameter, returned parameter, type of parameter

   ```python
    def my_method(my_parameter):
       """
       Description of he method
       :param my_parameter: description of he parameter
       :type my_parameter: str
       """
   ```

1. Respect [PEP 8](https://www.python.org/dev/peps/pep-0008/) -- Style Guide for Python Code
   We recommend the usage of an IDE like [Pycharm](https://www.jetbrains.com/pycharm/)

## Limitations

1. The management of incoming variable from the signal order when they are **numbers or float are not efficient**.
   - Because of the differences between the STTs outputs: some are returning word some numbers (two != 2).
   - Because of the i18n, we are not able to know if a variable should be interpreted in english, french, spanish, etc ... ("two" != "deux" != "dos")
