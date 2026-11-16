---
name: ddd
description: DDD 領域驅動設計 - 戰略設計。專注於產出 Domain Model 文件，包括識別核心域/支撐域/通用域、拆分 Bounded Context、定義 Ubiquitous Language 與 Context Map。Use when (1) the user asks how to split Bounded Contexts, (2) the user asks to define Ubiquitous Language, (3) the user wants to create a Domain Model document, (4) the project uses DDD architecture and requires strategic design.
---

# DDD 領域驅動設計 — 戰略設計

本 Skill 專注於**產出戰略設計文件**，幫助使用者將業務需求轉化為清晰的領域模型。

## 產出目標

產出一份 **DOMAIN-MODEL.md** 文件，包含：

1. **領域與子域 (Domain & Subdomains)** — 識別核心子域、支撐子域、通用子域
2. **限界上下文 (Bounded Contexts)** — 根據子域拆分軟體邊界
3. **通用語言 (Ubiquitous Language)** — 中英對照的詞彙定義表
4. **上下文映射 (Context Map)** — 定義上下文間的溝通規則與領域事件

---

## 產出流程

> 由使用者提出需求，或與 Agent 討論後產出。

### Step 1: 識別領域與子域

```
提問方向：
- 這個系統的核心價值是什麼？靠什麼賺錢？
- 哪些業務是必需的？哪些可以外包？
- 團隊擅長什麼？市場上有哪些現成方案？
```

**產出格式：**
```markdown
## 領域與子域

**Domain：** [系統要解決的問題領域]

**Subdomains：**

- **核心子域 (Core Subdomain):** [最有價值的業務，需自行開發的護城河]
- **支撐子域 (Supporting Subdomain):** [支撐核心子域的業務，可自行開發或客製化]
- **通用子域 (Generic Subdomain):** [可直接使用外部方案的業務]
```

### Step 2: 識別限界上下文

```
提問方向：
- 這個業務中，哪些術語雖然相同但關注點完全不同？
- 哪些功能必須同時成功？哪些可以延遲？
- 哪些功能會獨立變更、互不影響？
```

**判斷標準：**
- **語言是否改變？** 同一個名詞在不同功能中，關注的屬性完全不同 → 拆分
- **是否需要強一致性？** 兩個操作必須在同一個 Transaction 完成 → 不拆分
- **業務變更獨立性？** 各自發展、互不影響 → 拆分

**產出格式：**
```markdown
## 限界上下文

1. **XXX Context** — 職責說明，對應[子域]
2. **YYY Context** — 職責說明，對應[子域]
```

### Step 3: 定義通用語言

```
提問方向：
- 這個業務中，最重要的名詞有哪些？
- 每個名詞在不同的上下文中，具體包含哪些屬性？
- 團隊內部怎麼稱呼這些概念？
```

**產出格式：**
```markdown
## 通用語言

| 中文業務名詞 | 英文命名 | 所在上下文 | 嚴格定義 |
| :---------- | :------- | :--------- | :------- |
| 任務         | Task     | TaskContext| 具備 id, title, isCompleted, dueDate |
```

### Step 4: 定義上下文映射

```
提問方向：
- 哪些上下文需要取得其他上下文的資料？
- 哪些操作完成後需要通知其他上下文？
- 上下游關係是什麼？
```

**溝通規則：**
- **禁止直接操作**：禁止跨 Context 直接 import 類別或查詢資料庫
- **ID 參照**：跨 Context 關聯使用純 ID（string/uuid），禁止 Foreign Key
- **事件驅動**：透過 Domain Event 觸發跨 Context 行為

**產出格式：**
```markdown
## 上下文映射

- **XXX Context [上游] → [下游] YYY Context**
  - 說明：XXX 發出事件，YYY 監聽處理

## 領域事件

| 事件名稱 | 來源上下文 | 監聽上下文 | 觸發時機 |
| :------- | :--------- | :--------- | :------- |
| TaskCompletedEvent | TaskContext | NotificationContext | 任務完成時 |
```

---

## 參考資源

根據當前任務讀取對應的 reference：

- 需要識別子域 → 讀 [references/domain-subdomains.md](references/domain-subdomains.md)
- 需要拆分 Bounded Context → 讀 [references/bounded-context.md](references/bounded-context.md)
- 需要定義 Ubiquitous Language → 讀 [references/ubiquitous-language.md](references/ubiquitous-language.md)
- 需要定義 Context Map → 讀 [references/context-map.md](references/context-map.md)

---

## 實作時的 DDD 檢查

當後續進行功能實作時，Agent 必須持續檢查：

- [ ] **Context 邊界**：這個功能屬於哪個 Context？程式碼是否在正確的資料夾？
- [ ] **命名一致性**：變數名、類別名、API 路徑是否 100% 符合 Ubiquitous Language？
- [ ] **跨 Context 隔離**：是否有偷偷 import 其他 Context 的內部類別？
- [ ] **ID 參照**：資料庫 Schema 是否有跨 Context 的 Foreign Key？

若發現問題，應立即修正或回報使用者。
