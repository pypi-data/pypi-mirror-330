import pytest
from shapely.geometry import LineString, Point, Polygon, MultiLineString, MultiPolygon
from ..Geometries import (
    GeoTrajectory,
    GeoMultiTrajectory,
    GeoPoint,
    GeoPolygon,
    GeoMultiPolygon,
)


def test_geo_trajectory_init():
    linestring = LineString([(12.620400, 55.687962), (12.632788, 55.691589)])
    geo_trajectory = GeoTrajectory(linestring)
    assert geo_trajectory.geometry == linestring
    assert geo_trajectory.crs == "WGS84"


def test_geo_multi_trajectory_init_with_linestring():
    linestring = LineString([(12.620400, 55.687962), (12.632788, 55.691589)])
    geo_multi_trajectory = GeoMultiTrajectory(linestring)
    assert geo_multi_trajectory.geometry == MultiLineString([linestring])
    assert geo_multi_trajectory.crs == "WGS84"


def test_geo_multi_trajectory_init_with_list_of_linestrings():
    linestrings = [
        LineString([(12.620400, 55.687962), (12.632788, 55.691589)]),
        LineString([(12.637446, 55.687689), (12.624924, 55.683489)]),
    ]
    geo_multi_trajectory = GeoMultiTrajectory(linestrings)
    assert geo_multi_trajectory.geometry == MultiLineString(linestrings)
    assert geo_multi_trajectory.crs == "WGS84"


def test_geo_point_init():
    point = Point(12.624924, 55.683489)
    geo_point = GeoPoint(point)
    assert geo_point.geometry == point
    assert geo_point.crs == "WGS84"


def test_geo_polygon_init_with_polygon():
    polygon = Polygon(
        [
            (12.620400, 55.687962),
            (12.632788, 55.691589),
            (12.637446, 55.687689),
            (12.624924, 55.683489),
        ]
    )
    geo_polygon = GeoPolygon(polygon)
    assert geo_polygon.geometry == polygon
    assert geo_polygon.crs == "WGS84"


def test_geo_polygon_init_with_linestring():
    linestring = LineString(
        [
            (12.620400, 55.687962),
            (12.632788, 55.691589),
            (12.637446, 55.687689),
            (12.624924, 55.683489),
        ]
    )
    geo_polygon = GeoPolygon(linestring)
    assert geo_polygon.geometry == Polygon(linestring)
    assert geo_polygon.crs == "WGS84"


def test_geo_multi_polygon_init_with_list_of_polygons():
    polygons = [
        Polygon(
            [
                (12.620400, 55.687962),
                (12.632788, 55.691589),
                (12.637446, 55.687689),
                (12.624924, 55.683489),
            ]
        ),
        Polygon(
            [
                (12.628446, 55.686489),
                (12.625924, 55.688489),
                (12.630924, 55.689489),
                (12.629446, 55.685489),
            ]
        ),
    ]
    geo_multi_polygon = GeoMultiPolygon(polygons)
    assert geo_multi_polygon.geometry == MultiPolygon(polygons)
    assert geo_multi_polygon.crs == "WGS84"


def test_geo_multi_polygon_init_with_multipolygon():
    multipolygon = MultiPolygon(
        [
            Polygon(
                [
                    (12.620400, 55.687962),
                    (12.632788, 55.691589),
                    (12.637446, 55.687689),
                    (12.624924, 55.683489),
                ]
            ),
            Polygon(
                [
                    (12.628446, 55.686489),
                    (12.625924, 55.688489),
                    (12.630924, 55.689489),
                    (12.629446, 55.685489),
                ]
            ),
        ]
    )
    geo_multi_polygon = GeoMultiPolygon(multipolygon)
    assert geo_multi_polygon.geometry == multipolygon
    assert geo_multi_polygon.crs == "WGS84"


if __name__ == "__main__":
    pytest.main(["-v", "-x", "trajgenpy/test_Geometries.py"])
