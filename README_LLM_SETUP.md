# LLM-Powered Mocking Backend Setup

This updated mocking backend now uses OpenAI's GPT-4o model to generate realistic Vietnamese mock data instead of hardcoded values.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key
You need to set your OpenAI API key as an environment variable:

**Option A: Export in terminal**
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

**Option B: Create .env file**
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

Then install python-dotenv and load it:
```bash
pip install python-dotenv
```

Add this to the top of `mocking_be.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 3. Run the Server
```bash
python mocking_be.py
```

## Features

### LLM-Generated Mock Data
- Uses GPT-4o to generate realistic Vietnamese mock data
- Contextually appropriate data based on field names and types
- Varied and realistic responses for each request

### Fallback System
- If LLM fails, automatically falls back to the original hardcoded method
- Ensures the API always returns data even if OpenAI is unavailable

### API Endpoints

**Get Mock Data (Single Record)**
```bash
curl -X GET "http://localhost:5001/api/mock/test1"
```

**Get Mock Data (Multiple Records)**
```bash
curl -X GET "http://localhost:5001/api/mock/test1?count=3"
```

**Response Format**
```json
{
  "success": true,
  "template": "test1",
  "data": {
    "field_name": "generated_value"
  },
  "generated_by": "llm"
}
```

## Benefits of LLM Integration

1. **Realistic Data**: Generated data is contextually appropriate and realistic
2. **Variety**: Each request generates different, varied data
3. **Vietnamese Context**: Properly localized Vietnamese names, addresses, and content
4. **Intelligent Field Recognition**: LLM understands field context and generates appropriate data
5. **Reliability**: Fallback system ensures API availability

## Testing

Run the test script to verify everything works:
```bash
python test_mock_api.py
```

The response will now include `"generated_by": "llm"` to indicate the data was generated using the LLM. 