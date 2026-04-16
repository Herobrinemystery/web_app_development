---
name: commit
description: 產生與執行 Git Commit。自動分析變更並產生符合 Conventional Commits 規範的訊息。
---

# Commit Skill

這個 skill 幫助開發者在完成一段程式碼後，自動分析變更並產生符合 Conventional Commits 規範的 Git Commit 訊息，並且能協助執行 commit 動作。

## When to use this skill

- 完成一個功能、修改或文件更新，準備提交程式碼時
- 希望快速分析目前的變更並產生專業的 Commit 訊息時

## How to use it

請在你的 prompt 裡輸入 `/commit` 或使用以下指示：

```
請檢查目前的 Git 狀態（包含 staged 和 unstaged 的變更）。
如果沒有變更，請告訴我目前工作區是乾淨的。
如果有變更：
1. 分析主要變動的內容。
2. 根據 Conventional Commits 規範，產生一個適合的 git commit 訊息。
3. 如果我尚未將檔案加入 staged，也請詢問我是否要執行 `git add .`。
4. 提供可以複製執行的 git commit 指令，或者直接幫我執行。
```

## Conventional Commits 規範

格式：`<type>(<scope>): <subject>`

常見的 Type：
- **feat**: 新功能 (Feature)
- **fix**: 修復 Bug
- **docs**: 文件更改
- **style**: 程式碼格式（不影響邏輯，例如空白、排版）
- **refactor**: 重構（既不是新增功能也不是修復 Bug 的程式碼變動）
- **test**: 新增或修改測試
- **chore**: 建置過程或輔助工具的變動

## 範例

建議的 Commit 訊息為：
`feat(skills): 新增自動化 commit skill`

指令：
`git commit -m "feat(skills): 新增自動化 commit skill"`
