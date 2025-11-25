# coding: utf-8
import requests  # HTTPリクエスト用ライブラリ
from bs4 import BeautifulSoup  # HTML解析用ライブラリ
import sqlite3  # SQLiteデータベース操作用ライブラリ
import time  # 待機用ライブラリ

# ========================================
# データベース作成
# ========================================
# "google_repos.db" というファイルに保存
conn = sqlite3.connect("google_repos.db")
cur = conn.cursor()

# テーブル作成（リポジトリ情報用）
cur.execute("""
CREATE TABLE IF NOT EXISTS repositories (
    name TEXT,         -- リポジトリ名
    language TEXT,     -- 主要な言語
    stars INTEGER      -- スター数
)
""")
conn.commit()  # 作成を反映

# ========================================
# スクレイピング設定
# ========================================
base_url = "https://github.com/google?tab=repositories"  # Googleのリポジトリ一覧ページ
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ページ取得
res = requests.get(base_url, headers=headers)
time.sleep(1)  # リクエスト間隔1秒
soup = BeautifulSoup(res.text, "html.parser")

# ========================================
# リポジトリ情報取得
# ========================================
# GitHubのページ構造に合わせて修正
repo_list = soup.select("li.public")  # 公開リポジトリのリスト

for repo in repo_list:
    # リポジトリ名
    name_tag = repo.find("a", itemprop="name codeRepository")
    name = name_tag.text.strip() if name_tag else None

    # 主要言語
    lang_tag = repo.find("span", itemprop="programmingLanguage")
    language = lang_tag.text.strip() if lang_tag else None

    # スター数
    star_tag = repo.find("a.Link--muted")
    if star_tag:
        stars_text = star_tag.text.strip()
        if "k" in stars_text.lower():  # 1000単位
            stars = int(float(stars_text.lower().replace("k",""))*1000)
        else:
            stars = int(stars_text.replace(",",""))
    else:
        stars = 0

    # データベースに保存
    cur.execute(
        "INSERT INTO repositories (name, language, stars) VALUES (?, ?, ?)",
        (name, language, stars)
    )
    conn.commit()  # 1件ずつ保存
    time.sleep(1)  # サーバー負荷軽減のため待機

# ========================================
# 保存データ確認
# ========================================
cur.execute("SELECT * FROM repositories")
rows = cur.fetchall()
for row in rows:
    print(row)  # データを表示

# ========================================
# データベース接続を閉じる
# ========================================
conn.close()

