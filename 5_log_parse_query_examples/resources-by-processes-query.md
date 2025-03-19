fields @timestamp, @logStream, @message
| filter @message like /fluent|solver|mesher/
| parse @message "* PID=* CPU=*% MEM=*MB" as process, pid, cpu_usage, memory
| stats avg(cpu_usage), avg(memory) by process, @logStream
| sort avg(cpu_usage) desc
