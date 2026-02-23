import requests
from bs4 import BeautifulSoup
import json

def get_dju_diet():
    # 대전대 식단 통합 페이지
    url = "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?mi=7064&cntntsId=4222"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        diet_results = {}
        target_cafeterias = ["5생활관", "2생활관", "혜화문화관"]
        
        # 모든 테이블을 가져와서 제목(caption)이나 주변 텍스트로 식당 찾기
        all_tables = soup.find_all('table')
        
        for name in target_cafeterias:
            found_text = "정보가 없습니다."
            for table in all_tables:
                # 테이블 내부나 바로 위 텍스트에 식당 이름이 있는지 확인
                parent_text = table.parent.get_text()
                table_text = table.get_text()
                
                if name in parent_text or name in table_text:
                    # 실제 메뉴가 적힌 텍스트만 추출
                    rows = table.find_all('tr')
                    menu_lines = []
                    for row in rows:
                        cells = row.find_all(['td', 'th'])
                        line = " | ".join([c.get_text(strip=True) for c in cells])
                        if line: menu_lines.append(line)
                    
                    if menu_lines:
                        found_text = "\n".join(menu_lines)
                        break
            
            diet_results[name] = found_text

        # JSON 저장
        with open('diet.json', 'w', encoding='utf-8') as f:
            json.dump(diet_results, f, ensure_ascii=False, indent=4)
        
        print("정상적으로 데이터를 가져왔습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    get_dju_diet()
