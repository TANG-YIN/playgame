# GitHub Pages 部署方式切换指南

## 📋 当前状态

- 仓库已配置 index.html（单页面游戏）
- 包含GitHub Actions工作流配置
- 支持两种部署方式：
  1. **从分支部署**（推荐，简单）
  2. **GitHub Actions部署**（更灵活）

## 🔄 切换部署方式

### 方式一：从分支部署（推荐）

#### 步骤：

1. 访问 GitHub Pages 设置
   - URL: https://github.com/TANG-YIN/playgame/settings/pages

2. 配置部署设置
   - **Source**: 选择 `Deploy from a branch`
   - **Branch**: 选择 `main`
   - **Folder**: 选择 `/(root)`
   - 点击 `Save`

3. 等待部署完成（1-3分钟）

4. 访问网站
   - URL: https://tang-yin.github.io/playgame/

#### 优点：
- ✅ 配置简单，只需几步
- ✅ 自动部署，无需手动触发
- ✅ 适合静态网站
- ✅ 部署速度快

#### 缺点：
- ❌ 自定义构建选项较少
- ❌ 无法执行复杂的构建脚本

---

### 方式二：GitHub Actions 部署

#### 步骤：

1. 访问 GitHub Pages 设置
   - URL: https://github.com/TANG-YIN/playgame/settings/pages

2. 配置部署设置
   - **Source**: 选择 `GitHub Actions`
   - 系统会自动检测到 `.github/workflows/deploy.yml`
   - 点击 `Save`

3. 确认Actions工作流
   - 访问: https://github.com/TANG-YIN/playgame/actions
   - 查看工作流是否正常运行

4. 等待部署完成（2-5分钟）

5. 访问网站
   - URL: https://tang-yin.github.io/playgame/

#### 优点：
- ✅ 更灵活的配置选项
- ✅ 可以执行复杂的构建步骤
- ✅ 可以添加测试、压缩等优化
- ✅ 适合需要构建过程的项目
- ✅ 更好的CI/CD集成

#### 缺点：
- ❌ 配置相对复杂
- ❌ 首次设置需要更多步骤
- ❌ 部署时间稍长

---

## 🎯 推荐方案

### 对于当前项目

**推荐使用：方式一（从分支部署）**

**原因：**
1. 项目是纯前端单页面游戏（index.html）
2. 不需要构建过程（无需编译、打包等）
3. 配置简单，易于维护
4. 部署速度更快

### 何时使用GitHub Actions

如果项目有以下需求，建议使用GitHub Actions：
- 需要编译/打包（如React、Vue、Angular等）
- 需要代码压缩和优化
- 需要运行测试后再部署
- 需要生成文档或构建资源
- 需要多环境部署（dev/staging/prod）

## 🔍 验证部署

### 检查部署状态

#### 方式一（从分支部署）：

1. 访问设置页面
   - URL: https://github.com/TANG-YIN/playgame/settings/pages
   - 查看部署状态（显示为绿色对勾表示成功）

2. 访问网站
   - URL: https://tang-yin.github.io/playgame/
   - 确认页面正常显示

#### 方式二（GitHub Actions部署）：

1. 访问Actions页面
   - URL: https://github.com/TANG-YIN/playgame/actions
   - 查看最新工作流的状态

2. 查看部署历史
   - URL: https://github.com/TANG-YIN/playgame/deployments
   - 查看所有部署记录

3. 访问网站
   - URL: https://tang-yin.github.io/playgame/
   - 确认页面正常显示

## 📝 切换流程

### 从分支部署 → GitHub Actions部署

1. 在Pages设置页面
   - 将 Source 改为 `GitHub Actions`
   - 保存

2. 确认Actions工作流
   - 访问 Actions 页面
   - 确认工作流正常运行

### GitHub Actions部署 → 从分支部署

1. 在Pages设置页面
   - 将 Source 改为 `Deploy from a branch`
   - 选择分支和文件夹
   - 保存

2. 删除工作流（可选）
   - 如果不再需要，可以删除 `.github/workflows/deploy.yml`

## 🛠️ 故障排除

### 问题1：从分支部署失败

**可能原因：**
- 分支选择错误
- 文件夹路径错误
- index.html文件不存在

**解决方法：**
1. 确保选择 `main` 分支
2. 确保选择 `/(root)` 文件夹
3. 检查根目录是否有 index.html
4. 尝试重新推送代码

### 问题2：GitHub Actions部署失败

**可能原因：**
- 工作流文件有语法错误
- 权限配置不正确
- 文件路径错误

**解决方法：**
1. 访问 Actions 页面查看详细错误日志
2. 检查 `.github/workflows/deploy.yml` 语法
3. 确认仓库启用了 GitHub Pages
4. 检查权限设置（contents: read, pages: write, id-token: write）

### 问题3：部署成功但404

**可能原因：**
- 部署还在进行中
- 浏览器缓存问题

**解决方法：**
1. 等待1-3分钟让部署完成
2. 清除浏览器缓存
3. 尝试使用无痕/隐私模式
4. 直接访问 https://tang-yin.github.io/playgame/index.html

## 📊 两种方式对比

| 特性 | 从分支部署 | GitHub Actions |
|------|-----------|----------------|
| 配置难度 | ⭐ 简单 | ⭐⭐⭐ 中等 |
| 部署速度 | ⭐⭐⭐⭐⭐ 快 | ⭐⭐⭐⭐ 较快 |
| 灵活性 | ⭐⭐ 低 | ⭐⭐⭐⭐⭐ 高 |
| 构建支持 | ❌ 不支持 | ✅ 支持 |
| 测试集成 | ❌ 不支持 | ✅ 支持 |
| 适用场景 | 简单静态网站 | 复杂项目/需要构建 |

## 🎉 总结

对于当前的德州扑克游戏项目：

1. **首选推荐**：从分支部署
   - 简单、快速、稳定
   - 适合纯静态HTML页面

2. **备选方案**：GitHub Actions部署
   - 已配置好工作流文件
   - 可随时切换使用

两种方式都已配置好，您可以根据需要选择使用！
