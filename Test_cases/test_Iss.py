import mock
from jsonschema import validate
import Main.Iss_location
from unittest.mock import patch
import unittest
import time


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

    def test_speed(self):
        """
        Purpose of this test is to verify that the speed covered by the ISS in 10 seconds is within range
        """
        range_min = 20000
        range_max = 30000
        x0 = Main.Iss_location.get_coordinates(Main.Iss_location.get_json())
        time.sleep(1)
        x1 = Main.Iss_location.get_coordinates(Main.Iss_location.get_json())
        speed = Main.Iss_location.get_avg_speed(x0, x1)

        # distance = getting1.distance_between_coordinate(x0, x1)
        # distance = 24000
        if range_min < speed < range_max:
            return True
        else:
            return False

    def test_distance(self):
        x = Main.Iss_location.distance_between_coordinate((11.1395, -143.6654), (11.9168, -143.0815))
        print(x)
        self.assertEqual(Main.Iss_location.distance_between_coordinate((11.1395, -143.6654), (11.9168, -143.0815)),
                         107.2522412348488)

    def tearDown(self):
        print("closed")


if __name__ == "__main__":
    unittest.main()
