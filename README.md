# llm-multi-experience
## 简介
一个用于比较和体验不同开源大型模型的项目，旨在为用户提供一个统一的平台来探索和评估各种模型的性能和应用场景。
![](./images/view.png)

## 功能
- **模型比较：** 用户可以在同一任务上比较不同模型的性能。
- **快速部署：** 简化了模型的部署流程，用户可以快速开始实验。
- **任务多样：** 支持多种类型的任务，如文本生成、文本分类、机器翻译等。
- **交互式体验：** 提供交互式界面，用户可以直接在线体验模型效果。

## 安装
1. 克隆仓库到本地。
```bash
git clone https://github.com/xunhanliu/llm-multi-experience.git
```
2. 安装依赖
```bash
pip install -r requirements.txt
```
3. 使用说明
运行主程序。
```bash
python app.py
```

## 注意
1. 需要安装chrome-driver
2. 需要安装chrome浏览器

## 编译
```bash
pyinstaller app.py
```

## 贡献
欢迎任何形式的贡献，包括但不限于提交bug修复、新增功能、优化代码等。

## 功能列表:
- [x] 实现cookie的保存以及恢复
- [x] 实现四个主流中文大模型的对比
- [x] 实现文本的同步输入
- [ ] 实现文件的同步输入
- [ ] 解决chatgpt相关的安全策略


