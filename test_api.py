import requests
import json
import sys

def test_tracking_number(tracking_number):
    """Test a tracking number against the Czech Post API and print the full response."""
    base_url = "https://b2c.cpost.cz/services/ParcelHistory/getDataAsJson"
    
    params = {
        "idParcel": tracking_number.strip(),
        "language": "en"  # Can be 'cs' for Czech
    }
    
    print(f"Making request to: {base_url}")
    print(f"With parameters: {params}")
    print("-" * 80)
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        
        print(f"Status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print("-" * 80)
        
        # Try to parse as JSON
        try:
            data = response.json()
            # Pretty print the JSON response with indentation
            print("JSON Response:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Raw response (not valid JSON):")
            print(response.text)
            
    except Exception as e:
        print(f"Error making request: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tracking_number = sys.argv[1]
    else:
        tracking_number = input("Enter tracking number to test: ")
    
    test_tracking_number(tracking_number) 