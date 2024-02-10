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
                # Convert the input date string to a datetime object
                date_obj = datetime.strptime(date, '%b. %d, %Y')
            
                # Format the datetime object as a string in "YYYY-MM-DD" format
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                # Handle the case where the input date string is not in the expected format
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
        # Ensure search_query is not None before filtering
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
            #stocks = Stock.objects.filter(Q(trade_code__icontains=search_query) | Q(date__icontains=search_query)| Q(low__icontains=search_query) | Q(high__icontains=search_query) | Q(open__icontains=search_query) | Q(volume__icontains=search_query) | Q(close__icontains=search_query))
    # Set the number of items per page
    per_page = 100

    # Use Django Paginator to paginate the stocks
    paginator = Paginator(stocks, per_page)
    
    # Get the requested page number from the URL parameter
    page = request.GET.get('page')

    try:
        # Get the stocks for the requested page
        stocks = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        stocks = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, show the last page
        stocks = paginator.page(paginator.num_pages)
    context = {"stocks": stocks,"search_query": search_query}
    return render(request, "index.html", context=context)


def home(request):
    # Load data from JSON file
    with open('E:\Django\jsonModel\home\stock_market_data.json') as f:
        data = json.load(f)
        for item in data:
            item['date'] = datetime.strptime(item['date'], '%Y-%m-%d').date()

            # Handle numeric field conversions
            for numeric_field in ['high', 'low', 'open', 'close', 'volume']:
                value = item[numeric_field].replace(',', '')

                # Check for special cases
                if value == '0':
                    item[numeric_field] = Decimal('0')
                else:
                    try:
                        # Try converting to Decimal using Decimal constructor
                        item[numeric_field] = Decimal(value)
                    except (InvalidOperation, TypeError, ValueError):
                        # If it fails, set to None or handle it as needed
                        print(f"Error converting {numeric_field} for item: {item}")
                        # Print or log the data types
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

