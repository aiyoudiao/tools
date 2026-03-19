# 🛠️ Project Tools

这里存放了项目开发过程中常用的辅助脚本工具，旨在提高开发效率和简化重复性操作。

## 📂 脚本列表

| 脚本文件 | 功能简介 | 典型用途 |
| :--- | :--- | :--- |
| [📄 copy_frontend.py](copy_frontend.py) | **前端资源拷贝工具**<br>将指定目录下的前端资源（忽略 `node_modules`）拷贝并合并到目标目录，带进度条显示。 | 用于将构建好的前端资源发布到指定位置，或在不同项目间同步代码。 |
| [📄 delete_dirs.py](delete_dirs.py) | **批量目录删除工具**<br>递归查找并删除指定名称的目录（默认 `node_modules`），支持处理 Windows 权限问题。 | 快速清理项目中所有的 `node_modules` 依赖，以便重新安装或释放磁盘空间。 |
| [📄 use_local_ollama.py](use_local_ollama.py) | **本地 Ollama 模型查询工具**<br>通过 HTTP API 调用本地 Ollama 服务，支持一次性输出和流式输出两种模式。 | 快速测试本地 Ollama 模型，或集成到其他脚本中进行 AI 辅助开发。 |
| [📄 encrypt_compress.py](encrypt_compress.py) | **加密压缩工具**<br>将文件或文件夹压缩为 tar.gz 格式并使用密码加密，生成 .enc 文件。 | 安全地备份和传输敏感数据，保护文件内容不被未授权访问。 |
| [📄 decrypt_decompress.py](decrypt_decompress.py) | **解密解压工具**<br>使用密码解密 .enc 文件并解压到指定目录。 | 恢复之前加密压缩的文件或文件夹，需要正确的密码才能解密。 |

## 🚀 使用说明

### 1. copy_frontend.py
**功能**：智能拷贝目录，自动忽略 `node_modules` 和 `.git`，支持增量合并。

```bash
# 基本用法
python copy_frontend.py "源目录路径" "目标目录路径"

# 示例
python copy_frontend.py "c:\MyWork\project\frontend" "c:\Deploy\frontend"
```

### 2. delete_dirs.py
**功能**：深度清理指定目录，彻底解决 Windows 下 `node_modules` 删除慢或权限报错的问题。

```bash
# 删除当前目录下所有的 node_modules
python delete_dirs.py .

# 删除指定目录下的所有 dist 文件夹
python delete_dirs.py "c:\MyWork\project" --target dist
```

### 3. use_local_ollama.py
**功能**：调用本地 Ollama 服务进行 AI 模型推理，支持一次性输出和流式输出两种模式。

```python
# 一次性输出示例
from use_local_ollama import query_ollama
response = query_ollama("帮我写一个二分查找法", model="qwen3.5:0.8b")
print(response)

# 流式输出示例
from use_local_ollama import query_ollama_stream
for chunk in query_ollama_stream("帮我写一个二分查找法", model="qwen3.5:0.8b"):
    print(chunk, end="", flush=True)
```

**前置条件**：
- 需要先安装 Ollama 并启动本地服务（默认端口 11434）
- 需要安装 requests 库：`pip install requests`

### 4. encrypt_compress.py
**功能**：将文件或文件夹压缩为 tar.gz 格式并使用密码加密，生成 .enc 文件。

```bash
# 加密压缩一个文件
python encrypt_compress.py "C:\path\to\file.txt" "C:\output\encrypted.enc" "mypassword"

# 加密压缩一个文件夹
python encrypt_compress.py "C:\path\to\folder" "C:\output\encrypted.enc" "mypassword"
```

**前置条件**：
- 需要安装 cryptography 库：`pip install cryptography`

### 5. decrypt_decompress.py
**功能**：使用密码解密 .enc 文件并解压到指定目录。

```bash
# 解密解压到指定目录
python decrypt_decompress.py "C:\path\to\encrypted.enc" "C:\output\folder" "mypassword"

# 解密解压到当前目录
python decrypt_decompress.py "C:\path\to\encrypted.enc" "." "mypassword"
```

**前置条件**：
- 需要安装 cryptography 库：`pip install cryptography`

---
> **提示**：建议在运行脚本前备份重要数据，虽然脚本已包含基本的错误处理，但数据安全始终是第一位的。
