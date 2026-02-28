import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# 대전대 학식 URL 목록
MENU_URLS = {
    "학생식당 (1 URL)": "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?mi=7064&cntntsId=4222",
    "교직원식당 (2 URL)": "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?cntntsId=4223&mi=7065",
    "기숙사식당 (3 URL)": "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?cntntsId=4224&mi=7066"
}

def get_todays_menu():
    today_menu_data = {}
    # 파이썬에서 요일은 0:월, 1:화, 2:수, 3:목, 4:금, 5:토, 6:일 입니다.
    weekday = datetime.today().weekday()
    
    # 학교 방화벽에서 봇으로 인식해 차단하지 않도록 브라우저 정보(User-Agent)를 넣습니다.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for name, url in MENU_URLS.items():
        if weekday >= 5: # 주말일 경우
            today_menu_data[name] = "오늘은 주말입니다. 식단을 제공하지 않습니다."
            continue

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. 식단표가 들어있는 첫 번째 테이블을 찾습니다.
            table = soup.find('table')
            if not table:
                today_menu_data[name] = "식단표를 찾을 수 없습니다."
                continue
            
            # 2. 테이블의 행(tr)들을 가져옵니다.
            rows = table.find('tbody').find_all('tr') if table.find('tbody') else table.find_all('tr')
            
            menu_text = ""
            # 3. 각 행(조식, 중식, 석식 등)을 돌면서 오늘 요일에 맞는 열(td)의 텍스트를 추출합니다.
            for row in rows:
                cols = row.find_all(['td', 'th'])
                
                # 대학교 식단표는 보통 [구분, 월, 화, 수, 목, 금] 구조입니다.
                # 따라서 오늘 요일(weekday)에 +1을 한 인덱스가 오늘의 메뉴 열이 됩니다.
                target_idx = weekday + 1 
                
                if target_idx < len(cols):
                    # <br> 태그 등을 줄바꿈(\n)으로 처리하며 텍스트 추출
                    cell_text = cols[target_idx].get_text(strip=True, separator='\n')
                    if cell_text:
                        # 첫 번째 열은 보통 '중식', '석식' 같은 구분자입니다.
                        category = cols[0].get_text(strip=True)
                        menu_text += f"[{category}]\n{cell_text}\n\n"
            
            today_menu_data[name] = menu_text.strip() if menu_text else "오늘의 메뉴 정보가 업데이트되지 않았습니다."

        except Exception as e:
            today_menu_data[name] = f"메뉴를 불러오는 중 오류가 발생했습니다."
            print(f"Error scraping {name}: {e}")
            
    return today_menu_data

@app.route('/')
def index():
    today_str = datetime.today().strftime("%Y년 %m월 %d일")
    # 크롤링 함수 실행
    menus = get_todays_menu()
    # HTML에 데이터 전달
    return render_template('index.html', date=today_str, menus=menus)

if __name__ == '__main__':
    # 서버 실행 (포트 5000)
    app.run(debug=True)
