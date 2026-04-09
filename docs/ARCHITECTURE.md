# 系統架構設計文件 (ARCHITECTURE.md)

## 1. 技術架構說明
本專案採用 **Flask MVC 模式** 開發，選用以下技術棧以達成快速開發與高內聚的功能實作：
- **後端框架：Python + Flask**
  - **原因**：Flask 是一個輕量級的 WSGI web 框架，適合中小型應用，有極高的擴展性。
  - **MVC 負責對應**：Controller 邏輯由 Flask 的 Routes (路由) 處理。
- **模板引擎：Jinja2**
  - **原因**：內建於 Flask，可直接將後端資料無縫渲染至 HTML 畫面。
  - **MVC 負責對應**：負責 View 邏輯展示。不需要前後端分離，統一由後端渲染畫面，降低開發與部署複雜度。
- **資料庫：SQLite (透過 sqlite3 或 SQLAlchemy)**
  - **原因**：無需配置獨立的資料庫伺服器，資料會被整合成一個檔案 (`.db`)，非常適合 MVP 專案。
  - **MVC 負責對應**：作為 Model 層，負責定義任務 (Task) 資料表結構並處理與資料庫的讀寫。

## 2. 專案資料夾結構

我們將採用經典的 Flask 專案組織結構：

```text
web_app_development/
├── app/
│   ├── __init__.py        # Flask 應用程式初始化與配置
│   ├── models/            # Model 區塊
│   │   └── task.py        # 定義 Task 資料結構與 CRUD 邏輯 (包含標題、狀態、優先級等)
│   ├── routes/            # Controller 區塊
│   │   └── task_routes.py # 接收前端請求並回傳渲染結果或重導向
│   ├── templates/         # View 區塊 (Jinja2 HTML 模板)
│   │   ├── base.html      # 共用的網頁基礎模板 (引入 CSS/JS 等)
│   │   └── index.html     # 任務列表主畫面
│   └── static/            # 分發到前端的靜態資源
│       ├── css/
│       │   └── style.css  # 玻璃擬物化與深色模式的 CSS
│       └── js/
│           └── main.js    # 處理微動畫、過濾互動等的客製化 JS
├── instance/
│   └── database.db        # SQLite 實體資料庫檔案 (不進版控)
├── docs/
│   ├── PRD.md             # 產品需求文件
│   └── ARCHITECTURE.md    # 系統架構文件 (本文件)
├── app.py                 # 專案啟動入口程式碼
└── requirements.txt       # Python 依賴套件列表
```

## 3. 元件關係圖

以下展示瀏覽器、路由、模型與資料庫之間的互動與資料流關係：

```mermaid
flowchart LR
    Browser[瀏覽器 (Browser)]
    Route[Flask Route\n(Controller)]
    Model[Task Model\n(Model)]
    DB[(SQLite DB)]
    Template[Jinja2 Template\n(View)]

    Browser -- "1. 發出 HTTP Request\n(GET / POST 等)" --> Route
    Route -- "2. 呼叫方法與傳遞參數" --> Model
    Model -- "3. 執行 SQL 語句" --> DB
    DB -- "4. 回傳查詢結果" --> Model
    Model -- "5. 將資料轉換為 Python 物件" --> Route
    Route -- "6. 傳遞變數並渲染模板" --> Template
    Template -- "7. 回傳最終生成的 HTML 網頁" --> Browser
```

## 4. 關鍵設計決策

1. **捨棄前後端分離，採用 SSR (伺服器端渲染) 與 Flask MVC**
   - **原因**：為了最快速建立 MVP，透過 Flask + Jinja2 能夠直接在伺服器端完成資料注入與頁面生成，省去建立與串接前端 RESTful API 的成本。這對目前僅有 Task CRUD 的需求是最簡潔、不易出錯的設計。

2. **選擇 SQLite 取代原訂的 localStorage**
   - **原因**：原本的 PRD 中提及使用 `localStorage` 來作資料持久化。但在導入 Flask 後，採用真正的關聯式資料庫 (SQLite) 將大幅提升後續擴充性 (如新增任務關聯或使用者認證)。SQLite 又具備零設定的優勢，完美符合此階段。

3. **前端保留 Vanilla CSS / JS，完全掌控設計美學**
   - **原因**：PRD 要求強烈的「視覺驚豔感」、玻璃擬物化與過渡動畫等高定義效果。不引入 Tailwind 或 Bootstrap，全面採用原生客製化 CSS，能賦予開發者最大的設計靈活度。而輕量級的原生 JavaScript 可用來觸發動態交互和微動畫，整體架構乾淨純粹。

4. **將 `models` 與 `routes` 模組化分拆**
   - **原因**：身為可擴充的 Web APP，將路由 (Controller 邏輯) 與資料庫操作 (Model 邏輯) 分拆在獨立資料夾中，可使單一職責更清晰；日後若要加入身分驗證等其他系統，也能無痛擴展。
