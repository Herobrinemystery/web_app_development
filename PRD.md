# Product Requirements Document (PRD): Task Management System

### Goal Description
這個專案的目標是開發一個現代化、動態且視覺上令人驚豔的「任務管理系統 (Task Management System) Web 應用程式」。這個應用程式旨在幫助使用者輕鬆組織、追蹤和管理他們的日常任務。為了確保絕佳的使用者體驗，系統將會採用頂級的現代網頁設計與微動畫，並具備高度響應式操作介面。

## 1. 產品概述與目標
提供一個直覺、高效的工具供使用者管理任務，解決忘記待辦事項或難以安排優先順序的痛點。

## 2. 核心功能需求 (MVP - 第一版)

### 2.1 任務管理 (CRUD)
- **新增任務 (Create)**：使用者可以輸入任務標題、詳細描述。
- **讀取任務 (Read)**：在主畫面清晰展示所有任務，支援過濾與搜尋。
- **編輯任務 (Update)**：使用者可以修改已存在的任務細節。
- **刪除任務 (Delete)**：使用者可以移除不需要的任務。

### 2.2 任務屬性與狀態
- **狀態追蹤**：未完成 (To Do)、進行中 (In Progress)、已完成 (Done)。
- **優先級 (Priority)**：低 (Low)、中 (Medium)、高 (High)，並有對應的視覺顏色標示。
- **截止日期 (Due Date)**：(選配) 可為任務設定預期完成時間。

### 2.3 介面與互動
- **動態過濾 (Filtering)**：快速過濾顯示「今日任務」、「已完成」、「高優先級」等。
- **拖曳功能 (Drag & Drop)**：(如果選擇看板視圖) 允許使用者在不同狀態欄位間拖曳任務。
- **資料持久化**：使用瀏覽器的 `localStorage` 保存任務資料，確保重新整理重新開啟後資料不會遺失。

## 3. UI/UX 與設計美學規範 (Design Aesthetics)

為了讓使用者在第一眼就感到驚豔 (WOW factor)，本系統的介面必須遵守以下設計準則：
- **深色模式/淺色模式 (Dark/Light Mode)**：提供精緻的玻璃擬物化 (Glassmorphism) 質感，預設採用深色模式以呈現頂級質感。
- **鮮豔且和諧的色彩調色盤**：避免使用死板的純紅、純藍，改用 HSL 調色（例如：霓虹紫、青藍漸層）。
- **現代字體**：引入 Google Fonts（如 `Inter` 或 `Outfit`）提升畫面精緻度與閱讀體驗。
- **微動畫 (Micro-animations)**：
  - 任務卡片 Hover 時的光暈或浮起效果。
  - 任務勾選完成時的流暢過渡動畫（如打勾動畫、卡片淡出或變灰）。
  - 流暢的頁面轉場與狀態切換。

## 4. Proposed Changes (實作計畫)

我們將採用循序漸進的開發方式。

### Frontend Architecture
專案將使用 `Vite` 初始化，資料夾結構大致如下：

#### `index.html`
- 語意化的 HTML5 結構，確保良好的 SEO 與無障礙體驗 (雖然是 Web App，但基礎包含 Title, Meta descriptions 等)。

#### `src/style.css`
- 定義 CSS 變數 (Design Tokens) 處理顏色、字體、陰影。
- 玻璃擬物化樣式 class 定義。
- 動畫設定 (Keyframes 及 Transitions)。

#### `src/main.js`
- 應用程式進入點與事件監聽綁定。

#### `src/components/TaskBoard.js`
- 渲染任務列表或看板的核心邏輯。

#### `src/store/TaskStore.js`
- 負責與 `localStorage` 互動，處理資料層的讀取、寫入與更新。
