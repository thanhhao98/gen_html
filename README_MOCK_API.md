# Mocking API Documentation

A Flask-based API that generates realistic Vietnamese mock data based on `specs.json` files from your form templates.

## Features

- **Intelligent Mock Data Generation**: Generates realistic Vietnamese data based on field types and names
- **Multiple Record Support**: Generate single or multiple mock records
- **Form Validation**: Mock form submission with validation against specs
- **Template Discovery**: Automatically discovers all available templates
- **Vietnamese Localization**: Uses Vietnamese Faker for realistic local data

## Installation

1. Install dependencies:
```bash
pip install -r requirements_mock.txt
```

2. Start the mocking API server:
```bash
python mocking_be.py
```

The API will run on `http://localhost:5001`

## API Endpoints

### 1. Health Check
```
GET /api/health
```
Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "service": "Mocking API",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### 2. List Templates
```
GET /api/templates
```
Lists all available templates with their field specifications.

**Response:**
```json
{
  "success": true,
  "count": 2,
  "templates": [
    {
      "name": "test3",
      "fields_count": 7,
      "fields": [
        {
          "display_name": "Họ và tên",
          "field_name": "full_name",
          "field_type": "text"
        },
        {
          "display_name": "Số điện thoại",
          "field_name": "phone_number",
          "field_type": "tel"
        }
      ]
    }
  ]
}
```

### 3. Generate Mock Data
```
GET /api/mock/{template_name}
GET /api/mock/{template_name}?count={number}
```
Generates mock data for a specific template.

**Parameters:**
- `template_name`: Name of the template folder
- `count` (optional): Number of records to generate (1-100, default: 1)

**Single Record Response:**
```json
{
  "success": true,
  "template": "test3",
  "data": {
    "full_name": "Nguyễn Văn An",
    "phone_number": "0987654321",
    "dob": "15/03/1990",
    "satisfaction": 4,
    "father_name": "Nguyễn Văn Bình",
    "mother_name": "Trần Thị Cẩm",
    "id_number": "123456789012"
  }
}
```

**Multiple Records Response:**
```json
{
  "success": true,
  "template": "test3",
  "count": 3,
  "data": [
    {
      "full_name": "Nguyễn Văn An",
      "phone_number": "0987654321",
      // ... other fields
    },
    // ... more records
  ]
}
```

### 4. Mock Form Submission
```
POST /api/mock/{template_name}/submit
```
Simulates form submission with validation against the template specs.

**Request Body:**
```json
{
  "full_name": "Nguyễn Văn An",
  "phone_number": "0987654321",
  "dob": "15/03/1990",
  "satisfaction": 4,
  "father_name": "Nguyễn Văn Bình",
  "mother_name": "Trần Thị Cẩm",
  "id_number": "123456789012"
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Form submitted successfully",
  "submission_id": "SUB_123456",
  "timestamp": "2024-01-15T10:30:00.123456",
  "submitted_data": {
    // ... submitted data
  }
}
```

**Validation Error Response:**
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": [
    "Invalid phone number format: phone_number",
    "Missing required field: full_name"
  ],
  "submitted_data": {
    // ... submitted data
  }
}
```

## Field Type Support

The API generates appropriate mock data based on field types:

| Field Type | Generated Data | Example |
|------------|----------------|---------|
| `text` | Names, addresses, companies, IDs | "Nguyễn Văn An" |
| `tel` | Vietnamese phone numbers | "0987654321" |
| `email` | Email addresses | "user@example.com" |
| `date` | Dates in DD/MM/YYYY format | "15/03/1990" |
| `rating` | Numeric ratings (1-5) | 4 |
| `number` | Random numbers | 42 |
| `select` | Contextual Vietnamese options | "Hà Nội" |
| `textarea` | Longer text content | "Lorem ipsum..." |
| `checkbox` | Boolean values | true/false |
| `radio` | Vietnamese options | "Có"/"Không" |

## Smart Field Recognition

The API intelligently recognizes field purposes based on field names:

- **Names**: Fields containing "name" or "ten" → Vietnamese names
- **Addresses**: Fields containing "address" or "dia_chi" → Vietnamese addresses
- **Companies**: Fields containing "company" or "cong_ty" → Vietnamese company names
- **IDs**: Fields containing "id", "cccd", or "can_cuoc" → 12-digit ID numbers
- **Gender**: Fields containing "gender" or "gioi_tinh" → "Nam"/"Nữ"/"Khác"
- **Cities**: Fields containing "city" or "thanh_pho" → Vietnamese cities

## Testing

Run the test script to verify all endpoints:

```bash
python test_mock_api.py
```

Make sure the mocking API server is running before executing tests.

## Error Handling

The API provides comprehensive error handling:

- **404**: Template or specs.json not found
- **400**: Invalid JSON format or validation errors
- **500**: Internal server errors

All error responses include descriptive messages to help with debugging.

## Usage Examples

### Generate Mock Data for Testing
```bash
# Get single mock record
curl http://localhost:5001/api/mock/test3

# Get 5 mock records
curl http://localhost:5001/api/mock/test3?count=5
```

### Test Form Submission
```bash
# Submit valid data
curl -X POST http://localhost:5001/api/mock/test3/submit \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test User","phone_number":"0987654321"}'
```

### Integration with Frontend
```javascript
// Fetch mock data for form testing
fetch('/api/mock/test3')
  .then(response => response.json())
  .then(data => {
    // Use mock data to populate form fields
    console.log(data.data);
  });

// Submit form data
fetch('/api/mock/test3/submit', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(formData)
})
.then(response => response.json())
.then(result => {
  if (result.success) {
    console.log('Form submitted successfully');
  } else {
    console.log('Validation errors:', result.errors);
  }
});
``` 