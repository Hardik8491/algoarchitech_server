# AlgoArchitect Backend

Django REST API backend for AlgoArchitect internship task.

## Features

- Fetches commodity data from AlphaVantage API
- Provides user/broker data endpoints
- Django REST Framework integration
- CORS enabled for frontend integration

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd algoarchitect-backend
```

2. Create and activate virtual environment
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Start the development server
```bash
python manage.py runserver 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Commodities Data
**GET** `/api/commodities/`

Fetches commodity price data from AlphaVantage API and returns formatted data for charts.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "Dec 1",
      "value": 10
    },
    ...
  ]
}
```

### 2. Users/Brokers Data
**GET** `/api/users/`

Returns broker account information with trading statistics.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "broker": "Zerodha (DU000004)",
      "no_of_active_positions": 1,
      "available_capital": "₹ 1.54 Cr",
      "total_deployed_strategies": 3,
      "active_strategies": 1,
      "status": "Active",
      "current_pnl": "₹ 50.02 K",
      "required_capital": "₹ 50.02 K"
    },
    ...
  ]
}
```

## Environment Variables

Create a `.env` file in the root directory (optional):

```
ALPHAVANTAGE_API_KEY=your_api_key_here
```

Default API key is set to "demo" if not provided.

## Tech Stack

- Django 5.0.1
- Django REST Framework 3.14.0
- django-cors-headers 4.3.1
- requests 2.31.0

## Project Structure

```
algoarchitect-backend/
├── algoarchitect/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/                    # API application
│   ├── views.py           # API view functions
│   └── urls.py            # API URL routes
├── manage.py
├── requirements.txt
└── README.md
```

## Development

The backend uses Django REST Framework to create API endpoints that:
1. Fetch real-time commodity data from AlphaVantage
2. Serve structured broker/user data
3. Enable CORS for frontend integration

## Notes

- The commodities endpoint fetches live data from AlphaVantage API
- Falls back to sample data if API request fails
- CORS is enabled for development (should be restricted in production)
- Uses SQLite database (default Django database)

## Author

Created for Algo Architech Internship Task
"# algoarchitech_server" 
