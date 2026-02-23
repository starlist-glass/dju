import requests
from bs4 import BeautifulSoup
import json

def get_dju_diet():
    # 1. 대전대학교 학식 페이지 접속
    url = "https://www.dju.ac.kr/dju/cm/cntnts/cntntsView.do?mi=7064&cntntsId=4222"
    headers = {'User-Agent': 'Mozilla/5.0'} # 접속 차단 방지용
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # 접속 에러 시 멈춤
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. 식단 테이블 모두 찾기 (보통 5생, 2생, 혜화 순서)
        tables = soup.select('table.board-list')
        
        # 식당 이름 매칭
        target_names = ["5생활관", "2생활관", "혜화문화관"]
        diet_results = {}

        for i, name in enumerate(target_names):
            if i < len(tables):
                # 테이블 안의 텍스트를 가져와서 불필요한 공백 제거
                raw_text = tables[i].get_text(separator='\n').strip()
                # 너무 긴 공백이나 줄바꿈 정리
                clean_text = "\n".join([line.strip() for line in raw_text.split('\n') if line.strip()])
                diet_results[name] = clean_text
            else:
                diet_results[name] = "식단 정보가 없습니다."

        # 3. 결과물을 JSON 파일로 저장
        with open('diet.json', 'w', encoding='utf-8') as f:
            json.dump(diet_results, f, ensure_ascii=False, indent=4)
            
        print("성공! diet.json 파일이 생성되었습니다.")

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    get_dju_diet()