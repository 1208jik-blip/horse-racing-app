import os
import pandas as pd
import pdfplumber
import re

def extract_and_separate():
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    individual_dir = os.path.join(processed_dir, "races")
    db_path = os.path.join(processed_dir, "race_database.csv")
    
    os.makedirs(individual_dir, exist_ok=True)

    all_data_list = []
    pdf_files = sorted([f for f in os.listdir(raw_dir) if f.endswith('.pdf')])
    
    print(f"📂 총 {len(pdf_files)}개 파일 추출 테스트 시작...")

    for file_name in pdf_files:
        meta = re.findall(r'(\d{8})_([a-zA-Z]+)_(\d{1,2})', file_name)
        if not meta: continue
        r_date, r_loc, r_num = meta[0]
        race_data = []

        with pdfplumber.open(os.path.join(raw_dir, file_name)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text: continue
                
                # 마번과 이름이 붙어있어도 분리하는 최적화된 정규식
                pattern = re.compile(r'(\d{1,2})\s*([\uac00-\ud7af]{2,})\s+([\uac00-\ud7af]{2,})\s+(\d+\.?\d*)')
                matches = pattern.findall(text)

                for m in matches:
                    row = {
                        "날짜": r_date, "장소": r_loc, "경주번호": int(r_num),
                        "마번": int(m[0]), "마명": m[1], "기수": m[2], "부담중량": float(m[3])
                    }
                    race_data.append(row)
                    all_data_list.append(row)
        
        if race_data:
            race_df = pd.DataFrame(race_data)
            race_filename = f"race_{r_loc}_{r_num.zfill(2)}.csv"
            race_df.to_csv(os.path.join(individual_dir, race_filename), index=False, encoding='utf-8-sig')
            print(f"✅ 추출 성공: {race_filename} ({len(race_df)}두)")

    if all_data_list:
        full_df = pd.DataFrame(all_data_list).drop_duplicates()
        full_df.to_csv(db_path, index=False, encoding='utf-8-sig')
        print(f"\n✨ 테스트 완료! 총 {len(full_df)}건의 데이터가 누적되었습니다.")

if __name__ == "__main__":
    extract_and_separate()