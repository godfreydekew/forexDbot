import requests
import json
from datetime import datetime, timedelta

url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"

def fetch_news():
    response = requests.get(url)
    news_data = response.json()

    high_impact_news = []

    # Loop through the news and filter by impact
    for news_item in news_data:
        if news_item['impact'] == 'High':
            title = news_item['title']
            country = news_item['country']
            date = news_item['date']
            forecast = news_item.get('forecast', 'N/A')
            previous = news_item.get('previous', 'N/A')

            # Convert the date string into a more readable format
            news_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
            
            # Add 5 hours to the UTC time (as you're 5 hours ahead)
            adjusted_date = news_date + timedelta(hours=7)

            # Format the adjusted date
            formatted_date = adjusted_date.strftime("%Y-%m-%d %H:%M:%S %Z")

            high_impact_news.append({
                'title': title,
                'country': country,
                'date': formatted_date,
                'forecast': forecast,
                'previous': previous
            })
    
    return high_impact_news

if __name__ == '__main__':
    news = fetch_news()
    for item in news:
        print(item)
