from django.shortcuts import render
from Stock.models import stock_data
from django.http import HttpResponse
import twstock

# Create your views here.


def home(request):

    try:
        # 變數 = 資料庫名稱.方法(條件)   .first()是指符合條件的第一筆  #還有其他拿資料的方法
        Stock_Symbol = request.GET.get("stock_symbol")
        unit = stock_data.objects.filter(
            stock_symbol=Stock_Symbol
        ).last()  # 讀取一筆資料

        # 打包到字典
        data_dict = {
            "1_1": "2330",
            "1_2": "2317",
            "1_3": "2454",
            "1_4": "1301",
            "1_5": "1303",
            "2_1": "2412",
            "2_2": "2308",
            "2_3": "2881",
            "2_4": "2891",
            "2_5": "2892",
        }
    except:
        print("Error")

    return render(request, "index.html", {"Data": data_dict})


def get(request):
    t = 0
    stock_symbols = [
        "2330",
        "2317",
        "2454",
        "1301",
        "1303",
        "2412",
        "2308",
        "2881",
        "2891",
        "2892",
    ]
    for symbol in stock_symbols:
        stock = twstock.Stock(symbol)
        historical_data = stock.fetch_from(2023, 4)  # 2023/4/到現在

        for data in historical_data:
            stock_data.objects.update_or_create(
                stock_symbol=symbol,
                date=data.date,
                defaults={
                    "total_capacity": data.capacity,
                    "total_turnover": data.turnover,
                    "open_price": data.open,
                    "high_price": data.high,
                    "low_price": data.low,
                    "close_price": data.close,
                    "change_price": data.change,
                    "trans_action": data.transaction,
                },
            )
    t += 1
    return HttpResponse("資料已成功存入資料庫")


def search(request):

    # 強烈建議了解資料庫內部結構後再進行操作，例如下載DB.Browser可查看資料庫內容
    try:
        # 變數 = 資料庫名稱.方法(條件)   .first()是指符合條件的第一筆  #還有其他拿資料的方法
        Stock_Symbol = request.GET.get("stock_symbol")
        unit = stock_data.objects.filter(
            stock_symbol=Stock_Symbol
        ).last()  # 讀取一筆資料

        # 打包到字典
        data_dict = {
            "col1": unit.stock_symbol,
            "col2": unit.high_price,
            "col3": unit.low_price,
            "col4": unit.change_price,
        }
    except:
        print("Error")

        # 在HTML文件中使用的變數.KEY會映射出這邊的字典對應值
    return render(request, "Get_data_Example.html", {"Data": data_dict})
