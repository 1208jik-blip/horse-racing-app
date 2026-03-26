import pandas as pd
import os
from datetime import datetime

def save_to_csv(data_list):
    """추출된 리스트 데이터를 CSV 파일로 저장합니다."""
    if not data_list:
        print("저장할 데이터가 없습니다.")
        return
    
    # 1. 리스트를 데이터프레임으로 변환
    df = pd.DataFrame(data_list)
    
    # 2. 파일 이름 만들기 (오늘 날짜 포함)
    today = datetime.now().strftime("%Y%m%d")
    filename = f"race_backup_{today}.csv"
    save_path = os.path.join("data", "processed", filename)
    
    # 3. CSV로 저장 (한글 깨짐 방지를 위해 utf-8-sig 사용)
    df.to_csv(save_path, index=False, encoding='utf-8-sig')
    print(f"✅ 데이터 백업 완료: {save_path}")