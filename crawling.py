import requests
from bs4 import BeautifulSoup
import json

def get_diet_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.select_one('table.board-list')
        if not table:
            table = soup.select_one('table')
            
        if table:
            rows = []
            for tr in table.find_all('tr'):
                # 각 셀(td, th)의 텍스트 사이에 공백을 추가하여 메뉴가 붙지 않게 함
                cells = [td.get_text(" ", strip=True) for td in tr.find_all(['th', 'td'])]
                rows.append(" | ".join(cells))
            return "\n".join(rows)
        return "식단 정보가 없습니다."
    except:
        return "데이터를 불러오는 중 오류 발생"

def main():
    urls = {
        "2생활관": "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?cntntsId=4223&mi=7065",
        "5생활관": "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?cntntsId=4224&mi=7066",
        "혜화문화관": "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?cntntsId=4222&mi=7064"
    }
    final_diet = {}
    for name, url in urls.items():
        final_diet[name] = get_diet_data(url)
    
    with open('diet.json', 'w', encoding='utf-8') as f:
        json.dump(final_diet, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
