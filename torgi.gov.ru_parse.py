from bs4 import BeautifulSoup
import requests


url = 'https://torgi.gov.ru/new/public/lots/reg'
url_api = 'https://torgi.gov.ru/new/api/public/lotcards/search'
params = {
    'byFirstVersion': True,
    'biddType': '178FZ',
    'dynSubjRF': 78,
    'lotStatus': 'PUBLISHED,APPLICATIONS_SUBMISSION',
    'withFacets': True,
    'size': 10,
    'sort': 'firstVersionPublicationDate,desc'
}
response = requests.get(url=url_api, params=params)
response.encoding = 'utf-8'
data = response.json()
result = []

content = data["content"]
i = 1
for line in content[:1]:

    cadastralNumberRealty = ''
    totalAreaRealty = ''
    if line['characteristics']:
        for characteristic in line['characteristics']:
            if characteristic['code'] == 'totalAreaRealty':
                totalAreaRealty = str(characteristic['characteristicValue']) + characteristic['unit']['symbol']
            elif characteristic['code'] == 'cadastralNumberRealty':
                cadastralNumberRealty = str(characteristic['characteristicValue'])

    url_api = f"https://torgi.gov.ru/new/api/public/lotcards/{line['id']}"
    line_full_info_response = requests.get(url=url_api, params=params)
    line_full_info_response.encoding = 'utf-8'
    line_full_info_data = line_full_info_response.json()

    documents = []
    for document in line_full_info_data['noticeAttachments']:
        documents.append(document['fileName'])

    result.append({
        'comment': '', #1. Комментарий – пустая графа для наших пометок 
        'number': i, # 2. № пп  
        'lotAttributeName': line['noticeNumber'], # 3. Id – номер извещения с сайта
        'metro': '', # 4. Метро 
        'biddType': line['biddType']['name'], # 5. Название торгов с сайта 
        'address': line['biddType']['lotDescription'], # 6. Адрес с сайта 
        'totalAreaRealty': totalAreaRealty, # 7. Площадь с сайта 
        'floor': line['biddType']['lotDescription'], # 8. Этаж с сайта
        # 9. Количество комнат в квартире с сайта 
        # 10. Этажность здания с сайта 
        'squareMeterPrice': float(line['priceMin']) / float(totalAreaRealty), # 11. Цена за кв. м. = Стартовая стоимость / площадь 
        'cadastralNumberRealty': cadastralNumberRealty, # 12. Кадастровый номер с сайта 
        'priceMin': line['priceMin'], # 13. Стартовая стоимость с сайта 
        'tradingResult': '', # 14. Итог торгов = пустая графа сами заполняем 
        'increaseProcentAuction': '', # 15. % увеличение цены в торгах = пустая графа сами заполняем 
        'expectedGrowthTradingEnd': '', # 16. Ожидаемый прирост по итогам торгов, прописать формулу стартовая цена увеличенная на 20% 
        'deposit': line_full_info_data['deposit'], # 17. Размер задатка с сайта 
        'priceStep': line_full_info_data['priceStep'], # 18. Шаг аукциона с сайта 
        'marketPrice': '', # 19. Рыночная цена = пустая графа сами заполняем 
        'tax13Procent': '', # 20. Налог 13% на прибыль с продажи имущества прописать формулу= (Рыночная цена - Стартовая цена)*0,13
        'repairCost': '', # 21. Стоимость ремонта = пустая графа сами заполняем 
        'margin': '',# 22. Маржа прописать формулу = рыночная цена – стартовая цена – налог на прибыль 13% - ремонт 
        'thresholdBidd': '', # 23. Порог для участия в торгах = пустая графа сами заполняем 
        'documents': documents,# 24. Документы и сведения с сайта список документов из извещения во вкладке документы и сведения 
        'Keywords': [], # 25. Ключевые слова с сайта (в таблице должно быть подсвечено цветом если попадаются следующие слова: «Ключевые слова» search по ключевым словам: обременение, залог, кредит, ипотека, домовая книга, выписка из домой книги, архивная выписка (если есть подсвечивать цветом), условие yes/no/non. При условии yes, необходимо скопировать через запятую ключевые слова, которые указаны выше). 
        'appEndDate': line['biddStartTime'], # 26. Дата начала приема заявок с сайта 
        'appEndDate': line['biddEndTime'],# 27. Дата конца приема заявок с сайта 
        'auctionStartDate': line_full_info_data['auctionStartDate'], # 28. Дата начала аукциона с сайта 
        'biddStartTime': line_full_info_data['biddStartTime'], # 29. Дата рассмотрения заявок с сайта 
        'etpUrl': line_full_info_data['etpUrl'], # 30. Ссылка на извещение с сайта 
        'depositRecipientName': line_full_info_data['depositRecipientName'], # 31. Наименование площадки с сайта
    })
    i += 1
# soup = BeautifulSoup(response.text, 'lxml')
# print(soup)