#!/bin/bash

# 矿池地址和端口列表（你可自定义）
declare -a POOLS=(
  "gulf.moneroocean.stream:10128"
  "gulf.moneroocean.stream:10001"
)

echo "==== 开始测试 XMR 矿池连通性 ===="
echo ""

# 循环测试每个地址
for pool in "${POOLS[@]}"
do
  HOST=$(echo $pool | cut -d':' -f1)
  PORT=$(echo $pool | cut -d':' -f2)

  echo -n "正在测试 $HOST:$PORT ... "

  nc -z -w2 $HOST $PORT
  if [ $? -eq 0 ]; then
    echo -e "\e[32m连接成功\e[0m"
  else
    echo -e "\e[31m连接失败\e[0m"
  fi
done

echo ""
echo "==== 测试完成 ===="
