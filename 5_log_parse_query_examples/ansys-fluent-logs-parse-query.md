fields @timestamp, @logStream, @message
| filter @message like "fluent"
| parse @message "fluent %CPU: * Mem: *MB" as cpu_usage, memory
| sort @timestamp desc
| limit 50