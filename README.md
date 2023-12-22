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
            "id": 207,
            "layanan_names": [
                "dryclean",
                "setrika"
            ],
            "name": "Sri Laundry"
        },
        {
            "id": 191,
            "layanan_names": [
                "cuci",
                "dryclean",
                "setrika",
                "komplit"
            ],
            "name": "SEKAR JAGO Laundry"
        },
        {
            "id": 176,
            "layanan_names": [
                "cuci",
                "dryclean",
                "setrika",
                "komplit"
            ],
            "name": "Shekar Laundry Semarang"
        },
        {
            "id": 172,
            "layanan_names": [
                "cuci",
                "dryclean",
                "setrika",
                "komplit"
            ],
            "name": "Cathy Laundry 2"
        },
        {
            "id": 137,
            "layanan_names": [
                "cuci",
                "dryclean",
                "setrika",
                "komplit"
            ],
            "name": "Washteria"
        }
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
```
### Laundry Terdekat
#### Endpoint

POST /laundry_terdekat

#### Request

- **Method**: `POST`
- **Content-Type**: `application/json`
- **Body**: JSON object with the following fields:
  - `latitude`: latitude of user
  - `longitude`: longitude of user
    
#### Request Body Example
  ```
  {
  "latitude": 37.7749,
  "longitude": -122.4194
  }
  ```
#### Response

- **Success Response:**

```json
{
    "nearest_laundries": [
        {
            "id": 744,
            "latitude": "0.9039482",
            "longitude": "-0.5684941",
            "name": "Laundry PBGa"
        },
        {
            "id": 745,
            "latitude": "0.903948",
            "longitude": "-0.568494",
            "name": "Laundry PBG"
        },
        {
            "id": 746,
            "latitude": "0.903948",
            "longitude": "-0.568494",
            "name": "Laundry Reza"
        },
        {
            "id": 747,
            "latitude": "0.903948",
            "longitude": "-0.568494",
            "name": "Laundry Reza"
        },
        {
            "id": 748,
            "latitude": "0.903948",
            "longitude": "-0.568494",
            "name": "Laundry Reza"
        }
    ]
}
```
- **Error Response**
```json
{
    "error": "400 Bad Request: The browser (or proxy) sent a request that this server could not understand."
}
```
