---
name: save-hsinchu-east-weather
description: 自動使用 playwright-cli 查詢新竹市東區的即時天氣。包含了自動迴避 Yahoo 隱私權同意視窗的實戰經驗 (坑) 與直接提煉氣溫與降雨機率的指令。
---

# 讀取「新竹市東區」天氣技能指引

這個技能會引導你如何透過 `playwright-cli` 自動取得 Yahoo 氣象的新竹市東區天氣資料。
在執行此任務時，**必定會遇到 Yahoo 阻擋爬蟲或新使用者的「隱私權選擇 (Privacy choices)」同意畫面這個坑**。本技能已將解法內建於流程中。

## 執行流程 (Workflows)

### 步驟 1：開啟目標網頁
利用 Playwright CLI 開啟 Yahoo 氣象（新竹市東區），背景會自動建立 default session。
為了方便使用者觀察也可以加上 `--headed`。

```bash
playwright-cli open "https://weather.yahoo.com/zh-hant-tw/tw/%E6%96%B0%E7%AB%B9%E5%B8%82/%E6%96%B0%E7%AB%B9%E5%B8%82/"
```

### 步驟 2：處理「隱私權同意視窗」的坑 (Consent Page)
**⚠️ 這個坑非常重要：**
Yahoo 會重新導向到 `consent.yahoo.com`。此時若直接抓取內文，只會抓到隱私權條款，無法看到天氣。
我們必須點擊「Accept all (同意全部)」按鈕來通過這個畫面。

👉 處理指令：
```bash
playwright-cli click "getByRole('button', { name: 'Accept all' })"
```
*(備註：送出點擊後，Playwright cli 會自動等待網頁跳轉回正確的氣象頁面。若此指令因頁面跳轉太快而提示 Element not found 也不用擔心，代表已經成功跳轉過了)*

### 步驟 3：抓取與提煉首頁天氣資料
我們需要讀取經過 JS 渲染後的 DOM 結構。使用 `--raw eval` 取前 500 個字元，通常就能精準包含我們需要的所有資訊（如局部雷雨、溫度、降雨機率等）。

```bash
playwright-cli --raw eval "document.body.innerText.substring(0, 500)"
```

### 步驟 4：總結回報給使用者
將上一個步驟印出的字串解析成人類易讀的格式。通常包含以下資訊請提煉出來：
- 所在區域（例如：台灣 東區）
- 目前天氣狀態（例如：局部雷雨）
- 目前氣溫與體感溫度（例如：31° RealFeel 30°）
- 今日最高溫 / 最低溫
- 降雨機率（例如：55%）
- 風向與風速

## 清理 (可選)
如果使用者沒有要求保持瀏覽器開啟，或者我們是在背景執行，請順手將瀏覽器關閉以節省記憶體：
```bash
playwright-cli close
```
