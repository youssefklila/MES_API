# MOMES API User Guide

*Last Updated: June 23, 2025*  
*Version: 1.0.0*

## Table of Contents
1. [Authentication](#authentication)
2. [Maintenance Configuration API](#maintenance-configuration-api)
3. [BOM (Bill of Materials) API](#bom-api)
4. [Failure Type API](#failure-type-api)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Versioning](#versioning)
8. [Response Format](#response-format)
9. [Pagination](#pagination)
10. [Filtering and Sorting](#filtering-and-sorting)
11. [Data Validation](#data-validation)

## Authentication
All API endpoints require authentication using OAuth2 with JWT tokens. Include the token in the `Authorization` header as a Bearer token.

```http
Authorization: Bearer <your_jwt_token>
```

## 1. Maintenance Configuration API

### Base URL: `/maintenance/configuration`

#### Get All Configurations
- **Endpoint:** `GET /`
- **Permission Required:** `maintenance:configuration:read`
- **Description:** Retrieve all maintenance configurations
- **Response:** List of configuration objects
- **Example Request:**
  ```http
  GET /maintenance/configuration/
  Authorization: Bearer your_jwt_token
  ```

#### Get Configuration by ID
- **Endpoint:** `GET /{config_id}`
- **Permission Required:** `maintenance:configuration:read`
- **Description:** Get a specific configuration by its ID
- **Parameters:**
  - `config_id` (path, required): The ID of the configuration to retrieve
- **Example Request:**
  ```http
  GET /maintenance/configuration/1
  Authorization: Bearer your_jwt_token
  ```

#### Create Configuration
- **Endpoint:** `POST /`
- **Permission Required:** `maintenance:configuration:create`
- **Description:** Create a new maintenance configuration
- **Request Body:**
  ```json
  {
    "name": "Nightly Backup",
    "description": "Configuration for nightly backup process",
    "url": "https://api.example.com/backup",
    "refresh_time": 86400,
    "state": "ACTIVE"
  }
  ```
- **Example Request:**
  ```http
  POST /maintenance/configuration/
  Authorization: Bearer your_jwt_token
  Content-Type: application/json
  
  {
    "name": "Nightly Backup",
    "description": "Configuration for nightly backup process",
    "url": "https://api.example.com/backup",
    "refresh_time": 86400,
    "state": "ACTIVE"
  }
  ```

#### Update Configuration
- **Endpoint:** `PUT /{config_id}`
- **Permission Required:** `maintenance:configuration:update`
- **Description:** Update an existing configuration
- **Parameters:**
  - `config_id` (path, required): The ID of the configuration to update
- **Request Body:** Fields to update (partial updates supported)
  ```json
  {
    "state": "INACTIVE"
  }
  ```
- **Example Request:**
  ```http
  PUT /maintenance/configuration/1
  Authorization: Bearer your_jwt_token
  Content-Type: application/json
  
  {
    "state": "INACTIVE"
  }
  ```

#### Delete Configuration
- **Endpoint:** `DELETE /{config_id}`
- **Permission Required:** `maintenance:configuration:delete`
- **Description:** Delete a configuration
- **Parameters:**
  - `config_id` (path, required): The ID of the configuration to delete
- **Example Request:**
  ```http
  DELETE /maintenance/configuration/1
  Authorization: Bearer your_jwt_token
  ```

## 2. BOM (Bill of Materials) API

### Base URL: `/bom`

#### Get All BOMs
- **Endpoint:** `GET /`
- **Permission Required:** `bom:read`
- **Description:** Retrieve all BOMs
- **Response:** List of BOM objects
- **Query Parameters:**
  - `skip` (optional): Number of records to skip (default: 0)
  - `limit` (optional): Maximum number of records to return (default: 100, max: 1000)
- **Example Request:**
  ```http
  GET /bom/?skip=0&limit=10
  Authorization: Bearer your_jwt_token
  ```

#### Get BOM by ID
- **Endpoint:** `GET /{bom_id}`
- **Permission Required:** `bom:read`
- **Description:** Get a specific BOM by its ID
- **Parameters:**
  - `bom_id` (path, required): The ID of the BOM to retrieve
- **Example Request:**
  ```http
  GET /bom/123
  Authorization: Bearer your_jwt_token
  ```

#### Create BOM
- **Endpoint:** `POST /`
- **Permission Required:** `bom:create`
- **Description:** Create a new BOM
- **Request Body:**
  ```json
  {
    "state": "DRAFT",
    "bom_type": "MANUFACTURING",
    "bom_version": "1.0.0",
    "part_number": "PN-12345"
  }
  ```
- **Example Request:**
  ```http
  POST /bom/
  Authorization: Bearer your_jwt_token
  Content-Type: application/json
  
  {
    "state": "DRAFT",
    "bom_type": "MANUFACTURING",
    "bom_version": "1.0.0",
    "part_number": "PN-12345"
  }
  ```

#### Update BOM
- **Endpoint:** `PUT /{bom_id}`
- **Permission Required:** `bom:update`
- **Description:** Update an existing BOM
- **Parameters:**
  - `bom_id` (path, required): The ID of the BOM to update
- **Request Body:** Fields to update (partial updates supported)
  ```json
  {
    "state": "APPROVED"
  }
  ```
- **Example Request:**
  ```http
  PUT /bom/123
  Authorization: Bearer your_jwt_token
  Content-Type: application/json
  
  {
    "state": "APPROVED"
  }
  ```

#### Delete BOM
- **Endpoint:** `DELETE /{bom_id}`
- **Permission Required:** `bom:delete`
- **Description:** Delete a BOM
- **Parameters:**
  - `bom_id` (path, required): The ID of the BOM to delete
- **Example Request:**
  ```http
  DELETE /bom/123
  Authorization: Bearer your_jwt_token
  ```

## 3. Failure Type API

### Base URL: `/failure-types`

#### Get All Failure Types
- **Endpoint:** `GET /`
- **Permission Required:** `failure_type:read`
- **Description:** Retrieve all failure types
- **Response:** List of failure type objects
- **Query Parameters:**
  - `skip` (optional): Number of records to skip (default: 0)
  - `limit` (optional): Maximum number of records to return (default: 100, max: 1000)
- **Example Request:**
  ```http
  GET /failure-types/?skip=0&limit=10
  Authorization: Bearer your_jwt_token
  ```

#### Get Failure Type by ID
- **Endpoint:** `GET /{failure_type_id}`
- **Permission Required:** `failure_type:read`
- **Description:** Get a specific failure type by its ID
- **Parameters:**
  - `failure_type_id` (path, required): The ID of the failure type to retrieve
- **Example Request:**
  ```http
  GET /failure-types/1
  Authorization: Bearer your_jwt_token
  ```

#### Get Failure Type by Code
- **Endpoint:** `GET /code/{failure_type_code}`
- **Permission Required:** `failure_type:read`
- **Description:** Get a specific failure type by its code
- **Parameters:**
  - `failure_type_code` (path, required): The code of the failure type to retrieve
- **Example Request:**
  ```http
  GET /failure-types/code/ELEC_001
  Authorization: Bearer your_jwt_token
  ```

#### Create Failure Type
- **Endpoint:** `POST /`
- **Permission Required:** `failure_type:create`
- **Description:** Create a new failure type
- **Request Body:**
  ```json
  {
    "code": "MECH_001",
    "name": "Bearing Failure",
    "description": "Failure related to bearing components",
    "failure_group_id": 1
  }
  ```
- **Example Request:**
  ```http
  POST /failure-types/
  Authorization: Bearer your_jwt_token
  Content-Type: application/json
  
  {
    "code": "MECH_001",
    "name": "Bearing Failure",
    "description": "Failure related to bearing components",
    "failure_group_id": 1
  }
  ```

#### Update Failure Type
- **Endpoint:** `PUT /{failure_type_id}`
- **Permission Required:** `failure_type:update`
- **Description:** Update an existing failure type
- **Parameters:**
  - `failure_type_id` (path, required): The ID of the failure type to update
- **Request Body:** Fields to update (partial updates supported)
  ```json
  {
    "description": "Updated description for bearing failure"
  }
  ```
- **Example Request:**
  ```http
  PUT /failure-types/1
  Authorization: Bearer your_jwt_token
  Content-Type: application/json
  
  {
    "description": "Updated description for bearing failure"
  }
  ```

#### Delete Failure Type
- **Endpoint:** `DELETE /{failure_type_id}`
- **Permission Required:** `failure_type:delete`
- **Description:** Delete a failure type
- **Parameters:**
  - `failure_type_id` (path, required): The ID of the failure type to delete
- **Example Request:**
  ```http
  DELETE /failure-types/1
  Authorization: Bearer your_jwt_token
  ```

## Error Handling

All API endpoints return appropriate HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Resource deleted successfully |
| 400 | Bad Request - Invalid request parameters |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

Example error response:
```json
{
  "detail": "Error message describing the issue"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. If you exceed the rate limit, you'll receive a `429 Too Many Requests` response with the following headers:

- `Retry-After`: The number of seconds to wait before making another request
- `X-RateLimit-Limit`: The maximum number of requests allowed in the time window
- `X-RateLimit-Remaining`: The number of requests remaining in the current window
- `X-RateLimit-Reset`: The time at which the current rate limit window resets (UTC epoch seconds)

## Versioning

The API is versioned through the URL path. The current version is `v1`.

Example: `/api/v1/failure-types`

## Response Format

All successful responses are returned in JSON format. The response structure depends on the endpoint but generally follows these patterns:

### Single Item Response
```json
{
  "id": 1,
  "name": "Item Name",
  "description": "Item description",
  "created_at": "2025-06-23T10:00:00Z",
  "updated_at": "2025-06-23T10:00:00Z"
}
```

### List Response
```json
{
  "items": [
    {
      "id": 1,
      "name": "Item 1"
    },
    {
      "id": 2,
      "name": "Item 2"
    }
  ],
  "total": 2,
  "skip": 0,
  "limit": 10
}
```

### Error Response
```json
{
  "detail": "Error message describing the issue"
}
```

## Pagination

Endpoints that return lists of items support pagination using query parameters:

- `skip` (integer, optional): Number of items to skip (default: 0)
- `limit` (integer, optional): Maximum number of items to return (default: 100, max: 1000)

Example: `GET /failure-types?skip=20&limit=10`

Pagination responses include the following metadata:

- `items`: Array of the requested items
- `total`: Total number of items available
- `skip`: Number of items skipped
- `limit`: Maximum number of items returned per page

## Filtering and Sorting

Most list endpoints support filtering and sorting using query parameters.

### Filtering

Filter items by including field names and values as query parameters:

```
GET /failure-types?state=ACTIVE&type=ELECTRICAL
```

### Sorting

Sort items by including a `sort` parameter with the field name and direction:

- `sort=field` - Sort by field in ascending order
- `sort=-field` - Sort by field in descending order

Multiple sort fields can be specified as comma-separated values:

```
GET /failure-types?sort=name,-created_at
```

## Data Validation

All input data is validated against the defined schemas. Invalid data will result in a `400 Bad Request` or `422 Unprocessable Entity` response with details about the validation errors.

Example validation error response:

```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

## Best Practices

1. **Always use HTTPS** to ensure data security and integrity.
2. **Handle errors gracefully** - Always check the response status code and handle errors appropriately.
3. **Implement retry logic** for failed requests, especially for rate-limited endpoints.
4. **Cache responses** when appropriate to reduce server load and improve performance.
5. **Use pagination** for large datasets to improve performance.
6. **Keep your API key secure** and never expose it in client-side code.
7. **Follow RESTful principles** when designing your API interactions.
8. **Use appropriate HTTP methods** (GET, POST, PUT, DELETE) as per their intended use.
9. **Include proper headers** like `Content-Type: application/json` for JSON payloads.
10. **Monitor your API usage** to stay within rate limits and identify issues early.

## Support

For support or questions about the API, please contact the MOMES support team at [support@momes.com](mailto:support@momes.com).

---
*Documentation generated on June 23, 2025*
