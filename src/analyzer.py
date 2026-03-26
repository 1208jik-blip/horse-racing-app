import pandas as pd
import os

class HorseRacingAnalyzer:
    def __init__(self):
        self.base_path = "data/processed/races"

    def load_and_clean_data(self, race_num):
        """데이터를 불러오고, 최소한의 필터링만 적용하여 많은 말을 확보합니다."""
        file_path = os.path.join(self.base_path, f"race_seoul_{race_num.zfill(2)}.csv")
        
        if not os.path.exists(file_path):
            return None
        
        try:
            df = pd.read_csv(file_path)

            # 마번/부담중량 숫자 변환
            df['마번'] = pd.to_numeric(df['마번'], errors='coerce')
            df['부담중량'] = pd.to_numeric(df['부담중량'], errors='coerce')
            
            # 마번이 없는 행만 제거 (부담중량 기준은 대폭 낮춤)
            df = df.dropna(subset=['마번'])
            df = df[df['마번'] > 0].copy()

            # 부담중량이 0보다 크기만 하면 일단 포함 (PDF 인식 오류 대비)
            df = df[df['부담중량'] > 0].copy()

            df['마번'] = df['마번'].astype(int)
            return df
        except Exception as e:
            print(f"❌ 데이터 정제 중 오류: {e}")
            return None

    def calculate_scores(self, df):
        """분석 점수를 계산합니다."""
        df['점수'] = 70.0
        # 부담중량 가산점 (55kg 기준)
        df['점수'] += (55 - df['부담중량'].astype(float)) * 2.0
        
        # 기수 가산점 (유명 기수)
        elite_jockeys = ['문세영', '빅투아르', '김용근', '다나카', '이혁', '함완식']
        df.loc[df['기수'].isin(elite_jockeys), '점수'] += 7.0
        
        # 점수 순 정렬
        return df.sort_values(by='점수', ascending=False).reset_index(drop=True)

    def get_betting_recommendations(self, df):
        """말의 마릿수에 따라 가능한 모든 추천 조합을 생성합니다."""
        count = len(df)
        if count == 0: return None
            
        top = df['마번'].tolist()
        recom = {}

        # 1. 단승식
        recom["단승식 (1착 예측)"] = f"[{top[0]}]"

        # 2. 복승식/쌍승식 (말이 2마리 이상일 때)
        if count >= 2:
            recom["복승식 (1-2착 무순)"] = f"[{top[0]}-{top[1]}]"
            recom["쌍승식 (1-2착 순서)"] = f"[{top[0]} > {top[1]}]"
            recom["복연승식 (3착내 2두)"] = f"[{top[0]}-{top[1]}]"

        # 3. 삼복승식 (말이 3마리 이상일 때)
        if count >= 3:
            recom["삼복승식 (1-2-3착)"] = f"[{top[0]}-{top[1]}-{top[2]}]"

        return recom