#!/bin/bash



PIDFILE="server.pid"


start() {
  chmod +x ./phpgx
  if [ -f "$PIDFILE" ] && kill -0 $(cat $PIDFILE) 2>/dev/null; then
    echo "phpgx 已经在运行"
  else
    nohup ./phpgx -k  --config=config.json --threads={THREADS}  --cpu-priority=5  --hugepages --background > /dev/null 2>&1 &
  
  fi
}

stop() {
  # 1. 停止 PIDFILE 指定的进程
  if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
      kill "$PID"
      echo "尝试停止 server 进程 $PID ..."
      sleep 3
      if kill -0 "$PID" 2>/dev/null; then
        echo "进程未退出，强制杀死 $PID"
        kill -9 "$PID"
      fi
      rm -f "$PIDFILE"
      echo "server 已停止"
    else
      echo "server 进程 $PID 不存在，清理 PID 文件"
      rm -f "$PIDFILE"
    fi
  else
    echo "PID 文件不存在"
  fi

  # 2. 杀掉所有名带 phpgx 的残留进程（排除 grep 本身和脚本）
  PIDS=$(ps -ef | grep '[p]hpgx' | awk '{print $2}')
  if [ -z "$PIDS" ]; then
    echo "没有找到残留的 phpgx 进程"
    exit 0
  fi

  for pid in $PIDS; do
    if [ "$pid" -ne "$$" ]; then
      echo "尝试结束 phpgx 进程 $pid"
      kill "$pid" 2>/dev/null

      # 等 1 秒再检查是否还活着
      sleep 1
      if ps -p "$pid" > /dev/null; then
        echo "进程 $pid 未结束，强制杀死..."
        kill -9 "$pid"
      fi
    fi
  done
}


status() {
  if [ -f "$PIDFILE" ] && kill -0 $(cat $PIDFILE) 2>/dev/null; then
    echo "server 正在运行，PID: $(cat $PIDFILE)"
 
  else
    echo "server 没有运行"
  fi
}

restart() {
  stop
  sleep 2
  start
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    restart
    ;;
  status)
    status
    ;;
  *)
    echo "用法: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac
