import os
import sys
from src.api_handler import KRAApiHandler
from src.analyzer import HorseRacingAnalyzer

def main():
    # 사용자의 API 키를 여기에 입력하세요
    API_KEY = "a2e9ffe3bb9e7bdb1dedef05a1651989d9da1d4d42564e2fc50d656dea55cfb8"
    api_handler = KRAApiHandler(API_KEY)
    analyzer = HorseRacingAnalyzer()

    while True:
        print("\n" + "="*50)
        print("🏇 WinRate Lab: 경마 AI 승식 추천 시스템")
        print("="*50)
        print(" 1. 데이터 수집 (1-1:과거성적, 1-2:출전표)")
        print(" 2. 승식별 추천 분석 (AI 예상)")
        print(" Q. 프로그램 종료")
        
        choice = input("\n👉 작업을 선택하세요: ").strip().upper()

        if choice == '1':
            print("\n[1-1] 과거 성적 수집 | [1-2] 오늘 출전표 수집")
            sub_choice = input("👉 선택(1 또는 2): ").strip()
            date = input("📅 날짜(YYYYMMDD): ").strip()
            
            if sub_choice == '1':
                df = api_handler.fetch_race_data(date)
            elif sub_choice == '2':
                df = api_handler.fetch_entry_data(date)
            else:
                print("❌ 잘못된 선택입니다.")
                continue

            if df is not None:
                api_handler.save_by_race(df)
                print("✨ 데이터 처리가 완료되었습니다.")
            else:
                print("📢 데이터가 없거나 수집에 실패했습니다.")

        elif choice == '2':
            num = input("🔢 분석할 경주 번호(1~11): ").strip()
            df = analyzer.load_and_clean_data(num)
            
            if df is not None and not df.empty:
                result = analyzer.calculate_scores(df)
                print(f"\n📊 [{num}경주] 분석 결과 상위 마필")
                print("-" * 55)
                print(result[['마번', '마명', '기수', '점수']].head(5).to_string(index=False))
                print("-" * 55)
                
                recom = analyzer.get_betting_recommendations(result)
                if recom:
                    print("\n💡 AI 승식별 추천")
                    for k, v in recom.items():
                        print(f"  • {k}: {v}")
                else:
                    print("⚠️ 추천을 위한 데이터가 부족합니다.")
            else:
                print("❌ 해당 경주 데이터가 없습니다. 먼저 1번에서 수집하세요.")

        elif choice == 'Q':
            print("👋 프로그램을 종료합니다.")
            break

if __name__ == "__main__":
    main()