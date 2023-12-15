# Consume MLModelAPI

## URL
https://mlmodel-api-mr4guvmuya-et.a.run.app

## Endpoints

### Process Input

#### Endpoint

POST /proses_input


#### Request

- **Method**: `POST`
- **Content-Type**: `application/json`
- **Body**: JSON object with the following fields:
  - `laundry_id`: ID of the laundry (int 1-740)

#### Request Body Example
  ```
    {
      "laundry_id": "738"
    }
  ```

#### Response

- **Success Response:**

```json
{
  "laundry_results": [
    {
      "id": 48,
      "name": "Laundry XYZ",
      "layanan_names": ["cuci", "setrika"]
    },
    // ... (additional laundry results)
  ]
}
```
- **Error Response:**
```
{
  "error": "Invalid laundry_id"
}

{
  "error": "No layanan data found for the given laundry_id"
}

{
  "error": "No layanan data found for the given laundry_id"
}

