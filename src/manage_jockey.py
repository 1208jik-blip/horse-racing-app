import pandas as pd
import os

def initialize_jockey_master():
    """기수 마스터 파일 초기 생성"""
    file_path = "data/jockey_master.csv"
    
    # 이미 파일이 있다면 생성하지 않음
    if os.path.exists(file_path):
        print(f"✅ 기존 기수 마스터 파일을 불러옵니다: {file_path}")
        return pd.read_csv(file_path)

    # 샘플 기수 데이터 (초기값)
    # 승률(win_rate), 복승률(place_rate), 주특기(style: 선행/추입), 숙련도 점수 등
    data = {
        "기수명": ["장추열", "빅투아르", "조한별", "조상범", "코지", "김태훈", 
                  "김효정", "푸르칸", "김정준", "이우철", "송재철", "씨위웅"],
        "통산승률": [12.5, 14.2, 5.1, 8.4, 9.2, 4.3, 6.1, 11.8, 7.5, 6.8, 9.1, 10.5],
        "복승률": [22.1, 25.8, 11.2, 16.5, 18.2, 9.5, 13.2, 21.5, 15.1, 14.3, 17.8, 19.2],
        "주특기": ["선행", "추입", "자유", "선행", "추입", "자유", "선행", "추입", "자유", "선행", "추입", "선행"],
        "숙련점수": [85, 90, 60, 75, 80, 55, 65, 88, 70, 68, 82, 84]
    }
    
    df = pd.DataFrame(data)
    
    # data 폴더가 없으면 생성
    if not os.path.exists("data"):
        os.makedirs("data")
        
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"🚀 기수 마스터 파일이 신규 생성되었습니다: {file_path}")
    return df

def update_jockey_data(jockey_name, win_rate=None, score=None):
    """특정 기수의 데이터를 업데이트 (누적용)"""
    file_path = "data/jockey_master.csv"
    df = pd.read_csv(file_path)
    
    if jockey_name in df['기수명'].values:
        if win_rate is not None:
            df.loc[df['기수명'] == jockey_name, '통산승률'] = win_rate
        if score is not None:
            df.loc[df['기수명'] == jockey_name, '숙련점수'] = score
        
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"🔄 {jockey_name} 기수 정보 업데이트 완료!")
    else:
        print(f"❌ {jockey_name} 기수를 찾을 수 없습니다.")

if __name__ == "__main__":
    initialize_jockey_master()