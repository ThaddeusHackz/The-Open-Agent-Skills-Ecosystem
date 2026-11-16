---
name: generate-domain-code
description: "Generate Busyming microservice boilerplate code (Entity, Mapper, Mapper XML, Service, Convert) from SQL CREATE TABLE statements. Use when the user provides SQL DDL, asks to create a new domain/table, or needs to scaffold backend code for a new entity."
---

# Generate Domain Code from SQL

从 SQL 建表语句自动生成 Busyming 微服务项目的全套基础代码。

## 输入

用户提供 SQL `CREATE TABLE` 语句（符合公司建表规范）。

## 变量推断

从项目 POM 和 SQL 推断以下变量：

| 变量 | 来源 | 示例 |
|------|------|------|
| `BASE_PACKAGE` | 项目 base package | `io.busyming.basic.mcp.market` |
| `DOMAIN_MODULE` | domain 模块路径 | `busyming-mcp-market-domain` |
| `SERVICE_MODULE` | service 模块路径 | `busyming-mcp-market-service` |
| `API_MODULE` | api 模块路径 | `busyming-mcp-market-api` |
| `{TableName}` | SQL 表名去掉 `t_` 前缀，转 PascalCase | `t_mcp_service` → `McpService` |
| `{tableName}` | 类名首字母小写 | `mcpService` |
| `{table_name}` | SQL 原始表名 | `t_mcp_service` |
| `{domain}` | 业务域名称小写 | `mcp` |

## 生成文件清单

按以下顺序逐一生成：

```
Task Progress:
- [ ] 1. Entity 类（domain 模块）
- [ ] 2. Mapper 接口（domain 模块）
- [ ] 3. Mapper XML（domain 模块 resources）
- [ ] 4. Convert 转换器（service 模块）
- [ ] 5. ReadService 接口（service 模块）
- [ ] 6. ReadServiceImpl 实现（service 模块）
- [ ] 7. WriteService 接口（service 模块）
- [ ] 8. WriteServiceImpl 实现（service 模块）
- [ ] 9. 编译验证
```

## Step 1: Entity 类

路径：`{DOMAIN_MODULE}/src/main/java/{BASE_PACKAGE}/domain/entity/{TableName}.java`

### SQL 类型 → Java 类型映射

| SQL 类型 | Java 类型 |
|----------|-----------|
| `bigint unsigned` | `Long` |
| `int` / `int unsigned` | `Integer` |
| `tinyint unsigned` | `Integer` |
| `varchar` | `String` |
| `text` | `String` |
| `datetime` | `java.util.Date` |
| `decimal` | `java.math.BigDecimal` |

### BaseModel 已包含的字段（不需要在子类中声明）

`io.busyming.framework.starter.mybatisplus.model.BaseModel<T>` 已包含：

| 字段 | Java 类型 | SQL 列 |
|------|-----------|--------|
| `id` | `T`（泛型） | `id` |
| `createdBy` | `Long` | `created_by` |
| `updatedBy` | `Long` | `updated_by` |
| `createdAt` | `Date` | `created_at` |
| `updatedAt` | `Date` | `updated_at` |
| `isDeleted` | `Boolean` | `is_delete` |

### 模板

```java
package {BASE_PACKAGE}.domain.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import io.busyming.framework.starter.mybatisplus.model.BaseModel;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * {中文表注释}实体
 */
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("{table_name}")
public class {TableName} extends BaseModel<Long> {

    // 只声明业务字段，BaseModel 中的字段不重复声明
    // SQL 列名 snake_case → Java 字段 camelCase
    // 不需要 @TableField，MyBatis-Plus 自动映射
    // 跳过 id、is_delete、created_by、updated_by、created_at、updated_at

    private String name;
    // ... 其他业务字段
}
```

## Step 2: Mapper 接口

路径：`{DOMAIN_MODULE}/src/main/java/{BASE_PACKAGE}/domain/mapper/{TableName}Mapper.java`

```java
package {BASE_PACKAGE}.domain.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import {BASE_PACKAGE}.domain.entity.{TableName};
import org.apache.ibatis.annotations.Mapper;

/**
 * {TableName} Mapper接口
 */
@Mapper
public interface {TableName}Mapper extends BaseMapper<{TableName}> {
}
```

## Step 3: Mapper XML

路径：`{DOMAIN_MODULE}/src/main/resources/mapper/{table_name_underscore}.xml`

文件名用表名去掉 `t_` 前缀，保持 snake_case：`t_mcp_service` → `mcp_service.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="{BASE_PACKAGE}.domain.mapper.{TableName}Mapper">
</mapper>
```

## Step 4: Convert 转换器

路径：`{SERVICE_MODULE}/src/main/java/{BASE_PACKAGE}/convert/{TableName}Convert.java`

```java
package {BASE_PACKAGE}.convert;

import {BASE_PACKAGE}.api.request.write.Create{Domain}Request;
import {BASE_PACKAGE}.api.request.write.Update{Domain}Request;
import {BASE_PACKAGE}.api.response.read.Query{Domain}DetailResponse;
import {BASE_PACKAGE}.api.response.read.Query{Domain}ListResponse;
import {BASE_PACKAGE}.domain.entity.{TableName};
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.Mappings;
import org.mapstruct.NullValuePropertyMappingStrategy;

@Mapper(
    componentModel = "spring",
    nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE
)
public interface {TableName}Convert {

    {TableName} request2do(Create{Domain}Request request);

    @Mappings({
        @Mapping(target = "isDeleted", ignore = true),
        @Mapping(target = "createdAt", ignore = true),
        @Mapping(target = "updatedAt", ignore = true),
        @Mapping(target = "createdBy", ignore = true),
        @Mapping(target = "updatedBy", ignore = true)
    })
    {TableName} updateRequest2do(Update{Domain}Request request);

    Query{Domain}ListResponse do2Queryresponse({TableName} entity);

    Query{Domain}DetailResponse do2QueryDetailResponse({TableName} entity);
}
```

## Step 5-6: ReadService 接口 + 实现

**接口路径**：`{SERVICE_MODULE}/src/main/java/{BASE_PACKAGE}/service/read/{Domain}ReadService.java`

```java
package {BASE_PACKAGE}.service.read;

import java.util.List;

/**
 * {Domain}读Service接口
 */
public interface {Domain}ReadService {

    List<Query{Domain}ListResponse> list{Domain}();

    Query{Domain}DetailResponse queryById(Query{Domain}ByIdRequest request);
}
```

**实现路径**：`{SERVICE_MODULE}/src/main/java/{BASE_PACKAGE}/service/read/impl/{Domain}ReadServiceImpl.java`

```java
package {BASE_PACKAGE}.service.read.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.List;

@Service
@Slf4j
public class {Domain}ReadServiceImpl implements {Domain}ReadService {

    private final {TableName}Mapper {tableName}Mapper;
    private final {TableName}Convert {tableName}Convert;

    // 构造函数注入

    @Override
    public List<Query{Domain}ListResponse> list{Domain}() {
        List<{TableName}> list = {tableName}Mapper.selectList(
            new LambdaQueryWrapper<{TableName}>().orderByDesc({TableName}::getUpdatedAt));
        List<Query{Domain}ListResponse> result = new ArrayList<>();
        for ({TableName} entity : list) {
            Query{Domain}ListResponse response = {tableName}Convert.do2Queryresponse(entity);
            response.setUpdateTime(entity.getUpdatedAt());
            result.add(response);
        }
        return result;
    }

    @Override
    public Query{Domain}DetailResponse queryById(Query{Domain}ByIdRequest request) {
        {TableName} entity = {tableName}Mapper.selectById(request.getId());
        if (entity == null) {
            throw new BusinessException("模块名", ErrorCode.{DOMAIN}_NOT_EXIST, request);
        }
        Query{Domain}DetailResponse response = {tableName}Convert.do2QueryDetailResponse(entity);
        response.setUpdateTime(entity.getUpdatedAt());
        return response;
    }
}
```

## Step 7-8: WriteService 接口 + 实现

**接口路径**：`{SERVICE_MODULE}/src/main/java/{BASE_PACKAGE}/service/write/{Domain}WriteService.java`

```java
package {BASE_PACKAGE}.service.write;

/**
 * {Domain}写Service接口
 */
public interface {Domain}WriteService {

    {Domain}CreateResponse create{Domain}(Create{Domain}Request request);

    void update{Domain}(Update{Domain}Request request);
}
```

**实现路径**：`{SERVICE_MODULE}/src/main/java/{BASE_PACKAGE}/service/write/impl/{Domain}WriteServiceImpl.java`

```java
package {BASE_PACKAGE}.service.write.impl;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Slf4j
public class {Domain}WriteServiceImpl implements {Domain}WriteService {

    private final {TableName}Mapper {tableName}Mapper;
    private final {TableName}Convert {tableName}Convert;

    // 构造函数注入

    @Override
    @Transactional(rollbackFor = Throwable.class)
    public {Domain}CreateResponse create{Domain}(Create{Domain}Request request) {
        {TableName} entity = {tableName}Convert.request2do(request);
        {tableName}Mapper.insert(entity);
        log.info("{domain}.create.success,id:{}", entity.getId());
        {Domain}CreateResponse response = new {Domain}CreateResponse();
        response.setId(entity.getId());
        return response;
    }

    @Override
    @Transactional(rollbackFor = Throwable.class)
    public void update{Domain}(Update{Domain}Request request) {
        {TableName} existing = {tableName}Mapper.selectById(request.getId());
        if (existing == null) {
            throw new BusinessException("模块名", ErrorCode.{DOMAIN}_NOT_EXIST, request);
        }
        {TableName} entity = {tableName}Convert.updateRequest2do(request);
        {tableName}Mapper.updateById(entity);
        log.info("{domain}.update.success,id:{}", request.getId());
    }
}
```

## Step 9: 编译验证

```bash
cd 项目根目录
JAVA_HOME=JDK8路径 mvn compile -q
```

确认无编译错误。

## 关键规则

1. **Entity 继承 BaseModel**：所有 Entity 必须 `extends BaseModel<Long>`，不要重复声明 `id`、`isDeleted`、`createdBy`、`updatedBy`、`createdAt`、`updatedAt`
2. **is_delete 字段**：由 BaseModel 提供，Java 类型 `Boolean`，SQL 列名 `is_delete`
3. **不需要 @TableField**：MyBatis-Plus 自动 camelCase → snake_case 映射
4. **构造函数注入**：禁止 `@Autowired`/`@Resource` 字段注入
5. **updateTime 手动赋值**：Response 的 `updateTime` 与 Entity 的 `updatedAt` 名称不同，MapStruct 无法自动映射，需 `response.setUpdateTime(entity.getUpdatedAt())`
6. **写操作加事务**：`@Transactional(rollbackFor = Throwable.class)`
7. **查不到抛异常**：`throw new BusinessException("模块名", ErrorCode, request)`
