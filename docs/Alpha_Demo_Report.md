# Alpha Demo Report

导入数量：21

成功：20

跳过重复：1

分析成功：20

分析失败：0

主要问题：

- 本机没有 Docker 和 PostgreSQL，Alpha 验收使用本地 SQLite `backend/alpha.db` 跑通。
- 本机没有 Safari / Chrome 可由命令行打开，`frontend/content-library.html` 页面文件已生成，但无法在当前环境自动打开浏览器验证。
- 当前未配置 `OPENAI_API_KEY`，AI 分析使用 Alpha 本地规则回退；真实 OpenAI 调用路径已接入。
- 为兼容本机 Python 3.9，已将运行路径中的新式类型注解改为兼容写法。

是否通过 Alpha：通过

