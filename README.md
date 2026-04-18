# 🚀 医疗 AI 创投 & 商务英语学习系统 (v3.0)
> **开发者**：Li Xueying & Gemini
> **定位**：基于《竞争战略》底层逻辑的医疗 AI 行业进阶工具

---

## 🛠️ 版本演进记录 (Version History)

### v1.0 | 基础框架期 (The Foundation)
* **核心突破**：建立 Python 自动化流。
* **技术实现**：使用 SQLite 3 存储结构化知识，通过 `import_data.py` 实现 JSON 到 DB 的无损转化，支持防重导入。

### v2.0 | 内容增强期 (Content & Media)
* **核心突破**：知识体系由“纯金融”进化为“商务英语+VC实战”双轨模型。
* **技术实现**：
  - **TTS 引擎**：集成浏览器原生 Web Speech API，实现零成本英文朗读。
  - **内容扩展**：数据库新增 `dialogue` 和 `case_study` 字段，支持情景模拟。

### v3.0 | 云端实战期 (Cloud & Interactive)
* **核心突破**：系统全面云端化，实现“沉浸式游戏感”学习。
* **技术实现**：
  - **动态沙盘引擎**：解析数据库 JSON 字符串，根据用户决策动态分支结局（A/B/C 路径）。
  - **逢七必考逻辑**：正则匹配算法，自动将历史语境中的核心词“挖空”，实现主动回忆测试。
  - **Stateless 适配**：采用侧边栏手动导航逻辑，完美兼容 Streamlit Cloud 免费服务器的休眠特性。

---

## 🏗️ 系统架构说明 (System Architecture)

### 1. 数据结构 (Database Schema)
* **`ai_english` 表**：存储核心词汇、学术定义、实战例句及情景对话。
* **`vc_finance` 表**：存储投资逻辑、真实案例及动态沙盘 JSON 逻辑树。

### 2. 技术栈 (Tech Stack)
* **前端/容器**：Streamlit
* **数据库**：SQLite 3
* **部署平台**：GitHub + Streamlit Community Cloud
* **访问方式**：iPhone Safari (支持 VPN 提速)

---

## 💡 给未来 AI 的开发者提示 (Prompt for Next AI)
如果你正在根据此文档接管项目，请遵循以下原则：
1. **数据一致性**：新生成的 JSON 必须包含 `sandbox` 字段，且格式需符合 `{"project_name": "...", "background": "...", "options": {...}, "outcomes": {...}}`。
2. **零成本原则**：除非用户明确要求，否则禁止引入收费 API。
3. **架构尊重**：维持目前的 `app.py` 和 `learning.db` 分离模式。

---

## 📂 维护流程
1. 修改本地 `daily_data.json`。
2. 运行 `python import_data.py`。
3. 将更新后的 `learning.db` 上传至 GitHub 仓库。
