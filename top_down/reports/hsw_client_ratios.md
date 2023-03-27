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

### 1.1.1 <a id="icache_misses">ICache_Misses</a>

This metric represents fraction of cycles the CPU was stalled due to instruction cache misses.. Using compiler's Profile-Guided Optimization (PGO) can reduce i-cache misses through improved hot code layout.

- Domain: Clocks
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: BigFoot, FetchLat, IcMiss

```python
CLKS = CPU_CLK_UNHALTED.THREAD
ICache_Misses = ICACHE.IFDATA_STALL / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- ICACHE.IFDATA_STALL

### 1.1.2 <a id="itlb_misses">ITLB_Misses</a>

This metric represents fraction of cycles the CPU was stalled due to Instruction TLB (ITLB) misses.. Consider large 2M pages for code (selectively prefer hot large-size function, due to limited 2M entries). Linux options: standard binaries use libhugetlbfs; Hfsort.. https://github. com/libhugetlbfs/libhugetlbfs;https://research.fb.com/public ations/optimizing-function-placement-for-large-scale-data- center-applications-2/

- Domain: Clocks
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: BigFoot, FetchLat, MemoryTLB
- sample: ITLB_MISSES.WALK_COMPLETED

```python
ITLB_Miss_Cycles = 14 * ITLB_MISSES.STLB_HIT + ITLB_MISSES.WALK_DURATION
CLKS = CPU_CLK_UNHALTED.THREAD
ITLB_Misses = ITLB_Miss_Cycles / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- ITLB_MISSES.WALK_DURATION
- ITLB_MISSES.STLB_HIT

### 1.1.3 <a id="branch_resteers">Branch_Resteers</a>

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

### 1.1.4 <a id="dsb_switches">DSB_Switches</a>

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

### 1.1.5 <a id="lcp">LCP</a>

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

### 1.1.6 <a id="ms_switches">MS_Switches</a>

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

### 1.2.1 <a id="mite">MITE</a>

This metric represents Core fraction of cycles in which CPU was likely limited due to the MITE pipeline (the legacy decode pipeline). This pipeline is used for code that was not pre-cached in the DSB or LSD. For example; inefficiencies due to asymmetric decoders; use of long immediate or LCP can manifest as MITE fetch bandwidth bottleneck.. Consider tuning codegen of 'small hotspots' that can fit in DSB. Read about 'Decoded ICache' in Optimization Manual:. http://www.intel.com/content/www/us/en /architecture-and-technology/64-ia-32-architectures- optimization-manual.html

- Domain: Slots_Estimated
- Threshold:  > 0.1 and parent over threshold
- Area: FE
- Metric group: DSBmiss, FetchBW

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
MITE = (IDQ.ALL_MITE_CYCLES_ANY_UOPS - IDQ.ALL_MITE_CYCLES_4_UOPS) / CORE_CLKS / 2
```

- IDQ.ALL_MITE_CYCLES_4_UOPS
- IDQ.ALL_MITE_CYCLES_ANY_UOPS
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

### 1.2.2 <a id="dsb">DSB</a>

This metric represents Core fraction of cycles in which CPU was likely limited due to DSB (decoded uop cache) fetch pipeline. For example; inefficient utilization of the DSB cache structure or bank conflict when reading from it; are categorized here.

- Domain: Slots_Estimated
- Threshold:  > 0.15 and parent over threshold
- Area: FE
- Metric group: DSB, FetchBW

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
DSB = (IDQ.ALL_DSB_CYCLES_ANY_UOPS - IDQ.ALL_DSB_CYCLES_4_UOPS) / CORE_CLKS / 2
```

- IDQ.ALL_DSB_CYCLES_ANY_UOPS
- IDQ.ALL_DSB_CYCLES_4_UOPS
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

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
STALLS_MEM_ANY = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('CYCLE_ACTIVITY.STALLS_LDM_PENDING', level)), level)
CLKS = CPU_CLK_UNHALTED.THREAD
IPC = INST_RETIRED.ANY / CLKS
Few_Uops_Executed_Threshold = UOPS_EXECUTED.CORE:c3 if IPC > 1.8 else UOPS_EXECUTED.CORE:c2
Frontend_RS_Empty_Cycles = RS_EVENTS.EMPTY_CYCLES if Fetch_Latency > 0.1 else 0
STALLS_TOTAL = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('CYCLE_ACTIVITY.CYCLES_NO_EXECUTE', level)), level)
Backend_Bound_Cycles = STALLS_TOTAL + (UOPS_EXECUTED.CORE:c1 - Few_Uops_Executed_Threshold) / 2 - Frontend_RS_Empty_Cycles + RESOURCE_STALLS.SB if smt_enabled else STALLS_TOTAL + UOPS_EXECUTED.CORE:c1 - Few_Uops_Executed_Threshold - Frontend_RS_Empty_Cycles + RESOURCE_STALLS.SB
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
- UOPS_EXECUTED.CORE:c2
- UOPS_EXECUTED.CORE:c3
- UOPS_EXECUTED.CORE:c1
- smt_enabled

### 3.1.1 <a id="l1_bound">L1_Bound</a>

This metric estimates how often the CPU was stalled without loads missing the L1 data cache. The L1 data cache typically has the shortest latency. However; in certain cases like loads blocked on older stores; a load might suffer due to high latency even though it is being satisfied by the L1. Another example is loads who miss in the TLB. These cases are characterized by execution unit stalls; while some non-completed demand load lives in the machine without having that demand load missing the L1 cache.

- Domain: Stalls
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Mem
- Metric group: CacheMisses, MemoryBound, TmaL3mem
- sample: MEM_LOAD_UOPS_RETIRED.L1_HIT:pp, MEM_LOAD_UOPS_RETIRED.HIT_LFB:pp

```python
STALLS_MEM_ANY = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('CYCLE_ACTIVITY.STALLS_LDM_PENDING', level)), level)
CLKS = CPU_CLK_UNHALTED.THREAD
L1_Bound = max((STALLS_MEM_ANY - CYCLE_ACTIVITY.STALLS_L1D_PENDING) / CLKS, 0)
```

- CPU_CLK_UNHALTED.THREAD
- CYCLE_ACTIVITY.STALLS_L1D_PENDING
- level
- EV

#### 3.1.1.1 <a id="dtlb_load">DTLB_Load</a>

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

#### 3.1.1.2 <a id="store_fwd_blk">Store_Fwd_Blk</a>

This metric roughly estimates fraction of cycles when the memory subsystem had loads blocked since they could not forward data from earlier (in program order) overlapping stores. To streamline memory operations in the pipeline; a load can avoid waiting for memory if a prior in-flight store is writing the data that the load wants to read (store forwarding process). However; in some cases the load may be blocked for a significant time pending the store forward. For example; when the prior store is writing a smaller region than the load is reading.

- Domain: Clocks_Estimated
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Mem

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Store_Fwd_Blk = 13 * LD_BLOCKS.STORE_FORWARD / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- LD_BLOCKS.STORE_FORWARD

#### 3.1.1.3 <a id="lock_latency">Lock_Latency</a>

This metric represents fraction of cycles the CPU spent handling cache misses due to lock operations. Due to the microarchitecture handling of locks; they are classified as L1_Bound regardless of what memory source satisfied them.

- Domain: Clocks
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Mem
- Metric group: Offcore
- sample: MEM_UOPS_RETIRED.LOCK_LOADS:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Mem_Lock_St_Fraction = MEM_UOPS_RETIRED.LOCK_LOADS / MEM_UOPS_RETIRED.ALL_STORES
ORO_Demand_RFO_C1 = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_RFO', level)), level)
Lock_Latency = Mem_Lock_St_Fraction * ORO_Demand_RFO_C1 / CLKS
```

- level
- EV
- MEM_UOPS_RETIRED.LOCK_LOADS
- MEM_UOPS_RETIRED.ALL_STORES
- CPU_CLK_UNHALTED.THREAD

#### 3.1.1.4 <a id="split_loads">Split_Loads</a>

This metric estimates fraction of cycles handling memory load split accesses - load that cross 64-byte cache line boundary. . Consider aligning data or hot structure fields. See the Optimization Manual for more details

- Domain: Clocks_Calculated
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Mem
- sample: MEM_UOPS_RETIRED.SPLIT_LOADS:pp

```python
Load_Miss_Real_Latency = L1D_PEND_MISS.PENDING / (MEM_LOAD_UOPS_RETIRED.L1_MISS + MEM_LOAD_UOPS_RETIRED.HIT_LFB)
CLKS = CPU_CLK_UNHALTED.THREAD
Split_Loads = Load_Miss_Real_Latency * LD_BLOCKS.NO_SR / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- LD_BLOCKS.NO_SR
- MEM_LOAD_UOPS_RETIRED.HIT_LFB
- MEM_LOAD_UOPS_RETIRED.L1_MISS
- L1D_PEND_MISS.PENDING

#### 3.1.1.5 <a id="g4k_aliasing">G4K_Aliasing</a>

This metric estimates how often memory load accesses were aliased by preceding stores (in program order) with a 4K address offset. False match is possible; which incur a few cycles load re-issue. However; the short re-issue duration is often hidden by the out-of-order core and HW optimizations; hence a user may safely ignore a high value of this metric unless it manages to propagate up into parent nodes of the hierarchy (e.g. to L1_Bound).. Consider reducing independent loads/stores accesses with 4K offsets. See the Optimization Manual for more details

- Domain: Clocks_Estimated
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Mem

```python
CLKS = CPU_CLK_UNHALTED.THREAD
G4K_Aliasing = LD_BLOCKS_PARTIAL.ADDRESS_ALIAS / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- LD_BLOCKS_PARTIAL.ADDRESS_ALIAS

#### 3.1.1.6 <a id="fb_full">FB_Full</a>

This metric does a *rough estimation* of how often L1D Fill Buffer unavailability limited additional L1D miss memory access requests to proceed. The higher the metric value; the deeper the memory hierarchy level the misses are satisfied from (metric values >1 are valid). Often it hints on approaching bandwidth limits (to L2 cache; L3 cache or external memory).. See $issueBW and $issueSL hints. Avoid software prefetches if indeed memory BW limited.

- Domain: Clocks_Calculated
- Threshold:  > 0.3
- Area: BE/Mem
- Metric group: MemoryBW

```python
Load_Miss_Real_Latency = L1D_PEND_MISS.PENDING / (MEM_LOAD_UOPS_RETIRED.L1_MISS + MEM_LOAD_UOPS_RETIRED.HIT_LFB)
CLKS = CPU_CLK_UNHALTED.THREAD
FB_Full = Load_Miss_Real_Latency * L1D_PEND_MISS.REQUEST_FB_FULL:c1 / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- L1D_PEND_MISS.REQUEST_FB_FULL:c1
- MEM_LOAD_UOPS_RETIRED.HIT_LFB
- MEM_LOAD_UOPS_RETIRED.L1_MISS
- L1D_PEND_MISS.PENDING

### 3.1.2 <a id="l2_bound">L2_Bound</a>

This metric estimates how often the CPU was stalled due to L2 cache accesses by loads. Avoiding cache misses (i.e. L1 misses/L2 hits) can improve the latency and increase performance.

- Domain: Stalls
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: CacheMisses, MemoryBound, TmaL3mem
- sample: MEM_LOAD_UOPS_RETIRED.L2_HIT:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
L2_Bound = (CYCLE_ACTIVITY.STALLS_L1D_PENDING - CYCLE_ACTIVITY.STALLS_L2_PENDING) / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- CYCLE_ACTIVITY.STALLS_L1D_PENDING
- CYCLE_ACTIVITY.STALLS_L2_PENDING

### 3.1.3 <a id="l3_bound">L3_Bound</a>

This metric estimates how often the CPU was stalled due to loads accesses to L3 cache or contended with a sibling Core. Avoiding cache misses (i.e. L2 misses/L3 hits) can improve the latency and increase performance.

- Domain: Stalls
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: CacheMisses, MemoryBound, TmaL3mem
- sample: MEM_LOAD_UOPS_RETIRED.L3_HIT:pp

```python
Mem_L3_Hit_Fraction = MEM_LOAD_UOPS_RETIRED.L3_HIT / (MEM_LOAD_UOPS_RETIRED.L3_HIT + Mem_L3_Weight * MEM_LOAD_UOPS_RETIRED.L3_MISS)
CLKS = CPU_CLK_UNHALTED.THREAD
L3_Bound = Mem_L3_Hit_Fraction * CYCLE_ACTIVITY.STALLS_L2_PENDING / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- MEM_LOAD_UOPS_RETIRED.L3_HIT
- MEM_LOAD_UOPS_RETIRED.L3_MISS
- Mem_L3_Weight
- CYCLE_ACTIVITY.STALLS_L2_PENDING

#### 3.1.3.1 <a id="contested_accesses">Contested_Accesses</a>

This metric estimates fraction of cycles while the memory subsystem was handling synchronizations due to contested accesses. Contested accesses occur when data written by one Logical Processor are read by another Logical Processor on a different Physical Core. Examples of contested accesses include synchronizations such as locks; true data sharing such as modified locked variables; and false sharing.

- Domain: Clocks_Estimated
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: DataSharing, Offcore, Snoop
- sample: MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HITM:pp, MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_MISS:pp

```python
LOAD_L1_MISS = MEM_LOAD_UOPS_RETIRED.L2_HIT + MEM_LOAD_UOPS_RETIRED.L3_HIT + MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HIT + MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HITM + MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_MISS
LOAD_L1_MISS_NET = LOAD_L1_MISS + MEM_LOAD_UOPS_RETIRED.L3_MISS
LOAD_XSNP_MISS = MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_MISS * (1 + MEM_LOAD_UOPS_RETIRED.HIT_LFB / LOAD_L1_MISS_NET)
CLKS = CPU_CLK_UNHALTED.THREAD
Mem_XSNP_HitM_Cost = 60
LOAD_XSNP_HITM = MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HITM * (1 + MEM_LOAD_UOPS_RETIRED.HIT_LFB / LOAD_L1_MISS_NET)
Mem_XSNP_Hit_Cost = 43
Contested_Accesses = (Mem_XSNP_HitM_Cost * LOAD_XSNP_HITM + Mem_XSNP_Hit_Cost * LOAD_XSNP_MISS) / CLKS
```

- MEM_LOAD_UOPS_RETIRED.HIT_LFB
- MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HIT
- MEM_LOAD_UOPS_RETIRED.L2_HIT
- MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HITM
- MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_MISS
- MEM_LOAD_UOPS_RETIRED.L3_HIT
- MEM_LOAD_UOPS_RETIRED.L3_MISS
- CPU_CLK_UNHALTED.THREAD

#### 3.1.3.2 <a id="data_sharing">Data_Sharing</a>

This metric estimates fraction of cycles while the memory subsystem was handling synchronizations due to data-sharing accesses. Data shared by multiple Logical Processors (even just read shared) may cause increased access latency due to cache coherency. Excessive data sharing can drastically harm multithreaded performance.

- Domain: Clocks_Estimated
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: Offcore, Snoop
- sample: MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HIT:pp

```python
Mem_XSNP_Hit_Cost = 43
LOAD_L1_MISS = MEM_LOAD_UOPS_RETIRED.L2_HIT + MEM_LOAD_UOPS_RETIRED.L3_HIT + MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HIT + MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HITM + MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_MISS
LOAD_L1_MISS_NET = LOAD_L1_MISS + MEM_LOAD_UOPS_RETIRED.L3_MISS
LOAD_XSNP_HIT = MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HIT * (1 + MEM_LOAD_UOPS_RETIRED.HIT_LFB / LOAD_L1_MISS_NET)
CLKS = CPU_CLK_UNHALTED.THREAD
Data_Sharing = Mem_XSNP_Hit_Cost * LOAD_XSNP_HIT / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- MEM_LOAD_UOPS_RETIRED.HIT_LFB
- MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HIT
- MEM_LOAD_UOPS_RETIRED.L2_HIT
- MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HITM
- MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_MISS
- MEM_LOAD_UOPS_RETIRED.L3_HIT
- MEM_LOAD_UOPS_RETIRED.L3_MISS

#### 3.1.3.3 <a id="l3_hit_latency">L3_Hit_Latency</a>

This metric represents fraction of cycles with demand load accesses that hit the L3 cache under unloaded scenarios (possibly L3 latency limited). Avoiding private cache misses (i.e. L2 misses/L3 hits) will improve the latency; reduce contention with sibling physical cores and increase performance. Note the value of this node may overlap with its siblings.

- Domain: Clocks_Estimated
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryLat
- sample: MEM_LOAD_UOPS_RETIRED.L3_HIT:pp

```python
Mem_XSNP_None_Cost = 29
LOAD_L1_MISS = MEM_LOAD_UOPS_RETIRED.L2_HIT + MEM_LOAD_UOPS_RETIRED.L3_HIT + MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HIT + MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HITM + MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_MISS
LOAD_L1_MISS_NET = LOAD_L1_MISS + MEM_LOAD_UOPS_RETIRED.L3_MISS
LOAD_L3_HIT = MEM_LOAD_UOPS_RETIRED.L3_HIT * (1 + MEM_LOAD_UOPS_RETIRED.HIT_LFB / LOAD_L1_MISS_NET)
CLKS = CPU_CLK_UNHALTED.THREAD
L3_Hit_Latency = Mem_XSNP_None_Cost * LOAD_L3_HIT / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- MEM_LOAD_UOPS_RETIRED.HIT_LFB
- MEM_LOAD_UOPS_RETIRED.L3_HIT
- MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HIT
- MEM_LOAD_UOPS_RETIRED.L2_HIT
- MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HITM
- MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_MISS
- MEM_LOAD_UOPS_RETIRED.L3_MISS

#### 3.1.3.4 <a id="sq_full">SQ_Full</a>

This metric measures fraction of cycles where the Super Queue (SQ) was full taking into account all request-types and both hardware SMT threads (Logical Processors).

- Domain: Clocks
- Threshold:  > 0.3 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryBW, Offcore

```python
SQ_Full_Cycles = OFFCORE_REQUESTS_BUFFER.SQ_FULL / 2 if smt_enabled else OFFCORE_REQUESTS_BUFFER.SQ_FULL
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SQ_Full = SQ_Full_Cycles / CORE_CLKS
```

- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- OFFCORE_REQUESTS_BUFFER.SQ_FULL

### 3.1.4 <a id="dram_bound">DRAM_Bound</a>

This metric estimates how often the CPU was stalled on accesses to external memory (DRAM) by loads. Better caching can improve the latency and increase performance.

- Domain: Stalls
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryBound, TmaL3mem
- sample: MEM_LOAD_UOPS_RETIRED.L3_MISS:pp

```python
Mem_L3_Hit_Fraction = MEM_LOAD_UOPS_RETIRED.L3_HIT / (MEM_LOAD_UOPS_RETIRED.L3_HIT + Mem_L3_Weight * MEM_LOAD_UOPS_RETIRED.L3_MISS)
CLKS = CPU_CLK_UNHALTED.THREAD
DRAM_Bound = (1 - Mem_L3_Hit_Fraction) * CYCLE_ACTIVITY.STALLS_L2_PENDING / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- MEM_LOAD_UOPS_RETIRED.L3_HIT
- MEM_LOAD_UOPS_RETIRED.L3_MISS
- Mem_L3_Weight
- CYCLE_ACTIVITY.STALLS_L2_PENDING

#### 3.1.4.1 <a id="mem_bandwidth">MEM_Bandwidth</a>

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

#### 3.1.4.2 <a id="mem_latency">MEM_Latency</a>

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

### 3.1.5 <a id="store_bound">Store_Bound</a>

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

#### 3.1.5.1 <a id="store_latency">Store_Latency</a>

This metric estimates fraction of cycles the CPU spent handling L1D store misses. Store accesses usually less impact out-of-order core performance; however; holding resources for longer time can lead into undesired implications (e.g. contention on L1D fill-buffer entries - see FB_Full). Consider to avoid/reduce unnecessary (or easily load-able/computable) memory store.

- Domain: Clocks_Estimated
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryLat, Offcore

```python
Mem_Lock_St_Fraction = MEM_UOPS_RETIRED.LOCK_LOADS / MEM_UOPS_RETIRED.ALL_STORES
Store_L2_Hit_Cycles = L2_RQSTS.RFO_HIT * Mem_L2_Store_Cost * (1 - Mem_Lock_St_Fraction)
CLKS = CPU_CLK_UNHALTED.THREAD
ORO_Demand_RFO_C1 = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_RFO', level)), level)
Store_Latency = (Store_L2_Hit_Cycles + (1 - Mem_Lock_St_Fraction) * ORO_Demand_RFO_C1) / CLKS
```

- level
- EV
- MEM_UOPS_RETIRED.LOCK_LOADS
- MEM_UOPS_RETIRED.ALL_STORES
- CPU_CLK_UNHALTED.THREAD
- L2_RQSTS.RFO_HIT
- Mem_L2_Store_Cost

#### 3.1.5.2 <a id="false_sharing">False_Sharing</a>

This metric roughly estimates how often CPU was handling synchronizations due to False Sharing. False Sharing is a multithreading hiccup; where multiple Logical Processors contend on different data-elements mapped into the same cache line. . False Sharing can be easily avoided by padding to make Logical Processors access different lines.

- Domain: Clocks_Estimated
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: DataSharing, Offcore, Snoop
- sample: MEM_LOAD_UOPS_L3_HIT_RETIRED.XSNP_HITM:pp, OFFCORE_RESPONSE.DEMAND_RFO.L3_HIT.HITM_OTHER_CORE

```python
Mem_XSNP_HitM_Cost = 60
CLKS = CPU_CLK_UNHALTED.THREAD
False_Sharing = Mem_XSNP_HitM_Cost * OFFCORE_RESPONSE.DEMAND_RFO.L3_HIT.HITM_OTHER_CORE / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- OFFCORE_RESPONSE.DEMAND_RFO.L3_HIT.HITM_OTHER_CORE

#### 3.1.5.3 <a id="split_stores">Split_Stores</a>

This metric represents rate of split store accesses. Consider aligning your data to the 64-byte cache line granularity.

- Domain: Core_Utilization
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Mem
- sample: MEM_UOPS_RETIRED.SPLIT_STORES:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Split_Stores = 2 * MEM_UOPS_RETIRED.SPLIT_STORES / CORE_CLKS
```

- MEM_UOPS_RETIRED.SPLIT_STORES
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

#### 3.1.5.4 <a id="dtlb_store">DTLB_Store</a>

This metric roughly estimates the fraction of cycles spent handling first-level data TLB store misses. As with ordinary data caching; focus on improving data locality and reducing working-set size to reduce DTLB overhead. Additionally; consider using profile-guided optimization (PGO) to collocate frequently-used data on the same page. Try using larger page sizes for large amounts of frequently- used data.

- Domain: Clocks_Estimated
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryTLB
- sample: MEM_UOPS_RETIRED.STLB_MISS_STORES:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
DTLB_Store = (Mem_STLB_Hit_Cost * DTLB_STORE_MISSES.STLB_HIT + DTLB_STORE_MISSES.WALK_DURATION) / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- Mem_STLB_Hit_Cost
- DTLB_STORE_MISSES.WALK_DURATION
- DTLB_STORE_MISSES.STLB_HIT

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
- sample: ARITH.DIVIDER_UOPS

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Divider = 10 * ARITH.DIVIDER_UOPS / CORE_CLKS
```

- ARITH.DIVIDER_UOPS
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
STALLS_MEM_ANY = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('CYCLE_ACTIVITY.STALLS_LDM_PENDING', level)), level)
CLKS = CPU_CLK_UNHALTED.THREAD
IPC = INST_RETIRED.ANY / CLKS
Few_Uops_Executed_Threshold = UOPS_EXECUTED.CORE:c3 if IPC > 1.8 else UOPS_EXECUTED.CORE:c2
Frontend_RS_Empty_Cycles = RS_EVENTS.EMPTY_CYCLES if Fetch_Latency > 0.1 else 0
STALLS_TOTAL = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('CYCLE_ACTIVITY.CYCLES_NO_EXECUTE', level)), level)
Backend_Bound_Cycles = STALLS_TOTAL + (UOPS_EXECUTED.CORE:c1 - Few_Uops_Executed_Threshold) / 2 - Frontend_RS_Empty_Cycles + RESOURCE_STALLS.SB if smt_enabled else STALLS_TOTAL + UOPS_EXECUTED.CORE:c1 - Few_Uops_Executed_Threshold - Frontend_RS_Empty_Cycles + RESOURCE_STALLS.SB
Ports_Utilization = (Backend_Bound_Cycles - RESOURCE_STALLS.SB - STALLS_MEM_ANY) / CLKS
```

- RESOURCE_STALLS.SB
- CPU_CLK_UNHALTED.THREAD
- level
- EV
- [Fetch_Latency](#fetch_latency)
- RS_EVENTS.EMPTY_CYCLES
- INST_RETIRED.ANY
- UOPS_EXECUTED.CORE:c2
- UOPS_EXECUTED.CORE:c3
- UOPS_EXECUTED.CORE:c1
- smt_enabled

#### 3.2.2.1 <a id="ports_utilized_0">Ports_Utilized_0</a>

This metric represents fraction of cycles CPU executed no uops on any execution port (Logical Processor cycles since ICL, Physical Core cycles otherwise). Long-latency instructions like divides may contribute to this metric.. Check assembly view and Appendix C in Optimization Manual to find out instructions with say 5 or more cycles latency.. http://www.intel.com/content/www/us/en/architecture-and- technology/64-ia-32-architectures-optimization-manual.html

- Domain: Clocks
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Core
- Metric group: PortsUtil

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
STALLS_TOTAL = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('CYCLE_ACTIVITY.CYCLES_NO_EXECUTE', level)), level)
Frontend_RS_Empty_Cycles = RS_EVENTS.EMPTY_CYCLES if Fetch_Latency > 0.1 else 0
Cycles_0_Ports_Utilized = UOPS_EXECUTED.CORE:i1:c1 / 2 if smt_enabled else STALLS_TOTAL - Frontend_RS_Empty_Cycles
Ports_Utilized_0 = Cycles_0_Ports_Utilized / CORE_CLKS
```

- [Fetch_Latency](#fetch_latency)
- RS_EVENTS.EMPTY_CYCLES
- smt_enabled
- UOPS_EXECUTED.CORE:i1:c1
- level
- EV
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- CPU_CLK_UNHALTED.THREAD_ANY

#### 3.2.2.2 <a id="ports_utilized_1">Ports_Utilized_1</a>

This metric represents fraction of cycles where the CPU executed total of 1 uop per cycle on all execution ports (Logical Processor cycles since ICL, Physical Core cycles otherwise). This can be due to heavy data-dependency among software instructions; or over oversubscribing a particular hardware resource. In some other cases with high 1_Port_Utilized and L1_Bound; this metric can point to L1 data-cache latency bottleneck that may not necessarily manifest with complete execution starvation (due to the short L1 latency e.g. walking a linked list) - looking at the assembly can be helpful.

- Domain: Clocks
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Core
- Metric group: PortsUtil

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Cycles_1_Port_Utilized = (UOPS_EXECUTED.CORE:c1 - UOPS_EXECUTED.CORE:c2) / 2 if smt_enabled else UOPS_EXECUTED.CORE:c1 - UOPS_EXECUTED.CORE:c2
Ports_Utilized_1 = Cycles_1_Port_Utilized / CORE_CLKS
```

- UOPS_EXECUTED.CORE:c1
- smt_enabled
- UOPS_EXECUTED.CORE:c2
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- CPU_CLK_UNHALTED.THREAD_ANY

#### 3.2.2.3 <a id="ports_utilized_2">Ports_Utilized_2</a>

This metric represents fraction of cycles CPU executed total of 2 uops per cycle on all execution ports (Logical Processor cycles since ICL, Physical Core cycles otherwise). Loop Vectorization -most compilers feature auto- Vectorization options today- reduces pressure on the execution ports as multiple elements are calculated with same uop.

- Domain: Clocks
- Threshold:  > 0.15 and parent over threshold
- Area: BE/Core
- Metric group: PortsUtil

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Cycles_2_Ports_Utilized = (UOPS_EXECUTED.CORE:c2 - UOPS_EXECUTED.CORE:c3) / 2 if smt_enabled else UOPS_EXECUTED.CORE:c2 - UOPS_EXECUTED.CORE:c3
Ports_Utilized_2 = Cycles_2_Ports_Utilized / CORE_CLKS
```

- smt_enabled
- UOPS_EXECUTED.CORE:c2
- UOPS_EXECUTED.CORE:c3
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- CPU_CLK_UNHALTED.THREAD_ANY

#### 3.2.2.4 <a id="ports_utilized_3m">Ports_Utilized_3m</a>

This metric represents fraction of cycles CPU executed total of 3 or more uops per cycle on all execution ports (Logical Processor cycles since ICL, Physical Core cycles otherwise).

- Domain: Clocks
- Threshold:  > 0.7 and parent over threshold
- Area: BE/Core
- Metric group: PortsUtil

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Cycles_3m_Ports_Utilized = UOPS_EXECUTED.CORE:c3 / 2 if smt_enabled else UOPS_EXECUTED.CORE:c3
Ports_Utilized_3m = Cycles_3m_Ports_Utilized / CORE_CLKS
```

- smt_enabled
- UOPS_EXECUTED.CORE:c3
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- CPU_CLK_UNHALTED.THREAD_ANY

##### 3.2.2.4.1 <a id="alu_op_utilization">ALU_Op_Utilization</a>

This metric represents Core fraction of cycles CPU dispatched uops on execution ports for ALU operations.

- Domain: Core_Execution
- Threshold:  > 0.6
- Area: BE/Core

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
ALU_Op_Utilization = (UOPS_DISPATCHED_PORT.PORT_0 + UOPS_DISPATCHED_PORT.PORT_1 + UOPS_DISPATCHED_PORT.PORT_5 + UOPS_DISPATCHED_PORT.PORT_6) / (4 * CORE_CLKS)
```

- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- UOPS_DISPATCHED_PORT.PORT_5
- UOPS_DISPATCHED_PORT.PORT_6
- UOPS_DISPATCHED_PORT.PORT_1
- UOPS_DISPATCHED_PORT.PORT_0

###### 3.2.2.4.1.1 <a id="port_0">Port_0</a>

This metric represents Core fraction of cycles CPU dispatched uops on execution port 0 ALU and 2nd branch

- Domain: Core_Clocks
- Threshold:  > 0.6
- Area: BE/Core
- Metric group: Compute
- sample: UOPS_DISPATCHED_PORT.PORT_0

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Port_0 = UOPS_DISPATCHED_PORT.PORT_0 / CORE_CLKS
```

- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- UOPS_DISPATCHED_PORT.PORT_0

###### 3.2.2.4.1.2 <a id="port_1">Port_1</a>

This metric represents Core fraction of cycles CPU dispatched uops on execution port 1 (ALU)

- Domain: Core_Clocks
- Threshold:  > 0.6
- Area: BE/Core
- sample: UOPS_DISPATCHED_PORT.PORT_1

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Port_1 = UOPS_DISPATCHED_PORT.PORT_1 / CORE_CLKS
```

- UOPS_DISPATCHED_PORT.PORT_1
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

###### 3.2.2.4.1.3 <a id="port_5">Port_5</a>

This metric represents Core fraction of cycles CPU dispatched uops on execution port 5 ALU. See section 'Handling Port 5 Pressure' in Optimization Manual:. http://www.intel.com/content/www/us/en/architecture-and- technology/64-ia-32-architectures-optimization-manual.html

- Domain: Core_Clocks
- Threshold:  > 0.6
- Area: BE/Core
- sample: UOPS_DISPATCHED_PORT.PORT_5

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Port_5 = UOPS_DISPATCHED_PORT.PORT_5 / CORE_CLKS
```

- UOPS_DISPATCHED_PORT.PORT_5
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

###### 3.2.2.4.1.4 <a id="port_6">Port_6</a>

This metric represents Core fraction of cycles CPU dispatched uops on execution port 6 ([HSW+]Primary Branch and simple ALU)

- Domain: Core_Clocks
- Threshold:  > 0.6
- Area: BE/Core
- sample: UOPS_DISPATCHED_PORT.PORT_6

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Port_6 = UOPS_DISPATCHED_PORT.PORT_6 / CORE_CLKS
```

- UOPS_DISPATCHED_PORT.PORT_6
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

##### 3.2.2.4.2 <a id="load_op_utilization">Load_Op_Utilization</a>

This metric represents Core fraction of cycles CPU dispatched uops on execution port for Load operations

- Domain: Core_Execution
- Threshold:  > 0.6
- Area: BE/Core

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Load_Op_Utilization = (UOPS_DISPATCHED_PORT.PORT_2 + UOPS_DISPATCHED_PORT.PORT_3 + UOPS_DISPATCHED_PORT.PORT_7 - UOPS_DISPATCHED_PORT.PORT_4) / (2 * CORE_CLKS)
```

- UOPS_DISPATCHED_PORT.PORT_7
- UOPS_DISPATCHED_PORT.PORT_2
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- UOPS_DISPATCHED_PORT.PORT_4
- UOPS_DISPATCHED_PORT.PORT_3

###### 3.2.2.4.2.1 <a id="port_2">Port_2</a>

This metric represents Core fraction of cycles CPU dispatched uops on execution port 2 ([SNB+]Loads and Store- address; [ICL+] Loads)

- Domain: Core_Clocks
- Threshold:  > 0.6
- Area: BE/Core
- sample: UOPS_DISPATCHED_PORT.PORT_2

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Port_2 = UOPS_DISPATCHED_PORT.PORT_2 / CORE_CLKS
```

- UOPS_DISPATCHED_PORT.PORT_2
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

###### 3.2.2.4.2.2 <a id="port_3">Port_3</a>

This metric represents Core fraction of cycles CPU dispatched uops on execution port 3 ([SNB+]Loads and Store- address; [ICL+] Loads)

- Domain: Core_Clocks
- Threshold:  > 0.6
- Area: BE/Core
- sample: UOPS_DISPATCHED_PORT.PORT_3

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Port_3 = UOPS_DISPATCHED_PORT.PORT_3 / CORE_CLKS
```

- UOPS_DISPATCHED_PORT.PORT_3
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

##### 3.2.2.4.3 <a id="store_op_utilization">Store_Op_Utilization</a>

This metric represents Core fraction of cycles CPU dispatched uops on execution port for Store operations

- Domain: Core_Execution
- Threshold:  > 0.6
- Area: BE/Core

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Store_Op_Utilization = UOPS_DISPATCHED_PORT.PORT_4 / CORE_CLKS
```

- UOPS_DISPATCHED_PORT.PORT_4
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

###### 3.2.2.4.3.1 <a id="port_4">Port_4</a>

This metric represents Core fraction of cycles CPU dispatched uops on execution port 4 (Store-data)

- Domain: Core_Clocks
- Threshold:  > 0.6
- Area: BE/Core
- sample: UOPS_DISPATCHED_PORT.PORT_4

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Port_4 = UOPS_DISPATCHED_PORT.PORT_4 / CORE_CLKS
```

- UOPS_DISPATCHED_PORT.PORT_4
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

###### 3.2.2.4.3.2 <a id="port_7">Port_7</a>

This metric represents Core fraction of cycles CPU dispatched uops on execution port 7 ([HSW+]simple Store- address)

- Domain: Core_Clocks
- Threshold:  > 0.6
- Area: BE/Core
- sample: UOPS_DISPATCHED_PORT.PORT_7

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Port_7 = UOPS_DISPATCHED_PORT.PORT_7 / CORE_CLKS
```

- UOPS_DISPATCHED_PORT.PORT_7
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

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

### 4.1.1 <a id="x87_use">X87_Use</a>

This metric serves as an approximation of legacy x87 usage. It accounts for instructions beyond X87 FP arithmetic operations; hence may be used as a thermometer to avoid X87 high usage and preferably upgrade to modern ISA. See Tip under Tuning Hint.. Tip: consider compiler flags to generate newer AVX (or SSE) instruction sets; which typically perform better and feature vectors.

- Domain: Uops
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- Metric group: Compute

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
UopPI = Retired_Slots / INST_RETIRED.ANY
X87_Use = INST_RETIRED.X87 * UopPI / Retired_Slots
```

- INST_RETIRED.ANY
- UOPS_RETIRED.RETIRE_SLOTS
- INST_RETIRED.X87

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

#### 4.2.1.1 <a id="assists">Assists</a>

This metric estimates fraction of slots the CPU retired uops delivered by the Microcode_Sequencer as a result of Assists. Assists are long sequences of uops that are required in certain corner-cases for operations that cannot be handled natively by the execution pipeline. For example; when working with very small floating point values (so-called Denormals); the FP units are not set up to perform these operations natively. Instead; a sequence of instructions to perform the computation on the Denormals is injected into the pipeline. Since these microcode sequences might be dozens of uops long; Assists can be extremely deleterious to performance and they can be avoided in many cases.

- Domain: Slots_Estimated
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- sample: OTHER_ASSISTS.ANY_WB_ASSIST

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Assists = Avg_Assist_Cost * OTHER_ASSISTS.ANY_WB_ASSIST / SLOTS
```

- OTHER_ASSISTS.ANY_WB_ASSIST
- Pipeline_Width
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- Avg_Assist_Cost

#### 4.2.1.2 <a id="cisc">CISC</a>

This metric estimates fraction of cycles the CPU retired uops originated from CISC (complex instruction set computer) instruction. A CISC instruction has multiple uops that are required to perform the instruction's functionality as in the case of read-modify-write as an example. Since these instructions require multiple uops they may or may not imply sub-optimal use of machine resources.

- Domain: Slots
- Threshold:  > 0.1 and parent over threshold
- Area: RET

```python
CISC = max(0, Microcode_Sequencer - Assists)
```

- [Microcode_Sequencer](#microcode_sequencer)
- [Assists](#assists)

# 5 General Metrics

## 5.1 <a id="metric_uptb">Metric_UpTB</a>

Instruction per taken branch

- Domain: Metric
- Threshold:  < Pipeline_Width * 1.5
- Area: Info.Thread
- Metric group: Branches, Fed, FetchBW

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
UpTB = Retired_Slots / BR_INST_RETIRED.NEAR_TAKEN
Metric_UpTB = UpTB
```

- BR_INST_RETIRED.NEAR_TAKEN
- UOPS_RETIRED.RETIRE_SLOTS

## 5.2 <a id="metric_cpi">Metric_CPI</a>

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

## 5.3 <a id="metric_dram_bw_use">Metric_DRAM_BW_Use</a>

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

## 5.4 <a id="metric_ipcall">Metric_IpCall</a>

Instructions per (near) call (lower number means higher occurrence rate)

- Domain: Inst_Metric
- Threshold:  < 200
- Area: Info.Inst_Mix
- Metric group: Branches, Fed, PGO

```python
IpCall = INST_RETIRED.ANY / BR_INST_RETIRED.NEAR_CALL
Metric_IpCall = IpCall
```

- BR_INST_RETIRED.NEAR_CALL
- INST_RETIRED.ANY

## 5.5 <a id="metric_ipload">Metric_IpLoad</a>

Instructions per Load (lower number means higher occurrence rate)

- Domain: Inst_Metric
- Threshold:  < 3
- Area: Info.Inst_Mix
- Metric group: InsType

```python
IpLoad = INST_RETIRED.ANY / MEM_UOPS_RETIRED.ALL_LOADS
Metric_IpLoad = IpLoad
```

- MEM_UOPS_RETIRED.ALL_LOADS
- INST_RETIRED.ANY

## 5.6 <a id="metric_l2_cache_fill_bw_1t">Metric_L2_Cache_Fill_BW_1T</a>

- Domain: Metric
- Threshold: True
- Area: Info.Memory.Thread
- Metric group: Mem, MemoryBW

```python
Time = interval-s
L2_Cache_Fill_BW = 64 * L2_LINES_IN.ALL / OneBillion / Time
L2_Cache_Fill_BW_1T = L2_Cache_Fill_BW
Metric_L2_Cache_Fill_BW_1T = L2_Cache_Fill_BW_1T
```

- L2_LINES_IN.ALL
- OneBillion
- interval-s

## 5.7 <a id="metric_l1d_cache_fill_bw_1t">Metric_L1D_Cache_Fill_BW_1T</a>

- Domain: Metric
- Threshold: True
- Area: Info.Memory.Thread
- Metric group: Mem, MemoryBW

```python
Time = interval-s
L1D_Cache_Fill_BW = 64 * L1D.REPLACEMENT / OneBillion / Time
L1D_Cache_Fill_BW_1T = L1D_Cache_Fill_BW
Metric_L1D_Cache_Fill_BW_1T = L1D_Cache_Fill_BW_1T
```

- L1D.REPLACEMENT
- OneBillion
- interval-s

## 5.8 <a id="metric_slots">Metric_SLOTS</a>

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

## 5.9 <a id="metric_l3_cache_fill_bw">Metric_L3_Cache_Fill_BW</a>

Average per-core data fill bandwidth to the L3 cache [GB / sec]

- Domain: Core_Metric
- Threshold: True
- Area: Info.Memory.Core
- Metric group: Mem, MemoryBW

```python
Time = interval-s
L3_Cache_Fill_BW = 64 * LONGEST_LAT_CACHE.MISS / OneBillion / Time
Metric_L3_Cache_Fill_BW = L3_Cache_Fill_BW
```

- LONGEST_LAT_CACHE.MISS
- OneBillion
- interval-s

## 5.10 <a id="metric_smt_2t_utilization">Metric_SMT_2T_Utilization</a>

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

## 5.11 <a id="metric_load_l2_miss_latency">Metric_Load_L2_Miss_Latency</a>

Average Latency for L2 cache miss demand Loads

- Domain: Clocks_Latency
- Max value: 1000
- Threshold: True
- Area: Info.Memory.ORO
- Metric group: Memory_Lat, Offcore

```python
Load_L2_Miss_Latency = OFFCORE_REQUESTS_OUTSTANDING.DEMAND_DATA_RD / OFFCORE_REQUESTS.DEMAND_DATA_RD
Metric_Load_L2_Miss_Latency = Load_L2_Miss_Latency
```

- OFFCORE_REQUESTS_OUTSTANDING.DEMAND_DATA_RD
- OFFCORE_REQUESTS.DEMAND_DATA_RD

## 5.12 <a id="metric_ipstore">Metric_IpStore</a>

Instructions per Store (lower number means higher occurrence rate)

- Domain: Inst_Metric
- Threshold:  < 8
- Area: Info.Inst_Mix
- Metric group: InsType

```python
IpStore = INST_RETIRED.ANY / MEM_UOPS_RETIRED.ALL_STORES
Metric_IpStore = IpStore
```

- INST_RETIRED.ANY
- MEM_UOPS_RETIRED.ALL_STORES

## 5.13 <a id="metric_uoppi">Metric_UopPI</a>

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

## 5.14 <a id="metric_turbo_utilization">Metric_Turbo_Utilization</a>

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

## 5.15 <a id="metric_data_l2_mlp">Metric_Data_L2_MLP</a>

Average Parallel L2 cache miss data reads

- Domain: Metric
- Max value: 100
- Threshold: True
- Area: Info.Memory.ORO
- Metric group: Memory_BW, Offcore

```python
Data_L2_MLP = OFFCORE_REQUESTS_OUTSTANDING.ALL_DATA_RD / OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DATA_RD
Metric_Data_L2_MLP = Data_L2_MLP
```

- OFFCORE_REQUESTS_OUTSTANDING.ALL_DATA_RD
- OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DATA_RD

## 5.16 <a id="metric_page_walks_utilization">Metric_Page_Walks_Utilization</a>

Utilization of the core's Page Walker(s) serving STLB misses triggered by instruction/Load/Store accesses

- Domain: Core_Metric
- Max value: 1.0
- Threshold:  > 0.5
- Area: Info.Memory.TLB
- Metric group: Mem, MemoryTLB

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Page_Walks_Utilization = (ITLB_MISSES.WALK_DURATION + DTLB_LOAD_MISSES.WALK_DURATION + DTLB_STORE_MISSES.WALK_DURATION) / CORE_CLKS
Metric_Page_Walks_Utilization = Page_Walks_Utilization
```

- DTLB_LOAD_MISSES.WALK_DURATION
- ITLB_MISSES.WALK_DURATION
- DTLB_STORE_MISSES.WALK_DURATION
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

## 5.17 <a id="metric_core_clks">Metric_CORE_CLKS</a>

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

## 5.18 <a id="metric_l2mpki">Metric_L2MPKI</a>

L2 cache true misses per kilo instruction for retired demand loads

- Domain: Metric
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, Backend, CacheMisses

```python
L2MPKI = 1000 * MEM_LOAD_UOPS_RETIRED.L2_MISS / INST_RETIRED.ANY
Metric_L2MPKI = L2MPKI
```

- INST_RETIRED.ANY
- MEM_LOAD_UOPS_RETIRED.L2_MISS

## 5.19 <a id="metric_l1mpki">Metric_L1MPKI</a>

L1 cache true misses per kilo instruction for retired demand loads

- Domain: Metric
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, CacheMisses

```python
L1MPKI = 1000 * MEM_LOAD_UOPS_RETIRED.L1_MISS / INST_RETIRED.ANY
Metric_L1MPKI = L1MPKI
```

- MEM_LOAD_UOPS_RETIRED.L1_MISS
- INST_RETIRED.ANY

## 5.20 <a id="metric_ilp">Metric_ILP</a>

Instruction-Level-Parallelism (average number of uops executed when there is execution) per-core

- Domain: Core_Metric
- Max value: Exe_Ports
- Threshold: True
- Area: Info.Core
- Metric group: Backend, Cor, Pipeline, PortsUtil

```python
Execute_Cycles = UOPS_EXECUTED.CORE:c1 / 2 if smt_enabled else UOPS_EXECUTED.CORE:c1
ILP = UOPS_EXECUTED.CORE / 2 / Execute_Cycles if smt_enabled else UOPS_EXECUTED.CORE / Execute_Cycles
Metric_ILP = ILP
```

- smt_enabled
- UOPS_EXECUTED.CORE
- UOPS_EXECUTED.CORE:c1

## 5.21 <a id="metric_ipunknown_branch">Metric_IpUnknown_Branch</a>

Instructions per speculative Unknown Branch Misprediction (BAClear) (lower number means higher occurrence rate)

- Domain: Metric
- Threshold: True
- Area: Info.Frontend
- Metric group: Fed

```python
Instructions = INST_RETIRED.ANY
IpUnknown_Branch = Instructions / BACLEARS.ANY
Metric_IpUnknown_Branch = IpUnknown_Branch
```

- BACLEARS.ANY
- INST_RETIRED.ANY

## 5.22 <a id="metric_ipfarbranch">Metric_IpFarBranch</a>

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

## 5.23 <a id="metric_kernel_utilization">Metric_Kernel_Utilization</a>

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

## 5.24 <a id="metric_cpu_utilization">Metric_CPU_Utilization</a>

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

## 5.25 <a id="metric_mlp">Metric_MLP</a>

Memory-Level-Parallelism (average number of L1 miss demand load when there is at least one such miss. Per-Logical Processor)

- Domain: Metric
- Max value: 10.0
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, MemoryBound, MemoryBW

```python
MLP = L1D_PEND_MISS.PENDING / L1D_PEND_MISS.PENDING_CYCLES
Metric_MLP = MLP
```

- L1D_PEND_MISS.PENDING
- L1D_PEND_MISS.PENDING_CYCLES

## 5.26 <a id="metric_instructions">Metric_Instructions</a>

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

## 5.27 <a id="metric_socket_clks">Metric_Socket_CLKS</a>

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

## 5.28 <a id="metric_ipc">Metric_IPC</a>

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

## 5.29 <a id="metric_ipmisp_indirect">Metric_IpMisp_Indirect</a>

Instructions per retired mispredicts for indirect CALL or JMP branches (lower number means higher occurrence rate).

- Domain: Inst_Metric
- Threshold:  < 1000
- Area: Info.Bad_Spec
- Metric group: Bad, BrMispredicts

```python
Instructions = INST_RETIRED.ANY
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
Retire_Fraction = Retired_Slots / UOPS_ISSUED.ANY
IpMisp_Indirect = Instructions / (Retire_Fraction * BR_MISP_EXEC.ALL_BRANCHES:u0xE4)
Metric_IpMisp_Indirect = IpMisp_Indirect
```

- UOPS_ISSUED.ANY
- UOPS_RETIRED.RETIRE_SLOTS
- INST_RETIRED.ANY
- BR_MISP_EXEC.ALL_BRANCHES:u0xE4

## 5.30 <a id="metric_kernel_cpi">Metric_Kernel_CPI</a>

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

## 5.31 <a id="metric_l2_cache_fill_bw">Metric_L2_Cache_Fill_BW</a>

Average per-core data fill bandwidth to the L2 cache [GB / sec]

- Domain: Core_Metric
- Threshold: True
- Area: Info.Memory.Core
- Metric group: Mem, MemoryBW

```python
Time = interval-s
L2_Cache_Fill_BW = 64 * L2_LINES_IN.ALL / OneBillion / Time
Metric_L2_Cache_Fill_BW = L2_Cache_Fill_BW
```

- L2_LINES_IN.ALL
- OneBillion
- interval-s

## 5.32 <a id="metric_mem_request_latency">Metric_MEM_Request_Latency</a>

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

## 5.33 <a id="metric_ipbranch">Metric_IpBranch</a>

Instructions per Branch (lower number means higher occurrence rate)

- Domain: Inst_Metric
- Threshold:  < 8
- Area: Info.Inst_Mix
- Metric group: Branches, Fed, InsType

```python
IpBranch = INST_RETIRED.ANY / BR_INST_RETIRED.ALL_BRANCHES
Metric_IpBranch = IpBranch
```

- BR_INST_RETIRED.ALL_BRANCHES
- INST_RETIRED.ANY

## 5.34 <a id="metric_coreipc">Metric_CoreIPC</a>

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

## 5.35 <a id="metric_mem_parallel_requests">Metric_MEM_Parallel_Requests</a>

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

## 5.36 <a id="metric_load_miss_real_latency">Metric_Load_Miss_Real_Latency</a>

Actual Average Latency for L1 data-cache miss demand load operations (in core cycles)

- Domain: Clocks_Latency
- Max value: 1000
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, MemoryBound, MemoryLat

```python
Load_Miss_Real_Latency = L1D_PEND_MISS.PENDING / (MEM_LOAD_UOPS_RETIRED.L1_MISS + MEM_LOAD_UOPS_RETIRED.HIT_LFB)
Metric_Load_Miss_Real_Latency = Load_Miss_Real_Latency
```

- MEM_LOAD_UOPS_RETIRED.HIT_LFB
- MEM_LOAD_UOPS_RETIRED.L1_MISS
- L1D_PEND_MISS.PENDING

## 5.37 <a id="metric_l3_cache_fill_bw_1t">Metric_L3_Cache_Fill_BW_1T</a>

- Domain: Metric
- Threshold: True
- Area: Info.Memory.Thread
- Metric group: Mem, MemoryBW

```python
Time = interval-s
L3_Cache_Fill_BW = 64 * LONGEST_LAT_CACHE.MISS / OneBillion / Time
L3_Cache_Fill_BW_1T = L3_Cache_Fill_BW
Metric_L3_Cache_Fill_BW_1T = L3_Cache_Fill_BW_1T
```

- LONGEST_LAT_CACHE.MISS
- OneBillion
- interval-s

## 5.38 <a id="metric_average_frequency">Metric_Average_Frequency</a>

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

## 5.39 <a id="metric_clks">Metric_CLKS</a>

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

## 5.40 <a id="metric_iptb">Metric_IpTB</a>

Instruction per taken branch

- Domain: Inst_Metric
- Threshold:  < Pipeline_Width * 2 + 1
- Area: Info.Inst_Mix
- Metric group: Branches, Fed, FetchBW, Frontend, PGO

```python
IpTB = INST_RETIRED.ANY / BR_INST_RETIRED.NEAR_TAKEN
Metric_IpTB = IpTB
```

- INST_RETIRED.ANY
- BR_INST_RETIRED.NEAR_TAKEN

## 5.41 <a id="metric_dsb_coverage">Metric_DSB_Coverage</a>

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

## 5.42 <a id="metric_bptkbranch">Metric_BpTkBranch</a>

Branch instructions per taken branch. . Can be used to approximate PGO-likelihood for non-loopy codes.

- Domain: Metric
- Threshold: True
- Area: Info.Inst_Mix
- Metric group: Branches, Fed, PGO

```python
BpTkBranch = BR_INST_RETIRED.ALL_BRANCHES / BR_INST_RETIRED.NEAR_TAKEN
Metric_BpTkBranch = BpTkBranch
```

- BR_INST_RETIRED.ALL_BRANCHES
- BR_INST_RETIRED.NEAR_TAKEN

## 5.43 <a id="metric_load_l2_mlp">Metric_Load_L2_MLP</a>

Average Parallel L2 cache miss demand Loads

- Domain: Metric
- Max value: 100
- Threshold: True
- Area: Info.Memory.ORO
- Metric group: Memory_BW, Offcore

```python
Load_L2_MLP = OFFCORE_REQUESTS_OUTSTANDING.DEMAND_DATA_RD / OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_DATA_RD
Metric_Load_L2_MLP = Load_L2_MLP
```

- OFFCORE_REQUESTS_OUTSTANDING.DEMAND_DATA_RD
- OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_DATA_RD

## 5.44 <a id="metric_time">Metric_Time</a>

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

## 5.45 <a id="metric_ipmispredict">Metric_IpMispredict</a>

Number of Instructions per non-speculative Branch Misprediction (JEClear) (lower number means higher occurrence rate)

- Domain: Inst_Metric
- Threshold:  < 200
- Area: Info.Bad_Spec
- Metric group: Bad, BadSpec, BrMispredicts

```python
IpMispredict = INST_RETIRED.ANY / BR_MISP_RETIRED.ALL_BRANCHES
Metric_IpMispredict = IpMispredict
```

- BR_MISP_RETIRED.ALL_BRANCHES
- INST_RETIRED.ANY

## 5.46 <a id="metric_l1d_cache_fill_bw">Metric_L1D_Cache_Fill_BW</a>

Average per-core data fill bandwidth to the L1 data cache [GB / sec]

- Domain: Core_Metric
- Threshold: True
- Area: Info.Memory.Core
- Metric group: Mem, MemoryBW

```python
Time = interval-s
L1D_Cache_Fill_BW = 64 * L1D.REPLACEMENT / OneBillion / Time
Metric_L1D_Cache_Fill_BW = L1D_Cache_Fill_BW
```

- L1D.REPLACEMENT
- OneBillion
- interval-s

## 5.47 <a id="metric_retire">Metric_Retire</a>

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

## 5.48 <a id="metric_l3mpki">Metric_L3MPKI</a>

L3 cache true misses per kilo instruction for retired demand loads

- Domain: Metric
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, CacheMisses

```python
L3MPKI = 1000 * MEM_LOAD_UOPS_RETIRED.L3_MISS / INST_RETIRED.ANY
Metric_L3MPKI = L3MPKI
```

- MEM_LOAD_UOPS_RETIRED.L3_MISS
- INST_RETIRED.ANY

