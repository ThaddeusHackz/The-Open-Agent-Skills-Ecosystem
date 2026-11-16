---
name: dameng-db-compatibility
description: "编写或维护同时支持 MySQL 与达梦数据库（DM8）的 Java/MyBatis 代码时使用。覆盖 Mapper XML 方言映射（FIND_IN_SET、GROUP_CONCAT、LIMIT/ROWNUM、IF/CASE WHEN）、`<choose>`+`_databaseId` 分支写法、避免 Statement ID 冲突、JDBC 跨驱动兼容（禁止硬编码 MySQL JDBC 类，使用反射调用 enableStreamingResults）、DriverDatabaseIdProvider 配置与启动排查、spring.factories 自动注册。触发场景：新增/修改 SQL 涉及 MySQL 特有语法、出现 `Mapped Statements collection already contains value` 报错、出现 `ClassCastException: DmdbPreparedStatement cannot be cast to JdbcPreparedStatement`、`_databaseId` 条件分支不生效、达梦驱动兼容、`bootstrap.yml`/`spring.factories` 中 DatabaseIdProvider 配置缺失或路径错误。"
version: 1.0.1
---

# 达梦数据库兼容开发规范（MyBatis + JDBC）

## 1. 项目双数据库架构

- 模块结构：`qsdi-system-api`（接口/实体）+ `qsdi-system-service`（服务/Mapper）。
- 双驱动共存：`mysql-connector-java` + `Dm8JdbcDriver18`（`pom.xml` 中仅保留 `com.dameng:Dm8JdbcDriver18`，删除重复的 `com.dm:DmJdbcDriver18`）。
- 驱动识别：通过公共 `com.qsdi.common.core.config.DatabaseIdProviderConfig`（位于 `common-core` 公共依赖，**非 `com.qsdi.common.mybatis.config`**）注册 MyBatis `VendorDatabaseIdProvider`，将驱动名归一化为 `_databaseId`：
  - MySQL → `mysql`
  - 达梦 → `dm`

## 2. Mapper XML 方言分支（核心模式）

**必须**采用「单语句 + `<choose>` 分支」模式，**严禁**复制整条语句分别加 `databaseId="dm"` 与默认 `databaseId` 属性，否则 MyBatis 启动会报 `Mapped Statements collection already contains value for xxx`。

```xml
<select id="getChilidByParentId" parameterType="integer" resultType="...SysOrgEntity">
    SELECT rd.*
    FROM sys_org rd
    WHERE
        <choose>
            <when test="_databaseId == 'dm'">
                CONCAT(',', parent_ids, ',') LIKE CONCAT('%,', #{parantId}, ',%')
            </when>
            <otherwise>
                FIND_IN_SET(#{parantId}, parent_ids) > 0
            </otherwise>
        </choose>
      and rd.status = 2
    UNION
    SELECT *
    FROM sys_org
    WHERE id = #{parantId}
      and status = 2
</select>
```

- 简短分支可压缩为单行：` <choose><when test="_databaseId == 'dm'">WM_CONCAT(...)</when><otherwise>GROUP_CONCAT(...)</otherwise></choose>`
- 表达式内分支可使用 `<if test="_databaseId == 'dm'">...</if>` + `<if test="_databaseId == 'mysql' or _databaseId == null">...</if>`，但必须保证两者互斥且至少一条命中。

## 3. 常用 SQL 方言映射

| MySQL 写法 | 达梦（DM8）兼容写法 | 备注 |
|---|---|---|
| `FIND_IN_SET(#{id}, parent_ids) > 0` | `CONCAT(',', parent_ids, ',') LIKE CONCAT('%,', #{id}, ',%')` | 两端补逗号避免子串误匹配（如 `'1'` 误中 `'12'`） |
| `IF(cond, a, b)` | `CASE WHEN cond THEN a ELSE b END` | 用于 SELECT 列表或递归 CTE 标记列 |
| `GROUP_CONCAT(col)` | `WM_CONCAT(col)` | 达梦默认分隔符为 `,` |
| `LIMIT n` / `LIMIT offset, n` | `WHERE rn = n` 包外层子查询 + `ROW_NUMBER() OVER (ORDER BY ...)` 或 `ROWNUM` | 见 §3.1 |
| `LIMIT 1` 简化写法 | `select * from (select t.*, rownum rn from ${table} t where ...) where rn = 1` | |
| `LIMIT 1` 等价取首行 | `SELECT ... FROM (... ORDER BY col) WHERE rn = 1` 套 `ROW_NUMBER()` | |
| `@pids := ...` 用户变量递归 | `CASE WHEN ... THEN @pids := CONCAT(...) END` 表达式 | 配合 FIND_IN_SET→CONCAT/LIKE 替换 |

### 3.1 分页/取首行的达梦标准写法

```xml
<choose>
    <when test="_databaseId == 'dm'">
        SELECT relation_id FROM (
            SELECT relation_id, ROW_NUMBER() OVER (ORDER BY relation_id) rn
            FROM icbd_device_relation
            <where>
                <if test="deviceIdList != null and deviceIdList.size > 0">
                    device_id IN
                    <foreach collection="deviceIdList" item="item" open="(" close=")" separator=",">
                        #{item}
                    </foreach>
                </if>
            </where>
        ) WHERE rn = 1
    </when>
    <otherwise>
        SELECT relation_id FROM icbd_device_relation
        <where>...</where>
        LIMIT 1
    </otherwise>
</choose>
```

## 4. JDBC 跨驱动兼容

达梦 MySQL 后若直接 unwrap 到 `com.mysql.cj.jdbc.JdbcPreparedStatement` 会在启动期或首调时抛：
`java.lang.ClassCastException: Cannot cast dm.jdbc.driver.DmdbPreparedStatement to com.mysql.cj.jdbc.JdbcPreparedStatement`

### 4.1 强制规则

- 局部变量一律使用标准 `java.sql.PreparedStatement` / `Connection` / `ResultSet`，**严禁** `import com.mysql.cj.jdbc.JdbcPreparedStatement;`。
- **严禁** 直接调用 `ps.unwrap(com.mysql.cj.jdbc.JdbcPreparedStatement.class)` 或 `enableStreamingResults()`。
- 必须通过 `conn.getMetaData().getDriverName()` 判断驱动（含 `mysql` 视为 MySQL）。

### 4.2 标准实现（流式读取示例）

参考 `qsdi-system-service/src/main/java/com/qsdi/device/service/holder/core/StreamDBLoader.java`：

```java
public void load(String sql, ResultSetHandler handler) {
    try (SqlSession session = factory.openSession()) {
        Connection conn = session.getConnection();
        PreparedStatement ps = conn.prepareStatement(sql,
                ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY);
        if (isMysqlConnection(conn)) {
            invokeEnableStreamingResults(ps);
        }
        ps.executeQuery();
        handler.handle(ps.getResultSet());
    }
}

private boolean isMysqlConnection(Connection conn) throws SQLException {
    String name = conn.getMetaData().getDriverName();
    return name != null && name.toLowerCase().contains("mysql");
}

private void invokeEnableStreamingResults(PreparedStatement ps) {
    try {
        Method m = ps.getClass().getMethod("enableStreamingResults");
        m.invoke(ps);
    } catch (NoSuchMethodException ignored) {
        // 非 MySQL 或驱动未提供，降级为标准读取
    } catch (ReflectiveOperationException e) {
        log.warn("启用MySQL流式读取失败，降级为标准读取: {}", e.getMessage());
    }
}
```

### 4.3 反射调用模板

凡涉及 MySQL/达梦驱动私有 API（`enableStreamingResults`、`useLocalSessionState` 等）一律走反射 + 异常降级。

## 5. DatabaseIdProvider 配置

### 5.1 公共注册类位置

类路径：**`com.qsdi.common.core.config.DatabaseIdProviderConfig`**（位于 `common-core` 公共模块，**非 `com.qsdi.common.mybatis.config`**）。

### 5.2 spring.factories 注册（qsdi-system-api）

`qsdi-system-api/src/main/resources/META-INF/spring.factories`：

```
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
com.qsdi.common.core.config.DatabaseIdProviderConfig
```

### 5.3 bootstrap.yml 启用

```yaml
mybatis-plus:
  configuration:
    database-id-provider: com.baomidou.mybatisplus.extension.plugins.inner.VendorDatabaseIdProvider
```

## 6. 调试排查速查

| 现象 | 根因 | 修复 |
|---|---|---|
| `Mapped Statements collection already contains value for xxx` | 同 namespace 下两个相同 id 的 statement（即使 databaseId 不同） | 改为单 id + `<choose>` 分支 |
| `_databaseId == 'dm'` 条件永不命中（MySQL 分支执行） | `DatabaseIdProviderConfig` 未注册或路径错 | 修正 `spring.factories` 中的全限定名为 `com.qsdi.common.core.config.DatabaseIdProviderConfig` |
| `Unable to read meta-data for class com.qsdi.common.mybatis.config.DatabaseIdProviderConfig` | 类实际在 `common.core` 而非 `common.mybatis` | 改正路径或从 `spring.factories` 中移除 |
| 启动期 `ClassCastException: DmdbPreparedStatement cannot be cast to JdbcPreparedStatement` | JDBC 代码 unwrap MySQL 类 | 改为反射调用 + 驱动名判断 |
| 达梦环境 `FIND_IN_SET` 函数不存在 | 使用了 MySQL 私有函数 | 替换为 `CONCAT + LIKE` |

## 7. 自检清单

提交 Mapper XML / JDBC 兼容代码前逐项核对：

- [ ] 同 namespace 下不存在重复 statement id
- [ ] 方言分支使用 `<choose>` + `<when test="_databaseId == 'dm'">` + `<otherwise>` 或互斥 `<if>`
- [ ] `FIND_IN_SET` 已替换为 `CONCAT(',', x, ',') LIKE CONCAT('%,', #{id}, ',%')`
- [ ] `LIMIT` 已通过 `<choose>` 提供达梦分支（`ROWNUM` 或 `ROW_NUMBER()`）
- [ ] `GROUP_CONCAT` 在达梦分支使用 `WM_CONCAT`
- [ ] `IF(...)` 在达梦分支使用 `CASE WHEN ... END`
- [ ] Java 代码无 `import com.mysql.cj.jdbc.*`
- [ ] Java 代码无 `unwrap(JdbcPreparedStatement.class)` / `enableStreamingResults()` 直调
- [ ] 跨驱动私有方法均通过 `Method m = ps.getClass().getMethod(...)` 反射调用并捕获 `NoSuchMethodException`
- [ ] 本地 Maven 仓库（`E:\maven\repository`）已下载 `common-core` 与 `Dm8JdbcDriver18`

## 8. 参考资料

- 详细方言映射、配置示例：[reference.md](reference.md)
- 本项目实际兼容代码片段：[examples.md](examples.md)