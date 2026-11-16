---
name: apaas-local-dev-workflow
description: Develop APAAS low-code app pages locally with React/TypeScript/Ant Design, then copy code into the APAAS platform. Use when building new APAAS pages, refactoring existing ones, or migrating local code to APAAS.
---

# APAAS 本地开发工作流

## 何时使用

- 在本地为 APAAS 平台开发新页面/组件
- 改造已有 APAAS 页面（UI、权限、统计口径等）
- 把本地代码复制到 APAAS 平台运行验证

## 项目结构

APAAS 平台的文件结构是**固定的**，只有 `components/` 下的文件名随项目变化，其余文件名固定不变：

```
.
├── components/          # 项目级组件（文件名随项目变化，如 DemandPoolTable.tsx）
├── models/
│   └── index.ts         # 固定文件名
├── pages/
│   └── index.tsx        # 固定文件名
├── services/
│   └── data.ts          # 固定文件名
├── docs/                # PRD、字段说明等（按需，不参与 APAAS 部署）
├── package.json         # 固定文件名（从 APAAS 平台复制）
└── tsconfig.json        # 固定文件名（从 APAAS 平台复制）
```

**初始化新项目时**：先创建上述固定文件（内容为空），由用户从 APAAS 平台复制内容填入，再按需新建 `components/` 下的项目组件文件。

## 技术栈约定

- React 18 + TypeScript
- Ant Design 5
- Tailwind CSS
- dayjs
- Zustand
- `@byted-apaas/client-sdk/page`（页面上下文）
- `@byted-apaas/client-sdk/data`（searchRecords / getRecord）

## 开发流程

1. **本地编写**
   - 页面入口固定写 `pages/index.tsx`
   - 数据查询固定写 `services/data.ts`
   - 状态管理固定写 `models/index.ts`
   - 项目专属组件写 `components/<项目组件名>.tsx`（文件名随项目变化）

2. **组件模板**

   ```tsx
   import React from 'react';
   import { ConfigProvider, Card } from 'antd';
   import { theme } from 'apaas-antd-theme';
   import { useGlobalContext } from '@byted-apaas/client-sdk/page';

   const Page: React.FC = () => {
     const globalContext = useGlobalContext();
     const currentUser = globalContext?.currentUser;
     return (
       <ConfigProvider theme={theme}>
         <div className="p-6 bg-gray-100 min-h-screen">
           <Card>...</Card>
         </div>
       </ConfigProvider>
     );
   };

   export default Page;
   ```

3. **数据服务模板**

   ```ts
   import { searchRecords } from '@byted-apaas/client-sdk/data';
   import { message } from 'antd';
   import dayjs from 'dayjs';

   export const getXxxList = async (filters?: any) => {
     const res = await searchRecords({
       objectApiName: 'object_api_name',
       pageSize: 200,
       filter: filters,
     });
     return res?.items || [];
   };
   ```

4. **模型模板**

   ```ts
   import { create } from 'zustand';

   interface State {
     list: any[];
     loading: boolean;
     fetchList: () => Promise<void>;
   }

   export const useXxxStore = create<State>((set) => ({
     list: [],
     loading: false,
     fetchList: async () => {
       set({ loading: true });
       // ...
       set({ list: data, loading: false });
     },
   }));
   ```

5. **复制到 APAAS**
   - 将 `pages/index.tsx`、`services/data.ts`、`models/index.ts`、`components/<组件名>.tsx` 内容粘贴到 APAAS 平台对应文件
   - 保持相对 import 路径一致
   - 在 APAAS 平台保存并预览

## 常见注意点

- **本地没有 node_modules**：VSCode/TS 会报模块找不到，这是正常的，不影响 APAAS 平台运行。不要花时间修这些报错。
- **权限过滤**：普通用户用 `currentUser.id` 过滤；`role_system` 用户可跳过过滤。
- **MonthPicker 双边界**：同时限制最小月份和最大月份时，用 `isBefore` + `isAfter`，并注意默认月份可能不在可选范围内。
- **树形表格**：用 AntD Table 的 `children` 树形数据，不要用 `expandedRowRender` 嵌套子表格。
- **IN 查询空数组**：APAAS 平台拒绝空数组 `IN` 条件，数组过滤前要先 `filter(Boolean)` 并判空。
- **日期字段**：APAAS 存储的是时间戳，查询 `_createdAt` 等字段时传 `dayjs(...).valueOf()`。

## 验证清单

- [ ] 页面在 APAAS 平台预览正常
- [ ] 数据查询返回预期条数
- [ ] 权限过滤符合预期（普通用户 / 系统管理员）
- [ ] 无新增 TypeScript 真实错误（忽略缺 node_modules 的报错）
- [ ] UI 在目标屏幕尺寸下正常
