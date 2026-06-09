# 就活管理アプリ

就活の企業情報・選考状況・締切を一元管理するWebアプリです。

## 機能

- 企業の追加・編集・削除
- ステータス管理（未応募 / ES提出 / 面接 / 内定 / 不合格）
- 締切日の記録
- ステータスでのフィルタリング
- サマリー表示（登録数・ES提出数・面接数・内定数）

## 使用技術

- **Backend**: Python / Flask
- **Frontend**: HTML / CSS（テンプレートエンジン: Jinja2）
- **データ保存**: JSON ファイル

## セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/job-tracker.git
cd job-tracker

# 依存ライブラリをインストール
pip install flask

# アプリを起動
python app.py
```

ブラウザで `http://localhost:5000` を開く。

## ディレクトリ構成

```
job-tracker/
├── app.py              # Flaskアプリ本体
├── data.json           # データ保存ファイル（自動生成）
├── templates/
│   ├── base.html
│   ├── index.html
│   └── form.html
└── static/
    └── css/
        └── style.css
```

## 今後追加したい機能

- [ ] 締切日が近い企業のハイライト表示
- [ ] 締切でのソート機能
- [ ] CSV エクスポート
