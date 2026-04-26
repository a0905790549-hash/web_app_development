# 路由設計 (ROUTES)

這份文件根據 PRD 與系統架構文件，定義線上抽籤系統的所有 URL 路徑與其對應的邏輯及畫面。

## 1. 路由總覽表

| 功能名稱 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁 (活動表單)** | GET | `/` | `templates/index.html` | 呈現填寫活動名稱、抽出數量與參加者名單的表單。 |
| **執行抽籤** | POST | `/draw` | — | 接收首頁表單資料，執行隨機抽籤與資料庫存檔，完成後重導向至結果頁面。 |
| **歷史紀錄列表** | GET | `/results` | `templates/results.html` | 列出系統中所有過去建立過的抽籤活動紀錄。 |
| **單一活動結果** | GET | `/results/<int:id>` | `templates/result_detail.html` | 呈現特定抽籤活動的參與者名單（區分中籤與未中籤）。若為剛抽完的導向，可由前端觸發抽籤動畫。 |

## 2. 詳細路由說明

### `GET /` (首頁)
- **輸入**: 無參數。
- **處理邏輯**: 單純渲染首頁表單畫面。
- **輸出**: 渲染 `index.html`。

### `POST /draw` (執行抽籤)
- **輸入 (表單資料)**:
  - `title` (文字): 活動名稱。
  - `draw_count` (數字): 預計抽出人數。
  - `participants` (文字): 多行文字，每行為一位參加者。
- **處理邏輯**:
  1. 驗證輸入合法性（人數是否大於 0、參加者名單是否為空、抽出人數是否大於名單總數）。
  2. 若驗證失敗，帶錯誤訊息重新渲染 `index.html`。
  3. 驗證成功後，使用 Python 的 `random.sample` 抽出中籤名單。
  4. 呼叫 Model 建立 `Event`，接著批次建立 `Participant`。
- **輸出**: 成功後使用 HTTP 302 重導向至 `GET /results/<event_id>?play_anim=1`。

### `GET /results` (歷史紀錄列表)
- **輸入**: 無。
- **處理邏輯**: 呼叫 Model 取得所有按照時間倒序排列的 `Event` 列表。
- **輸出**: 將資料傳入並渲染 `results.html`。

### `GET /results/<int:id>` (單一活動結果)
- **輸入**: URL 參數 `id` (活動的 ID)，可選 Query String `play_anim`。
- **處理邏輯**:
  1. 呼叫 Model 取得指定的 `Event` 以及對應的 `Participant` 列表。
  2. 若找不到對應活動，回傳 404 錯誤。
- **輸出**: 將活動資訊與參與者名單傳入並渲染 `result_detail.html`。

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 資料夾下：

1. **`base.html`**
   - **說明**: 共用基礎版型，包含 HTML `<head>`（引用 CSS/JS）、網站的 Navigation Bar 與 Footer。
2. **`index.html`**
   - **說明**: 繼承 `base.html`。首頁表單，提供文字框與 textarea 讓使用者貼上名單。
3. **`results.html`**
   - **說明**: 繼承 `base.html`。利用迴圈條列顯示所有歷史抽籤紀錄。
4. **`result_detail.html`**
   - **說明**: 繼承 `base.html`。展示抽籤結果名單，並且在收到特定的 query 參數時，負責載入並播放前端抽籤動畫。
