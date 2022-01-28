import mock
from jsonschema import validate
import Main.Iss_location
from unittest.mock import patch, Mock
import unittest


class TestcaseISS(unittest.TestCase):

    def setUp(self) -> None:
        self.todo = {"iss_position": {"longitude": "95.9239", "latitude": "-40.1192"}, "message": "success",
                     "timestamp": 1643231083}
        self.dic_schema = {
            "type": "object",
            "properties": {
                "timestamp": {"type": "integer", "minLength": 2},
                "latitude": {"type": "number", "minLength": 2},
                "longitude": {"type": "number"}
            }
        }
        self.schema = {
            "type": "object",
            "properties": {
                "iss_position": {
                    "type": "object",
                    "properties": {
                        "longitude": {"type": "string"},
                        "latitude": {"type": "string"}}
                    ,
                    "required": ["longitude", "latitude"]
                },
                "message": {"type": "string"},
                "timestamp": {"type": "integer"}
            }
        }

        self.dictio = {'timestamp': 1643287729, 'latitude': -45.2044, 'longitude': -58.7498}

    @mock.patch("Main.Iss_location.get_json")
    def test_call_api(self, mock_get):
        my_mock_response = mock.Mock(status_code=200)
        mock_get.return_value = my_mock_response

    def test_json_data(self):
        with patch("Main.Iss_location.get_json") as mk:
            mk.return_value.json.return_value = self.todo
            resp = Main.Iss_location.get_json().json()

            assert 'timestamp' in resp
            assert 'iss_position' in resp
            assert 'longitude' in resp['iss_position']
            assert 'latitude' in resp['iss_position']
            assert 'message' in resp

            validate(resp, self.schema)
            self.assertEqual(resp, self.todo)

    def test_coordinates_data(self):
        with patch("Main.Iss_location.get_coordinates", return_value='success') as mk:
            mk.return_value = self.dictio
            resp = Main.Iss_location.get_coordinates(Main.Iss_location.get_json())
            resp1 = Main.Iss_location.get_json()

            validate(resp, self.dic_schema)
            self.assertEqual(resp1["message"], "success")
            self.assertEqual(resp, self.dictio)

    def test_distance(self):
        x = Main.Iss_location.distance_between_coordinate((11.1395, -143.6654), (11.9168, -143.0815))
        print(x)
        self.assertEqual(Main.Iss_location.distance_between_coordinate((11.1395, -143.6654), (11.9168, -143.0815)),
                         107.2522412348488)

    def test_avg_speed(self):
        self.assertEqual(Main.Iss_location.get_avg_speed({'timestamp': 1643322942, 'latitude': 37.1165, 'longitude': -118.179},
                                                {'timestamp': 1643322957, 'latitude': 37.7436, 'longitude': -117.2545}),
                         25750.036451600303)
        # with self.assertRaises(ValueError):
        #     getting1.get_avg_speed({'timestamp': "", 'latitude': 37.1165, 'longitude': -118.179},
        #                           {'timestamp': 1643322957, 'latitude': 37.7436, 'longitude': -117.2545})

    def tearDown(self):
        print("closed")

# if __name__ == "__main__":
#     unittest.main()
