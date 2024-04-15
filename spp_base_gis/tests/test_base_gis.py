import json

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


# TODO: Add more test cases
class BaseGISTest(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.test_model = cls.env["spp.base.gis.test.model"]

        geojson_polygon_1 = {
            "type": "Polygon",
            "coordinates": [
                [
                    [124.719702, 7.848172],
                    [124.750567, 7.848008],
                    [124.76422, 7.836532],
                    [124.681638, 7.833007],
                    [124.680976, 7.84891],
                    [124.719702, 7.848172],
                ]
            ],
        }

        cls.test_record_1 = cls.test_model.create(
            {
                "name": "Record 1",
                "geo_polygon_field": json.dumps(geojson_polygon_1),
            }
        )

        geojson_polygon_2 = {
            "type": "Polygon",
            "coordinates": [
                [
                    [124.935721, 7.956489],
                    [125.008514, 7.941196],
                    [124.999691, 7.890945],
                    [124.935721, 7.956489],
                ]
            ],
        }

        cls.test_record_2 = cls.test_model.create(
            {
                "name": "Record 2",
                "geo_polygon_field": json.dumps(geojson_polygon_2),
            }
        )

        # Coordinates of a point inside Record 1's polygon
        cls.longitude_1, cls.latitude_1 = 124.7291574142456, 7.841423068566499

        # Coordinates of a point inside Record 2's polygon
        cls.longitude_2, cls.latitude_2 = 124.98706532650226, 7.931953944598931

        # Coordinates of a point outside both polygons
        cls.longitude_3, cls.latitude_3 = 124.81488191551932, 7.773921858866217

    def test_gis_locational_query_intersects(self):
        feature_collection_1 = self.test_model.gis_locational_query(
            longitude=self.longitude_1, latitude=self.latitude_1
        )
        feature_collection_2 = self.test_model.gis_locational_query(
            longitude=self.longitude_2, latitude=self.latitude_2
        )
        feature_collection_3 = self.test_model.gis_locational_query(
            longitude=self.longitude_3, latitude=self.latitude_3
        )

        self.assertEqual(feature_collection_1["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_1["features"]), 1)
        self.assertEqual(feature_collection_1["features"][0]["properties"]["name"], self.test_record_1.name)

        self.assertEqual(feature_collection_2["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_2["features"]), 1)
        self.assertEqual(feature_collection_2["features"][0]["properties"]["name"], self.test_record_2.name)

        self.assertEqual(feature_collection_3["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_3["features"]), 0)

    def test_gis_locational_query_intersects_with_distance(self):
        feature_collection_1 = self.test_model.gis_locational_query(
            longitude=self.longitude_1, latitude=self.latitude_1, distance=1000
        )
        feature_collection_2 = self.test_model.gis_locational_query(
            longitude=self.longitude_2, latitude=self.latitude_2, distance=1000
        )
        feature_collection_3 = self.test_model.gis_locational_query(
            longitude=self.longitude_3, latitude=self.latitude_3, distance=1000
        )

        self.assertEqual(feature_collection_1["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_1["features"]), 1)
        self.assertEqual(feature_collection_1["features"][0]["properties"]["name"], self.test_record_1.name)

        self.assertEqual(feature_collection_2["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_2["features"]), 1)
        self.assertEqual(feature_collection_2["features"][0]["properties"]["name"], self.test_record_2.name)

        self.assertEqual(feature_collection_3["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_3["features"]), 0)

    def test_gis_locational_query_within(self):
        feature_collection_1 = self.test_model.gis_locational_query(
            longitude=self.longitude_1, latitude=self.latitude_1, spatial_relation="within"
        )
        feature_collection_2 = self.test_model.gis_locational_query(
            longitude=self.longitude_2, latitude=self.latitude_2, spatial_relation="within"
        )
        feature_collection_3 = self.test_model.gis_locational_query(
            longitude=self.longitude_3, latitude=self.latitude_3, spatial_relation="within"
        )

        self.assertEqual(feature_collection_1["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_1["features"]), 1)
        self.assertEqual(feature_collection_1["features"][0]["properties"]["name"], self.test_record_1.name)

        self.assertEqual(feature_collection_2["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_2["features"]), 1)
        self.assertEqual(feature_collection_2["features"][0]["properties"]["name"], self.test_record_2.name)

        self.assertEqual(feature_collection_3["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_3["features"]), 0)

    def test_gis_locational_query_within_with_distance(self):
        feature_collection_1 = self.test_model.gis_locational_query(
            longitude=self.longitude_1, latitude=self.latitude_1, spatial_relation="within", distance=1000
        )
        feature_collection_2 = self.test_model.gis_locational_query(
            longitude=self.longitude_2, latitude=self.latitude_2, spatial_relation="within", distance=1000
        )
        feature_collection_3 = self.test_model.gis_locational_query(
            longitude=self.longitude_3, latitude=self.latitude_3, spatial_relation="within", distance=1000
        )

        self.assertEqual(feature_collection_1["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_1["features"]), 0)

        self.assertEqual(feature_collection_2["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_2["features"]), 1)
        self.assertEqual(feature_collection_2["features"][0]["properties"]["name"], self.test_record_2.name)

        self.assertEqual(feature_collection_3["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_3["features"]), 0)

    def test_gis_locational_query_contains(self):
        feature_collection_1 = self.test_model.gis_locational_query(
            longitude=self.longitude_1, latitude=self.latitude_1, spatial_relation="contains"
        )
        feature_collection_2 = self.test_model.gis_locational_query(
            longitude=self.longitude_2, latitude=self.latitude_2, spatial_relation="contains"
        )
        feature_collection_3 = self.test_model.gis_locational_query(
            longitude=self.longitude_3, latitude=self.latitude_3, spatial_relation="contains"
        )

        self.assertEqual(feature_collection_1["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_1["features"]), 0)

        self.assertEqual(feature_collection_2["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_2["features"]), 0)

        self.assertEqual(feature_collection_3["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_3["features"]), 0)

    def test_gis_locational_query_contains_with_distance(self):
        feature_collection_1 = self.test_model.gis_locational_query(
            longitude=self.longitude_1, latitude=self.latitude_1, spatial_relation="contains", distance=10000
        )
        feature_collection_2 = self.test_model.gis_locational_query(
            longitude=self.longitude_2, latitude=self.latitude_2, spatial_relation="contains", distance=10000
        )
        feature_collection_3 = self.test_model.gis_locational_query(
            longitude=self.longitude_3, latitude=self.latitude_3, spatial_relation="contains", distance=1000
        )

        self.assertEqual(feature_collection_1["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_1["features"]), 1)
        self.assertEqual(feature_collection_1["features"][0]["properties"]["name"], self.test_record_1.name)

        self.assertEqual(feature_collection_2["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_2["features"]), 1)
        self.assertEqual(feature_collection_2["features"][0]["properties"]["name"], self.test_record_2.name)

        self.assertEqual(feature_collection_3["type"], "FeatureCollection")
        self.assertEqual(len(feature_collection_3["features"]), 0)

    def test_gis_locational_query_errors(self):
        spatial_relation = "error"
        with self.assertRaisesRegex(UserError, f"Invalid spatial relation {spatial_relation}"):
            self.test_model.gis_locational_query(
                longitude=self.longitude_1, latitude=self.latitude_1, spatial_relation=spatial_relation
            )

        layer_type = "triangle"
        with self.assertRaisesRegex(UserError, f"Invalid layer type {layer_type}"):
            self.test_model.gis_locational_query(
                longitude=self.longitude_1, latitude=self.latitude_1, layer_type=layer_type
            )

        distance = -1
        with self.assertRaisesRegex(UserError, "Distance must be a positive number"):
            self.test_model.gis_locational_query(
                longitude=self.longitude_1, latitude=self.latitude_1, distance=distance
            )

        distance = "distance"
        with self.assertRaisesRegex(UserError, "Distance must be a number"):
            self.test_model.gis_locational_query(
                longitude=self.longitude_1, latitude=self.latitude_1, distance=distance
            )

        longitude, latitude = "zero", "one"
        with self.assertRaisesRegex(UserError, f"Invalid coordinates: latitude={latitude}, longitude={longitude}"):
            self.test_model.gis_locational_query(longitude=longitude, latitude=latitude)

        longitude, latitude = 80, 181
        with self.assertRaisesRegex(UserError, f"Invalid coordinates: latitude={latitude}, longitude={longitude}"):
            self.test_model.gis_locational_query(longitude=longitude, latitude=latitude)

        longitude, latitude = 80, -181
        with self.assertRaisesRegex(UserError, f"Invalid coordinates: latitude={latitude}, longitude={longitude}"):
            self.test_model.gis_locational_query(longitude=longitude, latitude=latitude)

        longitude, latitude = 91, 100
        with self.assertRaisesRegex(UserError, f"Invalid coordinates: latitude={latitude}, longitude={longitude}"):
            self.test_model.gis_locational_query(longitude=longitude, latitude=latitude)

        longitude, latitude = -91, 100
        with self.assertRaisesRegex(UserError, f"Invalid coordinates: latitude={latitude}, longitude={longitude}"):
            self.test_model.gis_locational_query(longitude=longitude, latitude=latitude)
