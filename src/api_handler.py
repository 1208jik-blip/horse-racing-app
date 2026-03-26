import requests
import pandas as pd
import os
import urllib.parse

class KRAApiHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        # 성적 데이터 URL (과거)
        self.result_url = "http://apis.data.go.kr/B551015/API211/getRaceHorseResult"
        # 출전마 데이터 URL (오늘/미래)
        self.entry_url = "http://apis.data.go.kr/B551015/API214/getRaceHorseEntry"

    def fetch_race_data(self, race_date, meet='1'):
        """과거 성적 데이터를 가져옵니다."""
        return self._get_request(self.result_url, race_date, meet)

    def fetch_entry_data(self, race_date, meet='1'):
        """오늘/미래의 출전마 명단을 가져옵니다."""
        return self._get_request(self.entry_url, race_date, meet)

    def _get_request(self, url, race_date, meet):
        # 인증키 인코딩 문제 해결을 위해 unquote 적용
        decoded_key = urllib.parse.unquote(self.api_key)
        params = {
            'serviceKey': decoded_key,
            'pageNo': '1',
            'numOfRows': '300',
            '_type': 'json',
            'rc_date': race_date,
            'meet': meet
        }
        
        try:
            print(f"📡 API 접속 시도 중... (날짜: {race_date})")
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ 서버 응답 에러: {response.status_code}")
                return None

            data = response.json()
            body = data.get('response', {}).get('body', {})
            items_container = body.get('items', {})
            
            if not items_container or not items_container.get('item'):
                print(f"⚠️ {race_date} 날짜에 데이터가 0건입니다. (API 서버 미업로드)")
                return None

            items = items_container.get('item')
            if isinstance(items, dict): items = [items]
            
            df = pd.DataFrame(items)
            print(f"✅ 수집 성공: {len(df)}건 확보")
            
            # 공통 컬럼 매핑
            return pd.DataFrame({
                '날짜': df['rc_date'],
                '경주번호': df['rc_no'],
                '마번': df['chul_no'],
                '마명': df['hr_nm'],
                '기수': df['jk_nm'],
                '부담중량': df['wg_budam']
            })
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return None

    def save_by_race(self, df):
        if df is None: return
        save_dir = "data/processed/races"
        os.makedirs(save_dir, exist_ok=True)
        for race_no, group in df.groupby('경주번호'):
            file_path = f"{save_dir}/race_seoul_{str(race_no).zfill(2)}.csv"
            group.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"💾 파일 저장됨: race_seoul_{str(race_no).zfill(2)}.csv")