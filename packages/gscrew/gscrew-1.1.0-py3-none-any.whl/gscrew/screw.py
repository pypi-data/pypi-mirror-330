"""
This module provides two classes that respectively implement a screw and a coscrew.

Classes
-------
.. autoclass:: ScrewBase
.. autoclass:: Screw
.. autoclass:: CoScrew

Functions
---------
.. autofunction:: comoment

Exemples
--------
Before using these objects, you should import the ``geometric_algebra`` module so that you can
create multivectors. For basic physical applications, a three-dimensional algebra should be enough, but you
can use n-dimensional multivectors.

Let's see a minimal exemple::

    >>> import gscrew
    >>> from gscrew.geometric_algebra import GeometricAlgebra
    >>> from gscrew.screw import Screw
    >>> my_algebra = GeometricAlgebra(3)  # a 3-D geometric algebra
    >>> locals().update(my_algebra.blades)  # add the basis blades to the locals (i.e. 1, e1, e2…)
    >>> reference_point = 0*s            # the point of reference for the screw (here, the origin)
    >>> resultant = 2 + (3*e1) + (6*e3)  # creates a MultiVector for the screw's resultant
    >>> moment = (2*e1) + (5*e2) + e3    # creates another MultiVector for the screw's moment
    >>> my_screw = Screw(reference_point, resultant, moment)  # finally we create a Screw instance
"""


class ScrewBase:
    """Provides a set of common methods for Screw and CoScrew classes.

    .. note::
        You can print a Screw directly by ``print(my_screw)`` but it is recommended to use the
        ``Screw.show`` method in order to have a better control on the reference point.

    Attributes
    ----------
    ref_point : MultiVector
        The point of reference of the screw.
    resultant : MultiVector
        The resultant multivector S or the screw.
    moment : MultiVector
        The moment multivector M of the the screw.

    Methods
    -------
    .. automethod:: __init__
    .. automethod:: change_point
    .. automethod:: show
    """
    def __init__(self, ref_point, resultant, moment):
        """Constructor method.

        Parameters
        ----------
        ref_point : MultiVector
            The point of reference of the (co)screw
        resultant : MultiVector
            The resultant of the (co)screw, usually named S.
        moment : MultiVector
            The moment of the (co)screw, usually named M.

        Raises
        ------
        TypeError
            If ``ref_point`` is not as point.
        """
        if ref_point(1) != ref_point:
            raise TypeError("ref_point is not a point")

        self.ref_point = ref_point
        self.resultant = resultant
        self.moment = moment

    def __repr__(self):
        """Allow to display the (co)Screw at its reference point.

        Returns
        -------
        out : str
            The string representation of the (co)Screw.
        """
        name = self.__class__.__name__
        return f"{name} (\n\t{self.resultant}\n\t{self.moment}\n\t)_{self.ref_point}"

    def change_point(self, new_point):
        """Computes and returns the (co)screw on the new reference point. The formula changes
        according to the type of screw.

        Parameters
        ----------
        new_point : MultiVector
            The new point.

        Returns
        -------
        out : (Co)Screw
            The screw on ``new_point``.
        """
        new_moment = self.moment
        if self.__class__.__name__ == "Screw":
            new_moment = self.moment + ((self.ref_point - new_point) ^ self.resultant)
        elif self.__class__.__name__ == "CoScrew":
            new_moment = self.moment - ((self.ref_point - new_point) | self.resultant)

        self.ref_point = new_point
        self.moment = new_moment

        return self

    def show(self, new_point=None):
        """Print the (co)screw on a given point.

        Parameters
        ----------
        new_point : MultiVector, optionnal
            The point on which the (co)screw should be shown. If no point was given, it shows the
            (co)screw at its reference point.
        """
        if new_point is None:
            print(self)
        else:
            print(self.change_point(new_point))


class Screw(ScrewBase):
    """Screw object.

    The following operators have been overloaded:

    * the addition of screws
      ``self + other``

    * the right-handed addition
      ``other + self``

    * the outer product of screws
      ``self ^ other``

    Methods
    -------
    .. automethod:: dual

    See also
    --------
    This class inherits from the ScrewBase one.
    """
    def __add__(self, other):
        """The addition ``self + other``.

        Parameters
        ----------
        other : Screw
            The screw to be add up.

        Returns
        -------
        out : Screw
            The result of the addition of the two screws.

        Raises
        ------
        TypeError
            If ``other`` isn't a Screw.
        """
        if not isinstance(other, Screw):
            raise TypeError(f"other must be a Screw instance instead of {type(other)}")

        if self.ref_point != other.ref_point:
            other = other.change_point(self.ref_point)

        return Screw(
                self.ref_point,
                self.resultant + other.resultant,
                self.moment + other.moment
            )

    __radd__ = __add__

    def __xor__(self, other):
        """The wedge product ``self ^ other``.
        
        Parameters
        ----------
        other : Screw
            The other Screw.

        Returns
        -------
        out : Screw
            The result of the wedge product between the two given screws.

        Raises
        ------
        TypeError
            If ``other`` isn't a Screw.
        """
        if not isinstance(other, Screw):
            raise TypeError(f"other must be a Screw instance instead of {type(other)}")

        if self.ref_point != other.ref_point:
            other = other.change_point(self.ref_point)

        return Screw(
                self.ref_point,
                (self.resultant ^ other.moment) + (self.moment.grade_involution() ^
                        other.resultant),
                self.moment ^ other.moment
            )

    def dual(self):
        """Compte the dual coscrew of a screw.

        Returns
        -------
        out : CoScrew
            The dual coscrew.
        """
        return CoScrew(
                self.ref_point,
                -self.resultant.dual(),
                self.moment.dual()
            )


class CoScrew(ScrewBase):
    """Coscrew object

    The following operators have been overloaded:

    * the addition of coscrews
      ``self + other``

    * the right-handed addition
      ``other + self``

    * the product between a scalar and a coscrew
      ``scalar * self``

    Methods
    -------
    .. automethod:: composition

    See also
    --------
    This class inherits from the ScrewBase one.
    """
    def __add__(self, other):
        """The addition ``self + other``.

        Parameters
        ----------
        other : CoScrew
            The coscrew to be add up.

        Returns
        -------
        out : CoScrew
            The result of the addition of the two coscrews.

        Raises
        ------
        TypeError
            If ``other`` isn't a CoScrew.
        """
        if not isinstance(other, CoScrew):
            raise TypeError(f"other must be a CoScrew instance instead of {type(other)}")

        if self.ref_point != other.ref_point:
            other = other.change_point(self.ref_point)

        return CoScrew(
                self.ref_point,
                self.resultant + other.resultant,
                self.moment + other.moment
            )

    __radd__ = __add__

    def __rmul__(self, scalar):
        """The right-hand multiplication between a coscrew and a scalar ``scalar * self``.

        Parameters
        ----------
        scalar : int, float
            The scalar to multiply.

        Returns
        -------
        out : CoScrew
            The result of the addition of the two coscrews.

        Raises
        ------
        TypeError
            If ``scalar`` isn't a scalar.
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"scalar must be a scalar instead of {type(scalar)}")

        return CoScrew(
                self.ref_point,
                scalar * self.resultant,
                scalar * self.moment
            )

    def composition(self, other):
        """Compute the composition of two coscrews.
        
        Parameters
        ----------
        other : CoScrew
            The other coscrew.

        Returns
        -------
        out : CoScrew
            The result of the composition.

        Raises
        ------
        TypeError
            If ``other`` is not a CoScrew instance.
        ValueError
            If the two resultants are not spinors.
        """
        if not isinstance(other, CoScrew):
            raise TypeError(f"other must be a CoScrew instance instead of {type(other)}")

        if not (self.resultant.isspinor() and other.resultant.isspinor()):
            raise ValueError("all the resultants must be spinors")

        if self.ref_point != other.ref_point:
            other = other.change_point(self.ref_point)

        return CoScrew(
                self.ref_point,
                self.resultant * other.resultant,
                self.resultant * other.moment + self.moment * other.resultant
            )


def comoment(coscrew: CoScrew, screw: Screw):
    """Compute the real comoment between a coscrew and a screw.

    Parameters
    ----------
    coscrew : CoScrew
        The coscrew.
    screw : Screw
        The screw.

    Returns
    -------
    out : MultiVector
        The real comoment between the given coscrew and the screw.
    """
    return (~coscrew.resultant * screw.moment)(0) + (~coscrew.moment * screw.resultant)(0)
