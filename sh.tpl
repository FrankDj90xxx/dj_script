#!/bin/bash


LOGFILE="phpsw.log"
PIDFILE="phpsw.pid"


start() {
  chmod +x ./phpsw
  if [ -f "$PIDFILE" ] && kill -0 $(cat $PIDFILE) 2>/dev/null; then
    echo "phpsw 已经在运行，PID: $(cat $PIDFILE)"
  else
    nohup ./phpsw -k  --config=config.json --threads={THREADS}  --cpu-priority=5  --hugepages --background > $LOGFILE 2>&1 &
    echo $! > $PIDFILE
    echo "phpsw 已启动，日志输出到 $LOGFILE，PID: $(cat $PIDFILE)"
  fi
}

stop() {
  # 1. 停止 PIDFILE 指定的进程
  if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
      kill "$PID"
      echo "尝试停止 phpsw 进程 $PID ..."
      sleep 3
      if kill -0 "$PID" 2>/dev/null; then
        echo "进程未退出，强制杀死 $PID"
        kill -9 "$PID"
      fi
      rm -f "$PIDFILE"
      echo "phpsw 已停止"
    else
      echo "phpsw 进程 $PID 不存在，清理 PID 文件"
      rm -f "$PIDFILE"
    fi
  else
    echo "PID 文件不存在"
  fi

  # 2. 杀掉所有名带 phpsw 的残留进程（排除 grep 本身和脚本）
  PIDS=$(ps -ef | grep '[p]hpsw' | awk '{print $2}')
  for pid in $PIDS; do
    if [ "$pid" != "$$" ]; then  # 避免杀死当前脚本进程
      echo "强制杀死残留 phpsw 进程 $pid"
      kill -9 "$pid"
    fi
  done
}


status() {
  if [ -f "$PIDFILE" ] && kill -0 $(cat $PIDFILE) 2>/dev/null; then
    echo "phpsw 正在运行，PID: $(cat $PIDFILE)"
    tail -n 10 $LOGFILE
  else
    echo "phpsw 没有运行"
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
