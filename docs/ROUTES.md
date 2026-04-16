# 路由設計 (ROUTES) - 食譜收藏夾系統

本文件定義系統所有的 Flask 路由，涵蓋首頁、使用者認證與食譜維護（包含食材搜尋功能）。

## 1. 路由總覽列表

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁模組** |
| 首頁 / 最新食譜 | GET | `/` | `templates/index.html` | 進入系統的第一眼，展示公開推薦食譜與搜尋入口區塊。 |
| **認證模組** |
| 註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單。 |
| 處理註冊 | POST | `/auth/register` | — | 接收 username/password，註冊成功後導向首頁或登入頁。 |
| 登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單。 |
| 處理登入 | POST | `/auth/login` | — | 驗證帳密，設定 session，並導向首頁。 |
| 登出系統 | GET | `/auth/logout` | — | 清除 session，並導向首頁。 |
| **食譜與食材模組** |
| 我的專屬食譜 | GET | `/recipes/my` | `templates/recipes/my_recipes.html` | 列出自己新增的食譜（不論公開或私有）。 |
| 新增食譜頁面 | GET | `/recipes/new` | `templates/recipes/new.html` | 顯示食譜新增表單，可輸入多個食材。 |
| 處理建立食譜 | POST | `/recipes/create` | — | 接收並儲存食譜、食材紀錄，導向到詳情頁或列表。 |
| 檢視食譜詳情 | GET | `/recipes/<int:recipe_id>` | `templates/recipes/detail.html` | 檢視單筆食譜步驟與包含食材。 |
| 編輯食譜頁面 | GET | `/recipes/<int:recipe_id>/edit`| `templates/recipes/edit.html` | 編輯食譜與其食材。 |
| 處理更新食譜 | POST | `/recipes/<int:recipe_id>/update`| — | 處理 HTML 表單修改，並更新資料庫。 |
| 處理刪除食譜 | POST | `/recipes/<int:recipe_id>/delete`| — | 刪除指定記錄，返回到食譜清單。 |
| 食材綜合搜尋 | GET | `/recipes/search` | `templates/recipes/search.html` | 利用 query string 搜尋（例如 `?q=豬肉`）。 |

---

## 2. 路由詳細說明

### 首頁模組
- **GET `/`** (首頁)
  - **處理邏輯**：調用 `Recipe.get_all(public_only=True)` 取得全站公開文章前 N 筆。
  - **輸出**：渲染 `index.html`，將取得的列表傳入 (`recipes=recipes`)。

### 認證模組 (Blueprint `auth`)
- **GET / POST `/auth/register`**
  - **輸入**：(POST) `username`, `password`
  - **處理邏輯**：驗證格式。將密碼使用 `werkzeug.security` 進行 hash 並呼叫 `User.create()`。若帳號重複需產生 flash 錯誤。
  - **輸出**：成功導向 `auth.login`，失敗導回 `auth.register` 並顯示 flash 錯誤訊息。

- **GET / POST `/auth/login`**
  - **輸入**：(POST) `username`, `password`
  - **處理邏輯**：呼叫 `User.get_by_username()`，驗證雜湊密碼是否吻合。若吻合，記錄到 `session['user_id']`。
  - **輸出**：成功後重導向 `/` 或 `/recipes/my`，失敗則 flash 錯誤。

### 食譜模組 (Blueprint `recipes`)
- **POST `/recipes/create`** (對應原本 RESTful 架構的 POST)
  - **輸入**：`title`, `steps`, `is_public` (checkbox), 以及輸入的多筆食材 (如 `ingredients` 欄位以逗號分隔)。
  - **處理邏輯**：解析食材字串，利用 `Ingredient.create()` 建立/取得每筆食材 ID，再呼叫 `Recipe.create()`，關聯剛建立的 ID 清單。
  - **輸出**：完成後重導向 `/recipes/my`。

- **GET `/recipes/search`**
  - **輸入**：URL param `q` 或特定的 ingredient_ids
  - **處理邏輯**：解析 query 並運用 `Ingredient.search_by_name()` 找到符合的 Ingredient ID，將它代入 `Recipe.search_by_ingredients()` 來篩選食譜。
  - **輸出**：取得結果後，渲染 `recipes/search.html`。

- **POST `/recipes/<int:recipe_id>/delete`**
  - **邏輯**：檢查身分（是否為作者或是 Admin），是則 `Recipe.delete(recipe_id)`。
  - **輸出**：安全刪除後導向回到上一頁或 `/recipes/my`。

---

## 3. Jinja2 模板清單

所有的模板將放置在 `app/templates` 中，並以 `base.html` 作為基礎版面設計，統一處理 CSS 載入與導覽列：

- `base.html` (核心佈局，處理 Flash 訊息與版面)
- `index.html` (首頁/公開食譜牆，繼承 base.html)
- `auth/` (使用者認證區 - 繼承 base.html)
  - `login.html`
  - `register.html`
- `recipes/` (食譜專區 - 繼承 base.html)
  - `my_recipes.html` (私人列表)
  - `new.html` (新增表單)
  - `edit.html` (編輯表單)
  - `detail.html` (詳情閱讀)
  - `search.html` (展示過濾/搜尋結果)
