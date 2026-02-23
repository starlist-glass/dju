import requests
from bs4 import BeautifulSoup
import json

def get_diet_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 식단이 들어있는 테이블 찾기
        table = soup.select_one('table.board-list')
        if not table:
            table = soup.select_one('table') # board-list가 없을 경우 대비
            
        if table:
            # 줄바꿈을 유지하며 텍스트 추출
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all(['th', 'td'])]
                rows.append(" | ".join(cells))
            return "\n".join(rows)
        return "식단 정보가 없습니다."
    except:
        return "데이터를 불러오는 중 오류가 발생했습니다."

def main():
    # 보내주신 식당별 개별 URL
    urls = {
        "2생활관": "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?cntntsId=4223&mi=7065",
        "5생활관": "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?cntntsId=4224&mi=7066",
        "혜화문화관": "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?cntntsId=4222&mi=7064"
    }
    
    final_diet = {}
    
    for name, url in urls.items():
        print(f"{name} 데이터를 가져오는 중...")
        final_diet[name] = get_diet_data(url)
    
    # JSON 파일로 저장
    with open('diet.json', 'w', encoding='utf-8') as f:
        json.dump(final_diet, f, ensure_ascii=False, indent=4)
    print("모든 식단 업데이트 완료!")

if __name__ == "__main__":
    main()
