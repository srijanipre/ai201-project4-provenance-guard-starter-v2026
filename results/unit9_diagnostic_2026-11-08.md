# Unit 9 diagnostics, 2026-11-08

Not formal criterion trials. Run to find the stage and mechanism behind the
U9-3 and U9-4 misses. No code was changed for any of these.

## 1. Where the cold-start time goes (before the improvement, code at 3a74586)

In one Python process: load gpt2, then score the 303-word cost passage six
times, timing each signal separately.

```
load 3529 ms
call 1: model_signal 3742.8 ms, style_signal 0.61 ms
call 2: model_signal 246.8 ms, style_signal 0.23 ms
call 3: model_signal 240.8 ms, style_signal 0.23 ms
call 4: model_signal 293.8 ms, style_signal 0.21 ms
call 5: model_signal 246.8 ms, style_signal 0.23 ms
call 6: model_signal 278.3 ms, style_signal 0.24 ms
```

Signal one is the whole cost. The first scoring pass after the load is slow on
its own, so loading the weights without scoring would not have been enough.

## 2. Token lengths

```
cost text tokens 365 warm-up text tokens 783 (both truncated at 400)
```

The cost passage is 365 tokens, not the full 400-token window.

## 3. Six extra fresh starts after the improvement (code at 3da0ba3)

gunicorn on port 5052, wait for /health, then one /submit of the cost passage
(curl's time_total). "warmed up in" is gunicorn's own log line from the
post_worker_init hook.

```
start 1: first submit 0.226142s, warmed up in 6.3 s
start 2: first submit 1.451313s, warmed up in 2.7 s
start 3: first submit 0.232506s, warmed up in 2.6 s
start 4: first submit 0.300767s, warmed up in 2.6 s
start 5: first submit 0.348389s, warmed up in 2.6 s
start 6: first submit 0.278082s, warmed up in 2.8 s
```

Memory state of the laptop right after (`memory_pressure`, `vm_stat`):

```
System-wide memory free percentage: 35%
Pages stored in compressor:             1151905.
Pages occupied by compressor:            179959.
Pageouts:                               6327176.
Swapouts:                             112817033.
```
