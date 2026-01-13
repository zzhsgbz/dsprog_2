import sqlite3
import requests

conn = sqlite3.connect("weather.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS areas (code TEXT PRIMARY KEY, name TEXT)")
cur.execute("""
CREATE TABLE IF NOT EXISTS forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_code TEXT,
    date TEXT,
    weather TEXT
)
""")
conn.commit()

area_url = "http://www.jma.go.jp/bosai/common/const/area.json"
area_data = requests.get(area_url).json()
offices = area_data["offices"]

for code, info in offices.items():
    cur.execute("INSERT OR IGNORE INTO areas VALUES (?, ?)", (code, info["name"]))
conn.commit()

print("=== 地域一覧 ===")
for row in cur.execute("SELECT code, name FROM areas ORDER BY code"):
    print(row[0], row[1])

area_code = input("地域コードを入力してください：").strip()

forecast_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
res = requests.get(forecast_url)

if res.status_code != 200:
    print("天気情報を取得できませんでした")
else:
    forecast = res.json()
    times = forecast[0]["timeSeries"][0]["timeDefines"]
    weathers = forecast[0]["timeSeries"][0]["areas"][0]["weathers"]

    print("=== 天気予報 ===")
    for d, w in zip(times, weathers):
        cur.execute(
            "INSERT INTO forecasts (area_code, date, weather) VALUES (?, ?, ?)",
            (area_code, d, w)
        )
        print(d, w)

conn.commit()
conn.close()
