---
name: media-manager
description: "管理 Emby 媒体库，支持查询媒体客户端、媒体列表、媒体详情，以及执行播放控制动作（播放、暂停、停止、上下曲、音量调节等）"
version: 1.0.0
author: EcoreHome
---

# Media Manager - CoPaw 技能

## 📖 功能概述

此技能用于管理 Emby 媒体库，包括：
- 查询媒体客户端列表
- 按关键字、人物、媒体类型等条件查询媒体列表
- 查看指定媒体的详细信息
- 对指定媒体设备执行播放控制动作

## 🔧 配置信息

```
CLI 工具：ehctl
命令格式：ehctl media [subcommand] [flags]
后端服务：GraphQL Federation 网关（默认 localhost:4000）
```

## 💡 可用命令

### 1. 查询媒体客户端

```
ehctl media client [flags]
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--format` | 否 | 输出格式 |

**输出字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `dev_id` | string | 媒体设备 dev_id |
| `name` | string | 媒体设备名称 |

**示例：**
```bash
# 查询所有媒体客户端
ehctl media client

# JSON 格式输出
ehctl media client --format json
```

---

### 2. 查询媒体列表

```
ehctl media list [flags]
```

**参数说明：**

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--search` | 否 | - | 检索关键字（影片名称、演员、歌手等） |
| `--start-index` | 否 | `0` | 起始索引 |
| `--person-id` | 否 | - | 人物 ID |
| `--media-type` | 否 | - | 媒体类型 |
| `--format` | 否 | 自动检测 | 输出格式 |
| `--output` | 否 | 全部字段 | 指定输出字段 |

**输出字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `media_id` | string | 媒体 ID |
| `name` | string | 媒体名称 |
| `duration` | string | 媒体时长，格式 `HH:MM:SS` |
| `media_type` | string | 媒体类型 |
| `series_name` | string | 系列名称或系列/季名称 |
| `index_number` | string | 集数序号 |

**示例：**
```bash
# 查询媒体列表（自动使用第一个客户端）
ehctl media list

# 按关键字检索
ehctl media list --search "周杰伦"

# 指定媒体类型并跳过前 20 条
ehctl media list --media-type Movie --start-index 20 --format json
```

**重要说明：**
- `media list` **不需要传 `--dev-id`**，命令内部会自动查询媒体客户端列表，并使用第一个客户端发起查询
- 如果没有匹配到媒体，命令会输出 `未找到符合条件的媒体`，而不是空数组 `[]`

---

### 3. 查看媒体详情

```
ehctl media detail --dev-id <dev_id> --media-id <media_id> [flags]
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--dev-id` | 是 | 媒体设备的 dev_id |
| `--media-id` | 是 | 媒体 ID |
| `--format` | 否 | 输出格式 |
| `--output` | 否 | 指定输出字段 |

**输出字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 名称 |
| `file_name` | string | 文件名 |
| `original_title` | string | 原始标题 |
| `duration` | string | 时长 |
| `size` | string | 大小 |
| `media_type` | string | 媒体类型 |
| `series_name` | string | 系列名称 |
| `premiere_date` | string | 首播日期 |
| `date_modified` | string | 更新时间 |
| `date_created` | string | 创建时间 |
| `community_rating` | string | 社区评分 |
| `container` | string | 容器格式 |
| `forced_sort_name` | string | 强制排序名称 |
| `genre_items` | string | 类型标签 |
| `media_streams` | string | 媒体流信息 |
| `aspect_ratio` | string | 宽高比 |
| `codec` | string | 编码格式 |
| `video_range` | string | 动态范围 |
| `parent_id` | string | 父级 ID |
| `part_count` | string | 分集数量 |
| `production_year` | string | 制作年份 |
| `production_locations` | string | 制作地点 |
| `path` | string | 源文件路径 |
| `playback_position_ticks` | string | 上次播放的位置 |
| `play_count` | string | 播放次数 |
| `is_favorite` | string | 是否收藏 |
| `last_played_date` | string | 最后播放时间 |
| `played` | string | 是否播放过 |
| `people` | string | 演职人员 |
| `overview` | string | 内容简介 |

**示例：**
```bash
# 查询媒体详情
ehctl media detail --dev-id media.livingroom --media-id 12345

# 仅输出名称、时长和简介
ehctl media detail --dev-id media.livingroom --media-id 12345 --output name,duration,overview --format json
```

---

### 4. 播放控制

```
ehctl media action --dev-id <dev_id> --action <action> [flags]
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--dev-id` | 是 | 媒体设备的 dev_id |
| `--action` | 是 | 动作：`play` / `pause` / `prev` / `next` / `volumeup` / `volumedown` / `stop` |
| `--media-id` | 否 | 媒体 ID（play 时需要） |
| `--format` | 否 | 输出格式 |
| `--output` | 否 | 指定输出字段 |

**说明：**
- `stop` 会在 CLI 内部转换为 `pause` 后调用后端
- `volumeup`、`volumedown` 可不传 `--media-id`

**输出字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | string | 是否执行成功 |
| `action` | string | 请求动作 |
| `dev_id` | string | 媒体设备 dev_id |
| `media_id` | string | 媒体 ID |

**示例：**
```bash
# 播放指定媒体
ehctl media action --dev-id media.livingroom --media-id 12345 --action play

# 增加音量
ehctl media action --dev-id media.livingroom --action volumeup --format json

# 暂停播放
ehctl media action --dev-id media.livingroom --action pause

# 上一曲
ehctl media action --dev-id media.livingroom --action prev

# 下一曲
ehctl media action --dev-id media.livingroom --action next

# stop 会自动映射为 pause
ehctl media action --dev-id media.livingroom --action stop
```

---

### 5. 组合使用示例

```bash
# 查询所有媒体客户端
ehctl media client

# 查询周杰伦的歌曲（自动使用第一个客户端）
ehctl media list --search "周杰伦"

# 查看某部电影的详情
ehctl media detail --dev-id media.livingroom --media-id 12345

# 播放某部电影
ehctl media action --dev-id media.livingroom --media-id 12345 --action play

# 暂停播放
ehctl media action --dev-id media.livingroom --action pause

# 增加音量
ehctl media action --dev-id media.livingroom --action volumeup
```

---

## 📋 媒体类型

常见的媒体类型包括：
- `Movie` — 电影
- `Series` — 剧集
- `Episode` — 剧集集数
- `Audio` — 音频
- `Photo` — 照片

## ⚠️ 使用注意

1. **media list 无需传 dev_id**：`media list` 命令内部会自动查询媒体客户端列表，并使用第一个客户端发起查询，**不需要传 `--dev-id` 参数**
2. **dev_id 获取**：使用 `media detail`、`media action` 前，需先用 `media client` 获取媒体设备的 dev_id
3. **media_id 获取**：使用 `media detail`、`media action` 播放前，需先用 `media list` 获取媒体 ID
4. **未找到媒体**：`media list` 搜索无结果时输出 `未找到符合条件的媒体`，**不是空数组 `[]`**
5. **动作选择**：`stop` 会自动映射为 `pause`，无需额外处理
6. **输出格式**：程序处理时使用 `--format json`，人类查看时使用默认 table 格式

## 🛠️ 故障排查

### 连接失败
如果看到 "connection refused" 错误：
- 🔧 检查后端服务是否运行
- 🌐 测试连接：`ehctl media client --host <正确IP> --port 4000`

### 设备不存在
如果看到设备不存在的错误：
- ✅ 先用 `ehctl media client` 查询可用的媒体设备列表
- ✅ 确认使用的 dev_id 是否正确

---

## 💡 使用建议

1. 先使用 `media client` 获取所有媒体设备列表
2. 使用 `media list` 浏览媒体库或搜索特定内容（**无需传 `--dev-id`**）
3. 使用 `media detail` 查看媒体详细信息（评分、简介、编码等）
4. 使用 `media action` 进行播放控制
5. 批量操作时使用 `--format json` 便于程序处理

---

## 🚀 快速示例

### 查询媒体客户端

```bash
ehctl media client
```

### 搜索影片（自动使用第一个客户端）

```bash
ehctl media list --search "第一滴血"
```

### 查看影片详情

```bash
ehctl media detail --dev-id media.livingroom --media-id 12345
```

### 播放影片

```bash
ehctl media action --dev-id media.livingroom --media-id 12345 --action play
```

### 暂停播放

```bash
ehctl media action --dev-id media.livingroom --action pause
```
