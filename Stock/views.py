from django.shortcuts import render
from Stock.models import stock_data
from django.http import HttpResponse
import twstock
# Create your views here.

def home(request):
    return render(request, 'index.html')
def get(request):
    t = 0
    stock_symbols = ['2330', '2317', '2454', '1301', '1303', '2412', '2308', '2881', '2891', '2892']
    for symbol in stock_symbols:
        stock = twstock.Stock(symbol)
        historical_data = stock.fetch_from(2023, 4) #2023/4/到現在

        for data in historical_data:
            stock_data.objects.update_or_create(
                stock_symbol=symbol,
                date=data.date,
                defaults={
                    'total_capacity': data.capacity,
                    'total_turnover': data.turnover,
                    'open_price': data.open,
                    'high_price': data.high,
                    'low_price': data.low,
                    'close_price': data.close,
                    'change_price': data.change,
                    'trans_action': data.transaction
                }
            )
    t += 1
    return HttpResponse("資料已成功存入資料庫")


def Get_data_Example(request):

    #強烈建議了解資料庫內部結構後再進行操作，例如下載DB.Browser可查看資料庫內容
    try: 
        # 變數 = 資料庫名稱.方法(條件)   .first()是指符合條件的第一筆  #還有其他拿資料的方法
        first  = stock_data.objects.filter(stock_symbol = '2330').first()
        Second = stock_data.objects.filter(stock_symbol = '2317').first()
        Third  = stock_data.objects.filter(stock_symbol = '2454').first()
        #打包到字典        
        data_dict = { '2330_1' : first.stock_symbol,
                      '2330_2' : first.high_price,  
                      '2330_3' : first.low_price,  
                      '2330_4' : first.change_price,
                      '2317_1' : Second.stock_symbol, 
                      '2317_2' : Second.high_price, 
                      '2317_3' : Second.low_price, 
                      '2317_4' : Second.change_price,
                      '2454_1' : Third.stock_symbol,  
                      '2454_2' : Third.high_price,  
                      '2454_3' : Third.low_price,  
                      '2454_4' : Third.change_price }
    except:
        print('Error')

                                #在HTML文件中使用的變數.KEY會映射出這邊的字典對應值
    return render( request, 'Get_data_Example.html' , { 'Data' : data_dict })