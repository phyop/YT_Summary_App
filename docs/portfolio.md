# Portfolio Collateral

## STAR 履歷要點

- 面對 YouTube 長影片難以快速吸收的問題，設計 Flask 本機應用串接 `yt-dlp`、公開字幕與 OpenAI Responses API，將單片、播放清單或頻道最新四片轉成結構化繁體中文摘要。
- 為避免公開專案洩漏金鑰，建立僅限本機 `127.0.0.1` 的執行邊界、記憶體型 API Key 輸入與完整 `.gitignore`，並以秘密字串掃描及 Git 狀態檢查驗證發布安全。
- 將影片探索、字幕擷取、模型摘要與展示層拆分，搭配 mocked API 測試與 URL 參數化測試，使外部服務不穩定時仍能驗證核心行為。
- 針對繁體中文長文閱讀重新設計資訊層級，以整體觀察、影片卡片、重點清單與一句話結論降低掃讀成本，並支援鍵盤 Enter 與行動版版面。

## LinkedIn 專案介紹

我把一次「整理 YouTube 頻道最新影片」的工作流程，做成可雙擊啟動的繁體中文摘要 App。使用者貼上單支影片、播放清單或頻道網址，按 Enter 後，系統會解析最新非直播影片、取得公開字幕，再透過 OpenAI 產生保留數字與不確定語氣的結構化摘要。技術上採 Flask、yt-dlp、YouTube Transcript API 與 OpenAI Responses API，並特別處理網址驗證、字幕缺漏、API Key 不落地、錯誤訊息與響應式閱讀介面。專案以單元測試、語法檢查、秘密掃描與 Git 發布檢查確保品質。這次實作讓我更深刻體會：AI 產品的價值不只在模型輸出，更在可靠的資料取得、清楚的安全邊界與真正好讀的使用體驗。

## Conventional Commit

`feat: build Traditional Chinese YouTube summary app`

## PR 描述

### Summary

建立可在 Windows 雙擊啟動的本機 YouTube 繁體中文摘要工具。

### Changes

- 支援影片、播放清單與頻道網址
- 擷取公開字幕並呼叫 OpenAI Responses API
- 加入響應式繁中閱讀介面、Enter 提交與錯誤處理
- 新增 Windows 啟動器、測試、安全說明與作品集文件

### Testing

- `pytest -q`
- `python -m compileall app.py src tests`
- `git diff --check`
- 秘密與敏感檔案掃描

### Screenshots

首頁與摘要結果介面截圖將於視覺驗證後補入 PR。

### Future Work

- 增加時間戳引用與 Markdown/PDF 匯出
- 提供本機模型後端與摘要快取
- 支援自訂影片數量、提示詞與模型

## 後續專案

- **AI Software Engineer：** 實作可重試工作佇列、字幕快取、模型評測資料集與端對端測試。
- **AI Solution Architect：** 建立可替換的雲端／本機模型介面、成本觀測、速率限制與多租戶部署藍圖。
- **AI Agent Consultant：** 延伸為研究代理，跨頻道追蹤論點、產生引用式週報並標記前後觀點變化。
