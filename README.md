# 发票管理系统

一个基于 PySide6 的现代化发票管理应用。

## 功能特性

- **现代化的用户界面设计**: 简洁、友好的用户界面。
- **多用户管理**: 支持添加、删除和重命名用户，发票数据按用户进行管理。
- **发票管理**: 全功能的增删改查（CRUD）操作。
- **文件缓存**: 原始发票文件（PDF、图片）将被缓存以便快速访问。
- **批量扫描**: 支持批量OCR扫描多个发票文件。
- **OCR 集成**: 使用 OCR 服务从发票中提取数据。
- **PDF 文本提取**: 直接从 PDF 文件中提取文本。
- **交互式表格**: 使用现代化表格展示发票，支持排序和状态指示。
- **动态按钮**: 操作按钮会根据当前选择智能启用或禁用。
- **侧边栏导航**: 现代化的可伸缩侧边栏，用于用户选择。
- **数据持久化**: 发票数据以 `invoices.json` 格式保存在本地。

## 安装与运行

### 方法一：使用启动脚本（推荐）
```bash
./run.sh
```

### 方法二：手动执行

1. **创建并激活虚拟环境**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2. **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

3. **运行应用**:
    ```bash
    python src/main.py
    ```

## 项目结构

```
Invoice_upload/
├── cache/                  # 缓存发票源文件的目录
├── src/                    # 源代码目录
│   ├── components/         # UI 组件模块
│   │   ├── button_widget.py    # 底部操作按钮
│   │   ├── invoice_dialog.py   # 添加/编辑发票的对话框
│   │   ├── progress_dialog.py  # 批量操作的进度对话框
│   │   ├── sidebar_widget.py   # 用于用户管理的左侧边栏
│   │   └── table_widget.py     # 主要的发票显示表格
│   ├── services/           # 后端服务
│   │   ├── ocr_service.py      # OCR 处理服务
│   │   ├── pdf_text_service.py # PDF 文本提取服务
│   │   └── verification_service.py # 发票验证服务
│   ├── styles/             # 样式管理模块
│   │   └── styles.py       # 样式定义
│   ├── data_manager.py     # 数据持久化与管理
│   ├── main_window.py      # 主窗口类
│   └── main.py             # 应用主入口
├── invoices.json           # 数据存储文件
├── requirements.txt        # 项目依赖
├── run.sh                  # 启动脚本
├── TODO.md                 # 开发计划
└── README.md               # 项目说明 (中文)
└── README_EN.md            # 项目说明 (英文)
```

## 开发进度

请查阅 `TODO.md` 文件以获取详细的开发计划和进度。

## 系统要求

- Python 3.7+
- PySide6
- `requirements.txt` 中列出的依赖
- Linux/Windows/macOS

## 贡献

欢迎提交问题和功能请求！ 