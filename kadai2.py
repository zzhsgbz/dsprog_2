import flet as ft
import urllib.request
import json

def main(page: ft.Page):
    # ページ設定
    page.title = "天気予報アプリ"
    page.window_width = 500
    page.window_height = 600
    page.padding = 20

    # 地域データを保存
    area_data = {}

    # 天気表示エリア
    weather_container = ft.Column(
        visible=False,
        spacing=10
    )

    area_name_text = ft.Text("", size=24, weight=ft.FontWeight.BOLD)
    report_time_text = ft.Text("", size=12, color=ft.Colors.GREY)

    # 3日間の天気カードを作成
    weather_cards = []
    for i in range(3):
        card = ft.Container(
            content=ft.Column([
                ft.Text("", size=14, weight=ft.FontWeight.BOLD),  # 日付
                ft.Text("", size=16),  # 天気
                ft.Text("", size=12, color=ft.Colors.GREY),  # 風向
            ], spacing=5),
            padding=15,
            border_radius=10,
            bgcolor=ft.Colors.BLUE_50,
            margin=ft.margin.only(bottom=10)
        )
        weather_cards.append(card)
    
    # 読み込み状態
    loading = ft.ProgressRing(visible=False, width=30, height=30)
    error_text = ft.Text("", color=ft.Colors.RED)

    def get_area_list():
        """地域リストを取得"""
        try:
            url = "http://www.jma.go.jp/bosai/common/const/area.json"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data
        except Exception as e:
            print(f"地域リストの取得に失敗: {e}")
            return None

    def get_weather(area_code):
        """天気予報を取得"""
        try:
            url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data
        except Exception as e:
            print(f"天気の取得に失敗: {e}")
            return None

    def on_area_change(e):
        """地域選択変更イベント"""
        if not dropdown.value:
            return

        # 読み込み状態を表示
        loading.visible = True
        error_text.value = ""
        weather_container.visible = False
        page.update()

        # 天気データを取得
        area_code = dropdown.value
        weather_data = get_weather(area_code)
        
        loading.visible = False
        
        if weather_data:
            try:
                # データを解析
                forecast = weather_data[0]
                time_series = forecast["timeSeries"][0]
                areas = time_series["areas"][0]

                # 地域名と発表時刻を更新
                area_name_text.value = areas["area"]["name"]
                report_time_text.value = f"発表時刻: {forecast['reportDatetime'][:16].replace('T', ' ')}"

                # 天気カードを更新
                time_defines = time_series["timeDefines"]
                weathers = areas.get("weathers", [])
                winds = areas.get("winds", [])
                
                for i, card in enumerate(weather_cards):
                    if i < len(time_defines):
                        # 日付を解析
                        date_str = time_defines[i][:10]

                        # 天気と風向を取得
                        weather = weathers[i] if i < len(weathers) else "---"
                        wind = winds[i] if i < len(winds) else "---"

                        # 日付ラベル
                        if i == 0:
                            day_label = "今日"
                        elif i == 1:
                            day_label = "明日"
                        else:
                            day_label = "明後日"

                        # カード内容を更新
                        card.content.controls[0].value = f"{day_label} ({date_str})"
                        card.content.controls[1].value = f"🌤️ {weather}"
                        card.content.controls[2].value = f"🌬️ {wind}"
                        card.visible = True
                    else:
                        card.visible = False
                
                weather_container.visible = True
                error_text.value = ""
                
            except Exception as e:
                error_text.value = f"データの解析に失敗しました: {e}"
        else:
            error_text.value = "天気データの取得に失敗しました"
        
        page.update()

    # ドロップダウンメニューを作成
    dropdown = ft.Dropdown(
        label="地域を選択してください",
        width=400,
        on_change=on_area_change
    )

    # 地域リストを読み込み
    def load_areas():
        loading.visible = True
        page.update()
        
        data = get_area_list()
        loading.visible = False

        if data:
            # offices（地方気象台）を選択肢として取得
            offices = data.get("offices", {})
            options = []
            for code, info in offices.items():
                name = info.get("name", code)
                options.append(ft.dropdown.Option(key=code, text=name))
                area_data[code] = name

            # 名前順にソート
            options.sort(key=lambda x: x.text)
            dropdown.options = options
            error_text.value = ""
        else:
            error_text.value = "地域リストの取得に失敗しました"
        
        page.update()

    # 天気コンテナを構築
    weather_container.controls = [
        area_name_text,
        report_time_text,
        ft.Divider(),
        *weather_cards
    ]

    # コンポーネントをページに追加
    page.add(
        ft.Text("天気予報アプリ", size=28, weight=ft.FontWeight.BOLD),
        ft.Text("気象庁APIを利用", size=12, color=ft.Colors.GREY),
        ft.Divider(),
        dropdown,
        loading,
        error_text,
        weather_container
    )

    # ページ読み込み完了後に地域リストを取得
    load_areas()

# アプリケーションを起動
ft.app(target=main)