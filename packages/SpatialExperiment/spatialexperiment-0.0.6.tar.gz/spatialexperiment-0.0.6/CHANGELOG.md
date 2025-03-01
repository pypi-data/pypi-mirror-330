# Changelog

## Version 0.0.6
- Added `read_tenx_visium()` function to load 10x Visium data as SpatialExperiment
- Added `combine_columns` function
- Implemented `__eq__` override for `SpatialImage` subclasses

## Version 0.0.5

- Implementing a placeholder `SpatialFeatureExperiment` class. This version only implements the data structure to hold various geometries but none of the methods except for slicing.

## Version 0.0.3 - 0.0.4

- Streamlining the `SpatialImage` class implementations.

## Version 0.0.1 - 0.0.2

- Initial version of the SpatialExperiment class with the additional slots.
- Allow spatial coordinates to be a numpy array
