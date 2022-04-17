# Log Processor

## Log Format

The expected log format is the following:

```shell
"<TIMESTAMP> <SESSION_ID> <MESSAGE>"
```

## How to Run

See below the example:
```shell
export PYTHONPATH="${PYTHONPATH}:/path/to/log-processor"
python3 src/run.py log_example/log.txt
```
