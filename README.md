# 🛠️ Project Tools

这里存放了项目开发过程中常用的辅助脚本工具，旨在提高开发效率和简化重复性操作。

## 📂 脚本列表

| 脚本文件 | 功能简介 | 典型用途 |
| :--- | :--- | :--- |
| [📄 copy_frontend.py](copy_frontend.py) | **前端资源拷贝工具**<br>将指定目录下的前端资源（忽略 `node_modules`）拷贝并合并到目标目录，带进度条显示。 | 用于将构建好的前端资源发布到指定位置，或在不同项目间同步代码。 |
| [📄 delete_dirs.py](delete_dirs.py) | **批量目录删除工具**<br>递归查找并删除指定名称的目录（默认 `node_modules`），支持处理 Windows 权限问题。 | 快速清理项目中所有的 `node_modules` 依赖，以便重新安装或释放磁盘空间。 |

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

---
> **提示**：建议在运行脚本前备份重要数据，虽然脚本已包含基本的错误处理，但数据安全始终是第一位的。
