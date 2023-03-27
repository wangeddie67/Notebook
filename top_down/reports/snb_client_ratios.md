# 1 <a id="frontend_bound">Frontend_Bound</a>

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
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- IDQ_UOPS_NOT_DELIVERED.CORE

## 1.1 <a id="fetch_latency">Fetch_Latency</a>

This metric represents fraction of slots the CPU was stalled due to Frontend latency issues. For example; instruction- cache misses; iTLB misses or fetch stalls after a branch misprediction are categorized under Frontend Latency. In such cases; the Frontend eventually delivers no uops for some period.

- Domain: Slots
- Threshold:  > 0.1 and parent over threshold
- Area: FE
- Metric group: Frontend, TmaL2
- sample: RS_EVENTS.EMPTY_END

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Frontend_Latency_Cycles = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('IDQ_UOPS_NOT_DELIVERED.CYCLES_0_UOPS_DELIV.CORE', level)), level)
Fetch_Latency = Pipeline_Width * Frontend_Latency_Cycles / SLOTS
```

- level
- EV
- Pipeline_Width
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

### 1.1.1 <a id="itlb_misses">ITLB_Misses</a>

This metric represents fraction of cycles the CPU was stalled due to Instruction TLB (ITLB) misses.. Consider large 2M pages for code (selectively prefer hot large-size function, due to limited 2M entries). Linux options: standard binaries use libhugetlbfs; Hfsort.. https://github. com/libhugetlbfs/libhugetlbfs;https://research.fb.com/public ations/optimizing-function-placement-for-large-scale-data- center-applications-2/

- Domain: Clocks
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: BigFoot, FetchLat, MemoryTLB
- sample: ITLB_MISSES.WALK_COMPLETED

```python
ITLB_Miss_Cycles = 12 * ITLB_MISSES.STLB_HIT + ITLB_MISSES.WALK_DURATION
CLKS = CPU_CLK_UNHALTED.THREAD
ITLB_Misses = ITLB_Miss_Cycles / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- ITLB_MISSES.WALK_DURATION
- ITLB_MISSES.STLB_HIT

### 1.1.2 <a id="branch_resteers">Branch_Resteers</a>

This metric represents fraction of cycles the CPU was stalled due to Branch Resteers. Branch Resteers estimates the Frontend delay in fetching operations from corrected path; following all sorts of miss-predicted branches. For example; branchy code with lots of miss-predictions might get categorized under Branch Resteers. Note the value of this node may overlap with its siblings.

- Domain: Clocks_Estimated
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: FetchLat
- sample: BR_MISP_RETIRED.ALL_BRANCHES

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Branch_Resteers = BAClear_Cost * (BR_MISP_RETIRED.ALL_BRANCHES + MACHINE_CLEARS.COUNT + BACLEARS.ANY) / CLKS
```

- MACHINE_CLEARS.COUNT
- BACLEARS.ANY
- BAClear_Cost
- BR_MISP_RETIRED.ALL_BRANCHES
- CPU_CLK_UNHALTED.THREAD

### 1.1.3 <a id="dsb_switches">DSB_Switches</a>

This metric represents fraction of cycles the CPU was stalled due to switches from DSB to MITE pipelines. The DSB (decoded i-cache) is a Uop Cache where the front-end directly delivers Uops (micro operations) avoiding heavy x86 decoding. The DSB pipeline has shorter latency and delivered higher bandwidth than the MITE (legacy instruction decode pipeline). Switching between the two pipelines can cause penalties hence this metric measures the exposed penalty.. See section 'Optimization for Decoded Icache' in Optimization Manual:. http://www.intel.com/content/www/us/en /architecture-and-technology/64-ia-32-architectures- optimization-manual.html

- Domain: Clocks
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: DSBmiss, FetchLat

```python
CLKS = CPU_CLK_UNHALTED.THREAD
DSB_Switches = DSB2MITE_SWITCHES.PENALTY_CYCLES / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- DSB2MITE_SWITCHES.PENALTY_CYCLES

### 1.1.4 <a id="lcp">LCP</a>

This metric represents fraction of cycles CPU was stalled due to Length Changing Prefixes (LCPs). Using proper compiler flags or Intel Compiler by default will certainly avoid this.

- Domain: Clocks
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: FetchLat

```python
CLKS = CPU_CLK_UNHALTED.THREAD
LCP = ILD_STALL.LCP / CLKS
```

- ILD_STALL.LCP
- CPU_CLK_UNHALTED.THREAD

### 1.1.5 <a id="ms_switches">MS_Switches</a>

This metric estimates the fraction of cycles when the CPU was stalled due to switches of uop delivery to the Microcode Sequencer (MS). Commonly used instructions are optimized for delivery by the DSB (decoded i-cache) or MITE (legacy instruction decode) pipelines. Certain operations cannot be handled natively by the execution pipeline; and must be performed by microcode (small programs injected into the execution stream). Switching to the MS too often can negatively impact performance. The MS is designated to deliver long uop flows required by CISC instructions like CPUID; or uncommon conditions like Floating Point Assists when dealing with Denormals.

- Domain: Clocks
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: FetchLat, MicroSeq
- sample: IDQ.MS_SWITCHES

```python
CLKS = CPU_CLK_UNHALTED.THREAD
MS_Switches = MS_Switches_Cost * IDQ.MS_SWITCHES / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- IDQ.MS_SWITCHES
- MS_Switches_Cost

## 1.2 <a id="fetch_bandwidth">Fetch_Bandwidth</a>

This metric represents fraction of slots the CPU was stalled due to Frontend bandwidth issues. For example; inefficiencies at the instruction decoders; or restrictions for caching in the DSB (decoded uops cache) are categorized under Fetch Bandwidth. In such cases; the Frontend typically delivers suboptimal amount of uops to the Backend.

- Domain: Slots
- Threshold:  > 0.1 and parent over threshold and HighIPC
- Area: FE
- Metric group: FetchBW, Frontend, TmaL2

```python
Fetch_Bandwidth = Frontend_Bound - Fetch_Latency
```

- [Fetch_Latency](#fetch_latency)
- [Frontend_Bound](#frontend_bound)

# 2 <a id="bad_speculation">Bad_Speculation</a>

This category represents fraction of slots wasted due to incorrect speculations. This include slots used to issue uops that do not eventually get retired and slots for which the issue-pipeline was blocked due to recovery from earlier incorrect speculation. For example; wasted work due to miss- predicted branches are categorized under Bad Speculation category. Incorrect data speculation followed by Memory Ordering Nukes is another example.

- Domain: Slots
- Threshold:  > 0.15
- Area: BAD
- Metric group: TmaL1

```python
Recovery_Cycles = INT_MISC.RECOVERY_CYCLES_ANY / 2 if smt_enabled else INT_MISC.RECOVERY_CYCLES
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Bad_Speculation = (UOPS_ISSUED.ANY - Retired_Slots + Pipeline_Width * Recovery_Cycles) / SLOTS
```

- UOPS_ISSUED.ANY
- Pipeline_Width
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- UOPS_RETIRED.RETIRE_SLOTS
- INT_MISC.RECOVERY_CYCLES_ANY
- INT_MISC.RECOVERY_CYCLES

## 2.1 <a id="branch_mispredicts">Branch_Mispredicts</a>

This metric represents fraction of slots the CPU has wasted due to Branch Misprediction. These slots are either wasted by uops fetched from an incorrectly speculated program path; or stalls when the out-of-order part of the machine needs to recover its state from a speculative path.. Using profile feedback in the compiler may help. Please see the Optimization Manual for general strategies for addressing branch misprediction issues.. http://www.intel.com/content/www/us/en/architecture-and- technology/64-ia-32-architectures-optimization-manual.html

- Domain: Slots
- Threshold:  > 0.1 and parent over threshold
- Area: BAD
- Metric group: BadSpec, BrMispredicts, TmaL2
- sample: BR_MISP_RETIRED.ALL_BRANCHES:pp

```python
Mispred_Clears_Fraction = BR_MISP_RETIRED.ALL_BRANCHES / (BR_MISP_RETIRED.ALL_BRANCHES + MACHINE_CLEARS.COUNT)
Branch_Mispredicts = Mispred_Clears_Fraction * Bad_Speculation
```

- [Bad_Speculation](#bad_speculation)
- BR_MISP_RETIRED.ALL_BRANCHES
- MACHINE_CLEARS.COUNT

## 2.2 <a id="machine_clears">Machine_Clears</a>

This metric represents fraction of slots the CPU has wasted due to Machine Clears. These slots are either wasted by uops fetched prior to the clear; or stalls the out-of-order portion of the machine needs to recover its state after the clear. For example; this can happen due to memory ordering Nukes (e.g. Memory Disambiguation) or Self-Modifying-Code (SMC) nukes.. See "Memory Disambiguation" in Optimization Manual and:. https://software.intel.com/sites/default/files/ m/d/4/1/d/8/sma.pdf

- Domain: Slots
- Threshold:  > 0.1 and parent over threshold
- Area: BAD
- Metric group: BadSpec, MachineClears, TmaL2
- sample: MACHINE_CLEARS.COUNT

```python
Machine_Clears = Bad_Speculation - Branch_Mispredicts
```

- [Branch_Mispredicts](#branch_mispredicts)
- [Bad_Speculation](#bad_speculation)

# 3 <a id="backend_bound">Backend_Bound</a>

This category represents fraction of slots where no uops are being delivered due to a lack of required resources for accepting new uops in the Backend. Backend is the portion of the processor core where the out-of-order scheduler dispatches ready uops into their respective execution units; and once completed these uops get retired according to program order. For example; stalls due to data-cache misses or stalls due to the divider unit being overloaded are both categorized under Backend Bound. Backend Bound is further divided into two main categories: Memory Bound and Core Bound.

- Domain: Slots
- Threshold:  > 0.2
- Area: BE
- Metric group: TmaL1

```python
Backend_Bound = 1 - (Frontend_Bound + Bad_Speculation + Retiring)
```

- [Bad_Speculation](#bad_speculation)
- [Retiring](#retiring)
- [Frontend_Bound](#frontend_bound)

## 3.1 <a id="memory_bound">Memory_Bound</a>

This metric represents fraction of slots the Memory subsystem within the Backend was a bottleneck. Memory Bound estimates fraction of slots where pipeline is likely stalled due to demand load or store instructions. This accounts mainly for (1) non-completed in-flight memory demand loads which coincides with execution units starvation; in addition to (2) cases where stores could impose backpressure on the pipeline when many of them get buffered at the same time (less common out of the two).

- Domain: Slots
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Mem
- Metric group: Backend, TmaL2

```python
STALLS_MEM_ANY = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('CYCLE_ACTIVITY.STALLS_L1D_PENDING', level)), level)
CLKS = CPU_CLK_UNHALTED.THREAD
IPC = INST_RETIRED.ANY / CLKS
Few_Uops_Executed_Threshold = UOPS_DISPATCHED.THREAD:c3 if IPC > 1.8 else UOPS_DISPATCHED.THREAD:c2
Frontend_RS_Empty_Cycles = RS_EVENTS.EMPTY_CYCLES if Fetch_Latency > 0.1 else 0
STALLS_TOTAL = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('CYCLE_ACTIVITY.CYCLES_NO_DISPATCH', level)), level)
Backend_Bound_Cycles = STALLS_TOTAL + UOPS_DISPATCHED.THREAD:c1 - Few_Uops_Executed_Threshold - Frontend_RS_Empty_Cycles + RESOURCE_STALLS.SB
Memory_Bound_Fraction = (STALLS_MEM_ANY + RESOURCE_STALLS.SB) / Backend_Bound_Cycles
Memory_Bound = Memory_Bound_Fraction * Backend_Bound
```

- [Backend_Bound](#backend_bound)
- RESOURCE_STALLS.SB
- level
- EV
- [Fetch_Latency](#fetch_latency)
- RS_EVENTS.EMPTY_CYCLES
- CPU_CLK_UNHALTED.THREAD
- INST_RETIRED.ANY
- UOPS_DISPATCHED.THREAD:c2
- UOPS_DISPATCHED.THREAD:c3
- UOPS_DISPATCHED.THREAD:c1

### 3.1.1 <a id="dtlb_load">DTLB_Load</a>

This metric roughly estimates the fraction of cycles where the Data TLB (DTLB) was missed by load accesses. TLBs (Translation Look-aside Buffers) are processor caches for recently used entries out of the Page Tables that are used to map virtual- to physical-addresses by the operating system. This metric approximates the potential delay of demand loads missing the first-level data TLB (assuming worst case scenario with back to back misses to different pages). This includes hitting in the second-level TLB (STLB) as well as performing a hardware page walk on an STLB miss..

- Domain: Clocks_Estimated
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryTLB
- sample: MEM_UOPS_RETIRED.STLB_MISS_LOADS:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
DTLB_Load = (Mem_STLB_Hit_Cost * DTLB_LOAD_MISSES.STLB_HIT + DTLB_LOAD_MISSES.WALK_DURATION) / CLKS
```

- DTLB_LOAD_MISSES.STLB_HIT
- DTLB_LOAD_MISSES.WALK_DURATION
- CPU_CLK_UNHALTED.THREAD
- Mem_STLB_Hit_Cost

### 3.1.2 <a id="l3_bound">L3_Bound</a>

This metric estimates how often the CPU was stalled due to loads accesses to L3 cache or contended with a sibling Core. Avoiding cache misses (i.e. L2 misses/L3 hits) can improve the latency and increase performance.

- Domain: Stalls
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: CacheMisses, MemoryBound, TmaL3mem
- sample: MEM_LOAD_UOPS_RETIRED.LLC_HIT:pp

```python
Mem_L3_Hit_Fraction = MEM_LOAD_UOPS_RETIRED.LLC_HIT / (MEM_LOAD_UOPS_RETIRED.LLC_HIT + Mem_L3_Weight * MEM_LOAD_UOPS_MISC_RETIRED.LLC_MISS)
CLKS = CPU_CLK_UNHALTED.THREAD
L3_Bound = Mem_L3_Hit_Fraction * CYCLE_ACTIVITY.STALLS_L2_PENDING / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- MEM_LOAD_UOPS_MISC_RETIRED.LLC_MISS
- Mem_L3_Weight
- MEM_LOAD_UOPS_RETIRED.LLC_HIT
- CYCLE_ACTIVITY.STALLS_L2_PENDING

### 3.1.3 <a id="dram_bound">DRAM_Bound</a>

This metric estimates how often the CPU was stalled on accesses to external memory (DRAM) by loads. Better caching can improve the latency and increase performance.

- Domain: Stalls
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryBound, TmaL3mem
- sample: MEM_LOAD_UOPS_MISC_RETIRED.LLC_MISS:pp

```python
Mem_L3_Hit_Fraction = MEM_LOAD_UOPS_RETIRED.LLC_HIT / (MEM_LOAD_UOPS_RETIRED.LLC_HIT + Mem_L3_Weight * MEM_LOAD_UOPS_MISC_RETIRED.LLC_MISS)
CLKS = CPU_CLK_UNHALTED.THREAD
DRAM_Bound = (1 - Mem_L3_Hit_Fraction) * CYCLE_ACTIVITY.STALLS_L2_PENDING / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- MEM_LOAD_UOPS_MISC_RETIRED.LLC_MISS
- Mem_L3_Weight
- MEM_LOAD_UOPS_RETIRED.LLC_HIT
- CYCLE_ACTIVITY.STALLS_L2_PENDING

#### 3.1.3.1 <a id="mem_bandwidth">MEM_Bandwidth</a>

This metric estimates fraction of cycles where the core's performance was likely hurt due to approaching bandwidth limits of external memory (DRAM). The underlying heuristic assumes that a similar off-core traffic is generated by all IA cores. This metric does not aggregate non-data-read requests by this logical processor; requests from other IA Logical Processors/Physical Cores/sockets; or other non-IA devices like GPU; hence the maximum external memory bandwidth limits may or may not be approached when this metric is flagged (see Uncore counters for that).. Improve data accesses to reduce cacheline transfers from/to memory. Examples: 1) Consume all bytes of a each cacheline before it is evicted (e.g. reorder structure elements and split non- hot ones), 2) merge computed-limited with BW-limited loops, 3) NUMA optimizations in multi-socket system. Note: software prefetches will not help BW-limited application..

- Domain: Clocks
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryBW, Offcore

```python
CLKS = CPU_CLK_UNHALTED.THREAD
ORO_DRD_BW_Cycles = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('OFFCORE_REQUESTS_OUTSTANDING.ALL_DATA_RD:c6', level)), level)
MEM_Bandwidth = ORO_DRD_BW_Cycles / CLKS
```

- level
- EV
- CPU_CLK_UNHALTED.THREAD

#### 3.1.3.2 <a id="mem_latency">MEM_Latency</a>

This metric estimates fraction of cycles where the performance was likely hurt due to latency from external memory (DRAM). This metric does not aggregate requests from other Logical Processors/Physical Cores/sockets (see Uncore counters for that).. Improve data accesses or interleave them with compute. Examples: 1) Data layout re-structuring, 2) Software Prefetches (also through the compiler)..

- Domain: Clocks
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryLat, Offcore

```python
ORO_DRD_Any_Cycles = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DATA_RD', level)), level)
CLKS = CPU_CLK_UNHALTED.THREAD
MEM_Latency = ORO_DRD_Any_Cycles / CLKS - MEM_Bandwidth
```

- [MEM_Bandwidth](#mem_bandwidth)
- CPU_CLK_UNHALTED.THREAD
- level
- EV

### 3.1.4 <a id="store_bound">Store_Bound</a>

This metric estimates how often CPU was stalled due to RFO store memory accesses; RFO store issue a read-for-ownership request before the write. Even though store accesses do not typically stall out-of-order CPUs; there are few cases where stores can lead to actual stalls. This metric will be flagged should RFO stores be a bottleneck.

- Domain: Stalls
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryBound, TmaL3mem
- sample: MEM_UOPS_RETIRED.ALL_STORES:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Store_Bound = RESOURCE_STALLS.SB / CLKS
```

- RESOURCE_STALLS.SB
- CPU_CLK_UNHALTED.THREAD

## 3.2 <a id="core_bound">Core_Bound</a>

This metric represents fraction of slots where Core non- memory issues were of a bottleneck. Shortage in hardware compute resources; or dependencies in software's instructions are both categorized under Core Bound. Hence it may indicate the machine ran out of an out-of-order resource; certain execution units are overloaded or dependencies in program's data- or instruction-flow are limiting the performance (e.g. FP-chained long-latency arithmetic operations).. Tip: consider Port Saturation analysis as next step.

- Domain: Slots
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Core
- Metric group: Backend, TmaL2, Compute

```python
Core_Bound = Backend_Bound - Memory_Bound
```

- [Memory_Bound](#memory_bound)
- [Backend_Bound](#backend_bound)

### 3.2.1 <a id="divider">Divider</a>

This metric represents fraction of cycles where the Divider unit was active. Divide and square root instructions are performed by the Divider unit and can take considerably longer latency than integer or Floating Point addition; subtraction; or multiplication.

- Domain: Clocks
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Core
- sample: ARITH.FPU_DIV_ACTIVE

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Divider = ARITH.FPU_DIV_ACTIVE / CORE_CLKS
```

- ARITH.FPU_DIV_ACTIVE
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

### 3.2.2 <a id="ports_utilization">Ports_Utilization</a>

This metric estimates fraction of cycles the CPU performance was potentially limited due to Core computation issues (non divider-related). Two distinct categories can be attributed into this metric: (1) heavy data-dependency among contiguous instructions would manifest in this metric - such cases are often referred to as low Instruction Level Parallelism (ILP). (2) Contention on some hardware execution unit other than Divider. For example; when there are too many multiply operations.. Loop Vectorization -most compilers feature auto-Vectorization options today- reduces pressure on the execution ports as multiple elements are calculated with same uop.

- Domain: Clocks
- Threshold:  > 0.15 and parent over threshold
- Area: BE/Core
- Metric group: PortsUtil

```python
STALLS_MEM_ANY = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('CYCLE_ACTIVITY.STALLS_L1D_PENDING', level)), level)
CLKS = CPU_CLK_UNHALTED.THREAD
IPC = INST_RETIRED.ANY / CLKS
Few_Uops_Executed_Threshold = UOPS_DISPATCHED.THREAD:c3 if IPC > 1.8 else UOPS_DISPATCHED.THREAD:c2
Frontend_RS_Empty_Cycles = RS_EVENTS.EMPTY_CYCLES if Fetch_Latency > 0.1 else 0
STALLS_TOTAL = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('CYCLE_ACTIVITY.CYCLES_NO_DISPATCH', level)), level)
Backend_Bound_Cycles = STALLS_TOTAL + UOPS_DISPATCHED.THREAD:c1 - Few_Uops_Executed_Threshold - Frontend_RS_Empty_Cycles + RESOURCE_STALLS.SB
Ports_Utilization = (Backend_Bound_Cycles - RESOURCE_STALLS.SB - STALLS_MEM_ANY) / CLKS
```

- RESOURCE_STALLS.SB
- CPU_CLK_UNHALTED.THREAD
- level
- EV
- [Fetch_Latency](#fetch_latency)
- RS_EVENTS.EMPTY_CYCLES
- INST_RETIRED.ANY
- UOPS_DISPATCHED.THREAD:c2
- UOPS_DISPATCHED.THREAD:c3
- UOPS_DISPATCHED.THREAD:c1

# 4 <a id="retiring">Retiring</a>

This category represents fraction of slots utilized by useful work i.e. issued uops that eventually get retired. Ideally; all pipeline slots would be attributed to the Retiring category. Retiring of 100% would indicate the maximum Pipeline_Width throughput was achieved. Maximizing Retiring typically increases the Instructions-per-cycle (see IPC metric). Note that a high Retiring value does not necessary mean there is no room for more performance. For example; Heavy-operations or Microcode Assists are categorized under Retiring. They often indicate suboptimal performance and can often be optimized or avoided. . A high Retiring value for non-vectorized code may be a good hint for programmer to consider vectorizing his code. Doing so essentially lets more computations be done without significantly increasing number of instructions thus improving the performance.

- Domain: Slots
- Threshold:  > 0.7 or self.Heavy_Operations.thresh
- Area: RET
- Metric group: TmaL1
- sample: UOPS_RETIRED.RETIRE_SLOTS

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Retiring = Retired_Slots / SLOTS
```

- Pipeline_Width
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- UOPS_RETIRED.RETIRE_SLOTS

## 4.1 <a id="light_operations">Light_Operations</a>

This metric represents fraction of slots where the CPU was retiring light-weight operations -- instructions that require no more than one uop (micro-operation). This correlates with total number of instructions used by the program. A uops-per-instruction (see UopPI metric) ratio of 1 or less should be expected for decently optimized software running on Intel Core/Xeon products. While this often indicates efficient X86 instructions were executed; high value does not necessarily mean better performance cannot be achieved.. Focus on techniques that reduce instruction count or result in more efficient instructions generation such as vectorization.

- Domain: Slots
- Threshold:  > 0.6
- Area: RET
- Metric group: Retire, TmaL2
- sample: INST_RETIRED.PREC_DIST

```python
Light_Operations = Retiring - Heavy_Operations
```

- [Heavy_Operations](#heavy_operations)
- [Retiring](#retiring)

### 4.1.1 <a id="fp_arith">FP_Arith</a>

This metric represents overall arithmetic floating-point (FP) operations fraction the CPU has executed (retired). Note this metric's value may exceed its parent due to use of "Uops" CountDomain and FMA double-counting.

- Domain: Uops
- Threshold:  > 0.2 and parent over threshold
- Area: RET
- Metric group: HPC

```python
FP_Arith = X87_Use + FP_Scalar + FP_Vector
```

- [X87_Use](#x87_use)
- [FP_Scalar](#fp_scalar)
- [FP_Vector](#fp_vector)

#### 4.1.1.1 <a id="x87_use">X87_Use</a>

This metric serves as an approximation of legacy x87 usage. It accounts for instructions beyond X87 FP arithmetic operations; hence may be used as a thermometer to avoid X87 high usage and preferably upgrade to modern ISA. See Tip under Tuning Hint.. Tip: consider compiler flags to generate newer AVX (or SSE) instruction sets; which typically perform better and feature vectors.

- Domain: Uops
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- Metric group: Compute

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
X87_Use = Retired_Slots * FP_COMP_OPS_EXE.X87 / UOPS_DISPATCHED.THREAD
```

- FP_COMP_OPS_EXE.X87
- UOPS_DISPATCHED.THREAD
- UOPS_RETIRED.RETIRE_SLOTS

#### 4.1.1.2 <a id="fp_scalar">FP_Scalar</a>

This metric approximates arithmetic floating-point (FP) scalar uops fraction the CPU has retired. May overcount due to FMA double counting.. Investigate what limits (compiler) generation of vector code.

- Domain: Uops
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- Metric group: Compute, Flops

```python
FP_Arith_Scalar = FP_COMP_OPS_EXE.SSE_SCALAR_SINGLE + FP_COMP_OPS_EXE.SSE_SCALAR_DOUBLE
FP_Scalar = FP_Arith_Scalar / UOPS_DISPATCHED.THREAD
```

- FP_COMP_OPS_EXE.SSE_SCALAR_SINGLE
- FP_COMP_OPS_EXE.SSE_SCALAR_DOUBLE
- UOPS_DISPATCHED.THREAD

#### 4.1.1.3 <a id="fp_vector">FP_Vector</a>

This metric approximates arithmetic floating-point (FP) vector uops fraction the CPU has retired aggregated across all vector widths. May overcount due to FMA double counting.. Check if vector width is expected

- Domain: Uops
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- Metric group: Compute, Flops

```python
FP_Arith_Vector = FP_COMP_OPS_EXE.SSE_PACKED_DOUBLE + FP_COMP_OPS_EXE.SSE_PACKED_SINGLE + SIMD_FP_256.PACKED_SINGLE + SIMD_FP_256.PACKED_DOUBLE
FP_Vector = FP_Arith_Vector / UOPS_DISPATCHED.THREAD
```

- SIMD_FP_256.PACKED_DOUBLE
- SIMD_FP_256.PACKED_SINGLE
- FP_COMP_OPS_EXE.SSE_PACKED_SINGLE
- FP_COMP_OPS_EXE.SSE_PACKED_DOUBLE
- UOPS_DISPATCHED.THREAD

## 4.2 <a id="heavy_operations">Heavy_Operations</a>

This metric represents fraction of slots where the CPU was retiring heavy-weight operations -- instructions that require two or more uops or micro-coded sequences. This highly-correlates with the uop length of these instructions/sequences.

- Domain: Slots
- Threshold:  > 0.1
- Area: RET
- Metric group: Retire, TmaL2

```python
Heavy_Operations = Microcode_Sequencer
```

- [Microcode_Sequencer](#microcode_sequencer)

### 4.2.1 <a id="microcode_sequencer">Microcode_Sequencer</a>

This metric represents fraction of slots the CPU was retiring uops fetched by the Microcode Sequencer (MS) unit. The MS is used for CISC instructions not supported by the default decoders (like repeat move strings; or CPUID); or by microcode assists used to address some operation modes (like in Floating Point assists). These cases can often be avoided..

- Domain: Slots
- Threshold:  > 0.05 and parent over threshold
- Area: RET
- Metric group: MicroSeq
- sample: IDQ.MS_UOPS

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
Retire_Fraction = Retired_Slots / UOPS_ISSUED.ANY
Microcode_Sequencer = Retire_Fraction * IDQ.MS_UOPS / SLOTS
```

- UOPS_ISSUED.ANY
- UOPS_RETIRED.RETIRE_SLOTS
- IDQ.MS_UOPS
- Pipeline_Width
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

# 5 General Metrics

## 5.1 <a id="metric_cpi">Metric_CPI</a>

Cycles Per Instruction (per Logical Processor)

- Domain: Metric
- Threshold: True
- Area: Info.Thread
- Metric group: Pipeline, Mem

```python
CLKS = CPU_CLK_UNHALTED.THREAD
IPC = INST_RETIRED.ANY / CLKS
CPI = 1 / IPC
Metric_CPI = CPI
```

- CPU_CLK_UNHALTED.THREAD
- INST_RETIRED.ANY

## 5.2 <a id="metric_dram_bw_use">Metric_DRAM_BW_Use</a>

Average external Memory Bandwidth Use for reads and writes [GB / sec]

- Domain: GB/sec
- Max value: 200
- Threshold: True
- Area: Info.System
- Metric group: HPC, Mem, MemoryBW, SoC

```python
Time = interval-s
DRAM_BW_Use = 64 * (UNC_ARB_TRK_REQUESTS.ALL + UNC_ARB_COH_TRK_REQUESTS.ALL) / OneMillion / Time / 1000
Metric_DRAM_BW_Use = DRAM_BW_Use
```

- UNC_ARB_TRK_REQUESTS.ALL
- UNC_ARB_COH_TRK_REQUESTS.ALL
- OneMillion
- interval-s

## 5.3 <a id="metric_slots">Metric_SLOTS</a>

Total issue-pipeline slots (per-Physical Core till ICL; per- Logical Processor ICL onward)

- Domain: Count
- Threshold: True
- Area: Info.Thread
- Metric group: TmaL1

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Metric_SLOTS = SLOTS
```

- Pipeline_Width
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

## 5.4 <a id="metric_smt_2t_utilization">Metric_SMT_2T_Utilization</a>

Fraction of cycles where both hardware Logical Processors were active

- Domain: Core_Metric
- Max value: 1.0
- Threshold: True
- Area: Info.System
- Metric group: SMT

```python
SMT_2T_Utilization = 1 - CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / (CPU_CLK_UNHALTED.REF_XCLK_ANY / 2) if smt_enabled else 0
Metric_SMT_2T_Utilization = SMT_2T_Utilization
```

- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- smt_enabled
- CPU_CLK_UNHALTED.REF_XCLK_ANY

## 5.5 <a id="metric_uoppi">Metric_UopPI</a>

Uops Per Instruction

- Domain: Metric
- Max value: 2.0
- Threshold:  > 1.05
- Area: Info.Thread
- Metric group: Pipeline, Ret, Retire

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
UopPI = Retired_Slots / INST_RETIRED.ANY
Metric_UopPI = UopPI
```

- INST_RETIRED.ANY
- UOPS_RETIRED.RETIRE_SLOTS

## 5.6 <a id="metric_turbo_utilization">Metric_Turbo_Utilization</a>

Average Frequency Utilization relative nominal frequency

- Domain: Core_Metric
- Max value: 10.0
- Threshold: True
- Area: Info.System
- Metric group: Power

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Turbo_Utilization = CLKS / CPU_CLK_UNHALTED.REF_TSC
Metric_Turbo_Utilization = Turbo_Utilization
```

- CPU_CLK_UNHALTED.REF_TSC
- CPU_CLK_UNHALTED.THREAD

## 5.7 <a id="metric_core_clks">Metric_CORE_CLKS</a>

Core actual clocks when any Logical Processor is active on the Physical Core

- Domain: Count
- Threshold: True
- Area: Info.Core
- Metric group: SMT

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Metric_CORE_CLKS = CORE_CLKS
```

- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

## 5.8 <a id="metric_ilp">Metric_ILP</a>

Instruction-Level-Parallelism (average number of uops executed when there is execution) per-core

- Domain: Core_Metric
- Max value: Exe_Ports
- Threshold: True
- Area: Info.Core
- Metric group: Backend, Cor, Pipeline, PortsUtil

```python
Execute_Cycles = UOPS_DISPATCHED.CORE:c1 / 2 if smt_enabled else UOPS_DISPATCHED.CORE:c1
ILP = UOPS_DISPATCHED.THREAD / Execute_Cycles
Metric_ILP = ILP
```

- UOPS_DISPATCHED.THREAD
- smt_enabled
- UOPS_DISPATCHED.CORE:c1

## 5.9 <a id="metric_ipfarbranch">Metric_IpFarBranch</a>

Instructions per Far Branch ( Far Branches apply upon transition from application to operating system, handling interrupts, exceptions) [lower number means higher occurrence rate]

- Domain: Inst_Metric
- Threshold:  < 1000000
- Area: Info.System
- Metric group: Branches, OS

```python
IpFarBranch = INST_RETIRED.ANY / BR_INST_RETIRED.FAR_BRANCH:USER
Metric_IpFarBranch = IpFarBranch
```

- INST_RETIRED.ANY
- BR_INST_RETIRED.FAR_BRANCH:USER

## 5.10 <a id="metric_kernel_utilization">Metric_Kernel_Utilization</a>

Fraction of cycles spent in the Operating System (OS) Kernel mode

- Domain: Metric
- Max value: 1.0
- Threshold:  > 0.05
- Area: Info.System
- Metric group: OS

```python
Kernel_Utilization = CPU_CLK_UNHALTED.THREAD_P:SUP / CPU_CLK_UNHALTED.THREAD
Metric_Kernel_Utilization = Kernel_Utilization
```

- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.THREAD_P:SUP

## 5.11 <a id="metric_cpu_utilization">Metric_CPU_Utilization</a>

Average CPU Utilization

- Domain: Metric
- Max value: 200
- Threshold: True
- Area: Info.System
- Metric group: HPC, Summary

```python
CPU_Utilization = CPU_CLK_UNHALTED.REF_TSC / msr/tsc/
Metric_CPU_Utilization = CPU_Utilization
```

- CPU_CLK_UNHALTED.REF_TSC
- msr/tsc/

## 5.12 <a id="metric_flopc">Metric_FLOPc</a>

Floating Point Operations Per Cycle

- Domain: Core_Metric
- Max value: 10.0
- Threshold: True
- Area: Info.Core
- Metric group: Ret, Flops

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
FLOP_Count = 1 * (FP_COMP_OPS_EXE.SSE_SCALAR_SINGLE + FP_COMP_OPS_EXE.SSE_SCALAR_DOUBLE) + 2 * FP_COMP_OPS_EXE.SSE_PACKED_DOUBLE + 4 * (FP_COMP_OPS_EXE.SSE_PACKED_SINGLE + SIMD_FP_256.PACKED_DOUBLE) + 8 * SIMD_FP_256.PACKED_SINGLE
FLOPc = FLOP_Count / CORE_CLKS
Metric_FLOPc = FLOPc
```

- SIMD_FP_256.PACKED_DOUBLE
- FP_COMP_OPS_EXE.SSE_SCALAR_SINGLE
- SIMD_FP_256.PACKED_SINGLE
- FP_COMP_OPS_EXE.SSE_PACKED_SINGLE
- FP_COMP_OPS_EXE.SSE_SCALAR_DOUBLE
- FP_COMP_OPS_EXE.SSE_PACKED_DOUBLE
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

## 5.13 <a id="metric_instructions">Metric_Instructions</a>

Total number of retired Instructions

- Domain: Count
- Threshold: True
- Area: Info.Inst_Mix
- Metric group: Summary, TmaL1

```python
Instructions = INST_RETIRED.ANY
Metric_Instructions = Instructions
```

- INST_RETIRED.ANY

## 5.14 <a id="metric_gflops">Metric_GFLOPs</a>

Giga Floating Point Operations Per Second. Aggregate across all supported options of: FP precisions, scalar and vector instructions, vector-width and AMX engine.

- Domain: Metric
- Max value: 200
- Threshold: True
- Area: Info.System
- Metric group: Cor, Flops, HPC

```python
Time = interval-s
FLOP_Count = 1 * (FP_COMP_OPS_EXE.SSE_SCALAR_SINGLE + FP_COMP_OPS_EXE.SSE_SCALAR_DOUBLE) + 2 * FP_COMP_OPS_EXE.SSE_PACKED_DOUBLE + 4 * (FP_COMP_OPS_EXE.SSE_PACKED_SINGLE + SIMD_FP_256.PACKED_DOUBLE) + 8 * SIMD_FP_256.PACKED_SINGLE
GFLOPs = FLOP_Count / OneBillion / Time
Metric_GFLOPs = GFLOPs
```

- SIMD_FP_256.PACKED_DOUBLE
- FP_COMP_OPS_EXE.SSE_SCALAR_SINGLE
- SIMD_FP_256.PACKED_SINGLE
- FP_COMP_OPS_EXE.SSE_PACKED_SINGLE
- FP_COMP_OPS_EXE.SSE_SCALAR_DOUBLE
- FP_COMP_OPS_EXE.SSE_PACKED_DOUBLE
- OneBillion
- interval-s

## 5.15 <a id="metric_socket_clks">Metric_Socket_CLKS</a>

Socket actual clocks when any core is active on that socket

- Domain: Count
- Threshold: True
- Area: Info.System
- Metric group: SoC

```python
Socket_CLKS = UNC_CLOCK.SOCKET
Metric_Socket_CLKS = Socket_CLKS
```

- UNC_CLOCK.SOCKET

## 5.16 <a id="metric_ipc">Metric_IPC</a>

Instructions Per Cycle (per Logical Processor)

- Domain: Metric
- Max value: Pipeline_Width + 2
- Threshold: True
- Area: Info.Thread
- Metric group: Ret, Summary

```python
CLKS = CPU_CLK_UNHALTED.THREAD
IPC = INST_RETIRED.ANY / CLKS
Metric_IPC = IPC
```

- CPU_CLK_UNHALTED.THREAD
- INST_RETIRED.ANY

## 5.17 <a id="metric_kernel_cpi">Metric_Kernel_CPI</a>

Cycles Per Instruction for the Operating System (OS) Kernel mode

- Domain: Metric
- Threshold: True
- Area: Info.System
- Metric group: OS

```python
Kernel_CPI = CPU_CLK_UNHALTED.THREAD_P:SUP / INST_RETIRED.ANY_P:SUP
Metric_Kernel_CPI = Kernel_CPI
```

- CPU_CLK_UNHALTED.THREAD_P:SUP
- INST_RETIRED.ANY_P:SUP

## 5.18 <a id="metric_mem_request_latency">Metric_MEM_Request_Latency</a>

Average latency of all requests to external memory (in Uncore cycles)

- Domain: Clocks_Latency
- Max value: 1000
- Threshold: True
- Area: Info.System
- Metric group: Mem, SoC

```python
MEM_Request_Latency = UNC_ARB_TRK_OCCUPANCY.ALL / UNC_ARB_TRK_REQUESTS.ALL
Metric_MEM_Request_Latency = MEM_Request_Latency
```

- UNC_ARB_TRK_REQUESTS.ALL
- UNC_ARB_TRK_OCCUPANCY.ALL

## 5.19 <a id="metric_coreipc">Metric_CoreIPC</a>

Instructions Per Cycle across hyper-threads (per physical core)

- Domain: Core_Metric
- Max value: Pipeline_Width + 2
- Threshold: True
- Area: Info.Core
- Metric group: Ret, SMT, TmaL1

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
CoreIPC = INST_RETIRED.ANY / CORE_CLKS
Metric_CoreIPC = CoreIPC
```

- INST_RETIRED.ANY
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

## 5.20 <a id="metric_mem_parallel_requests">Metric_MEM_Parallel_Requests</a>

Average number of parallel requests to external memory. Accounts for all requests

- Domain: Metric
- Max value: 100
- Threshold: True
- Area: Info.System
- Metric group: Mem, SoC

```python
MEM_Parallel_Requests = UNC_ARB_TRK_OCCUPANCY.ALL / UNC_ARB_TRK_OCCUPANCY.CYCLES_WITH_ANY_REQUEST
Metric_MEM_Parallel_Requests = MEM_Parallel_Requests
```

- UNC_ARB_TRK_OCCUPANCY.CYCLES_WITH_ANY_REQUEST
- UNC_ARB_TRK_OCCUPANCY.ALL

## 5.21 <a id="metric_average_frequency">Metric_Average_Frequency</a>

Measured Average Frequency for unhalted processors [GHz]

- Domain: SystemMetric
- Threshold: True
- Area: Info.System
- Metric group: Summary, Power

```python
Time = interval-s
CLKS = CPU_CLK_UNHALTED.THREAD
Turbo_Utilization = CLKS / CPU_CLK_UNHALTED.REF_TSC
Average_Frequency = Turbo_Utilization * msr/tsc/ / OneBillion / Time
Metric_Average_Frequency = Average_Frequency
```

- CPU_CLK_UNHALTED.REF_TSC
- CPU_CLK_UNHALTED.THREAD
- msr/tsc/
- OneBillion
- interval-s

## 5.22 <a id="metric_clks">Metric_CLKS</a>

Per-Logical Processor actual clocks when the Logical Processor is active.

- Domain: Count
- Threshold: True
- Area: Info.Thread
- Metric group: Pipeline

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Metric_CLKS = CLKS
```

- CPU_CLK_UNHALTED.THREAD

## 5.23 <a id="metric_dsb_coverage">Metric_DSB_Coverage</a>

Fraction of Uops delivered by the DSB (aka Decoded ICache; or Uop Cache). See section 'Decoded ICache' in Optimization Manual. http://www.intel.com/content/www/us/en/architecture- and-technology/64-ia-32-architectures-optimization- manual.html

- Domain: Metric
- Max value: 1.0
- Threshold:  < 0.7 and HighIPC
- Area: Info.Frontend
- Metric group: DSB, Fed, FetchBW

```python
Fetched_Uops = IDQ.DSB_UOPS + LSD.UOPS + IDQ.MITE_UOPS + IDQ.MS_UOPS
DSB_Coverage = IDQ.DSB_UOPS / Fetched_Uops
Metric_DSB_Coverage = DSB_Coverage
```

- LSD.UOPS
- IDQ.MS_UOPS
- IDQ.MITE_UOPS
- IDQ.DSB_UOPS

## 5.24 <a id="metric_time">Metric_Time</a>

Run duration time in seconds

- Domain: Seconds
- Threshold:  < 1
- Area: Info.System
- Metric group: Summary

```python
Time = interval-s
Metric_Time = Time
```

- interval-s

## 5.25 <a id="metric_execute_per_issue">Metric_Execute_per_Issue</a>

The ratio of Executed- by Issued-Uops. Ratio > 1 suggests high rate of uop micro-fusions. Ratio < 1 suggest high rate of "execute" at rename stage.

- Domain: Metric
- Threshold: True
- Area: Info.Thread
- Metric group: Cor, Pipeline

```python
Execute_per_Issue = UOPS_DISPATCHED.THREAD / UOPS_ISSUED.ANY
Metric_Execute_per_Issue = Execute_per_Issue
```

- UOPS_DISPATCHED.THREAD
- UOPS_ISSUED.ANY

## 5.26 <a id="metric_retire">Metric_Retire</a>

Average number of Uops retired in cycles where at least one uop has retired.

- Domain: Metric
- Threshold: True
- Area: Info.Pipeline
- Metric group: Pipeline, Ret

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
Retire = Retired_Slots / UOPS_RETIRED.RETIRE_SLOTS:c1
Metric_Retire = Retire
```

- UOPS_RETIRED.RETIRE_SLOTS:c1
- UOPS_RETIRED.RETIRE_SLOTS

