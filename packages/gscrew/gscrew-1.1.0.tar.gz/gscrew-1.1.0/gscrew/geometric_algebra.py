"""
Implements a MultiVector object and its basic manipulations. This module also provides a
GeometricAlgebra class to have a workspace for multivectors instance.

Classes
-------
.. autoclass:: GeometricAlgebra
.. autoclass:: MultiVector
"""
import itertools
import math
import numpy as np

class GeometricAlgebra:
    """Implements a geometric algebra of a given dimension.

    In most cases, you won't have to manipulate this object.

    Print a GeometricAlgebra instance will display the basis blades of the algebra.

    Attributes
    ----------
    dim : int
        The dimension of the algebra. This will create the basis blades of the algebra.
    nb_blades : int
        The number of basis blades the algebra has.
    blades_by_grade : list
        The number of basis blades per grade.
        e.g. for a 3D-algebra, it will be ``[1, 3, 3, 1]``
    blades_ids : list
        It contains the ids of the basis blades.
        e.g. for a 2D-algebra, the basis blades are: ``s, e1, e2, e12`` so the ids will be:
        ``[(), (1,), (2,), (1, 2)]``.
    blades : dict
        This dictionnary contains the basis blades: ``{name: value}`` where
        ``name`` is a string (e.g. ``'s'``, ``'e1'``, ``'e2'`` etc) and ``value`` the associated
        MultiVector instance.

    Methods
    -------
    .. automethod:: __init__
    .. automethod:: get_grade
    """
    def __init__(self, dim: int=3):
        """Constructor method.
        
        Parameters
        ----------
        dim : int, optionnal
            The wanted dimension if the geometric algebra. By default, this will generate a three
            dimensional one. 
        """
        self.dim = dim
        self.nb_blades = 2 ** dim

        self.blades_by_grade = [binomial_coefficient(dim, i) for i in range(dim + 1)]

        ids = list(range(self.nb_blades))
        self.blades_ids = sorted(ids, key=lambda elmnt: elmnt.bit_count())

        self.blades = {}
        self.__generate_blades()

    def __repr__(self):
        """Returns the string representation of the geometric algebra.

        Returns
        -------
        out : str
            The string representation of the algebra.
        """
        return str(list(self.blades.values()))

    def __generate_blades(self):
        """Generate the basis blades for the given dimension."""
        ids = [i + 1 for i in range(self.dim)]
        blades_names = list(itertools.chain.from_iterable(
                itertools.combinations(ids, r)
                for r in range(self.dim + 1)
            ))

        names = []
        for index, blade_name in enumerate(blades_names):
            if index:
                names.append("e" + "".join(map(str, blade_name)))
            else:
                names.append("s")

        value = np.zeros(self.nb_blades)
        for i in range(self.nb_blades):
            value[i] = 1
            self.blades[names[i]] = MultiVector(self, value)
            value[i] = 0

    def get_grade(self, grade: int):
        """Returns the first and the last index of the researched grade. It can be useful if you
        search all the k-vectors of a given algebra, then you give the grade (i.e. k) and this
        method will return you the index of the first k-vector and the index of the last k-vector of
        your algebra.

        Parameters
        ----------
        grade : int
            The grade you are searching for.

        Returns
        -------
        out : tuple
            The output is a tuple composed of two elements. The first one is the first index and the
            second one, the last.

        Exemples
        --------
        If we work in a three-dimensionnal algebra::

            >>> geo_alg = GeometricAlgebra(3)
            >>> geo_alg.get_grade(2)
            (4, 6)

        Indeed, the first bivector (i.e. e12) is at index 4 and the last one (i.e. e23) is at 6.
        """
        first_index = sum(self.blades_by_grade[:grade])
        last_index = first_index + self.blades_by_grade[grade]
        return first_index, last_index - 1


class MultiVector:
    r"""An element of the geometric algebra.

    The following operators have been overloaded:

    * the addition
      ``self + other``

    * the substraction
      ``self - other``

    * the geometric product
      ``self * other``

    * the outer product
      ``self ^ other``

    * the inner product
      ``self | other``

    * the scalar division
      ``self / scalar``

    Some others manipulations are available:

    * the projection on grade k
      ``my_multivector(k)``
    
    * the norm
      ``abs(my_multivector)``

    * the inversion
      ``my_multivector.inverse()``

    * the reversion :math:`A^{\dagger}`
      ``~my_multivector``

    * the dual calculation
      ``my_multivector.dual()``

    * the grade involution
      ``my_multivector.grade_involution()``

    Attributes
    ----------
    geo_alg : GeometricAlgebra
        The geometric algebra to which the multivector belongs.
    value : np.array
        The coefficients on each basis blade.

    Methods
    -------
    .. automethod:: __init__
    .. automethod:: __call__
    .. automethod:: __getitem__
    .. automethod:: copy
    .. automethod:: dual
    .. automethod:: grade_involution
    .. automethod:: inverse
    .. automethod:: isspinor

    Exemples
    --------
    Let's show you a complete exemple of a manipulation of MultiVector.
    You must start by importing the module::

        >>> import gscrew
        >>> from gscrew.geometric_algebra import GeometricAlgebra, MultiVector
        >>> ga = GeometricAlgebra(3)    # you should give the dimension of the algebra
        >>> locals().update(ga.blades)  # import the basis blades e.g. s, e1, e2, e3, e12 etc

    Then you have fully initialize the module. To create a new MultiVector instance, you have two
    possibilities. The first one is also the easiest::

        >>> my_mv = 1 + 1*e1 + 5*e2 + (1/5) * e13

    You can also call the constructor method manually::
        
        >>> my_mv = MultiVector(geo_alg, (1, 1, 5, 0, 0, 1/5, 0, 0))

    .. warning::
        In the second case you have to give all the coefficients and the GeometricAlgebra instance.

    .. note::
        When you create a new MultiVector by using the basis blades, the new instance inherits
        the geometric algebra of the basis blades.
    """
    def __init__(self, geo_alg: GeometricAlgebra, value=None):
        """Constructor method.

        .. note:: ``value`` must be transtypable into an ``numpy.array``.

        Parameters
        ----------
        geo_alg : GeometricAlgebra
            The algebra to which the multivector belongs.
        value
            The coefficients of the multivector.
        """ 
        self.geo_alg = geo_alg
        if value is None:
            self.value = np.zeros(geo_alg.nb_blades)
        else:
            if isinstance(value, (int, float)):
                new_value = np.zeros(geo_alg.nb_blades)
                new_value[0] = value
            else:
                new_value = np.array(value)
            self.value = new_value

        self.precision = 5

    def __abs__(self):
        """Computes the norm of the multivector.

        Returns
        -------
        out : float
            The norm of the multivector"""
        result = 0
        for component in self.value:
            result += abs(component ** 2)

        return math.sqrt(result)

    def __add__(self, other):
        """Computes the addition ``self + other``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to add up.

        Returns
        -------
        out : MultiVector
            The result of the addition.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        new_value = self.value.copy()
        if np.isscalar(other):
            new_value[0] += other

        elif isinstance(other, MultiVector):
            new_value += other.value

        else:
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        return MultiVector(self.geo_alg, new_value)

    def __call__(self, *grades):
        """Projects the multivector on the basis blades of given grades.

        Parameters
        ----------
        *grades
            The grades on which the multivector will be project.

        Returns
        -------
        out : MultiVector
            The result of the projection.

        Exemples
        --------
        Let ``my_mv`` be a multivector such that ``my_mv = 1 + (2^e1) + (3^e2) + (4^e12)`` and let's
        see some projections::

            >>> my_mv = 1 + (2^e1) + (3^e2) + (4^e12)
            >>> my_mv(0)  # projection on scalar
            1
            >>> my_mv(1)  # projection on vectors
            (2^e1) + (3^e2)
            >>> my_mv(0, 2)  # projection on scalar and bivectors
            1 + (4^e12)
        """
        new_value = np.zeros(self.geo_alg.nb_blades)
        for grade in grades:
            first_index, last_index = self.geo_alg.get_grade(grade)
            for index in range(first_index, last_index + 1):
                new_value[index] = self.value[index]
        return MultiVector(self.geo_alg, new_value)

    def __eq__(self, other):
        """Tests the equality between two multivectors.

        Parameters
        ----------
        other : MultiVector
            The other multivector.

        Returns
        -------
        out : bool
            This method will return ``True`` if all the components of the two multivectors are
            equals. 
        """
        if np.isscalar(other):
            return self[0] == other
        return (self.value == other.value).all()

    def __getitem__(self, index: int):
        """Returns the component at the given index.

        Parameters
        ----------
        index : int
            The index of the desired component.

        Returns
        -------
        out : float
            The desired component.
        """
        return self.value[index]

    def __invert__(self):
        """Computes the reversion of the multivector ``~self``.

        Returns
        -------
        new_mv : MultiVector
            The result of the reversion
        """
        new_mv = MultiVector(self.geo_alg)
        for k in range(self.geo_alg.dim + 1):
            new_mv += (-1) ** ((k**2 - k)/2) * self(k)

        return new_mv

    def __mul__(self, other):
        """Computes the geometrical product ``self * other``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to multiply.

        Returns
        -------
        out : MultiVector
            The result of the geometrical product.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        if np.isscalar(other):
            return MultiVector(self.geo_alg, self.value * other)

        if not isinstance(other, MultiVector):
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        new_value = np.zeros(self.geo_alg.nb_blades)
        for i in range(self.geo_alg.nb_blades):
            if self[i]:
                for j in range(self.geo_alg.nb_blades):
                    if other[j]:
                        index, sgn = self.__mul_basis(i, j)
                        new_value[index] += sgn * self[i] * other[j]

        return MultiVector(self.geo_alg, new_value)

    def __neg__(self):
        """Unary minus ``-self``.

        Returns
        -------
        out : MultiVector
            The opposed MultiVector.
        """
        return MultiVector(self.geo_alg, -self.value.copy())

    def __or__(self, other):
        """Compute the inner product ``self | other``.

        Parameters
        ----------
        other : MultiVector
            The other MultiVector.

        Returns
        -------
        new_mv : MultiVector
            The result of the inner product.

        Raises
        ------
        TypeError
            If ``other`` isn't a MultiVector instance.
        """
        if not isinstance(other, MultiVector):
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        new_mv = MultiVector(self.geo_alg)
        for gd1 in range(1, self.geo_alg.dim + 1):
            for gd2 in range(1, self.geo_alg.dim + 1):
                new_mv += (self(gd1) * other(gd2))(abs(gd2 - gd1))

        return new_mv

    __radd__ = __add__

    def __repr__(self):
        """Returns the string representation of the MultiVector.

        Returns
        -------
        string : str
            The string representation of the MultiVector.
        """
        string = ""
        blades_names = tuple(self.geo_alg.blades.keys())
        for index, coeff in enumerate(self.value):
            if coeff:
                if coeff > 0 and string:
                    string += " + "
                if coeff < 0:
                    string += " - "
                if index:
                    string += f"({abs(coeff)}^{blades_names[index]})"
                else:
                    string += f"{abs(coeff)}"

        if not string:
            return "0"
        return string.strip()

    def __rmul__(self, other):
        """Compute the right-hand geometrical product ``other * self``.

        Parameters
        ----------
        other : scalar
            The scalar to multiply.

        Returns
        -------
        out : MultiVector
            The result of the geometrical product.

        Raises
        ------
        TypeError
            If ``other`` is not a scalar.
        """
        if np.isscalar(other):
            return MultiVector(self.geo_alg, other * self.value)

        else:
            raise TypeError(f"other must be a scalar instead of {type(other)}")

    def __rsub__(self, other):
        """Compute the subtraction ``other - self``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to subtract.

        Returns
        -------
        out : MultiVector
            The result of the subtraction.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        new_value = np.zeros(self.geo_alg.nb_blades)
        if np.isscalar(other):
            new_value[0] = other - self.value[0]
            new_value[1:] -= self.value[1:]

        elif isinstance(other, MultiVector):
            new_value = other.value.copy()
            new_value -= self.value

        else:
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        return MultiVector(self.geo_alg, new_value)

    def __rxor__(self, other):
        """Compute the right-hand outer product ``other ^ self``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to multiply.

        Returns
        -------
        out : MultiVector
            The result of the outer product.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        if np.isscalar(other):
            return other * self

        if not isinstance(other, MultiVector):
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        return other ^ self

    __str__ = __repr__

    def __sub__(self, other):
        """Compute the subtraction ``self - other``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to subtract.

        Returns
        -------
        out : MultiVector
            The result of the subtraction.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        new_value = self.value.copy()
        if np.isscalar(other):
            new_value[0] -= other

        elif isinstance(other, MultiVector):
            new_value -= other.value

        else:
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        return MultiVector(self.geo_alg, new_value)

    def __truediv__(self, other):
        """Compute the division ``self / other``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to divide.

        Returns
        -------
        out : MultiVector
            The result of the division.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        if np.isscalar(other):
            new_value = self.value / other
            return MultiVector(self.geo_alg, new_value)

        if not isinstance(other, MultiVector):
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        return MultiVector(self.geo_alg)

    def __xor__(self, other):
        """Compute the outer product ``self ^ other``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to multiply.

        Returns
        -------
        out : MultiVector
            The result of the outer product.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        if np.isscalar(other):
            return self * other

        if not isinstance(other, MultiVector):
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        new_mv = MultiVector(self.geo_alg)
        for gd1 in range(self.geo_alg.dim):
            for gd2 in range(self.geo_alg.dim):
                if gd1 + gd2 <= self.geo_alg.dim:
                    new_mv += (self(gd1) * other(gd2))(gd1 + gd2)

        return new_mv

    def __mul_basis(self, index1: int, index2: int):
        """Compute the geometrical product between two basis blades.

        Parameters
        ----------
        index1 : int
            The first basis blade (its index).
        index2 : int
            The second basis blade (its index).

        Returns
        -------
        out : tuple
            A tuple of the form: ``(index, sign)`` where ``index`` is the index of the
            resulting basis blade and ``sign`` the sign of the result.
        """
        new_index = self.geo_alg.blades_ids[index1] ^ self.geo_alg.blades_ids[index2]
        sign = self.__get_sign(self.geo_alg.blades_ids[index1], self.geo_alg.blades_ids[index2])
        return self.geo_alg.blades_ids[new_index], sign

    def __get_sign(self, index1: int, index2: int):
        """Calculate the sign of the geometric product between the given basis blades.

        Parameters
        ----------
        index1 : int
            The index of the first basis blade.
        index2 : int
            The index of the second basis blade.

        Returns
        -------
        out : int
            The sign of the geometric product between the two basis blades.
        """
        index1 //= 2
        n_swap = 0
        while index1:
            n_swap += (index1 & index2).bit_count()
            index1 //= 2
        n_swap += 1
        return 2 * (n_swap % 2) - 1


    def copy(self):
        """Create a deep copy of the instance.

        Returns
        -------
        out : MultiVector
            The copy of the instance.
        """
        return MultiVector(self.geo_alg, self.value.copy())

    def grade_involution(self):
        """Compute the grade involution of the multivector.

        Returns
        -------
        new_mv : MultiVector
            The result of the grade involution.
        """
        new_mv = MultiVector(self.geo_alg)
        for i in range(self.geo_alg.dim + 1):
            new_mv += (-1)**i * self(i)
        return new_mv

    def inverse(self):
        """Compute the inverse of a given multivector.

        Returns
        -------
        out : MultiVector
            The inverted multivector.
        """
        system = np.zeros((self.geo_alg.nb_blades, self.geo_alg.nb_blades))
        for i in range(self.geo_alg.nb_blades):
            column = (self * tuple(self.geo_alg.blades.values())[i]).value
            for j in range(self.geo_alg.nb_blades):
                if column[j] > 1e-10 or column[j] < -1e-10:
                    system[j, i] = column[j]

        new_value = list(map(
                lambda x: round(x, self.precision),
                np.linalg.solve(system, tuple(self.geo_alg.blades.values())[0].value)
            ))
        return MultiVector(self.geo_alg, new_value)

    def dual(self):
        """Compute the dual multivector.

        Returns
        -------
        out : MultiVector
            The dual.
        """
        return self * tuple(self.geo_alg.blades.values())[-1].inverse()

    def isspinor(self):
        """Tests if the multivector is a spinor, i.e. if all its blade have even grade.

        Returns
        -------
        out : bool
            It equals to ``True`` if the multivector is a spinor, ``False`` else.
        """
        return self == sum(self(k) for k in range(self.geo_alg.dim + 1) if k % 2 == 0)


def binomial_coefficient(n: int, k: int):
    """Compute the binomial coefficient nCk.
    
    Parameters
    ----------
    n : int
        The first integer.
    k : int
        The second integer

    Returns
    -------
    coeff : int
        The binomial coefficient: nCk.
    """
    if k < 0 or k > n:
        return 0
    if k in (0, n):
        return 1
    k = min(k, n - k)

    coeff = 1
    for i in range(k):
        coeff = coeff * (n - i) // (i + 1)

    return coeff
