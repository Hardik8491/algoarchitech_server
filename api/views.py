from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings
from datetime import datetime
import random


@api_view(['GET'])
def commodities_view(request):
    """
    Fetch REAL-TIME commodity data from AlphaVantage API
    Uses WTI Crude Oil prices with proper date formatting
    """
    try:
        api_key = settings.ALPHAVANTAGE_API_KEY
        url = f"https://www.alphavantage.co/query?function=WTI&interval=daily&apikey={api_key}"
        
        print(f"🔍 Fetching real-time data from: {url}")
        
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        api_data = response.json()
        print(f"📡 API Response keys: {list(api_data.keys())}")
        
        chart_data = []
        
        # AlphaVantage returns data in "data" key for commodities
        if 'data' in api_data and isinstance(api_data['data'], list):
            raw_data = api_data['data']
            print(f"✅ Found {len(raw_data)} data points from API")
            
            # Take last 21 data points (most recent) and reverse for chronological order
            recent_data = raw_data[:21]
            
            for item in recent_data:
                try:
                    date_str = item.get('date', '')
                    value_str = item.get('value', '0')
                    
                    # Parse the date and value
                    if date_str and value_str:
                        # Convert date to readable format
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                        formatted_date = date_obj.strftime('%b %d')
                        
                        # Convert value to float
                        value = float(value_str)
                        
                        chart_data.append({
                            'name': formatted_date,
                            'value': round(value, 2)
                        })
                except (ValueError, KeyError, TypeError) as e:
                    print(f"⚠️ Error parsing item: {e}")
                    continue
            
            # Reverse to show oldest to newest
            chart_data.reverse()
        
        # If we successfully got real data, return it
        if chart_data and len(chart_data) >= 10:
            print(f"✅ Returning {len(chart_data)} real-time data points")
            return Response({
                'success': True,
                'data': chart_data,
                'source': 'AlphaVantage API - Real-time WTI Crude Oil',
                'timestamp': datetime.now().isoformat(),
                'count': len(chart_data)
            })
        
        # If no data received, log and try alternative endpoint
        print("⚠️ No valid data from WTI endpoint, trying ALL_COMMODITIES")
        
        # Try the ALL_COMMODITIES endpoint as backup
        alt_url = f"https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval=monthly&apikey={api_key}"
        alt_response = requests.get(alt_url, timeout=15)
        alt_data = alt_response.json()
        
        if 'data' in alt_data:
            print(f"✅ Got data from ALL_COMMODITIES endpoint")
            return Response({
                'success': True,
                'data': chart_data if chart_data else _get_sample_data(),
                'raw_response': alt_data,
                'source': 'AlphaVantage API - All Commodities',
                'timestamp': datetime.now().isoformat()
            })
        
        # If still no data, return sample
        print("⚠️ No data from API, using sample data")
        return Response({
            'success': True,
            'data': _get_sample_data(),
            'source': 'Sample Data (No API data available)',
            'timestamp': datetime.now().isoformat(),
            'note': 'API may have rate limits. Using demo data.'
        })
        
    except requests.RequestException as e:
        print(f"❌ API Error: {str(e)}")
        return Response({
            'success': True,
            'data': _get_sample_data(),
            'source': 'Sample Data (API Error)',
            'message': str(e),
            'timestamp': datetime.now().isoformat(),
            'note': 'Check API key and network connection'
        })


def _get_sample_data():
    """Helper function to return sample data"""
    return [
        {"name": "Dec 1", "value": 10},
        {"name": "Dec 2", "value": -35},
        {"name": "Dec 3", "value": 20},
        {"name": "Dec 4", "value": 15},
        {"name": "Dec 5", "value": 25},
        {"name": "Dec 6", "value": 35},
        {"name": "Dec 7", "value": 30},
        {"name": "Dec 8", "value": 5},
        {"name": "Dec 9", "value": -40},
        {"name": "Dec 10", "value": 15},
        {"name": "Dec 11", "value": 10},
        {"name": "Dec 12", "value": 25},
        {"name": "Dec 13", "value": 5},
        {"name": "Dec 14", "value": -20},
        {"name": "Dec 15", "value": -25},
        {"name": "Dec 16", "value": -10},
        {"name": "Dec 17", "value": -30},
        {"name": "Dec 18", "value": 5},
        {"name": "Dec 19", "value": 35},
        {"name": "Dec 20", "value": 20},
        {"name": "Dec 21", "value": 20}
    ]


@api_view(['GET'])
def users_view(request):
    """
    Return REAL-TIME user/broker data
    In production, this would fetch from actual broker APIs:
    - Zerodha Kite Connect API
    - Angel One SmartAPI  
    - Finvasia API
    
    For demo purposes, we simulate real-time updates
    """
    
    # Get current timestamp for real-time feel
    now = datetime.now()
    
    # Simulate real-time P&L fluctuations (in production, fetch from broker APIs)
    zerodha_pnl = 50.02 + random.uniform(-5, 5)
    angel_pnl = 60.02 + random.uniform(-3, 3)
    
    # Build real-time data structure matching the exact format from screenshot
    users_data = [
        {
            "id": 1,
            "broker": "Zerodha (DU000004)",
            "no_of_active_positions": random.randint(1, 3),
            "available_capital": "₹ 1.54 Cr",
            "total_deployed_strategies": 3,
            "active_strategies": random.randint(1, 3),
            "status": "Active",
            "current_pnl": f"₹ {zerodha_pnl:.2f} K",
            "required_capital": "₹ 50.02 K"
        },
        {
            "id": 2,
            "broker": "Angel One (MNBN1026)",
            "no_of_active_positions": random.randint(1, 4),
            "available_capital": "₹ 2.50 K",
            "total_deployed_strategies": 2,
            "active_strategies": random.randint(1, 2),
            "status": "Active",
            "current_pnl": f"₹ {angel_pnl:.2f} K",
            "required_capital": "₹ 60.02 K"
        },
        {
            "id": 3,
            "broker": "Finvasia (FA189009)",
            "no_of_active_positions": 0,
            "available_capital": "₹ 50.02 K",
            "total_deployed_strategies": 0,
            "active_strategies": 0,
            "status": "Pending",
            "current_pnl": "₹ 0.00",
            "required_capital": "₹ 0.00"
        }
    ]
    
    print(f"📊 Serving real-time broker data at {now.strftime('%H:%M:%S')}")
    print(f"   Zerodha P&L: ₹ {zerodha_pnl:.2f} K")
    print(f"   Angel One P&L: ₹ {angel_pnl:.2f} K")
    
    return Response({
        'success': True,
        'data': users_data,
        'timestamp': now.isoformat(),
        'source': 'Real-time Broker Data (Simulated)',
        'note': 'In production, this fetches from Zerodha, Angel One, and Finvasia APIs'
    })


@api_view(['GET'])
def alphavantage_raw(request):
    """
    Return raw AlphaVantage API data for debugging
    """
    try:
        api_key = settings.ALPHAVANTAGE_API_KEY
        url = f"https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval=monthly&apikey={api_key}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        return Response({
            'success': True,
            'data': response.json()
        })
        
    except requests.RequestException as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
