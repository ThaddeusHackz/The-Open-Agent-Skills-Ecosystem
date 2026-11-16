---
name: mysql-schema
description: 扫描 MySQL 数据库的所有表结构，生成 mysql_schema/mysql_schema.md（含表清单和每张表的字段详情）。当用户要求导出数据库表结构、查看 MySQL Schema、扫描数据库设计或提到 /mysql-schema 时使用。
---

# List MySQL Schema

通过 Python 脚本连接 MySQL 数据库，扫描所有表结构，生成 `mysql_schema/mysql_schema.md`。

## 执行步骤

### 1. 收集数据库连接信息

使用 widget 表单收集连接信息，参数说明如下：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| host | 数据库主机地址 | 无，必填 |
| port | 端口号 | 3306 |
| user | 用户名 | 无，必填 |
| password | 密码 | 无，必填 |
| database | Schema 名称 | 无，必填 |

**显示表单步骤：**

1. 调用 `genui.load_guidelines`，modules 传 `["form"]`
2. 调用 `genui.show_widget`，使用以下参数：
   - `title`: `"mysql_connection_form"`
   - `widget_code`: 直接传递下方表单 HTML 代码（使用内联渲染，不打开右侧面板）
   - `artifact`: `{ "enabled": false }`
   - `i_have_seen_guidelines`: `true`
   - 如果用户之前提供过部分参数，通过 `data` 传入预填值，例如 `{ "host": "127.0.0.1", "port": 3306 }`

widget_code 内容如下：

```html
<style>
.conn-form { max-width: 480px; margin: 0 auto; }
.conn-form .desc { color: var(--color-text-muted); font-size: 14px; margin-bottom: 1.25rem; }
.conn-form .section-title { font-size: 11px; font-weight: 600; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.6rem; padding-bottom: 0.3rem; border-bottom: 1px solid var(--color-border); }
.conn-form .section { margin-bottom: 1.25rem; }
.conn-form .form-group { margin-bottom: 0.85rem; }
.conn-form .form-label { display: block; font-size: 12px; color: var(--color-text-muted); margin-bottom: 4px; font-weight: 500; }
.conn-form .req { color: var(--color-danger); }
.conn-form .form-input { width: 100%; padding: 0.5rem 0.75rem; background: var(--color-input-bg); border: 1px solid var(--color-input-border); border-radius: 6px; color: var(--color-input-text); font-size: 14px; font-family: inherit; }
.conn-form .form-input:focus { outline: none; border-color: var(--color-focus); }
.conn-form .form-input::placeholder { color: var(--color-text-muted); opacity: 0.6; }
.conn-form .row { display: grid; grid-template-columns: 2fr 1fr; gap: 0.75rem; }
.conn-form .hint { font-size: 11px; color: var(--color-text-muted); margin-top: 3px; }
.conn-form .btns { display: flex; gap: 0.75rem; margin-top: 1.25rem; }
.conn-form .btn-primary { flex: 1; padding: 0.5rem 1rem; background: var(--color-accent); color: var(--color-accent-text); border: none; border-radius: 6px; font-size: 14px; font-weight: 500; cursor: pointer; }
.conn-form .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.conn-form .btn-sec { padding: 0.5rem 1rem; background: var(--color-hover); color: var(--color-text); border: none; border-radius: 6px; font-size: 14px; cursor: pointer; }
.conn-form .status { margin-top: 0.75rem; font-size: 12px; color: var(--color-text-muted); display: flex; align-items: center; gap: 0.4rem; }
.conn-form .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--color-text-muted); }
.conn-form .dot.on { background: var(--color-success); }
</style>

<div class="conn-form">
  <p class="desc">请输入 MySQL 数据库连接信息，用于扫描表结构并生成文档。</p>

  <div class="section">
    <div class="section-title">连接设置</div>
    <div class="row">
      <div class="form-group">
        <label class="form-label">主机地址 <span class="req">*</span></label>
        <input class="form-input" type="text" id="cf-host" placeholder="例如：127.0.0.1 或 db.example.com">
      </div>
      <div class="form-group">
        <label class="form-label">端口</label>
        <input class="form-input" type="number" id="cf-port" value="3306">
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">认证信息</div>
    <div class="form-group">
      <label class="form-label">用户名 <span class="req">*</span></label>
      <input class="form-input" type="text" id="cf-user" placeholder="数据库用户名">
    </div>
    <div class="form-group">
      <label class="form-label">密码 <span class="req">*</span></label>
      <input class="form-input" type="password" id="cf-password" placeholder="数据库密码">
      <div class="hint">密码仅在提交时使用，不会被存储。</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">数据库</div>
    <div class="form-group">
      <label class="form-label">Schema 名称 <span class="req">*</span></label>
      <input class="form-input" type="text" id="cf-database" placeholder="要扫描的数据库名称">
    </div>
  </div>

  <div class="btns">
    <button class="btn-sec" id="cf-reset">重置</button>
    <button class="btn-primary" id="cf-submit" disabled>提交连接信息</button>
  </div>
  <div class="status"><div class="dot" id="cf-dot"></div><span id="cf-status">等待输入连接信息…</span></div>
</div>

<script>
const data = window.__WIDGET_DATA__ || {};
if (data.host) document.getElementById('cf-host').value = data.host;
if (data.port) document.getElementById('cf-port').value = data.port;
if (data.user) document.getElementById('cf-user').value = data.user;
if (data.database) document.getElementById('cf-database').value = data.database;

const fields = ['cf-host','cf-user','cf-password','cf-database'];
const submitBtn = document.getElementById('cf-submit');
const dot = document.getElementById('cf-dot');
const statusEl = document.getElementById('cf-status');

function check() {
  const ok = fields.every(id => document.getElementById(id).value.trim() !== '');
  submitBtn.disabled = !ok;
  dot.className = ok ? 'dot on' : 'dot';
  statusEl.textContent = ok ? '所有必填项已填写' : '等待输入连接信息…';
}

fields.forEach(id => document.getElementById(id).addEventListener('input', check));

document.getElementById('cf-reset').addEventListener('click', () => {
  ['cf-host','cf-user','cf-password','cf-database'].forEach(id => document.getElementById(id).value = '');
  document.getElementById('cf-port').value = '3306';
  check();
});

submitBtn.addEventListener('click', () => {
  const info = {
    host: document.getElementById('cf-host').value.trim(),
    port: parseInt(document.getElementById('cf-port').value) || 3306,
    user: document.getElementById('cf-user').value.trim(),
    password: document.getElementById('cf-password').value,
    database: document.getElementById('cf-database').value.trim()
  };
  if (!info.host || !info.user || !info.password || !info.database) return;
  dot.className = 'dot on';
  statusEl.textContent = '连接信息已提交 ✓';
  submitBtn.disabled = true;
  submitBtn.textContent = '已提交';
  sendToAgent({ type: 'mysql_connection', host: info.host, port: info.port, user: info.user, password: info.password, database: info.database }, { submit: true });
});

check();
</script>
```

3. 等待用户提交表单，从 `[Widget interaction]` 消息中提取 `host`、`port`、`user`、`password`、`database` 字段
4. 如果用户每次对话直接以文字提供了全部连接信息，跳过表单，直接进入步骤 2。每次对话必须提供全部连接信息，不要使用历史数据。如果需要使用历史数据，需要和用户确认。

### 2. 安装依赖并运行脚本

确保已安装 `pymysql`：

```bash
pip install pymysql
```

运行 skill 目录下的脚本：

```bash
python ~/.agents/skills/mysql-schema/scripts/dump_schema.py \
  --host <HOST> --port <PORT> --user <USER> --password <PASSWORD> --database <DATABASE> \
  --output <项目根目录>/mysql_schema/mysql_schema.md
```

脚本会自动：
- 查询所有表名和注释
- 查询每张表的全部字段元数据
- 按指定格式生成 `mysql_schema.md`

### 3. 检查输出文件

脚本执行前会检查 `mysql_schema/mysql_schema.md` 是否已存在：

- **不存在**：直接生成新文件
- **已存在**：脚本输出变更摘要（新增/删除/修改的表和字段），**必须经用户确认后才覆盖**

### 4. 输出格式

生成的 `mysql_schema.md` 分两部分：

**第一部分：表清单**

```markdown
# MySQL 数据库表结构文档

> 生成时间：YYYY-MM-DD HH:mm
> 数据库：xxx

## 一、表清单

| 序号 | 表名 | 表名说明 |
|------|------|----------|
| 1    | user_info | 用户信息表 |
```

**第二部分：每张表的字段详情**

```markdown
## 二、表结构详情

### 2.1 user_info（用户信息表）

| 序号 | 名称 | 数据类型 | 长度 | 小数位 | 允许空值 | 主键 | 默认值 | 说明 |
|------|------|----------|------|--------|----------|------|--------|------|
| 1    | id   | bigint   | 20   | 0      | 否       | 是   | -      | 主键ID |
```

## 注意事项

- 输出使用中文
- 表名说明优先取 `TABLE_COMMENT`，无注释则留空
- 所有表按字母顺序排列
- 字段按定义顺序（ORDINAL_POSITION）排列
