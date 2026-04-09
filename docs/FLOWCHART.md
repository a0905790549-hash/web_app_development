# 流程圖設計：線上抽籤系統

這份文件基於產品需求 (PRD) 與系統架構 (ARCHITECTURE) 進行視覺化的流程設計。包含了使用者操作的旅程，以及後方系統是如何互動儲存資料的流程。

## 1. 使用者流程圖 (User Flow)

這張圖呈現了使用者造訪網站後，經過哪些畫面，可能會遇到哪些分支與操作選項。
透過這張圖，開發者與設計師能清楚判斷是否有遺漏的保護機制或錯誤處理。

```mermaid
flowchart TD
    A([使用者造訪系統]) --> B[首頁 - 抽籤活動設定]
    B --> C[輸入活動名稱]
    C --> D[貼上參加者名單]
    D --> E[設定抽出數量]
    E --> F[點擊「開始抽籤」]
    
    F --> G{系統驗證資料合法性}
    G -->|數量大於總人數或名單空白| H[畫面跳轉：顯示錯誤提示語]
    H --> B
    
    G -->|驗證成功與後端儲存完畢| I[進入抽籤結果頁面 (資料已存入)]
    I --> J[播放抽籤滾動動畫]
    J --> K[動畫結束：浮現最終中籤名單]
    
    A --> M[也可以選擇點擊「歷史紀錄」]
    M --> N[檢視過往所有的抽籤結果與中獎名單]
    K -.-> N
```

---

## 2. 系統序列圖 (Sequence Diagram)

這張序列圖深入探討當使用者「點擊開始抽籤」送出表單後，在系統內部，瀏覽器、Flask 後端、資料操作 Model 與 SQLite 資料庫之間發生了什麼對話。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (HTML/JS)
    participant Flask as Flask (Router/Controller)
    participant Model as Model (database.py)
    participant DB as SQLite

    User->>Browser: 於首頁填妥表單(名單/人數)，點擊「開始抽籤」
    Browser->>Flask: 發送 POST 請求並攜帶表單資料至 /draw
    
    %% 後端運算階段
    Flask->>Flask: 檢查抽出數量是否不大於總人數等防呆邏輯
    alt 驗證失敗
        Flask-->>Browser: 回傳錯誤訊息並重新渲染表單
    else 驗證成功
        Flask->>Flask: 呼叫 Python 的 random.sample() 執行隨機抽籤
        
        %% 資料庫儲存階段
        Flask->>Model: 請求將本次「活動資訊」與「抽中與未抽中的名單」存入資料庫
        Model->>DB: INSERT INTO 寫入相關資料表
        DB-->>Model: 確保寫入完成，回傳新增紀錄的 ID
        Model-->>Flask: 取得資料庫操作成功的狀態
        
        %% 回傳給前端
        Flask-->>Browser: 回傳 HTML 文件 (帶有中籤名單及動畫播放標記)
        
        %% 畫面呈現
        Browser->>Browser: 執行 JS 腳本，播放抽籤轉場動畫
        Browser->>User: 顯示最終抽出的獲勝名單
    end
```

---

## 3. 功能清單與路由對照表

這是統整前後端對接的網址結構，幫助我們在下一步進入實作或 API 設計階段時有所依循。

| 功能名稱 | 說明 | HTTP 路由 (URL) | 方法 (Method) |
| --- | --- | --- | --- |
| **首頁與表單** | 呈現填寫抽籤資訊的介面 | `/` | `GET` |
| **執行抽籤** | 接收表單、驗證、計算抽籤結果、存 DB 並回傳畫面 | `/draw` | `POST` |
| **歷史紀錄列表** | 列出過去所有建立過的抽籤活動 | `/results` | `GET` |
| **單一活動結果** | 檢視某一次特定活動（由 ID 指定）的完整名單 | `/results/<int:id>` | `GET` |
