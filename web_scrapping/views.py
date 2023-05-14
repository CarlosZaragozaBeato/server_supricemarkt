from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from selenium.webdriver.chrome.options import Options
from web_scrapping.scrapping.Search import Search
from selenium import webdriver


@require_http_methods(["GET"])
def getMainData(request):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome()
        producto = request.GET.get('producto')
        data = []
        search = Search(driver=driver, product_name=producto)
        data = search.SearchAll()
        driver.quit()
        return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def getCarrefourData(request):
        data = []
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        producto = request.GET.get("producto")
        search = Search(driver=driver, producto_name = producto)
        data = search.SearchCarrefourName()
        driver.quit()
        return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def getAhorraMasData(request):
        data = []
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver = webdriver.Chrome()
        producto = request.GET.get("producto")
        search = Search(driver=driver, producto_name = producto)
        data = search.SearchAhorraMasName()
        driver.quit()
        return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def getDiaData(request):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        producto = request.GET.get('producto')
        data = []
        search = Search(driver=driver, product_name=producto)
        data = search.SearchDiaName()
        driver.quit()
        return JsonResponse(data, safe=False)
