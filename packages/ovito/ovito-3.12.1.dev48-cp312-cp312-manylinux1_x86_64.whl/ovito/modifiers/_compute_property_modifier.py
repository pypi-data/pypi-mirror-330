from __future__ import annotations
from . import ComputePropertyModifier
import collections.abc

# Implement the ComputePropertyModifier.neighbor_mode property.
def ComputePropertyModifier_neighbor_mode(self) -> "ComputePropertyModifier.NeighborMode":
    """
        Selects the criterion for visiting neighboring particles. Supported modes are:

          * ``ComputePropertyModifier.NeighborMode.Cutoff``
          * ``ComputePropertyModifier.NeighborMode.Bonded``

        :Default: ``ComputePropertyModifier.NeighborMode.Cutoff``
    """
    if self.operate_on != 'particles': return ComputePropertyModifier.NeighborMode.Cutoff
    return self.delegate.neighbor_mode
def ComputePropertyModifier_set_neighbor_mode(self, mode):
    self.operate_on = 'particles'
    self.delegate.neighbor_mode = mode
ComputePropertyModifier.neighbor_mode = property(ComputePropertyModifier_neighbor_mode, ComputePropertyModifier_set_neighbor_mode)

# Implement the ComputePropertyModifier.cutoff_radius property.
def ComputePropertyModifier_cutoff_radius(self) -> float:
    """
        The cutoff radius up to which neighboring particles are visited to compute :py:attr:`neighbor_expressions`.
        This parameter is only used if :py:attr:`operate_on` is set to ``'particles'``, :py:attr:`neighbor_mode` is set to ``Cutoff``,
        and :py:attr:`neighbor_expressions` has been specified.

        :Default: 3.0
    """
    if self.operate_on != 'particles': return 3.0
    return self.delegate.cutoff_radius
def ComputePropertyModifier_set_cutoff_radius(self, radius):
    self.operate_on = 'particles'
    self.delegate.cutoff_radius = radius
ComputePropertyModifier.cutoff_radius = property(ComputePropertyModifier_cutoff_radius, ComputePropertyModifier_set_cutoff_radius)

# Implement the ComputePropertyModifier.neighbor_expressions property.
def ComputePropertyModifier_neighbor_expressions(self) -> collections.abc.Sequence[str]:
    """
        The tuple of strings containing the math expressions for the per-neighbor terms, one for each vector component of the output particle property.
        If the output property is scalar, the tuple must comprise one string only.

        The neighbor expressions are only evaluated for each neighbor particle and the value is added to the output property of the central particle.
        Neighbor expressions are only evaluated if :py:attr:`operate_on` is set to ``'particles'``.

        :Default: ``()``
    """
    if self.operate_on != 'particles': return ()
    expressions = self.delegate.neighbor_expressions
    # Reduce length of tuple to include only non-empty strings.
    while len(expressions) != 0 and len(expressions[-1]) == 0: expressions = expressions[:-1]
    return expressions
def ComputePropertyModifier_set_neighbor_expressions(self, expressions):
    self.operate_on = 'particles'
    self.delegate.neighbor_expressions = expressions
ComputePropertyModifier.neighbor_expressions = property(ComputePropertyModifier_neighbor_expressions, ComputePropertyModifier_set_neighbor_expressions)
