import pandas as pd
import os

class HorseRacingAnalyzer:
    def __init__(self):
        self.base_path = "data/processed/races"

    def load_and_clean_data(self, race_num):
        """데이터를 불러오고, 섞인 쓰레기 데이터를 완벽하게 걸러냅니다."""
        file_path = os.path.join(self.base_path, f"race_seoul_{race_num.zfill(2)}.csv")
        
        if not os.path.exists(file_path):
            return None
        
        try:
            df = pd.read_csv(file_path)

            # 1. 숫자형 변환 (에러는 NaN으로)
            df['마번'] = pd.to_numeric(df['마번'], errors='coerce')
            df['부담중량'] = pd.to_numeric(df['부담중량'], errors='coerce')
            
            # 2. 마번이 없는 행 제거 및 정수 변환
            df = df.dropna(subset=['마번'])
            df = df[df['마번'] > 0].copy()
            df['마번'] = df['마번'].astype(int)

            # 3. [핵심] 쓰레기 단어 필터링 (마명이나 기수에 아래 단어가 있으면 삭제)
            # PDF에서 잘못 추출된 단어들을 여기에 계속 추가하세요.
            junk_words = ['등급', '루키', '중지', '취소', '제외', '변경', '천원', '상금']
            
            # 마명이나 기수 컬럼에서 쓰레기 단어가 포함된 행은 버립니다.
            for word in junk_words:
                df = df[~df['마명'].str.contains(word, na=False)]
                df = df[~df['기수'].str.contains(word, na=False)]

            # 4. [핵심] 이름이 너무 짧은 경우 필터링 (보통 이름은 2자 이상)
            df = df[df['마명'].str.len() >= 2]
            df = df[df['기수'].str.len() >= 2]

            # 5. [핵심] 중복 마번 제거 (한 번호에 한 마리만 남김)
            # PDF 오류로 한 마번이 두 줄로 나올 경우 마지막 정상 데이터만 남깁니다.
            df = df.drop_duplicates(subset=['마번'], keep='last')

            return df
        except Exception as e:
            print(f"❌ 정제 중 오류: {e}")
            return None

    def calculate_scores(self, df):
        """분석 점수를 계산합니다."""
        df['점수'] = 70.0
        # 부담중량 가산점 (55kg 기준)
        df['점수'] += (55 - df['부담중량'].astype(float)) * 2.0
        
        # 기수 가산점
        elite_jockeys = ['문세영', '빅투아르', '김용근', '다나카', '이혁', '장추열']
        df.loc[df['기수'].isin(elite_jockeys), '점수'] += 7.0
        
        return df.sort_values(by='점수', ascending=False).reset_index(drop=True)

    def get_betting_recommendations(self, df):
        """승식별 추천 조합을 생성합니다."""
        count = len(df)
        if count == 0: return None
            
        top = df['마번'].tolist()
        recom = {}

        recom["단승식 (1착 예측)"] = f"[{top[0]}]"

        if count >= 2:
            recom["복승식 (1-2착 무순)"] = f"[{top[0]}-{top[1]}]"
            recom["쌍승식 (1-2착 순서)"] = f"[{top[0]} > {top[1]}]"
            recom["복연승식 (3착내 2두)"] = f"[{top[0]}-{top[1]}]"

        if count >= 3:
            recom["삼복승식 (1-2-3착)"] = f"[{top[0]}-{top[1]}-{top[2]}]"

        return recom
