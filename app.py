import flet as ft
from src.api_handler import KRAApiHandler
from src.analyzer import HorseRacingAnalyzer
import datetime

def main(page: ft.Page):
    # --- 앱 기본 설정 ---
    page.title = "WinRate Lab - 경마 AI 추천"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 800
    page.padding = 20
    
    # 로직 객체 생성
    API_KEY = "a2e9ffe3bb9e7bdb1dedef05a1651989d9da1d4d42564e2fc50d656dea55cfb8"
    api_handler = KRAApiHandler(API_KEY)
    analyzer = HorseRacingAnalyzer()

    # --- UI 요소 정의 ---
    date_input = ft.TextField(
        label="날짜 입력 (YYYYMMDD)", 
        value=datetime.datetime.now().strftime("%Y%m%d"),
        text_align=ft.TextAlign.CENTER
    )
    
    race_num_input = ft.Dropdown(
        label="경주 번호 선택",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 13)],
        value="1"
    )

    status_text = ft.Text("", color=ft.colors.BLUE_700)
    recommend_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ADAPTIVE)

    # --- 버튼 클릭 이벤트 ---
    def on_fetch_click(e):
        status_text.value = "⏳ API 데이터 수집 중..."
        page.update()
        
        # 오늘 출전표 수집
        df = api_handler.fetch_entry_data(date_input.value)
        if df is not None:
            api_handler.save_by_race(df)
            status_text.value = "✅ 데이터 수집 및 저장 완료!"
            status_text.color = ft.colors.GREEN_700
        else:
            status_text.value = "❌ 데이터를 가져오지 못했습니다."
            status_text.color = ft.colors.RED_700
        page.update()

    def on_analyze_click(e):
        recommend_list.controls.clear()
        df = analyzer.load_and_clean_data(race_num_input.value)
        
        if df is not None and not df.empty:
            result = analyzer.calculate_scores(df)
            recom = analyzer.get_betting_recommendations(result)
            
            if recom:
                recommend_list.controls.append(ft.Text("💡 AI 추천 조합", size=20, weight="bold"))
                for k, v in recom.items():
                    recommend_list.controls.append(
                        ft.Container(
                            content=ft.ListTile(
                                leading=ft.Icon(ft.icons.STARS, color=ft.colors.ORANGE),
                                title=ft.Text(k, weight="bold"),
                                subtitle=ft.Text(v, size=18, color=ft.colors.BLUE_900),
                            ),
                            bgcolor=ft.colors.BLUE_50,
                            border_radius=10
                        )
                    )
            else:
                recommend_list.controls.append(ft.Text("⚠️ 마필 정보가 부족합니다."))
        else:
            recommend_list.controls.append(ft.Text("❌ 먼저 데이터를 수집하세요.", color="red"))
        
        page.update()

    # --- 화면 구성 ---
    page.add(
        ft.Row([ft.Icon(ft.icons.STADIUM, size=30), ft.Text("WinRate Lab", size=30, weight="bold")], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        date_input,
        ft.ElevatedButton("오늘의 출전표 가져오기", icon=ft.icons.DOWNLOAD, on_click=on_fetch_click, width=400),
        status_text,
        ft.Divider(),
        race_num_input,
        ft.FilledButton("AI 승식별 추천 분석", icon=ft.icons.ANALYTICS, on_click=on_analyze_click, width=400),
        ft.Divider(),
        recommend_list
    )

# 웹으로 실행할 수 있게 설정
ft.app(target=main, view=ft.AppView.WEB_BROWSER)