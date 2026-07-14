# import the necessary modules and libraries
import json, unittest
from dateutil import parser   # more robust timestamp parsing

# use the open function to open and read the three json files
with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)

# convert json data from format 1 to the expected format
def convertFromFormat1(jsonObject):
    # split location string into parts
    locationParts = jsonObject["location"].split("/")
    if len(locationParts) != 5:
        raise ValueError("Invalid location format in Type 1 JSON")

    # create a new dictionary for the unified format
    result = {
        'deviceID': jsonObject['deviceID'],
        'deviceType': jsonObject['deviceType'],
        'timestamp': jsonObject['timestamp'],  # already in ms since epoch
        'location': {
            'country': locationParts[0],
            'city': locationParts[1],
            'area': locationParts[2],
            'factory': locationParts[3],
            'section': locationParts[4]
        },
        'data': {
            'status': jsonObject['operationStatus'],
            'temperature': jsonObject['temp']
        }
    }
    return result


# convert json data from format 2 to the expected format
def convertFromFormat2(jsonObject):
    # convert the ISO 8601 timestamp to milliseconds since epoch
    data = parser.isoparse(jsonObject['timestamp'])
    timestamp = round(data.timestamp() * 1000)

    # create a new dictionary for the unified format
    result = {
        'deviceID': jsonObject['device']['id'],
        'deviceType': jsonObject['device']['type'],
        'timestamp': timestamp,
        'location': {
            'country': jsonObject['country'],
            'city': jsonObject['city'],
            'area': jsonObject['area'],
            'factory': jsonObject['factory'],
            'section': jsonObject['section']
        },
        'data': jsonObject['data']
    }
    return result


def main(jsonObject):
    if jsonObject.get('device') is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)


# Test cases using unittest module
class TestSolution(unittest.TestCase):

    def test_sanity(self):
        # sanity test to ensure expected result is as intended
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )


if __name__ == '__main__':
    # run the tests
    unittest.main()