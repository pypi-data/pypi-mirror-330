#!/usr/bin/env python
# coding: utf-8

from typing import Union
from dataclasses import dataclass

import numpy as np

import shapely.affinity as affine
import shapely.geometry as geom
import shapely.ops
import shapely.wkt as wkt

# import weavingspace.tiling_utils as tiling_utils
from weavingspace import tiling_utils

@dataclass
class WeaveGrid:
  """Class to encapsulate generation of sites where strands intersect.

  Can generate both triangular and square grid 'cells' as visual
  representation of overlaps of two or three strands at a site.

  NOTE: there is no 'gridification' or 'cleaning' in the geometry of this
  code - we leave that to steps further down the pipeline, preferring to
  perform this low level geometry with maximum precision. The only limited
  break with this is in get_visible_cell_strands, where strands in higher
  layers are buffered by a small amount to avoid closely aligned polygon
  edges producing slivers etc.
  
  Atrributes:
    basis (np.ndarray): matrix to calculate x,y coordinates of a
      site from its (integer) grid coordinates,
    orientations (tuple[float]: orientations of the two or three
      axes either (0, -90) or (0, 120, 240).
    grid_cell (geom.Polygon): the base triangle or square of the grid.
    n_axes (int): the number of axes in the weave, 2 or 3.
      Defaults to 2.
    spacing (float): spacing of the strands. Defaults to 10_000.
  """
  basis: np.ndarray
  orientations: tuple[float]
  grid_cell: geom.Polygon = None
  n_axes: int = None
  spacing: float = 10000

  def __init__(self, n_axes, orientations, spacing = 10000):
    """Initialises _WeaveGrid.
    """
    self.n_axes = n_axes
    self.orientations = orientations
    self.spacing = spacing
    self.basis = self.setup_basis()
    self.grid_cell = self._make_grid_cell()

  def setup_basis(self) -> np.ndarray:
    """Sets up the basis of the grid coordinate generation matrix.

    Returns:
      np.nd.array: self.n_axes x 2 matrix to generate float coordinates
        of cells in Cartesian space from integer grid coordinates of
        cells.
    """
    # angles are perpendicular to the direction of their respective strands
    # so e.g. 2nd strand in 3 axis case is at 120, and perpendicular is 210
    if self.n_axes == 2:
      angles = (np.pi / 2, 0)
      dx = [self.spacing * np.cos(a) for a in angles]  # [0, 1]
      dy = [self.spacing * np.sin(a) for a in angles]  # [1, 0]
    elif self.n_axes == 3:
      angles = [np.pi / 6 * x for x in range(3, 12, 4)]  # [90, 210, 330]
      dx = [self.spacing * 2 / 3 * np.cos(a) for a in angles]
      dy = [self.spacing * 2 / 3 * np.sin(a) for a in angles]
    return np.array(dx + dy).reshape((2, self.n_axes))


  def get_coordinates(self, coords: tuple) -> np.ndarray:
    """Uses self.basis to determine Cartesian coordinates of cell centroid
    from grid coordinates.

    Args:
      coords (tuple[int]): integer coordinate pair of grid location.

    Returns:
      np.ndarray: float coordinate pair of grid cell centroid.
    """
    return self.basis @ coords


  def get_grid_cell_at(self, coords: tuple[int] = None) -> geom.Polygon:
    """Returns grid cell polygon centred on coords.

    Args:
      coords (tuple[int], optional): _description_. Defaults to None.

    Returns:
      geom.Polygon: square or triangle centred at the specified
        coordinates.
    """
    if coords is None:
      coords = tuple([0] * self.n_axes)
    if self.grid_cell is None:
      polygon = self._make_grid_cell()
    else:
      polygon = self.grid_cell
      xy = self.get_coordinates(coords)
      polygon = affine.translate(polygon, xy[0], xy[1])
    if self.n_axes == 2 or sum(coords) %2 == 0:
      return polygon
    else:
      return affine.rotate(polygon, 180, origin = polygon.centroid)


  def _make_grid_cell(self) -> geom.Polygon:
    r"""Returns base cell polygon for this _WeaveGrid

    Grid cell is centred at (0, 0) with  number of sides dependent
    on self.n_axes. One side of polygon will be horizontal below the
    x-axis symmetric about the y-axis. Radii to corners are either

    n_axes=2:   n_axes=3:
      \  /          |
       \/           |
       /\          / \
      /  \        /   \

    face to face distance of cell from base vertically to the opposite face
    or corner is (square) L = 2 Rcos(45), or (triangle) L = R + Rcos(60) where R is the radius of the circumcircle.

    Polygon is generated by finding points equally spaced on the
    circumcircle. Note that the code could easily be altered to return a
    hexagon, if the need arises (this would require a change to the basis
    calculation also).

    Returns:
      Polygon: square or triangular cell of appropriate size i.e. spacing
        centred at (0, 0).
    """
    n_sides = 4 if self.n_axes == 2 else 3
    if n_sides == 4:
      R = self.spacing / (2 * np.cos(np.pi / n_sides))
    else:
      R = self.spacing / (1 + np.cos(np.pi / n_sides))
    angles = self._get_angles(n_sides)
    corners = [(R * np.cos(a), R * np.sin(a)) for a in angles]
    return geom.Polygon(corners)


  def _get_angles(self, n: int = 4) -> list[float]:
    """Returns angles to corners of n sides polygon, assuming one side is horizontal parallel to x-axis.

    To determine angles start at 6 o'clock (3pi/2) and add (pi/n), then
    subtract a series of n - 1 2pi/n steps. Note we subtract due to the CW
    polygon winding order convention

    Args:
      n (int, optional): Number of sides. Defaults to 4.

    Returns:
      list[float]: angles in radians.
    """
    return [(3 * np.pi/2) + (np.pi/n) - (i/n * 2 * np.pi) for i in range(n)]


  def _get_grid_cell_slices(self, L:float, W:float = 1,
                n_slices:int = 1) -> list[geom.Polygon]:
    r"""Gets list of rectangular polygons represneting 'slices' across cell.

    Returns 'slices' across grid cell (i.e. horizontally) centred vertically
    relative to the cell, ie

             /\
            /  \
    +------------------+
    |     /      \     |
    +------------------+
    |   /          \   |
    +------------------+
      /              \
     /________________\

    Horizontal extent is L, total width of the strips is W * self.spacing,
    they are 'sliced' horizontally in n_slices slices of equal width.

    Args:
      L (float, optional): length of slices. Defaults to 0.
      W (float, optional): width of slices relative to grid spacing.
        Defaults to 1.
      n_slices (int, optional): number of slices to divide strands into
        along their length. Defaults to 1.

    Returns:
      list[geom.Polygon]: _description_
    """
    L = self.spacing if L == 0 else L
    # note that strand width is based on self.spacing, not L because L
    # may be larger if generating slices for aspect < 1 when strands
    # will extend outside grid cell.
    strand_w = self.spacing * W
    slice_w = strand_w / n_slices
    odd_numbers = [x for x in range(1, 2 * n_slices, 2)]
    slice_offsets = [(slice_w * o / 2) - (strand_w / 2) for o in odd_numbers]
    base_slice = geom.Polygon([(-L/2, -slice_w/2), (-L/2,  slice_w/2),
                               ( L/2,  slice_w/2), ( L/2, -slice_w/2)])
    return [affine.translate(base_slice, 0, offset) 
        for offset in slice_offsets]
    

  def _get_cell_strands(
      self, width:float = 1.0, coords:tuple[int] = None,
      orientation:int = 0, n_slices:int = 1
    ) -> list[Union[geom.Polygon,geom.MultiPolygon]]:
    """Gets n_slices cells strands with specified total width across the
    grid cell at coords at orientation.

    Args:
      width (float, optional): total width of strands relative to
        self.spacing. Defaults to 1.0.
      coords (tuple[int], optional): integer grid coordinates of
        cell. Defaults to None.
      orientation (int, optional): orientation of the strands.
        Defaults to 0.
      n_slices (int, optional): number of length-wise slices to cut
        strands into. Defaults to 1.

    Returns:
      list[Union[geom.Polygon,geom.MultiPolygon]]: polygons representing the 
        strands.
    """
    cell = self.get_grid_cell_at(coords)
    # when aspect is <1 strands extend outside cell by some scale factor
    sf = 2 - width if self.n_axes == 2 else (5 - 3 * width) / 2
    expanded_cell = affine.scale(cell, sf, sf, origin = cell.centroid)
    big_l = (sf * self.spacing       ## rectangular case is simple
             if self.n_axes == 2     ## triangular less so!
             else sf * self.spacing * 2 / np.sqrt(3) * (3 - width) / 2)
    strands = geom.MultiPolygon(
      self._get_grid_cell_slices(L = big_l, W = width, n_slices = n_slices))
    # we need centre of cell bounding box to shift strands to 
    # vertical center of triangular cells. In rectangular case
    # this will be (0, 0).
    cell_offset = cell.envelope.centroid
    strands = affine.translate(strands, cell_offset.x, cell_offset.y)
    strands = geom.MultiPolygon(
        [expanded_cell.intersection(s) for s in strands.geoms])
    strands = affine.rotate(strands, orientation, origin = cell.centroid)
    return [s for s in strands.geoms]


  def get_visible_cell_strands(
      self, width:float= 1.0, coords:tuple[int] = None,
      strand_order:tuple[int] = (0, 1, 2), n_slices:tuple[int] = (1, 1, 1)
    ) -> list[Union[geom.Polygon,geom.MultiPolygon]]:
    """Returns visible strands in grid cell based on layer order.

    Returns visible parts of the strands in a grid cell, given strand width, strand layer order and the number of slices in each direction.

    Args:
      width (float): total width of strands relative to self.spacing.
        Defaults to 1.0.
      coords (tuple[int], optional): grid cell coordinates. Defaults
        to None.
      strand_order (tuple[int], optional): order of the layers from top,
        at this cell site. Defaults to (0, 1, 2).
      n_slices (tuple[int], optional): number of slices in each layer
        at this cell site. Defaults to (1, 1, 1).

    Returns:
      list[Union[geom.Polygon,geom.MultiPolygon]]: those polygons that
        will be visible at this site given requested strand order from
        the top.
    """
    all_polys = []
    for order in strand_order[:self.n_axes]:
        next_polys = self._get_cell_strands(width, coords, 
                                            self.orientations[order], 
                                            n_slices[order])
        if all_polys == []:
            all_polys.extend(next_polys)
            mask = shapely.unary_union(next_polys)
        else:
            # buffering the mask cleans up many issues with closely
            # aligned polygon edges in overlayed layers
            all_polys.extend([p.difference(
              mask.buffer(tiling_utils.RESOLUTION, join_style = 2, cap_style = 3)) 
              for p in next_polys])
            mask = mask.union(shapely.unary_union(next_polys))
    return all_polys


  def get_tile_from_cells(self, approx_tile:geom.Polygon) -> geom.Polygon:
    """Returns a rectangle or hexagon derived from the bounds of the
    supplied approximation to a tile.

    This is required because we know the required tile is an exact 4 or
    6 cornered polygon, but the MultiPolygon formed by unary_union is likely
    to have many more corners than this (for some reason...).

    Args:
      approx_tile (geom.Polygon): MultiPolygon formed from the cells of
        the tile.

    Returns:
      geom.Polygon (geom.Polygon): rectangle or hexagon geom.Polygon.
    """
    xmin, ymin, xmax, ymax = approx_tile.bounds
    if self.n_axes == 2:
      w = np.round((xmax - xmin) / self.spacing) * self.spacing
    else:
      h_spacing = self.spacing * 2 / np.sqrt(3)
      w = np.round((xmax - xmin) / h_spacing) * h_spacing
    h = np.round((ymax - ymin) / self.spacing) * self.spacing
    if self.n_axes == 2:
      return geom.Polygon([(-w/2, -h/2), (-w/2, h/2),
                           (w/2, h/2), (w/2, -h/2)])
    else:
      return geom.Polygon([(w/4, -h/2), (-w/4, -h/2), (-w/2, 0),
                           (-w/4, h/2), ( w/4, h/2), (w/2, 0)])


  # THIS IS HERE FOR SAFE KEEPING... at various times the shapely.set_precision
  # function causes havoc in this class, and the below has proven more stable
  # Note that the more aggressive precision setting here might be relevant also
  # def _gridify(self, shape: geom.Polygon, precision = 4) -> geom.Polygon:
  #   """Returns polygon with coordinates at specified precision.
    
  #   IMPORTANT (and not understood...!!!). This local method seems to work 
  #   better on the kinds of gridification required for the weave grid polygons 
  #   to work... I have no idea why. It may relate to the reordering of 
  #   coordinates that shapely.set_precision engages in... or... it might not. 
  #   It clearly has something to do with floating point issues. I JUST DON'T 
  #   KNOW...
    
  #   TODO: Figure this the hell out at some point!

  #   Args:
  #     shape (geom.Polygon): polygon to gridify.
  #     precision (int): digits of precision. Defaults to 4.

  #   Returns:
  #     geom.Polygon: gridified polygon.
  #   """
  #   return wkt.loads(wkt.dumps(shape, rounding_precision = precision))
  