# 1 <a id="bad_speculation">Bad_Speculation</a>

Counts the total number of issue slots that were not consumed by the backend because allocation is stalled due to a mispredicted jump or a machine clear. Only issue slots wasted due to fast nukes such as memory ordering nukes are counted. Other nukes are not accounted for. Counts all issue slots blocked during this recovery window including relevant microcode flows and while uops are not yet available in the instruction queue (IQ). Also includes the issue slots that were consumed by the backend but were thrown away because they were younger than the mispredict or machine clear.

- Domain: Slots
- Threshold:  > 0.15
- Area: BAD

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Bad_Speculation = (TOPDOWN_BAD_SPECULATION.MISPREDICT + TOPDOWN_BAD_SPECULATION.MONUKE) / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_BAD_SPECULATION.MONUKE
- TOPDOWN_BAD_SPECULATION.MISPREDICT

## 1.1 <a id="branch_mispredicts">Branch_Mispredicts</a>

Counts the number of issue slots that were not consumed by the backend due to branch mispredicts.

- Domain: Slots
- Threshold:  > 0.05
- Area: BAD

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Branch_Mispredicts = TOPDOWN_BAD_SPECULATION.MISPREDICT / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_BAD_SPECULATION.MISPREDICT

## 1.2 <a id="machine_clears">Machine_Clears</a>

Counts the total number of issue slots that were not consumed by the backend because allocation is stalled due to a machine clear (nuke) of any kind including memory ordering and memory disambiguation.

- Domain: Slots
- Threshold:  > 0.05
- Area: BAD

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Machine_Clears = TOPDOWN_BAD_SPECULATION.MONUKE / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_BAD_SPECULATION.MONUKE

### 1.2.1 <a id="fast_nuke">Fast_Nuke</a>

Counts the number of issue slots that were not consumed by the backend due to a machine clear classified as a fast nuke due to memory ordering, memory disambiguation and memory renaming.

- Domain: Slots
- Threshold:  > 0.05
- Area: BAD

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Fast_Nuke = TOPDOWN_BAD_SPECULATION.MONUKE / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_BAD_SPECULATION.MONUKE

# 2 <a id="backend_bound">Backend_Bound</a>

Counts the total number of issue slots that were not consumed by the backend due to backend stalls. Note that uops must be available for consumption in order for this event to count. If a uop is not available (IQ is empty), this event will not count. The rest of these subevents count backend stalls, in cycles, due to an outstanding request which is memory bound vs core bound. The subevents are not slot based events and therefore can not be precisely added or subtracted from the Backend_Bound_Aux subevents which are slot based.

- Domain: Slots
- Threshold:  > 0.1
- Area: BE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Backend_Bound = TOPDOWN_BE_BOUND.ALL / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_BE_BOUND.ALL

## 2.1 <a id="load_store_bound">Load_Store_Bound</a>

Counts the number of cycles the core is stalled due to stores or loads.

- Domain: Cycles
- Threshold:  > 0.2
- Area: BE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Load_Store_Bound = (MEM_BOUND_STALLS.LOAD_L2_HIT + MEM_BOUND_STALLS.LOAD_LLC_HIT + MEM_BOUND_STALLS.LOAD_DRAM_HIT) / CLKS
```

- MEM_BOUND_STALLS.LOAD_L2_HIT
- MEM_BOUND_STALLS.LOAD_LLC_HIT
- CPU_CLK_UNHALTED.CORE
- MEM_BOUND_STALLS.LOAD_DRAM_HIT

### 2.1.1 <a id="l2_bound">L2_Bound</a>

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

### 2.1.2 <a id="l3_bound">L3_Bound</a>

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

### 2.1.3 <a id="dram_bound">DRAM_Bound</a>

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

# 3 <a id="retiring">Retiring</a>

Counts the numer of issue slots that result in retirement slots.

- Domain: Slots
- Threshold:  > 0.75
- Area: RET

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Retiring = TOPDOWN_RETIRING.ALL / SLOTS
```

- TOPDOWN_RETIRING.ALL
- CPU_CLK_UNHALTED.CORE

## 3.1 <a id="base">Base</a>

Counts the number of uops that are not from the microsequencer.

- Domain: Slots
- Threshold:  > 0.6
- Area: RET

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Base = (TOPDOWN_RETIRING.ALL - UOPS_RETIRED.MS) / SLOTS
```

- TOPDOWN_RETIRING.ALL
- CPU_CLK_UNHALTED.CORE
- UOPS_RETIRED.MS

### 3.1.1 <a id="fp_uops">FP_uops</a>

Counts the number of floating point divide uops retired (x87 and SSE, including x87 sqrt).

- Domain: Slots
- Threshold:  > 0.2
- Area: RET

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
FP_uops = UOPS_RETIRED.FPDIV / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- UOPS_RETIRED.FPDIV

### 3.1.2 <a id="other_ret">Other_Ret</a>

Counts the number of uops retired excluding ms and fp div uops.

- Domain: Slots
- Threshold:  > 0.3
- Area: RET

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Other_Ret = (TOPDOWN_RETIRING.ALL - UOPS_RETIRED.MS - UOPS_RETIRED.FPDIV) / SLOTS
```

- TOPDOWN_RETIRING.ALL
- CPU_CLK_UNHALTED.CORE
- UOPS_RETIRED.MS
- UOPS_RETIRED.FPDIV

## 3.2 <a id="ms_uops">MS_uops</a>

Counts the number of uops that are from the complex flows issued by the micro-sequencer (MS). This includes uops from flows due to complex instructions, faults, assists, and inserted flows.

- Domain: Slots
- Threshold:  > 0.05
- Area: RET

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
MS_uops = UOPS_RETIRED.MS / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- UOPS_RETIRED.MS

# 4 General Metrics

## 4.1 <a id="metric_cpi">Metric_CPI</a>

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

## 4.2 <a id="metric_ipcall">Metric_IpCall</a>

Instruction per (near) call (lower number means higher occurance rate)

- Threshold: True
- Area: Info.Inst_Mix

```python
IpCall = INST_RETIRED.ANY / BR_INST_RETIRED.CALL
Metric_IpCall = IpCall
```

- INST_RETIRED.ANY
- BR_INST_RETIRED.CALL

## 4.3 <a id="metric_ipload">Metric_IpLoad</a>

Instructions per Load

- Threshold: True
- Area: Info.Inst_Mix

```python
IpLoad = INST_RETIRED.ANY / MEM_UOPS_RETIRED.ALL_LOADS
Metric_IpLoad = IpLoad
```

- MEM_UOPS_RETIRED.ALL_LOADS
- INST_RETIRED.ANY

## 4.4 <a id="metric_idiv_uop_ratio">Metric_IDiv_Uop_Ratio</a>

Percentage of all uops which are IDiv uops

- Threshold: True
- Area: Info.Inst_Mix

```python
IDiv_Uop_Ratio = 100 * UOPS_RETIRED.IDIV / UOPS_RETIRED.ALL
Metric_IDiv_Uop_Ratio = IDiv_Uop_Ratio
```

- UOPS_RETIRED.IDIV
- UOPS_RETIRED.ALL

## 4.5 <a id="metric_cycles_per_demand_load_dram_hit">Metric_Cycles_per_Demand_Load_DRAM_Hit</a>

Cycle cost per DRAM hit

- Threshold: True
- Area: Info.Memory

```python
Cycles_per_Demand_Load_DRAM_Hit = MEM_BOUND_STALLS.LOAD_DRAM_HIT / MEM_LOAD_UOPS_RETIRED.DRAM_HIT
Metric_Cycles_per_Demand_Load_DRAM_Hit = Cycles_per_Demand_Load_DRAM_Hit
```

- MEM_LOAD_UOPS_RETIRED.DRAM_HIT
- MEM_BOUND_STALLS.LOAD_DRAM_HIT

## 4.6 <a id="metric_slots">Metric_SLOTS</a>

- Domain: Cycles
- Threshold: True
- Area: Info.Core

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Metric_SLOTS = SLOTS
```

- CPU_CLK_UNHALTED.CORE

## 4.7 <a id="metric_microcode_uop_ratio">Metric_Microcode_Uop_Ratio</a>

Percentage of all uops which are ucode ops

- Threshold: True
- Area: Info.Inst_Mix

```python
Microcode_Uop_Ratio = 100 * UOPS_RETIRED.MS / UOPS_RETIRED.ALL
Metric_Microcode_Uop_Ratio = Microcode_Uop_Ratio
```

- UOPS_RETIRED.ALL
- UOPS_RETIRED.MS

## 4.8 <a id="register">Register</a>

Counts the number of issue slots that were not consumed by the backend due to the physical register file unable to accept an entry (marble stalls).

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Register = TOPDOWN_BE_BOUND.REGISTER / SLOTS
```

- TOPDOWN_BE_BOUND.REGISTER
- CPU_CLK_UNHALTED.CORE

## 4.9 <a id="reorder_buffer">Reorder_Buffer</a>

Counts the number of issue slots that were not consumed by the backend due to the reorder buffer being full (ROB stalls).

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Reorder_Buffer = TOPDOWN_BE_BOUND.REORDER_BUFFER / SLOTS
```

- TOPDOWN_BE_BOUND.REORDER_BUFFER
- CPU_CLK_UNHALTED.CORE

## 4.10 <a id="metric_load_splits">Metric_Load_Splits</a>

Percentage of total non-speculative loads that are splits

- Threshold: True
- Area: Info.L1_Bound

```python
Load_Splits = 100 * MEM_UOPS_RETIRED.SPLIT_LOADS / MEM_UOPS_RETIRED.ALL_LOADS
Metric_Load_Splits = Load_Splits
```

- MEM_UOPS_RETIRED.ALL_LOADS
- MEM_UOPS_RETIRED.SPLIT_LOADS

## 4.11 <a id="metric_ipstore">Metric_IpStore</a>

Instructions per Store

- Threshold: True
- Area: Info.Inst_Mix

```python
IpStore = INST_RETIRED.ANY / MEM_UOPS_RETIRED.ALL_STORES
Metric_IpStore = IpStore
```

- INST_RETIRED.ANY
- MEM_UOPS_RETIRED.ALL_STORES

## 4.12 <a id="metric_turbo_utilization">Metric_Turbo_Utilization</a>

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

## 4.13 <a id="non_mem_scheduler">Non_Mem_Scheduler</a>

Counts the number of issue slots that were not consumed by the backend due to IEC or FPC RAT stalls, which can be due to FIQ or IEC reservation stalls in which the integer, floating point or SIMD scheduler is not able to accept uops.

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Non_Mem_Scheduler = TOPDOWN_BE_BOUND.NON_MEM_SCHEDULER / SLOTS
```

- TOPDOWN_BE_BOUND.NON_MEM_SCHEDULER
- CPU_CLK_UNHALTED.CORE

## 4.14 <a id="backend_bound_aux">Backend_Bound_Aux</a>

Counts the total number of issue slots that were not consumed by the backend due to backend stalls. Note that UOPS must be available for consumption in order for this event to count. If a uop is not available (IQ is empty), this event will not count. All of these subevents count backend stalls, in slots, due to a resource limitation. These are not cycle based events and therefore can not be precisely added or subtracted from the Backend_Bound subevents which are cycle based. These subevents are supplementary to Backend_Bound and can be used to analyze results from a resource perspective at allocation.

- Domain: Slots
- Threshold:  > 0.2
- Area: BE_aux

```python
Backend_Bound_Aux = Backend_Bound
```

- [Backend_Bound](#backend_bound)

## 4.15 <a id="metric_upi">Metric_UPI</a>

Uops Per Instruction

- Threshold: True
- Area: Info.Core

```python
UPI = UOPS_RETIRED.ALL / INST_RETIRED.ANY
Metric_UPI = UPI
```

- UOPS_RETIRED.ALL
- INST_RETIRED.ANY

## 4.16 <a id="metric_memloadpki">Metric_MemLoadPKI</a>

load ops retired per 1000 instruction

- Threshold: True
- Area: Info.Memory

```python
MemLoadPKI = 1000 * MEM_UOPS_RETIRED.ALL_LOADS / INST_RETIRED.ANY
Metric_MemLoadPKI = MemLoadPKI
```

- MEM_UOPS_RETIRED.ALL_LOADS
- INST_RETIRED.ANY

## 4.17 <a id="metric_fpdiv_uop_ratio">Metric_FPDiv_Uop_Ratio</a>

Percentage of all uops which are FPDiv uops

- Threshold: True
- Area: Info.Inst_Mix

```python
FPDiv_Uop_Ratio = 100 * UOPS_RETIRED.FPDIV / UOPS_RETIRED.ALL
Metric_FPDiv_Uop_Ratio = FPDiv_Uop_Ratio
```

- UOPS_RETIRED.ALL
- UOPS_RETIRED.FPDIV

## 4.18 <a id="metric_cycles_per_demand_load_l3_hit">Metric_Cycles_per_Demand_Load_L3_Hit</a>

Cycle cost per LLC hit

- Threshold: True
- Area: Info.Memory

```python
Cycles_per_Demand_Load_L3_Hit = MEM_BOUND_STALLS.LOAD_LLC_HIT / MEM_LOAD_UOPS_RETIRED.L3_HIT
Metric_Cycles_per_Demand_Load_L3_Hit = Cycles_per_Demand_Load_L3_Hit
```

- MEM_BOUND_STALLS.LOAD_LLC_HIT
- MEM_LOAD_UOPS_RETIRED.L3_HIT

## 4.19 <a id="metric_store_fwd_blocks">Metric_Store_Fwd_Blocks</a>

Percentage of total non-speculative loads with a store forward or unknown store address block

- Threshold: True
- Area: Info.L1_Bound

```python
Store_Fwd_Blocks = 100 * LD_BLOCKS.DATA_UNKNOWN / MEM_UOPS_RETIRED.ALL_LOADS
Metric_Store_Fwd_Blocks = Store_Fwd_Blocks
```

- MEM_UOPS_RETIRED.ALL_LOADS
- LD_BLOCKS.DATA_UNKNOWN

## 4.20 <a id="metric_ipfarbranch">Metric_IpFarBranch</a>

Instructions per Far Branch

- Threshold: True
- Area: Info.Inst_Mix

```python
IpFarBranch = INST_RETIRED.ANY / (BR_INST_RETIRED.FAR_BRANCH / 2)
Metric_IpFarBranch = IpFarBranch
```

- INST_RETIRED.ANY
- BR_INST_RETIRED.FAR_BRANCH

## 4.21 <a id="metric_kernel_utilization">Metric_Kernel_Utilization</a>

Fraction of cycles spent in Kernel mode

- Threshold: True
- Area: Info.System

```python
Kernel_Utilization = CPU_CLK_UNHALTED.CORE_P:sup / CPU_CLK_UNHALTED.CORE_P
Metric_Kernel_Utilization = Kernel_Utilization
```

- CPU_CLK_UNHALTED.CORE_P
- CPU_CLK_UNHALTED.CORE_P:sup

## 4.22 <a id="metric_cpu_utilization">Metric_CPU_Utilization</a>

Average CPU Utilization

- Threshold: True
- Area: Info.System

```python
CPU_Utilization = CPU_CLK_UNHALTED.REF_TSC / msr/tsc/
Metric_CPU_Utilization = CPU_Utilization
```

- CPU_CLK_UNHALTED.REF_TSC
- msr/tsc/

## 4.23 <a id="store_buffer">Store_Buffer</a>

Counts the number of issue slots that were not consumed by the backend due to store buffers stalls.

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Store_Buffer = TOPDOWN_BE_BOUND.STORE_BUFFER / SLOTS
```

- TOPDOWN_BE_BOUND.STORE_BUFFER
- CPU_CLK_UNHALTED.CORE

## 4.24 <a id="metric_branch_mispredict_ratio">Metric_Branch_Mispredict_Ratio</a>

Ratio of all branches which mispredict

- Threshold: True
- Area: Info.Inst_Mix

```python
Branch_Mispredict_Ratio = BR_MISP_RETIRED.ALL_BRANCHES / BR_INST_RETIRED.ALL_BRANCHES
Metric_Branch_Mispredict_Ratio = Branch_Mispredict_Ratio
```

- BR_MISP_RETIRED.ALL_BRANCHES
- BR_INST_RETIRED.ALL_BRANCHES

## 4.25 <a id="metric_clks_p">Metric_CLKS_P</a>

- Domain: Cycles
- Threshold: True
- Area: Info.Core

```python
CLKS_P = CPU_CLK_UNHALTED.CORE_P
Metric_CLKS_P = CLKS_P
```

- CPU_CLK_UNHALTED.CORE_P

## 4.26 <a id="metric_ipc">Metric_IPC</a>

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

## 4.27 <a id="frontend_bound">Frontend_Bound</a>

Counts the number of issue slots that were not consumed by the backend due to frontend stalls.

- Domain: Slots
- Threshold:  > 0.2
- Area: FE

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Frontend_Bound = TOPDOWN_FE_BOUND.ALL / SLOTS
```

- TOPDOWN_FE_BOUND.ALL
- CPU_CLK_UNHALTED.CORE

## 4.28 <a id="resource_bound">Resource_Bound</a>

Counts the total number of issue slots that were not consumed by the backend due to backend stalls. Note that uops must be available for consumption in order for this event to count. If a uop is not available (IQ is empty), this event will not count.

- Domain: Slots
- Threshold:  > 0.2
- Area: BE_aux

```python
Resource_Bound = Backend_Bound
```

- [Backend_Bound](#backend_bound)

## 4.29 <a id="metric_cycles_per_demand_load_l2_hit">Metric_Cycles_per_Demand_Load_L2_Hit</a>

Cycle cost per L2 hit

- Threshold: True
- Area: Info.Memory

```python
Cycles_per_Demand_Load_L2_Hit = MEM_BOUND_STALLS.LOAD_L2_HIT / MEM_LOAD_UOPS_RETIRED.L2_HIT
Metric_Cycles_per_Demand_Load_L2_Hit = Cycles_per_Demand_Load_L2_Hit
```

- MEM_LOAD_UOPS_RETIRED.L2_HIT
- MEM_BOUND_STALLS.LOAD_L2_HIT

## 4.30 <a id="metric_branch_mispredict_to_unknown_branch_ratio">Metric_Branch_Mispredict_to_Unknown_Branch_Ratio</a>

Ratio between Mispredicted branches and unknown branches

- Threshold: True
- Area: Info.Inst_Mix

```python
Branch_Mispredict_to_Unknown_Branch_Ratio = BR_MISP_RETIRED.ALL_BRANCHES / BACLEARS.ANY
Metric_Branch_Mispredict_to_Unknown_Branch_Ratio = Branch_Mispredict_to_Unknown_Branch_Ratio
```

- BR_MISP_RETIRED.ALL_BRANCHES
- BACLEARS.ANY

## 4.31 <a id="serialization">Serialization</a>

Counts the number of issue slots that were not consumed by the backend due to scoreboards from the instruction queue (IQ), jump execution unit (JEU), or microcode sequencer (MS).

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Serialization = TOPDOWN_BE_BOUND.SERIALIZATION / SLOTS
```

- CPU_CLK_UNHALTED.CORE
- TOPDOWN_BE_BOUND.SERIALIZATION

## 4.32 <a id="metric_ipbranch">Metric_IpBranch</a>

Instructions per Branch (lower number means higher occurance rate)

- Threshold: True
- Area: Info.Inst_Mix

```python
IpBranch = INST_RETIRED.ANY / BR_INST_RETIRED.ALL_BRANCHES
Metric_IpBranch = IpBranch
```

- BR_INST_RETIRED.ALL_BRANCHES
- INST_RETIRED.ANY

## 4.33 <a id="metric_clks">Metric_CLKS</a>

- Domain: Cycles
- Threshold: True
- Area: Info.Core

```python
CLKS = CPU_CLK_UNHALTED.CORE
Metric_CLKS = CLKS
```

- CPU_CLK_UNHALTED.CORE

## 4.34 <a id="mem_scheduler">Mem_Scheduler</a>

Counts the number of issue slots that were not consumed by the backend due to memory reservation stalls in which a scheduler is not able to accept uops.

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Mem_Scheduler = TOPDOWN_BE_BOUND.MEM_SCHEDULER / SLOTS
```

- TOPDOWN_BE_BOUND.MEM_SCHEDULER
- CPU_CLK_UNHALTED.CORE

## 4.35 <a id="metric_ipmispredict">Metric_IpMispredict</a>

Number of Instructions per non-speculative Branch Misprediction

- Threshold: True
- Area: Info.Inst_Mix

```python
IpMispredict = INST_RETIRED.ANY / BR_MISP_RETIRED.ALL_BRANCHES
Metric_IpMispredict = IpMispredict
```

- BR_MISP_RETIRED.ALL_BRANCHES
- INST_RETIRED.ANY

## 4.36 <a id="metric_address_alias_blocks">Metric_Address_Alias_Blocks</a>

Percentage of total non-speculative loads with a address aliasing block

- Threshold: True
- Area: Info.L1_Bound

```python
Address_Alias_Blocks = 100 * LD_BLOCKS.4K_ALIAS / MEM_UOPS_RETIRED.ALL_LOADS
Metric_Address_Alias_Blocks = Address_Alias_Blocks
```

- MEM_UOPS_RETIRED.ALL_LOADS
- LD_BLOCKS.4K_ALIAS

## 4.37 <a id="alloc_restriction">Alloc_Restriction</a>

Counts the number of issue slots that were not consumed by the backend due to certain allocation restrictions.

- Domain: Slots
- Threshold:  > 0.1
- Area: BE_aux

```python
CLKS = CPU_CLK_UNHALTED.CORE
Pipeline_Width = 4
SLOTS = Pipeline_Width * CLKS
Alloc_Restriction = TOPDOWN_BE_BOUND.ALLOC_RESTRICTIONS / SLOTS
```

- TOPDOWN_BE_BOUND.ALLOC_RESTRICTIONS
- CPU_CLK_UNHALTED.CORE

