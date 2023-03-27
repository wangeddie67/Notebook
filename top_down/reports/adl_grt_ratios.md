# 1 <a id="frontend_bound">Frontend_Bound</a>

Counts the number of issue slots that were not consumed by the backend due to frontend stalls.

- Domain: Slots
- Threshold:  > 0.2
- Area: FE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Frontend_Bound = TOPDOWN_FE_BOUND.ALL / SLOTS
```

- TOPDOWN_FE_BOUND.ALL
- CPU_CLK_UNHALTED.CORE

## 1.1 <a id="frontend_latency">Frontend_Latency</a>

Counts the number of issue slots that were not delivered by the frontend due to frontend bandwidth restrictions due to decode, predecode, cisc, and other limitations.

- Domain: Slots
- Threshold:  > 0.15
- Area: FE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Frontend_Latency = TOPDOWN_FE_BOUND.FRONTEND_LATENCY / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_FE_BOUND.FRONTEND_LATENCY

### 1.1.1 <a id="icache">Icache</a>

Counts the number of issue slots that were not delivered by the frontend due to instruction cache misses.

- Domain: Slots
- Threshold:  > 0.05
- Area: FE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Icache = TOPDOWN_FE_BOUND.ICACHE / SLOTS
```

- TOPDOWN_FE_BOUND.ICACHE
- CPU_CLK_UNHALTED.CORE

### 1.1.2 <a id="itlb">ITLB</a>

Counts the number of issue slots that were not delivered by the frontend due to Instruction Table Lookaside Buffer (ITLB) misses.

- Domain: Slots
- Threshold:  > 0.05
- Area: FE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
ITLB = TOPDOWN_FE_BOUND.ITLB / SLOTS
```

- TOPDOWN_FE_BOUND.ITLB
- CPU_CLK_UNHALTED.CORE

### 1.1.3 <a id="branch_detect">Branch_Detect</a>

Counts the number of issue slots that were not delivered by the frontend due to BACLEARS, which occurs when the Branch Target Buffer (BTB) prediction or lack thereof, was corrected by a later branch predictor in the frontend. Includes BACLEARS due to all branch types including conditional and unconditional jumps, returns, and indirect branches.

- Domain: Slots
- Threshold:  > 0.05
- Area: FE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Branch_Detect = TOPDOWN_FE_BOUND.BRANCH_DETECT / SLOTS
```

- TOPDOWN_FE_BOUND.BRANCH_DETECT
- CPU_CLK_UNHALTED.CORE

### 1.1.4 <a id="branch_resteer">Branch_Resteer</a>

Counts the number of issue slots that were not delivered by the frontend due to BTCLEARS, which occurs when the Branch Target Buffer (BTB) predicts a taken branch.

- Domain: Slots
- Threshold:  > 0.05
- Area: FE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Branch_Resteer = TOPDOWN_FE_BOUND.BRANCH_RESTEER / SLOTS
```

- TOPDOWN_FE_BOUND.BRANCH_RESTEER
- CPU_CLK_UNHALTED.CORE

## 1.2 <a id="frontend_bandwidth">Frontend_Bandwidth</a>

Counts the number of issue slots that were not delivered by the frontend due to frontend bandwidth restrictions due to decode, predecode, cisc, and other limitations.

- Domain: Slots
- Threshold:  > 0.1
- Area: FE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Frontend_Bandwidth = TOPDOWN_FE_BOUND.FRONTEND_BANDWIDTH / SLOTS
```

- TOPDOWN_FE_BOUND.FRONTEND_BANDWIDTH
- CPU_CLK_UNHALTED.CORE

### 1.2.1 <a id="cisc">Cisc</a>

Counts the number of issue slots that were not delivered by the frontend due to the microcode sequencer (MS).

- Domain: Slots
- Threshold:  > 0.05
- Area: FE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Cisc = TOPDOWN_FE_BOUND.CISC / SLOTS
```

- TOPDOWN_FE_BOUND.CISC
- CPU_CLK_UNHALTED.CORE

### 1.2.2 <a id="decode">Decode</a>

Counts the number of issue slots that were not delivered by the frontend due to decode stalls.

- Domain: Slots
- Threshold:  > 0.05
- Area: FE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Decode = TOPDOWN_FE_BOUND.DECODE / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_FE_BOUND.DECODE

### 1.2.3 <a id="predecode">Predecode</a>

Counts the number of issue slots that were not delivered by the frontend due to wrong predecodes.

- Domain: Slots
- Threshold:  > 0.05
- Area: FE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Predecode = TOPDOWN_FE_BOUND.PREDECODE / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_FE_BOUND.PREDECODE

### 1.2.4 <a id="other_fb">Other_FB</a>

Counts the number of issue slots that were not delivered by the frontend due to other common frontend stalls not categorized.

- Domain: Slots
- Threshold:  > 0.05
- Area: FE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Other_FB = TOPDOWN_FE_BOUND.OTHER / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_FE_BOUND.OTHER

# 2 <a id="bad_speculation">Bad_Speculation</a>

Counts the total number of issue slots that were not consumed by the backend because allocation is stalled due to a mispredicted jump or a machine clear. Only issue slots wasted due to fast nukes such as memory ordering nukes are counted. Other nukes are not accounted for. Counts all issue slots blocked during this recovery window including relevant microcode flows and while uops are not yet available in the instruction queue (IQ). Also includes the issue slots that were consumed by the backend but were thrown away because they were younger than the mispredict or machine clear.

- Domain: Slots
- Threshold:  > 0.15
- Area: BAD

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Bad_Speculation = TOPDOWN_BAD_SPECULATION.ALL / SLOTS
```

- TOPDOWN_BAD_SPECULATION.ALL
- CPU_CLK_UNHALTED.CORE

## 2.1 <a id="branch_mispredicts">Branch_Mispredicts</a>

Counts the number of issue slots that were not consumed by the backend due to branch mispredicts.

- Domain: Slots
- Threshold:  > 0.05
- Area: BAD

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Branch_Mispredicts = TOPDOWN_BAD_SPECULATION.MISPREDICT / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_BAD_SPECULATION.MISPREDICT

## 2.2 <a id="machine_clears">Machine_Clears</a>

Counts the total number of issue slots that were not consumed by the backend because allocation is stalled due to a machine clear (nuke) of any kind including memory ordering and memory disambiguation.

- Domain: Slots
- Threshold:  > 0.05
- Area: BAD

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Machine_Clears = TOPDOWN_BAD_SPECULATION.MACHINE_CLEARS / SLOTS
```

- TOPDOWN_BAD_SPECULATION.MACHINE_CLEARS
- CPU_CLK_UNHALTED.CORE

### 2.2.1 <a id="nuke">Nuke</a>

Counts the number of issue slots that were not consumed by the backend due to a machine clear (slow nuke).

- Domain: Slots
- Threshold:  > 0.05
- Area: BAD

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Nuke = TOPDOWN_BAD_SPECULATION.NUKE / SLOTS
```

- TOPDOWN_BAD_SPECULATION.NUKE
- CPU_CLK_UNHALTED.CORE

#### 2.2.1.1 <a id="smc">SMC</a>

Counts the number of machine clears relative to the number of nuke slots due to SMC.

- Domain: Count
- Threshold:  > 0.02
- Area: BAD

```python
SMC = Nuke * (MACHINE_CLEARS.SMC / MACHINE_CLEARS.SLOW)
```

- MACHINE_CLEARS.SLOW
- [Nuke](#nuke)
- MACHINE_CLEARS.SMC

#### 2.2.1.2 <a id="memory_ordering">Memory_Ordering</a>

Counts the number of machine clears relative to the number of nuke slots due to memory ordering.

- Domain: Count
- Threshold:  > 0.02
- Area: BAD

```python
Memory_Ordering = Nuke * (MACHINE_CLEARS.MEMORY_ORDERING / MACHINE_CLEARS.SLOW)
```

- MACHINE_CLEARS.MEMORY_ORDERING
- MACHINE_CLEARS.SLOW
- [Nuke](#nuke)

#### 2.2.1.3 <a id="fp_assist">FP_Assist</a>

Counts the number of machine clears relative to the number of nuke slots due to FP assists.

- Domain: Count
- Threshold:  > 0.02
- Area: BAD

```python
FP_Assist = Nuke * (MACHINE_CLEARS.FP_ASSIST / MACHINE_CLEARS.SLOW)
```

- MACHINE_CLEARS.FP_ASSIST
- MACHINE_CLEARS.SLOW
- [Nuke](#nuke)

#### 2.2.1.4 <a id="disambiguation">Disambiguation</a>

Counts the number of machine clears relative to the number of nuke slots due to memory disambiguation.

- Domain: Count
- Threshold:  > 0.02
- Area: BAD

```python
Disambiguation = Nuke * (MACHINE_CLEARS.DISAMBIGUATION / MACHINE_CLEARS.SLOW)
```

- MACHINE_CLEARS.DISAMBIGUATION
- MACHINE_CLEARS.SLOW
- [Nuke](#nuke)

#### 2.2.1.5 <a id="page_fault">Page_Fault</a>

Counts the number of machine clears relative to the number of nuke slots due to page faults.

- Domain: Count
- Threshold:  > 0.02
- Area: BAD

```python
Page_Fault = Nuke * (MACHINE_CLEARS.PAGE_FAULT / MACHINE_CLEARS.SLOW)
```

- MACHINE_CLEARS.PAGE_FAULT
- MACHINE_CLEARS.SLOW
- [Nuke](#nuke)

### 2.2.2 <a id="fast_nuke">Fast_Nuke</a>

Counts the number of issue slots that were not consumed by the backend due to a machine clear classified as a fast nuke due to memory ordering, memory disambiguation and memory renaming.

- Domain: Slots
- Threshold:  > 0.05
- Area: BAD

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Fast_Nuke = TOPDOWN_BAD_SPECULATION.FASTNUKE / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_BAD_SPECULATION.FASTNUKE

# 3 <a id="backend_bound">Backend_Bound</a>

Counts the total number of issue slots that were not consumed by the backend due to backend stalls. Note that uops must be available for consumption in order for this event to count. If a uop is not available (IQ is empty), this event will not count. The rest of these subevents count backend stalls, in cycles, due to an outstanding request which is memory bound vs core bound. The subevents are not slot based events and therefore can not be precisely added or subtracted from the Backend_Bound_Aux subevents which are slot based.

- Domain: Slots
- Threshold:  > 0.1
- Area: BE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Backend_Bound = TOPDOWN_BE_BOUND.ALL / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_BE_BOUND.ALL

## 3.1 <a id="core_bound">Core_Bound</a>

Counts the number of cycles due to backend bound stalls that are core execution bound and not attributed to outstanding demand load or store stalls.

- Domain: Cycles
- Threshold:  > 0.1
- Area: BE

```python
Core_Bound = max(0, Backend_Bound - Load_Store_Bound)
```

- [Backend_Bound](#backend_bound)
- [Load_Store_Bound](#load_store_bound)

## 3.2 <a id="load_store_bound">Load_Store_Bound</a>

Counts the number of cycles the core is stalled due to stores or loads.

- Domain: Cycles
- Threshold:  > 0.2
- Area: BE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Load_Store_Bound = min(TOPDOWN_BE_BOUND.ALL / SLOTS, LD_HEAD.ANY_AT_RET / CLKS + Store_Bound)
```

- [Store_Bound](#store_bound)
- LD_HEAD.ANY_AT_RET
- CPU_CLK_UNHALTED.CORE
- TOPDOWN_BE_BOUND.ALL

### 3.2.1 <a id="store_bound">Store_Bound</a>

Counts the number of cycles the core is stalled due to store buffer full.

- Domain: Cycles
- Threshold:  > 0.1
- Area: BE

```python
Store_Bound = Mem_Scheduler * (MEM_SCHEDULER_BLOCK.ST_BUF / MEM_SCHEDULER_BLOCK.ALL)
```

- [Mem_Scheduler](#mem_scheduler)
- MEM_SCHEDULER_BLOCK.ST_BUF
- MEM_SCHEDULER_BLOCK.ALL

### 3.2.2 <a id="l1_bound">L1_Bound</a>

Counts the number of cycles that the oldest load of the load buffer is stalled at retirement due to a load block.

- Domain: Cycles
- Threshold:  > 0.1
- Area: BE

```python
CLKS = CPU_CLK_UNHALTED.CORE
L1_Bound = LD_HEAD.L1_BOUND_AT_RET / CLKS
```

- CPU_CLK_UNHALTED.CORE
- LD_HEAD.L1_BOUND_AT_RET

#### 3.2.2.1 <a id="store_fwd">Store_Fwd</a>

Counts the number of cycles that the oldest load of the load buffer is stalled at retirement due to a store forward block.

- Domain: Cycles
- Threshold:  > 0.05
- Area: BE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Store_Fwd = LD_HEAD.ST_ADDR_AT_RET / CLKS
```

- CPU_CLK_UNHALTED.CORE
- LD_HEAD.ST_ADDR_AT_RET

#### 3.2.2.2 <a id="stlb_hit">STLB_Hit</a>

Counts the number of cycles that the oldest load of the load buffer is stalled at retirement due to a first level TLB miss.

- Domain: Cycles
- Threshold:  > 0.05
- Area: BE

```python
CLKS = CPU_CLK_UNHALTED.CORE
STLB_Hit = LD_HEAD.DTLB_MISS_AT_RET / CLKS
```

- LD_HEAD.DTLB_MISS_AT_RET
- CPU_CLK_UNHALTED.CORE

#### 3.2.2.3 <a id="stlb_miss">STLB_Miss</a>

Counts the number of cycles that the oldest load of the load buffer is stalled at retirement due to a second level TLB miss requiring a page walk.

- Domain: Cycles
- Threshold:  > 0.05
- Area: BE

```python
CLKS = CPU_CLK_UNHALTED.CORE
STLB_Miss = LD_HEAD.PGWALK_AT_RET / CLKS
```

- LD_HEAD.PGWALK_AT_RET
- CPU_CLK_UNHALTED.CORE

#### 3.2.2.4 <a id="other_l1">Other_L1</a>

Counts the number of cycles that the oldest load of the load buffer is stalled at retirement due to a number of other load blocks.

- Domain: Cycles
- Threshold:  > 0.05
- Area: BE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Other_L1 = LD_HEAD.OTHER_AT_RET / CLKS
```

- CPU_CLK_UNHALTED.CORE
- LD_HEAD.OTHER_AT_RET

### 3.2.3 <a id="l2_bound">L2_Bound</a>

Counts the number of cycles a core is stalled due to a demand load which hit in the L2 Cache.

- Domain: Cycles
- Threshold:  > 0.1
- Area: BE

```python
CLKS = CPU_CLK_UNHALTED.CORE
L2_Bound = MEM_BOUND_STALLS.LOAD_L2_HIT / CLKS
```

- CPU_CLK_UNHALTED.CORE
- MEM_BOUND_STALLS.LOAD_L2_HIT

### 3.2.4 <a id="l3_bound">L3_Bound</a>

Counts the number of cycles a core is stalled due to a demand load which hit in the Last Level Cache (LLC) or other core with HITE/F/M.

- Domain: Cycles
- Threshold:  > 0.1
- Area: BE

```python
CLKS = CPU_CLK_UNHALTED.CORE
L3_Bound = MEM_BOUND_STALLS.LOAD_LLC_HIT / CLKS
```

- MEM_BOUND_STALLS.LOAD_LLC_HIT
- CPU_CLK_UNHALTED.CORE

### 3.2.5 <a id="dram_bound">DRAM_Bound</a>

Counts the number of cycles the core is stalled due to a demand load miss which hit in DRAM or MMIO (Non-DRAM).

- Domain: Cycles
- Threshold:  > 0.1
- Area: BE

```python
CLKS = CPU_CLK_UNHALTED.CORE
DRAM_Bound = MEM_BOUND_STALLS.LOAD_DRAM_HIT / CLKS
```

- CPU_CLK_UNHALTED.CORE
- MEM_BOUND_STALLS.LOAD_DRAM_HIT

# 4 <a id="retiring">Retiring</a>

Counts the numer of issue slots that result in retirement slots.

- Domain: Slots
- Threshold:  > 0.75
- Area: RET

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Retiring = TOPDOWN_RETIRING.ALL / SLOTS
```

- TOPDOWN_RETIRING.ALL
- CPU_CLK_UNHALTED.CORE

## 4.1 <a id="base">Base</a>

Counts the number of uops that are not from the microsequencer.

- Domain: Slots
- Threshold:  > 0.6
- Area: RET

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Base = (TOPDOWN_RETIRING.ALL - UOPS_RETIRED.MS) / SLOTS
```

- TOPDOWN_RETIRING.ALL
- CPU_CLK_UNHALTED.CORE
- UOPS_RETIRED.MS

### 4.1.1 <a id="fp_uops">FP_uops</a>

Counts the number of floating point divide uops retired (x87 and SSE, including x87 sqrt).

- Domain: Slots
- Threshold:  > 0.2
- Area: RET

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
FP_uops = UOPS_RETIRED.FPDIV / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- UOPS_RETIRED.FPDIV

### 4.1.2 <a id="other_ret">Other_Ret</a>

Counts the number of uops retired excluding ms and fp div uops.

- Domain: Slots
- Threshold:  > 0.3
- Area: RET

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Other_Ret = (TOPDOWN_RETIRING.ALL - UOPS_RETIRED.MS - UOPS_RETIRED.FPDIV) / SLOTS
```

- TOPDOWN_RETIRING.ALL
- CPU_CLK_UNHALTED.CORE
- UOPS_RETIRED.MS
- UOPS_RETIRED.FPDIV

## 4.2 <a id="ms_uops">MS_uops</a>

Counts the number of uops that are from the complex flows issued by the micro-sequencer (MS). This includes uops from flows due to complex instructions, faults, assists, and inserted flows.

- Domain: Slots
- Threshold:  > 0.05
- Area: RET

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
MS_uops = UOPS_RETIRED.MS / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- UOPS_RETIRED.MS

# 5 General Metrics

## 5.1 <a id="metric_cpi">Metric_CPI</a>

Cycles Per Instruction

- Threshold: True
- Area: Info.Core

```python
CLKS = CPU_CLK_UNHALTED.CORE
CPI = CLKS / INST_RETIRED.ANY
Metric_CPI = CPI
```

- CPU_CLK_UNHALTED.CORE
- INST_RETIRED.ANY

## 5.2 <a id="metric_inst_miss_cost_l3hit_percent">Metric_Inst_Miss_Cost_L3Hit_Percent</a>

Percent of instruction miss cost that hit in the L3

- Threshold: True
- Area: Info.Frontend

```python
Inst_Miss_Cost_L3Hit_Percent = 100 * MEM_BOUND_STALLS.IFETCH_LLC_HIT / MEM_BOUND_STALLS.IFETCH
Metric_Inst_Miss_Cost_L3Hit_Percent = Inst_Miss_Cost_L3Hit_Percent
```

- MEM_BOUND_STALLS.IFETCH
- MEM_BOUND_STALLS.IFETCH_LLC_HIT

## 5.3 <a id="st_buffer">ST_Buffer</a>

Counts the number of cycles, relative to the number of mem_scheduler slots, in which uops are blocked due to store buffer full

- Domain: Count
- Threshold:  > 0.05
- Area: BE_aux

```python
ST_Buffer = Mem_Scheduler * (MEM_SCHEDULER_BLOCK.ST_BUF / MEM_SCHEDULER_BLOCK.ALL)
```

- [Mem_Scheduler](#mem_scheduler)
- MEM_SCHEDULER_BLOCK.ST_BUF
- MEM_SCHEDULER_BLOCK.ALL

## 5.4 <a id="metric_ipcall">Metric_IpCall</a>

Instruction per (near) call (lower number means higher occurance rate)

- Threshold: True
- Area: Info.Inst_Mix

```python
IpCall = INST_RETIRED.ANY / BR_INST_RETIRED.CALL
Metric_IpCall = IpCall
```

- INST_RETIRED.ANY
- BR_INST_RETIRED.CALL

## 5.5 <a id="metric_ipload">Metric_IpLoad</a>

Instructions per Load

- Threshold: True
- Area: Info.Inst_Mix

```python
IpLoad = INST_RETIRED.ANY / MEM_UOPS_RETIRED.ALL_LOADS
Metric_IpLoad = IpLoad
```

- MEM_UOPS_RETIRED.ALL_LOADS
- INST_RETIRED.ANY

## 5.6 <a id="metric_idiv_uop_ratio">Metric_IDiv_Uop_Ratio</a>

Percentage of all uops which are IDiv uops

- Threshold: True
- Area: Info.Inst_Mix

```python
IDiv_Uop_Ratio = 100 * UOPS_RETIRED.IDIV / UOPS_RETIRED.ALL
Metric_IDiv_Uop_Ratio = IDiv_Uop_Ratio
```

- UOPS_RETIRED.IDIV
- UOPS_RETIRED.ALL

## 5.7 <a id="metric_cycles_per_demand_load_dram_hit">Metric_Cycles_per_Demand_Load_DRAM_Hit</a>

Cycle cost per DRAM hit

- Threshold: True
- Area: Info.Memory

```python
Cycles_per_Demand_Load_DRAM_Hit = MEM_BOUND_STALLS.LOAD_DRAM_HIT / MEM_LOAD_UOPS_RETIRED.DRAM_HIT
Metric_Cycles_per_Demand_Load_DRAM_Hit = Cycles_per_Demand_Load_DRAM_Hit
```

- MEM_LOAD_UOPS_RETIRED.DRAM_HIT
- MEM_BOUND_STALLS.LOAD_DRAM_HIT

## 5.8 <a id="metric_estimated_pause_cost">Metric_Estimated_Pause_Cost</a>

Estimated Pause cost. In percent

- Threshold: True
- Area: Info.Bottleneck

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Estimated_Pause_Cost = 100 * SERIALIZATION.NON_C01_MS_SCB / SLOTS
Metric_Estimated_Pause_Cost = Estimated_Pause_Cost
```

- CPU_CLK_UNHALTED.CORE
- SERIALIZATION.NON_C01_MS_SCB

## 5.9 <a id="metric_slots">Metric_SLOTS</a>

- Domain: Cycles
- Threshold: True
- Area: Info.Core

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Metric_SLOTS = SLOTS
```

- CPU_CLK_UNHALTED.CORE

## 5.10 <a id="metric_microcode_uop_ratio">Metric_Microcode_Uop_Ratio</a>

Percentage of all uops which are ucode ops

- Threshold: True
- Area: Info.Inst_Mix

```python
Microcode_Uop_Ratio = 100 * UOPS_RETIRED.MS / UOPS_RETIRED.ALL
Metric_Microcode_Uop_Ratio = Microcode_Uop_Ratio
```

- UOPS_RETIRED.ALL
- UOPS_RETIRED.MS

## 5.11 <a id="register">Register</a>

Counts the number of issue slots that were not consumed by the backend due to the physical register file unable to accept an entry (marble stalls).

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Register = TOPDOWN_BE_BOUND.REGISTER / SLOTS
```

- TOPDOWN_BE_BOUND.REGISTER
- CPU_CLK_UNHALTED.CORE

## 5.12 <a id="reorder_buffer">Reorder_Buffer</a>

Counts the number of issue slots that were not consumed by the backend due to the reorder buffer being full (ROB stalls).

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Reorder_Buffer = TOPDOWN_BE_BOUND.REORDER_BUFFER / SLOTS
```

- TOPDOWN_BE_BOUND.REORDER_BUFFER
- CPU_CLK_UNHALTED.CORE

## 5.13 <a id="metric_load_splits">Metric_Load_Splits</a>

Percentage of total non-speculative loads that are splits

- Threshold: True
- Area: Info.L1_Bound

```python
Load_Splits = 100 * MEM_UOPS_RETIRED.SPLIT_LOADS / MEM_UOPS_RETIRED.ALL_LOADS
Metric_Load_Splits = Load_Splits
```

- MEM_UOPS_RETIRED.ALL_LOADS
- MEM_UOPS_RETIRED.SPLIT_LOADS

## 5.14 <a id="metric_ipstore">Metric_IpStore</a>

Instructions per Store

- Threshold: True
- Area: Info.Inst_Mix

```python
IpStore = INST_RETIRED.ANY / MEM_UOPS_RETIRED.ALL_STORES
Metric_IpStore = IpStore
```

- INST_RETIRED.ANY
- MEM_UOPS_RETIRED.ALL_STORES

## 5.15 <a id="metric_turbo_utilization">Metric_Turbo_Utilization</a>

Average Frequency Utilization relative nominal frequency

- Threshold: True
- Area: Info.System

```python
CLKS = CPU_CLK_UNHALTED.CORE
Turbo_Utilization = CLKS / CPU_CLK_UNHALTED.REF_TSC
Metric_Turbo_Utilization = Turbo_Utilization
```

- CPU_CLK_UNHALTED.REF_TSC
- CPU_CLK_UNHALTED.CORE

## 5.16 <a id="non_mem_scheduler">Non_Mem_Scheduler</a>

Counts the number of issue slots that were not consumed by the backend due to IEC or FPC RAT stalls, which can be due to FIQ or IEC reservation stalls in which the integer, floating point or SIMD scheduler is not able to accept uops.

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Non_Mem_Scheduler = TOPDOWN_BE_BOUND.NON_MEM_SCHEDULER / SLOTS
```

- TOPDOWN_BE_BOUND.NON_MEM_SCHEDULER
- CPU_CLK_UNHALTED.CORE

## 5.17 <a id="backend_bound_aux">Backend_Bound_Aux</a>

Counts the total number of issue slots that were not consumed by the backend due to backend stalls. Note that UOPS must be available for consumption in order for this event to count. If a uop is not available (IQ is empty), this event will not count. All of these subevents count backend stalls, in slots, due to a resource limitation. These are not cycle based events and therefore can not be precisely added or subtracted from the Backend_Bound subevents which are cycle based. These subevents are supplementary to Backend_Bound and can be used to analyze results from a resource perspective at allocation.

- Domain: Slots
- Threshold:  > 0.2
- Area: BE_aux

```python
Backend_Bound_Aux = Backend_Bound
```

- [Backend_Bound](#backend_bound)

## 5.18 <a id="metric_upi">Metric_UPI</a>

Uops Per Instruction

- Threshold: True
- Area: Info.Core

```python
UPI = UOPS_RETIRED.ALL / INST_RETIRED.ANY
Metric_UPI = UPI
```

- UOPS_RETIRED.ALL
- INST_RETIRED.ANY

## 5.19 <a id="metric_memloadpki">Metric_MemLoadPKI</a>

load ops retired per 1000 instruction

- Threshold: True
- Area: Info.Memory

```python
MemLoadPKI = 1000 * MEM_UOPS_RETIRED.ALL_LOADS / INST_RETIRED.ANY
Metric_MemLoadPKI = MemLoadPKI
```

- MEM_UOPS_RETIRED.ALL_LOADS
- INST_RETIRED.ANY

## 5.20 <a id="metric_fpdiv_uop_ratio">Metric_FPDiv_Uop_Ratio</a>

Percentage of all uops which are FPDiv uops

- Threshold: True
- Area: Info.Inst_Mix

```python
FPDiv_Uop_Ratio = 100 * UOPS_RETIRED.FPDIV / UOPS_RETIRED.ALL
Metric_FPDiv_Uop_Ratio = FPDiv_Uop_Ratio
```

- UOPS_RETIRED.ALL
- UOPS_RETIRED.FPDIV

## 5.21 <a id="ld_buffer">LD_Buffer</a>

Counts the number of cycles, relative to the number of mem_scheduler slots, in which uops are blocked due to load buffer full

- Domain: Count
- Threshold:  > 0.05
- Area: BE_aux

```python
LD_Buffer = Mem_Scheduler * MEM_SCHEDULER_BLOCK.LD_BUF / MEM_SCHEDULER_BLOCK.ALL
```

- MEM_SCHEDULER_BLOCK.ALL
- MEM_SCHEDULER_BLOCK.LD_BUF
- [Mem_Scheduler](#mem_scheduler)

## 5.22 <a id="metric_cycles_per_demand_load_l3_hit">Metric_Cycles_per_Demand_Load_L3_Hit</a>

Cycle cost per LLC hit

- Threshold: True
- Area: Info.Memory

```python
Cycles_per_Demand_Load_L3_Hit = MEM_BOUND_STALLS.LOAD_LLC_HIT / MEM_LOAD_UOPS_RETIRED.L3_HIT
Metric_Cycles_per_Demand_Load_L3_Hit = Cycles_per_Demand_Load_L3_Hit
```

- MEM_BOUND_STALLS.LOAD_LLC_HIT
- MEM_LOAD_UOPS_RETIRED.L3_HIT

## 5.23 <a id="metric_store_fwd_blocks">Metric_Store_Fwd_Blocks</a>

Percentage of total non-speculative loads with a store forward or unknown store address block

- Threshold: True
- Area: Info.L1_Bound

```python
Store_Fwd_Blocks = 100 * LD_BLOCKS.DATA_UNKNOWN / MEM_UOPS_RETIRED.ALL_LOADS
Metric_Store_Fwd_Blocks = Store_Fwd_Blocks
```

- MEM_UOPS_RETIRED.ALL_LOADS
- LD_BLOCKS.DATA_UNKNOWN

## 5.24 <a id="metric_ipfarbranch">Metric_IpFarBranch</a>

Instructions per Far Branch

- Threshold: True
- Area: Info.Inst_Mix

```python
IpFarBranch = INST_RETIRED.ANY / (BR_INST_RETIRED.FAR_BRANCH / 2)
Metric_IpFarBranch = IpFarBranch
```

- INST_RETIRED.ANY
- BR_INST_RETIRED.FAR_BRANCH

## 5.25 <a id="metric_kernel_utilization">Metric_Kernel_Utilization</a>

Fraction of cycles spent in Kernel mode

- Threshold: True
- Area: Info.System

```python
Kernel_Utilization = CPU_CLK_UNHALTED.CORE:sup / CPU_CLK_UNHALTED.CORE
Metric_Kernel_Utilization = Kernel_Utilization
```

- CPU_CLK_UNHALTED.CORE:sup
- CPU_CLK_UNHALTED.CORE

## 5.26 <a id="metric_cpu_utilization">Metric_CPU_Utilization</a>

Average CPU Utilization

- Threshold: True
- Area: Info.System

```python
CPU_Utilization = CPU_CLK_UNHALTED.REF_TSC / msr/tsc/
Metric_CPU_Utilization = CPU_Utilization
```

- CPU_CLK_UNHALTED.REF_TSC
- msr/tsc/

## 5.27 <a id="metric_branch_mispredict_ratio">Metric_Branch_Mispredict_Ratio</a>

Ratio of all branches which mispredict

- Threshold: True
- Area: Info.Inst_Mix

```python
Branch_Mispredict_Ratio = BR_MISP_RETIRED.ALL_BRANCHES / BR_INST_RETIRED.ALL_BRANCHES
Metric_Branch_Mispredict_Ratio = Branch_Mispredict_Ratio
```

- BR_MISP_RETIRED.ALL_BRANCHES
- BR_INST_RETIRED.ALL_BRANCHES

## 5.28 <a id="metric_clks_p">Metric_CLKS_P</a>

- Domain: Cycles
- Threshold: True
- Area: Info.Core

```python
CLKS_P = CPU_CLK_UNHALTED.CORE_P
Metric_CLKS_P = CLKS_P
```

- CPU_CLK_UNHALTED.CORE_P

## 5.29 <a id="metric_ipc">Metric_IPC</a>

Instructions Per Cycle

- Threshold: True
- Area: Info.Core

```python
CLKS = CPU_CLK_UNHALTED.CORE
IPC = INST_RETIRED.ANY / CLKS
Metric_IPC = IPC
```

- CPU_CLK_UNHALTED.CORE
- INST_RETIRED.ANY

## 5.30 <a id="rsv">RSV</a>

Counts the number of cycles, relative to the number of mem_scheduler slots, in which uops are blocked due to RSV full relative

- Domain: Count
- Threshold:  > 0.05
- Area: BE_aux

```python
RSV = Mem_Scheduler * MEM_SCHEDULER_BLOCK.RSV / MEM_SCHEDULER_BLOCK.ALL
```

- MEM_SCHEDULER_BLOCK.ALL
- MEM_SCHEDULER_BLOCK.RSV
- [Mem_Scheduler](#mem_scheduler)

## 5.31 <a id="metric_inst_miss_cost_l2hit_percent">Metric_Inst_Miss_Cost_L2Hit_Percent</a>

Percent of instruction miss cost that hit in the L2

- Threshold: True
- Area: Info.Frontend

```python
Inst_Miss_Cost_L2Hit_Percent = 100 * MEM_BOUND_STALLS.IFETCH_L2_HIT / MEM_BOUND_STALLS.IFETCH
Metric_Inst_Miss_Cost_L2Hit_Percent = Inst_Miss_Cost_L2Hit_Percent
```

- MEM_BOUND_STALLS.IFETCH
- MEM_BOUND_STALLS.IFETCH_L2_HIT

## 5.32 <a id="resource_bound">Resource_Bound</a>

Counts the total number of issue slots that were not consumed by the backend due to backend stalls. Note that uops must be available for consumption in order for this event to count. If a uop is not available (IQ is empty), this event will not count.

- Domain: Slots
- Threshold:  > 0.2
- Area: BE_aux

```python
Resource_Bound = Backend_Bound
```

- [Backend_Bound](#backend_bound)

## 5.33 <a id="metric_cycles_per_demand_load_l2_hit">Metric_Cycles_per_Demand_Load_L2_Hit</a>

Cycle cost per L2 hit

- Threshold: True
- Area: Info.Memory

```python
Cycles_per_Demand_Load_L2_Hit = MEM_BOUND_STALLS.LOAD_L2_HIT / MEM_LOAD_UOPS_RETIRED.L2_HIT
Metric_Cycles_per_Demand_Load_L2_Hit = Cycles_per_Demand_Load_L2_Hit
```

- MEM_LOAD_UOPS_RETIRED.L2_HIT
- MEM_BOUND_STALLS.LOAD_L2_HIT

## 5.34 <a id="metric_branch_mispredict_to_unknown_branch_ratio">Metric_Branch_Mispredict_to_Unknown_Branch_Ratio</a>

Ratio between Mispredicted branches and unknown branches

- Threshold: True
- Area: Info.Inst_Mix

```python
Branch_Mispredict_to_Unknown_Branch_Ratio = BR_MISP_RETIRED.ALL_BRANCHES / BACLEARS.ANY
Metric_Branch_Mispredict_to_Unknown_Branch_Ratio = Branch_Mispredict_to_Unknown_Branch_Ratio
```

- BR_MISP_RETIRED.ALL_BRANCHES
- BACLEARS.ANY

## 5.35 <a id="metric_ipbranch">Metric_IpBranch</a>

Instructions per Branch (lower number means higher occurance rate)

- Threshold: True
- Area: Info.Inst_Mix

```python
IpBranch = INST_RETIRED.ANY / BR_INST_RETIRED.ALL_BRANCHES
Metric_IpBranch = IpBranch
```

- BR_INST_RETIRED.ALL_BRANCHES
- INST_RETIRED.ANY

## 5.36 <a id="serialization">Serialization</a>

Counts the number of issue slots that were not consumed by the backend due to scoreboards from the instruction queue (IQ), jump execution unit (JEU), or microcode sequencer (MS).

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Serialization = TOPDOWN_BE_BOUND.SERIALIZATION / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_BE_BOUND.SERIALIZATION

## 5.37 <a id="metric_x87_uop_ratio">Metric_X87_Uop_Ratio</a>

Percentage of all uops which are x87 uops

- Threshold: True
- Area: Info.Inst_Mix

```python
X87_Uop_Ratio = 100 * UOPS_RETIRED.X87 / UOPS_RETIRED.ALL
Metric_X87_Uop_Ratio = X87_Uop_Ratio
```

- UOPS_RETIRED.ALL
- UOPS_RETIRED.X87

## 5.38 <a id="metric_clks">Metric_CLKS</a>

- Domain: Cycles
- Threshold: True
- Area: Info.Core

```python
CLKS = CPU_CLK_UNHALTED.CORE
Metric_CLKS = CLKS
```

- CPU_CLK_UNHALTED.CORE

## 5.39 <a id="mem_scheduler">Mem_Scheduler</a>

Counts the number of issue slots that were not consumed by the backend due to memory reservation stalls in which a scheduler is not able to accept uops.

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Mem_Scheduler = TOPDOWN_BE_BOUND.MEM_SCHEDULER / SLOTS
```

- TOPDOWN_BE_BOUND.MEM_SCHEDULER
- CPU_CLK_UNHALTED.CORE

## 5.40 <a id="metric_inst_miss_cost_dramhit_percent">Metric_Inst_Miss_Cost_DRAMHit_Percent</a>

Percent of instruction miss cost that hit in DRAM

- Threshold: True
- Area: Info.Frontend

```python
Inst_Miss_Cost_DRAMHit_Percent = 100 * MEM_BOUND_STALLS.IFETCH_DRAM_HIT / MEM_BOUND_STALLS.IFETCH
Metric_Inst_Miss_Cost_DRAMHit_Percent = Inst_Miss_Cost_DRAMHit_Percent
```

- MEM_BOUND_STALLS.IFETCH
- MEM_BOUND_STALLS.IFETCH_DRAM_HIT

## 5.41 <a id="metric_ipmispredict">Metric_IpMispredict</a>

Number of Instructions per non-speculative Branch Misprediction

- Threshold: True
- Area: Info.Inst_Mix

```python
IpMispredict = INST_RETIRED.ANY / BR_MISP_RETIRED.ALL_BRANCHES
Metric_IpMispredict = IpMispredict
```

- BR_MISP_RETIRED.ALL_BRANCHES
- INST_RETIRED.ANY

## 5.42 <a id="metric_address_alias_blocks">Metric_Address_Alias_Blocks</a>

Percentage of total non-speculative loads with a address aliasing block

- Threshold: True
- Area: Info.L1_Bound

```python
Address_Alias_Blocks = 100 * LD_BLOCKS.4K_ALIAS / MEM_UOPS_RETIRED.ALL_LOADS
Metric_Address_Alias_Blocks = Address_Alias_Blocks
```

- MEM_UOPS_RETIRED.ALL_LOADS
- LD_BLOCKS.4K_ALIAS

## 5.43 <a id="alloc_restriction">Alloc_Restriction</a>

Counts the number of issue slots that were not consumed by the backend due to certain allocation restrictions.

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 5
SLOTS = Pipeline_Width * CLKS
Alloc_Restriction = TOPDOWN_BE_BOUND.ALLOC_RESTRICTIONS / SLOTS
```

- TOPDOWN_BE_BOUND.ALLOC_RESTRICTIONS
- CPU_CLK_UNHALTED.CORE

