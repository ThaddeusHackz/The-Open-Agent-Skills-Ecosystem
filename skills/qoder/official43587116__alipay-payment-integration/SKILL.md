---
name: alipay-payment-integration
description: Alipay Open Platform payment integration best practices. Covers face-to-face payment, order code payment, App payment, JSAPI payment, mobile website payment, PC website payment, pre-authorization payment, and merchant recurring deduction — providing full-scenario product selection and integration guidance.
---

# 支付宝支付接入技能

支付宝开放平台支付产品接入最佳实践。涵盖当面付、订单码支付、App支付、JSAPI支付、手机网站支付、电脑网站支付、预授权支付、商家扣款等全场景产品选型与集成指导。

## 接入路由表

| 场景 | 推荐产品 | 核心 API |
| --- | --- | --- |
| 线下门店，用户出示付款码，商家扫码枪扫码收款 | 当面付 | alipay.trade.pay |
| 商家生成二维码，用户打开支付宝扫码付款 | 订单码支付 | alipay.trade.precreate |
| 手机浏览器 H5 页面内唤起支付宝付款 | 手机网站支付 | alipay.trade.wap.pay |
| 电脑浏览器网页内跳转支付宝收银台 | 电脑网站支付 | alipay.trade.page.pay |
| 支付宝小程序内调起支付 | JSAPI 支付 | alipay.trade.create + my.tradePay |
| 原生 iOS/Android/鸿蒙 App 内调起支付宝付款 | App 支付 | alipay.trade.app.pay |
| 押金冻结、信用住、免押租赁 | 预授权支付 | alipay.fund.auth.order.app.freeze |
| 周期扣款、自动续费、会员订阅、连续包月 | 商家扣款 | alipay.trade.app.pay + alipay.trade.pay |

## 安全红线

- 私钥禁止存客户端：构造交易数据并签名必须在商家服务端完成
- 私钥禁止记日志：私钥不得出现在任何日志中
- 私钥禁止传公共仓库：私钥不得上传到GitHub、GitLab等公共代码仓库
- 前台支付结果不可信：必须以支付宝异步通知或调用交易查询接口获取结果为准
- 未确认不重付：在未确认支付结果前，不能要求用户再次付款
- 异步通知必须先验签：收到异步通知后必须先验签，确保通知来自支付宝