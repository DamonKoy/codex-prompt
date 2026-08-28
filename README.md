# Prompt Refiner for Codex

一个本地优先的 Codex 插件：把口语化任务或草稿提示词改写为可直接发送的 Codex 提示词。

它只生成文本，不执行原始任务；不包含 MCP 服务、Hook、网络请求、遥测或文件读写逻辑。

## 使用方式

在 Codex 的新任务中输入：

```text
$prompt-refiner 把下面的需求整理为可执行的 Codex 提示词：
为订单导出增加 CSV 下载，并覆盖异常与权限场景。
```

插件会返回一个可复制的提示词。检查内容后，把它作为下一条消息发送给 Codex。

## 设计原则

- 保留用户已经明确的目标、事实、范围与授权边界。
- 缺失信息只有在会实质影响结果或副作用时才提出一个澄清问题。
- 不制造路径、数据、权限、验收结果或外部授权。
- 对代码任务强调先读后写、最小改动和项目既有验证流程。
- 不要求暴露思维链，也不堆叠无关角色和工具指令。

## 本地测试安装

在该仓库根目录执行：

```bash
codex plugin marketplace add .
codex plugin add prompt-refiner@prompt-refiner
```

然后新开一个 Codex 任务，使用 `$prompt-refiner` 调用。更新插件后重新安装，并在新任务中验证。

插件提供 `composerIcon` 元数据，Codex 可以在支持的界面呈现其入口；具体显示位置与排序由 Codex 宿主控制，插件不能指定固定插入到语音与模型控件之间。

安装前或提交前可运行离线结构校验：

```bash
python3 scripts/validate.py
```

## 入口说明

- 主入口：在 Codex 输入框输入 `$prompt-refiner`，或从 `@` / Skills 选择器调用。
- `composerIcon`：官方插件元数据，宿主若支持会在输入区显示插件图标；**不能**指定插入到“语音按钮”与“模型选择器”之间的固定槽位。
- 不做客户端注入、Accessibility 自动点击或 App 二进制补丁；这些会破坏升级安全。

## 发布给其他用户

将仓库推送到 GitHub 后，其他用户可执行：

```bash
codex plugin marketplace add DamonKoy/codex-prompt
codex plugin add prompt-refiner@prompt-refiner
```

每次发布请同步更新 `CHANGELOG.md` 并递增 `plugins/prompt-refiner/.codex-plugin/plugin.json` 中的版本号。

## 开源许可

本项目采用 [MIT License](LICENSE)。
