# mathviz — 数学函数可视化工具

这是一个用于数学函数分析与可视化的小型 Python 项目模板，包含：符号解析、求导/积分/泰勒展开、2D/3D 绘图、多函数对比等功能。

**快速开始**

- 克隆仓库后（或已在本地），在项目根目录运行：

```powershell
uv sync
```

- 运行示例脚本：

```powershell
uv run python -m mathviz.main --expr "sin(x)*exp(-x**2)" --xmin -5 --xmax 5
```

或者打开交互 notebook：

```powershell
uv run jupyter notebook
```

**项目结构**

```
mathviz/
├── pyproject.toml
├── uv.lock
├── README.md
├── .python-version
├── src/
│   └── mathviz/
│       ├── __init__.py
│       ├── main.py
│       ├── analysis.py
│       └── plotter.py
├── notebooks/
├── figures/
├── data/
└── tests/
```

**安装依赖（通过 `uv` 管理器）**

示例：

```powershell
uv add numpy scipy matplotlib sympy plotly
uv sync
```

（`uv` 会更新 `uv.lock`，保证可复现）

**使用方法与示例**

- 解析表达式并绘图（2D）：

```powershell
uv run python -m mathviz.main --expr "sin(x)*exp(-x**2)" --xmin -5 --xmax 5 --points 800
```

- 比较多个函数：

```powershell
uv run python -m mathviz.main --expr "sin(x);cos(x);sin(x)+cos(x)" --xmin -6.28 --xmax 6.28
```

**开发与测试**

- 运行测试：

```powershell
uv run python -m pytest -q
```

**备注**

- 请不要提交本地虚拟环境（例如 `.venv/`）。
- `uv.lock` 已包含示例版本；在你本地使用 `uv` 操作后，`uv.lock` 会被实际锁定。
