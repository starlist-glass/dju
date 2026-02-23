import requests
from bs4 import BeautifulSoup
import json

def get_dju_diet():
    url = "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?mi=7064&cntntsId=4222"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8' # 한글 깨짐 방지
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 모든 테이블 가져오기
        tables = soup.find_all('table')
        diet_results = {}
        
        # 대전대 식단 페이지의 식당 순서: 5생활관, 2생활관, 혜화문화관
        names = ["5생활관", "2생활관", "혜화문화관"]
        
        # 실제 식단이 들어있는 테이블만 추출 (보통 클래스에 board- 가 들어감)
        valid_tables = [t for t in tables if 'board' in str(t.get('class', ''))]

        for i, name in enumerate(names):
            if i < len(valid_tables):
                # 텍스트 추출 및 불필요한 공백 정리
                text = valid_tables[i].get_text(separator='\n').strip()
                clean_text = "\n".join([line.strip() for line in text.split('\n') if line.strip()])
                
                # 만약 내용이 너무 짧으면(예: "데이터가 없습니다") 처리
                if len(clean_text) < 5:
                    diet_results[name] = "이번 주 식단 업데이트 전이거나 정보가 없습니다."
                else:
                    diet_results[name] = clean_text
            else:
                diet_results[name] = "식단을 찾을 수 없습니다."

        with open('diet.json', 'w', encoding='utf-8') as f:
            json.dump(diet_results, f, ensure_ascii=False, indent=4)
            
        print("업데이트 완료!")

    except Exception as e:
        print(f"에러: {e}")

if __name__ == "__main__":
    get_dju_diet()
