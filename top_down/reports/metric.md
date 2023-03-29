# Frontend_Bound

## snb_client_ratios.py, jkt_server_ratios.py, ivb_client_ratios.py, ivb_server_ratios.py, hsw_client_ratios.py, hsx_server_ratios.py, bdx_server_ratios.py, bdw_client_ratios.py

This category represents fraction of slots where the processor's Frontend undersupplies its Backend. Frontend denotes the first part of the processor core responsible to fetch operations that are executed later on by the Backend part. Within the Frontend; a branch predictor predicts the next address to fetch; cache-lines are fetched from the memory subsystem; parsed into instructions; and lastly decoded into micro-operations (uops). Ideally the Frontend can issue Pipeline_Width uops every cycle to the Backend. Frontend Bound denotes unutilized issue-slots when there is no Backend stall; i.e. bubbles where Frontend delivered no uops while Backend could have accepted them. For example; stalls due to instruction-cache misses would be categorized under Frontend Bound.

- Domain: Slots
- Threshold:  > 0.15
- Area: FE
- Metric group: TmaL1, PGO

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Frontend_Bound = IDQ_UOPS_NOT_DELIVERED.CORE / SLOTS
```

- Pipeline_Width
- smt_enabled
- CPU_CLK_UNHALTED.REF_XCLK
- CPU_CLK_UNHALTED.THREAD_ANY
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- ebs_mode
- IDQ_UOPS_NOT_DELIVERED.CORE



## skl_client_ratios.py, skx_server_ratios.py, clx_server_ratios.py

This category represents fraction of slots where the processor's Frontend undersupplies its Backend. Frontend denotes the first part of the processor core responsible to fetch operations that are executed later on by the Backend part. Within the Frontend; a branch predictor predicts the next address to fetch; cache-lines are fetched from the memory subsystem; parsed into instructions; and lastly decoded into micro-operations (uops). Ideally the Frontend can issue Pipeline_Width uops every cycle to the Backend. Frontend Bound denotes unutilized issue-slots when there is no Backend stall; i.e. bubbles where Frontend delivered no uops while Backend could have accepted them. For example; stalls due to instruction-cache misses would be categorized under Frontend Bound.

- Domain: Slots
- Threshold:  > 0.15
- Area: FE
- Metric group: TmaL1, PGO
- sample: FRONTEND_RETIRED.LATENCY_GE_4:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Frontend_Bound = IDQ_UOPS_NOT_DELIVERED.CORE / SLOTS
```

- Pipeline_Width
- smt_enabled
- CPU_CLK_UNHALTED.REF_XCLK
- CPU_CLK_UNHALTED.THREAD_ANY
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- ebs_mode
- IDQ_UOPS_NOT_DELIVERED.CORE



## icl_client_ratios.py, icx_server_ratios.py, adl_glc_ratios.py, spr_server_ratios.py

This category represents fraction of slots where the processor's Frontend undersupplies its Backend. Frontend denotes the first part of the processor core responsible to fetch operations that are executed later on by the Backend part. Within the Frontend; a branch predictor predicts the next address to fetch; cache-lines are fetched from the memory subsystem; parsed into instructions; and lastly decoded into micro-operations (uops). Ideally the Frontend can issue Pipeline_Width uops every cycle to the Backend. Frontend Bound denotes unutilized issue-slots when there is no Backend stall; i.e. bubbles where Frontend delivered no uops while Backend could have accepted them. For example; stalls due to instruction-cache misses would be categorized under Frontend Bound.

- Domain: Slots
- Threshold:  > 0.15
- Area: FE
- Metric group: TmaL1, PGO
- sample: FRONTEND_RETIRED.LATENCY_GE_4:pp

```python
SLOTS = TOPDOWN.SLOTS if topdown_use_fixed else TOPDOWN.SLOTS
PERF_METRICS_SUM = PERF_METRICS.FRONTEND_BOUND / TOPDOWN.SLOTS + PERF_METRICS.BAD_SPECULATION / TOPDOWN.SLOTS + PERF_METRICS.RETIRING / TOPDOWN.SLOTS + PERF_METRICS.BACKEND_BOUND / TOPDOWN.SLOTS if topdown_use_fixed else 0
Frontend_Bound = PERF_METRICS.FRONTEND_BOUND / TOPDOWN.SLOTS / PERF_METRICS_SUM - INT_MISC.UOP_DROPPING / SLOTS if topdown_use_fixed else (IDQ_UOPS_NOT_DELIVERED.CORE - INT_MISC.UOP_DROPPING) / SLOTS
```

- PERF_METRICS.RETIRING
- TOPDOWN.SLOTS
- PERF_METRICS.FRONTEND_BOUND
- topdown_use_fixed
- PERF_METRICS.BAD_SPECULATION
- PERF_METRICS.BACKEND_BOUND
- IDQ_UOPS_NOT_DELIVERED.CORE
- INT_MISC.UOP_DROPPING



## adl_grt_ratios.py

Counts the number of issue slots that were not consumed by the backend due to frontend stalls.

- Domain: Slots
- Threshold:  > 0.2
- Area: FE

```python
Pipeline_Width = 5
CLKS = CPU_CLK_UNHALTED.CORE
SLOTS = Pipeline_Width * CLKS
Frontend_Bound = TOPDOWN_FE_BOUND.ALL / SLOTS
```

- TOPDOWN_FE_BOUND.ALL
- CPU_CLK_UNHALTED.CORE



## ehl_ratios.py

Counts the number of issue slots that were not consumed by the backend due to frontend stalls.

- Domain: Slots
- Threshold:  > 0.2
- Area: FE

```python
Pipeline_Width = 4
CLKS = CPU_CLK_UNHALTED.CORE
SLOTS = Pipeline_Width * CLKS
Frontend_Bound = TOPDOWN_FE_BOUND.ALL / SLOTS
```

- TOPDOWN_FE_BOUND.ALL
- CPU_CLK_UNHALTED.CORE



