from .exceptions import SierraResponseConverterException


class SierraResponseConverter:
    """Converts a JSON response from the Sierra API to MARC-in-JSON format."""
    
    def __init__(self, response: dict):
        if not isinstance(response, dict):
            raise SierraResponseConverterException("Please provide a valid JSON response.")
        self.response = response
    
    def _map_control_fields(self, field: dict) -> dict:
        # for tags < 010, no subfields, instead one str value in "value" 
        return {field["tag"]: field["value"]}
    
    def _map_data_fields(self, field: dict) -> dict:
        """ Maps marc fields > 010. 

        Args:
            field (dict): Contains the marc tag and list with indicators and subfields.

        Returns:
            dict: standardised marc-in-json format.
        """
        
        data = field["data"]
        
        # Order matters ind1, in2, subfields
        field_data = {
            "ind1": data.get("ind1", " "),
            "ind2": data.get("ind2", " "),
            "subfields": data.get("subfields", [])
        }
        
        return {field["tag"]: field_data}
    
    def _is_marc21structured(self, field: dict) -> bool:
        """Checks if the field is already structured according to MARC21 in JSON"""
        return any(key.isdigit() for key in field.keys())
        
    
    def _handle_field_type(self, field: dict) -> dict:
        
        if self._is_marc21structured(field):
            return field
        
        if field.get("data"):
            return self._map_data_fields(field)
        
        tag = field.get("tag")
        
        if not tag:
            raise SierraResponseConverterException("Field is missing MARC21 tag.")
        
        if tag < "010":
            return self._map_control_fields(field)
        else:
            return self._map_data_fields(field)
        
    def _convert_response(self) -> list:
        entries = self.response.get("entries")
        if not entries:
            raise SierraResponseConverterException("No entries found in the response.")
        
        try:
            return {"fields": [
                {e["id"]: [
                    self._handle_field_type(f) for f in e["marc"]["fields"]
                    ]}
                for e in entries
            ]}
            
        except KeyError as e:
            raise SierraResponseConverterException(f"Malformed response: missing key {e}")
        
    
    def convert(self) -> list:
        try:
            return self._convert_response()
        except Exception as e:
            raise SierraResponseConverterException(f"An unexpected error occurred: {e}")
