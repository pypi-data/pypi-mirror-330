# GScrew (Generalized Screw Calculus)
[![Documentation Status](https://readthedocs.org/projects/gscrew/badge/?version=latest)](https://gscrew.readthedocs.io/en/latest/?badge=latest)
[![Licence](https://img.shields.io/github/license/GenScrew/GScrew?color=green)](https://github.com/GenScrew/GScrew/blob/master/LICENSE)
[![Build Status](https://github.com/GenScrew/GScrew/actions/workflows/python-publish.yml/badge.svg)](https://github.com/GenScrew/GScrew/blob/master/.github/workflows/python-publish.yml)

## Description
A Python module to manipulate generalized Screws and Coscrews with geometric algebras (real Clifford algebras).

- [readthedocs Documentation](https://gscrew.readthedocs.io/en/latest/)
- [Bug tracker](https://github.com/GenScrew/GScrew/issues)

## Installation
A Pypi package is available, please refer to the [Pypi page](https://pypi.org/project/GScrew/) or enter `pip install gscrew` in a terminal.

## Exemples
First of all, you need to import the modules:
```
import gscrew
from gscrew.geometric_algebra import GeometricAlgebra
from gscrew.screw import Screw
```
The `screw` module also provides a `CoScrew` object and the `comoment` function for calculating the comoment between a coscrew and a screw.

Once these modules have been imported, we can create the geometric algebra in which we will be working. For basic physical applications, a three-dimensionnal algebra should suffice:
```
my_algebra = GeometricAlgebra(3)
locals().update(my_algebra.blades)
```
The second line adds the basis blades to the local variables so that we will be able to create new multivectors just by performing linear combinations of these basis blades. For a 3D algebra, the basis blades are: s, e1, e2, e3, e12, e13, e32, e123.

We can now start working with Screw and CoScrew classes:
```
O = 0 * s  # the origin of the reference frame
S = 1 + (2*e2) + (3*e3)  # the resultant of the screw
M = (e1) + (5*e3)        # the moment of the screw
my_screw = Screw(O, S, M)
```

## Licence
All the code is provided under the GNU General Public Licence v3.0+ (GPLv3+)
