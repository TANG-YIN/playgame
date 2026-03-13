# GitHub Pages 启用指南

## 📋 前提条件

- 拥有GitHub账号
- 仓库代码已推送到GitHub（已完成）

## 🚀 启用步骤

### 第一步：访问GitHub仓库设置

1. 打开浏览器，访问：https://github.com/TANG-YIN/playgame/settings/pages

### 第二步：配置GitHub Pages

在页面中找到 **"Build and deployment"** 部分：

1. **Source（源）**
   - 点击下拉菜单
   - 选择：`Deploy from a branch`（从分支部署）

2. **Branch（分支）**
   - 点击第一个下拉菜单，选择：`main`
   - 点击第二个下拉菜单（Folder），选择：`/(root)` 或 `/`（根目录）
   
   配置示例：
   ```
   Branch: main
   Folder: / (root)
   ```

3. **保存设置**
   - 点击右下角的 **Save** 按钮
   - 等待页面刷新

### 第三步：等待部署

保存后，GitHub会自动开始部署：

1. **查看部署状态**
   - 在同一页面，你会看到部署状态
   - 通常显示为：`Deploying...` 或 `Your site is live at...`

2. **等待时间**
   - 首次部署通常需要 **1-3分钟**
   - 后续更新会更快（约30秒-1分钟）

3. **部署成功标志**
   - 状态变为绿色对勾 ✓
   - 显示访问链接：`https://tang-yin.github.io/playgame/`

### 第四步：访问网站

部署成功后：

1. **直接访问**
   - 打开：https://tang-yin.github.io/playgame/

2. **或从GitHub访问**
   - 访问：https://github.com/TANG-YIN/playgame
   - 点击右侧的 "Settings" 标签
   - 选择左侧的 "Pages"
   - 点击显示的链接

## ❓ 常见问题

### Q1: 保存后还是显示 "There isn't a GitHub Pages site here"

**A:** 需要等待1-3分钟让GitHub完成部署。如果超过5分钟仍未成功：
- 检查是否选择了正确的分支（main）
- 检查是否选择了正确的文件夹（/ 或 /root）
- 尝试刷新页面

### Q2: 显示 404 错误

**A:** 可能原因：
- 部署还在进行中，等待完成
- 检查仓库根目录是否有 `index.html` 文件
- 尝试访问完整URL：`https://tang-yin.github.io/playgame/index.html`

### Q3: 页面显示但样式不对

**A:** 这是正常的，因为我们的index.html包含了内联CSS。如果样式完全缺失：
- 清除浏览器缓存
- 尝试使用无痕/隐私模式打开

### Q4: 如何更新网站

**A:** 只需：
1. 修改代码
2. `git add .`
3. `git commit -m "your message"`
4. `git push`
5. GitHub会自动重新部署

### Q5: 部署历史在哪里查看

**A:** 在仓库中：
- 访问 https://github.com/TANG-YIN/playgame/deployments
- 可以看到所有部署历史和状态

## 🔧 高级配置

### 自定义域名

如果需要使用自定义域名：

1. 在Pages设置页面
2. 点击 "Custom domain"
3. 输入你的域名（如：game.example.com）
4. 按照提示配置DNS记录

### 强制HTTPS

在Pages设置页面：
- 找到 "Enforce HTTPS"
- 勾选该选项
- 确保使用HTTPS访问

### 添加自定义404页面

在仓库根目录创建 `404.html`：
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>404 - 页面未找到</title>
</head>
<body>
    <h1>404 - 页面未找到</h1>
    <p><a href="/">返回首页</a></p>
</body>
</html>
```

## 📊 监控部署

### 查看部署日志

1. 访问仓库的 Actions 标签
2. 点击最近的 workflow run
3. 查看详细日志

### 部署失败排查

如果部署失败：
1. 检查Actions日志中的错误信息
2. 确保没有语法错误
3. 确保所有文件都已提交
4. 尝试重新推送代码

## ✅ 验证清单

部署完成后，请检查：

- [ ] 可以访问 https://tang-yin.github.io/playgame/
- [ ] 页面显示正常
- [ ] 可以点击"开始新游戏"按钮
- [ ] 游戏可以正常运行
- [ ] 所有操作按钮都能使用
- [ ] AI对手能够正常行动

## 🎉 完成！

如果以上步骤都完成，您应该可以：
1. 访问 https://tang-yin.github.io/playgame/
2. 看到德州扑克游戏界面
3. 点击"开始新游戏"开始玩
4. 与3个AI对手进行对战

如有问题，请查看上述"常见问题"部分或访问GitHub文档：https://docs.github.com/en/pages
