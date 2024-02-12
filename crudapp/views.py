import json
from django.shortcuts import render
from .models import Stock
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from django.shortcuts import render
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views import View
import io
import matplotlib.pyplot as plt 
from django.http import HttpResponse
from django.views import View
from django.http import JsonResponse
import plotly.graph_objs as go
from django.db.models import Max



def home(request):
   # load the given json file 
    with open('E:\Django\crudapplication\crudapp\stock_market_data.json') as f:
        data = json.load(f)
        for item in data:
            item['date'] = datetime.strptime(item['date'], '%Y-%m-%d').date()

            
            for numeric_field in ['high', 'low', 'open', 'close', 'volume']:
                value = item[numeric_field].replace(',', '')

               
                if value == '0':
                    item[numeric_field] = Decimal('0')
                else:
                    try:
                       
                        item[numeric_field] = Decimal(value)
                    except (InvalidOperation, TypeError, ValueError):
                        
                        print(f"Error converting {numeric_field} for item: {item}")
                       
                        print(f"{numeric_field}: {type(item[numeric_field])}")
                        item[numeric_field] = None

                

            try:
                Stock.objects.create(**item)
            except Exception as e:
                print(f"Error creating object with item: {item}")
                print(e)

    # Retrieve all data from the JsonModel
    data_from_db = Stock.objects.all()
    
    return render(request, 'home.html', {'data': data_from_db})

def index(request):
    stocks = Stock.objects.all()
    search_query = ""
    
    if request.method == "POST": 
        if "create" in request.POST:
            date = request.POST.get("date")
            trade_code = request.POST.get("trade_code")
            high = request.POST.get("High")
            low = request.POST.get("Low")
            open = request.POST.get("Open")
            close = request.POST.get("Close")
            volume = request.POST.get("volume")

            

            Stock.objects.create(
                date=date,
                trade_code=trade_code,
                high=high,
                low=low,
                open=open,
                close=close,
                volume=volume
            )

            messages.success(request, "Stock added successfully")
        
        elif "update" in request.POST:
            id = request.POST.get("id")
            trade_code = request.POST.get("trade_code")
            high = request.POST.get("High")
            low = request.POST.get("Low")
            open = request.POST.get("Open")
            close = request.POST.get("Close")
            volume = request.POST.get("volume")
            date = request.POST.get("date")
            stock = Stock.objects.get(id=id)

            try:
                
                date_obj = datetime.strptime(date, '%b. %d, %Y')
            
                
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                
                raise ValidationError('Invalid date format. Please use MMM. D, YYYY format.')

            stock.trade_code = trade_code
            stock.date= formatted_date
            stock.high = high
            stock.low = low
            stock.open = open
            stock.close = close
            stock.volume = volume
            stock.save()

            messages.success(request, "Stock updated successfully")
        elif "delete" in request.POST:
            id = request.POST.get("id")
            Stock.objects.get(id=id).delete()
            messages.success(request, "Stock deleted successfully")
        
        elif "search" in request.POST:
            search_query = request.POST.get("query")
        
        if search_query is not None:
            stocks = Stock.objects.filter(
                Q(trade_code__icontains=search_query) |
                Q(date__icontains=search_query) |
                Q(low__icontains=search_query) |
                Q(high__icontains=search_query) |
                Q(open__icontains=search_query) |
                Q(volume__icontains=search_query) |
                Q(close__icontains=search_query)
        )
            
    per_page = 100

    
    paginator = Paginator(stocks, per_page)
    
    
    page = request.GET.get('page')

    try:
        
        stocks = paginator.page(page)
    except PageNotAnInteger:
       
        stocks = paginator.page(1)
    except EmptyPage:
       
        stocks = paginator.page(paginator.num_pages)
    context = {"stocks": stocks,"search_query": search_query}
    return render(request, "index.html", context=context)






def stock_chart(request):
    # Get distinct trade codes
    trade_codes = Stock.objects.values_list('trade_code', flat=True).distinct()

    # Default values
    selected_trade_code = trade_codes[2]  # Select the first trade code by default

    if 'selected_trade_code' in request.GET:
        selected_trade_code = request.GET['selected_trade_code']

    # Filter stocks based on selected trade code
    stocks = Stock.objects.filter(trade_code=selected_trade_code)

    # Extract date, open, close prices, and volume for the line/bar chart
    dates = [stock.date for stock in stocks]
    open_prices = [stock.open for stock in stocks]
    close_prices = [stock.close for stock in stocks]
    volumes = [stock.volume for stock in stocks]

    # Create the Plotly trace for close prices (line chart)
    trace_close = go.Scatter(x=dates, y=close_prices, mode='lines', name='Close Prices')

    # Create the Plotly trace for open prices (line chart)
    trace_open = go.Scatter(x=dates, y=open_prices, mode='lines', name='Open Prices')

    # Create the Plotly trace for volume (bar chart)
    trace_volume = go.Bar(x=dates, y=volumes, name='Volume', yaxis='y2')

    # Create the Plotly layout for line/bar chart
    line_bar_chart_layout = go.Layout(
        title=f'Stock Prices and Volume Over Time for {selected_trade_code}',
        xaxis=dict(title='Date', range=[min(dates), max(dates)]),
        yaxis=dict(title='Price', range=[min(min(open_prices), min(close_prices)), max(max(open_prices), max(close_prices))]),
        yaxis2=dict(title='Volume', overlaying='y', side='right', range=[0, max(volumes)])
    )

    # Create the Plotly figure with multiple traces and axes for line/bar chart
    line_bar_chart = go.Figure(data=[trace_close, trace_open, trace_volume], layout=line_bar_chart_layout)

    # Convert the Plotly figure for line/bar chart to JSON
    line_bar_chart_json = line_bar_chart.to_json()

    # Extract open, high, low, close prices for the candlestick chart
    open_prices = [stock.open for stock in stocks]
    high_prices = [stock.high for stock in stocks]
    low_prices = [stock.low for stock in stocks]
    close_prices = [stock.close for stock in stocks]

    # Create the Plotly trace for candlestick chart
    trace_candlestick = go.Candlestick(x=dates,
                                       open=open_prices,
                                       high=high_prices,
                                       low=low_prices,
                                       close=close_prices,
                                       name='Candlestick')

    # Create the Plotly layout for candlestick chart
    candlestick_chart_layout = go.Layout(
        title=f'Candlestick Chart for {selected_trade_code}',
        xaxis=dict(title='Date', range=[min(dates), max(dates)]),
        yaxis=dict(title='Price', range=[min(low_prices), max(high_prices)])
    )

    # Create the Plotly figure with candlestick trace and layout for candlestick chart
    candlestick_chart = go.Figure(data=[trace_candlestick], layout=candlestick_chart_layout)

    # Convert the Plotly figure for candlestick chart to JSON
    candlestick_chart_json = candlestick_chart.to_json()

    # Extract the last volume for each trade code
    top_10_volumes = Stock.objects.values('trade_code').annotate(last_volume=Max('volume')).order_by('-last_volume')[:10]

    # Create the Plotly trace for pie chart of last volumes for top 10 trade codes
    trace_pie = go.Pie(labels=[item['trade_code'] for item in top_10_volumes],
                   values=[item['last_volume'] for item in top_10_volumes],
                   name='Last Volume')

    # Create the Plotly layout for pie chart
    pie_chart_layout = go.Layout(title='Top 10 Trade Codes with Highest Trading Volumes',autosize=False,
    width=500,
    height=500)

    # Create the Plotly figure with pie chart trace and layout for pie chart
    pie_chart = go.Figure(data=[trace_pie], layout=pie_chart_layout)

    # Convert the Plotly figure for pie chart to JSON
    pie_chart_json = pie_chart.to_json()


    # Extract the last close price for each trade code
    top_10_close_prices = Stock.objects.values('trade_code').annotate(last_close_price=Max('close')).order_by('-last_close_price')[:10]

    # Create the Plotly trace for pie chart of last close prices for top 10 trade codes
    trace_pie_close_prices = go.Pie(labels=[item['trade_code'] for item in top_10_close_prices],
                                values=[item['last_close_price'] for item in top_10_close_prices],
                                name='Last Close Price')

    # Create the Plotly layout for pie chart of last close prices
    pie_chart_layout_close_prices = go.Layout(title='Top 10 Trade Codes by Closing Prices',
                                          autosize=False,
                                          width=500,
                                          height=500)

    # Create the Plotly figure with pie chart trace and layout for pie chart of last close prices
    pie_chart_close_prices = go.Figure(data=[trace_pie_close_prices], layout=pie_chart_layout_close_prices)

    # Convert the Plotly figure for pie chart of last close prices to JSON
    pie_chart_json_close_prices = pie_chart_close_prices.to_json()    
    # Extract the open price for each trade code
    top_10_open_prices = Stock.objects.values('trade_code').annotate(max_open_price=Max('open')).order_by('-max_open_price')[:10]
    
    # Create the Plotly trace for pie chart of open prices for top 10 trade codes
    trace_pie_op = go.Pie(labels=[item['trade_code'] for item in top_10_open_prices],
                   values=[item['max_open_price'] for item in top_10_open_prices],
                   name='Open Price')

    # Create the Plotly layout for pie chart
    pie_chart_layout_op = go.Layout(
        title='Top 10 Trade Codes by Opening Prices',
        autosize=False,
        width=500,
        height=500
                    )

    # Create the Plotly figure with pie chart trace and layout for pie chart
    pie_chart_op = go.Figure(data=[trace_pie_op], layout=pie_chart_layout_op)

    # Convert the Plotly figure for pie chart to JSON
    pie_chart_json_op = pie_chart_op.to_json()    


    context = {
        'line_bar_chart_json': line_bar_chart_json,
        'candlestick_chart_json': candlestick_chart_json,
        'pie_chart_json':pie_chart_json,
        'pie_chart_json_close_prices':pie_chart_json_close_prices,
        'pie_chart_json_op':pie_chart_json_op,
        'trade_codes': trade_codes,
        'selected_trade_code': selected_trade_code
    }
    return render(request, 'stock_chart.html', context)
