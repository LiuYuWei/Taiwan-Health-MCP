# 更新日誌 (Changelog)

所有對本專案的重要更改都將記錄在此檔案中。

遵循 [Keep a Changelog](https://keepachangelog.com/) 規範。

版本遵循 [語意版本控制](https://semver.org/) 規範。

---

## [1.1.0] - 2025-01-03

### 新增

- ✨ **健康食品與營養服務** - 新增健康食品查詢和營養成分分析
- ✨ **FHIR 互操作性工具** - 增強 FHIR 資源驗證和轉換功能
- ✨ **檢驗分析功能** - 實現實驗室檢驗結果判讀和參考範圍對比
- ✨ **MkDocs 文檔網站** - 構建完整的技術文檔網站及部署指南
- ✨ **LOINC 資料整合** - 支援 87,000+ LOINC 檢驗代碼（可選）

### 改進

- 🔧 優化 ICD-10 代碼搜尋效率
- 🔧 增強藥品查詢的模糊匹配功能
- 🔧 改進 FHIR Condition 資源轉換邏輯
- 🔧 更新文檔和示例代碼

### 文檔

- 📚 添加詳細的系統架構文檔
- 📚 新增完整的 API 參考
- 📚 提供 FHIR 整合使用指南
- 📚 增加常見問題解答

### 開源準備

- 🌍 添加 MIT License
- 🌍 創建 CONTRIBUTING.md 貢獻指南
- 🌍 創建 CODE_OF_CONDUCT.md 行為準則
- 🌍 更新所有文檔中的 GitHub URL
- 🌍 完整掃描並修復敏感信息

---

## [1.0.0] - 2024-12-01

### 新增

- 🎯 **核心 MCP 伺服器** - 完整的台灣醫療健康資料 MCP 伺服器實現
- 📋 **ICD-10 服務** - 台灣 ICD-10-CM/PCS 代碼查詢與搜尋
- 💊 **藥品服務** - FDA 藥品信息查詢與識別
- 🏥 **FHIR 整合** - Condition 和 Medication 資源的 FHIR R4 轉換
- 🔬 **基礎檢驗服務** - 30+ 常用檢驗項目的參考範圍查詢
- 📖 **臨床指引服務** - 臨床診療路徑和指引查詢
- 🐳 **Docker 支援** - 完整的 Docker 和 Docker Compose 配置
- 📊 **資料整合** - 整合台灣 FDA 開放資料

### 技術特性

- Python 3.8+ 支援
- 完整的類型提示
- 結構化錯誤處理
- 詳細的日誌系統
- 自動資料更新機制

### 文檔

- 📖 完整的 README 和快速開始指南
- 🏗️ 系統架構設計文檔
- 📡 API 接口文檔
- 💻 開發環境設置指南

---

## 版本說明

### 語意版本控制

我們遵循 [Semantic Versioning](https://semver.org/)：

- **MAJOR** - 不兼容的 API 更改
- **MINOR** - 向後兼容的新功能
- **PATCH** - 錯誤修復

### 發佈頻率

- 重大更新：根據新功能開發進度
- 錯誤修復：按需發佈
- 安全修補：立即發佈

---

## 未來規劃

### 計劃中的功能

- [ ] 擴展 LOINC 整合支援
- [ ] 添加自然語言處理查詢
- [ ] 實現實時資料同步
- [ ] 支援多語言介面
- [ ] 性能優化和快取機制
- [ ] GraphQL API 支援

### 社區貢獻

歡迎社區貢獻！如有功能建議或問題報告，請開啟 [GitHub Issue](https://github.com/audi0417/Taiwan-Health-MCP/issues)。

---

## 如何貢獻

請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳細的貢獻指南。

---

## 許可

本專案採用 [MIT License](LICENSE)。

---

## 聯絡方式

如有任何疑問或建議，歡迎聯絡：

- 📧 提交 [GitHub Issue](https://github.com/audi0417/Taiwan-Health-MCP/issues)
- 💬 開啟 [GitHub Discussion](https://github.com/audi0417/Taiwan-Health-MCP/discussions)

---

**感謝所有貢獻者的支持！** 🙏
