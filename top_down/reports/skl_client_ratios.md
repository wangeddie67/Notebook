# 1 <a id="frontend_bound">Frontend_Bound</a>

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
- sample: FRONTEND_RETIRED.LATENCY_GE_16:pp, FRONTEND_RETIRED.LATENCY_GE_8:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Fetch_Latency = Pipeline_Width * IDQ_UOPS_NOT_DELIVERED.CYCLES_0_UOPS_DELIV.CORE / SLOTS
```

- IDQ_UOPS_NOT_DELIVERED.CYCLES_0_UOPS_DELIV.CORE
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
- sample: FRONTEND_RETIRED.L2_MISS:pp, FRONTEND_RETIRED.L1I_MISS:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
ICache_Misses = (ICACHE_16B.IFDATA_STALL + 2 * ICACHE_16B.IFDATA_STALL:c1:e1) / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- ICACHE_16B.IFDATA_STALL
- ICACHE_16B.IFDATA_STALL:c1:e1

### 1.1.2 <a id="itlb_misses">ITLB_Misses</a>

This metric represents fraction of cycles the CPU was stalled due to Instruction TLB (ITLB) misses.. Consider large 2M pages for code (selectively prefer hot large-size function, due to limited 2M entries). Linux options: standard binaries use libhugetlbfs; Hfsort.. https://github. com/libhugetlbfs/libhugetlbfs;https://research.fb.com/public ations/optimizing-function-placement-for-large-scale-data- center-applications-2/

- Domain: Clocks
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: BigFoot, FetchLat, MemoryTLB
- sample: FRONTEND_RETIRED.STLB_MISS:pp, FRONTEND_RETIRED.ITLB_MISS:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
ITLB_Misses = ICACHE_64B.IFTAG_STALL / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- ICACHE_64B.IFTAG_STALL

### 1.1.3 <a id="branch_resteers">Branch_Resteers</a>

This metric represents fraction of cycles the CPU was stalled due to Branch Resteers. Branch Resteers estimates the Frontend delay in fetching operations from corrected path; following all sorts of miss-predicted branches. For example; branchy code with lots of miss-predictions might get categorized under Branch Resteers. Note the value of this node may overlap with its siblings.

- Domain: Clocks_Estimated
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: FetchLat
- sample: BR_MISP_RETIRED.ALL_BRANCHES

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Branch_Resteers = INT_MISC.CLEAR_RESTEER_CYCLES / CLKS + Unknown_Branches
```

- INT_MISC.CLEAR_RESTEER_CYCLES
- [Unknown_Branches](#unknown_branches)
- CPU_CLK_UNHALTED.THREAD

#### 1.1.3.1 <a id="mispredicts_resteers">Mispredicts_Resteers</a>

This metric represents fraction of cycles the CPU was stalled due to Branch Resteers as a result of Branch Misprediction at execution stage.

- Domain: Clocks
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: BadSpec, BrMispredicts
- sample: INT_MISC.CLEAR_RESTEER_CYCLES

```python
Mispred_Clears_Fraction = BR_MISP_RETIRED.ALL_BRANCHES / (BR_MISP_RETIRED.ALL_BRANCHES + MACHINE_CLEARS.COUNT)
CLKS = CPU_CLK_UNHALTED.THREAD
Mispredicts_Resteers = Mispred_Clears_Fraction * INT_MISC.CLEAR_RESTEER_CYCLES / CLKS
```

- INT_MISC.CLEAR_RESTEER_CYCLES
- CPU_CLK_UNHALTED.THREAD
- BR_MISP_RETIRED.ALL_BRANCHES
- MACHINE_CLEARS.COUNT

#### 1.1.3.2 <a id="clears_resteers">Clears_Resteers</a>

This metric represents fraction of cycles the CPU was stalled due to Branch Resteers as a result of Machine Clears.

- Domain: Clocks
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: BadSpec, MachineClears
- sample: INT_MISC.CLEAR_RESTEER_CYCLES

```python
Mispred_Clears_Fraction = BR_MISP_RETIRED.ALL_BRANCHES / (BR_MISP_RETIRED.ALL_BRANCHES + MACHINE_CLEARS.COUNT)
CLKS = CPU_CLK_UNHALTED.THREAD
Clears_Resteers = (1 - Mispred_Clears_Fraction) * INT_MISC.CLEAR_RESTEER_CYCLES / CLKS
```

- INT_MISC.CLEAR_RESTEER_CYCLES
- CPU_CLK_UNHALTED.THREAD
- BR_MISP_RETIRED.ALL_BRANCHES
- MACHINE_CLEARS.COUNT

#### 1.1.3.3 <a id="unknown_branches">Unknown_Branches</a>

This metric represents fraction of cycles the CPU was stalled due to new branch address clears. These are fetched branches the Branch Prediction Unit was unable to recognize (e.g. first time the branch is fetched or hitting BTB capacity limit).

- Domain: Clocks
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: BigFoot, FetchLat
- sample: BACLEARS.ANY

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Unknown_Branches = BAClear_Cost * BACLEARS.ANY / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- BACLEARS.ANY
- BAClear_Cost

### 1.1.4 <a id="dsb_switches">DSB_Switches</a>

This metric represents fraction of cycles the CPU was stalled due to switches from DSB to MITE pipelines. The DSB (decoded i-cache) is a Uop Cache where the front-end directly delivers Uops (micro operations) avoiding heavy x86 decoding. The DSB pipeline has shorter latency and delivered higher bandwidth than the MITE (legacy instruction decode pipeline). Switching between the two pipelines can cause penalties hence this metric measures the exposed penalty.. See section 'Optimization for Decoded Icache' in Optimization Manual:. http://www.intel.com/content/www/us/en /architecture-and-technology/64-ia-32-architectures- optimization-manual.html

- Domain: Clocks
- Threshold:  > 0.05 and parent over threshold
- Area: FE
- Metric group: DSBmiss, FetchLat
- sample: FRONTEND_RETIRED.DSB_MISS:pp

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
- sample: FRONTEND_RETIRED.LATENCY_GE_2_BUBBLES_GE_1:pp, FRONTEND_RETIRED.LATENCY_GE_1:pp, FRONTEND_RETIRED.LATENCY_GE_2:pp

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
- sample: FRONTEND_RETIRED.ANY_DSB_MISS

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

#### 1.2.1.1 <a id="decoder0_alone">Decoder0_Alone</a>

This metric represents fraction of cycles where decoder-0 was the only active decoder

- Domain: Slots_Estimated
- Threshold:  > 0.1 and parent over threshold
- Area: FE
- Metric group: DSBmiss, FetchBW

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Decoder0_Alone = (INST_DECODED.DECODERS:c1 - INST_DECODED.DECODERS:c2) / CORE_CLKS / 2
```

- INST_DECODED.DECODERS:c2
- INST_DECODED.DECODERS:c1
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

### 1.2.3 <a id="lsd">LSD</a>

This metric represents Core fraction of cycles in which CPU was likely limited due to LSD (Loop Stream Detector) unit. LSD typically does well sustaining Uop supply. However; in some rare cases; optimal uop-delivery could not be reached for small loops whose size (in terms of number of uops) does not suit well the LSD structure.

- Domain: Slots_Estimated
- Threshold:  > 0.15 and parent over threshold
- Area: FE
- Metric group: FetchBW, LSD

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
LSD = (LSD.CYCLES_ACTIVE - LSD.CYCLES_4_UOPS) / CORE_CLKS / 2
```

- LSD.CYCLES_ACTIVE
- LSD.CYCLES_4_UOPS
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
Recovery_Cycles = INT_MISC.RECOVERY_CYCLES_ANY / 2 if smt_enabled else INT_MISC.RECOVERY_CYCLES
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Backend_Bound = 1 - Frontend_Bound - (UOPS_ISSUED.ANY + Pipeline_Width * Recovery_Cycles) / SLOTS
```

- UOPS_ISSUED.ANY
- [Frontend_Bound](#frontend_bound)
- Pipeline_Width
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- INT_MISC.RECOVERY_CYCLES_ANY
- INT_MISC.RECOVERY_CYCLES

## 3.1 <a id="memory_bound">Memory_Bound</a>

This metric represents fraction of slots the Memory subsystem within the Backend was a bottleneck. Memory Bound estimates fraction of slots where pipeline is likely stalled due to demand load or store instructions. This accounts mainly for (1) non-completed in-flight memory demand loads which coincides with execution units starvation; in addition to (2) cases where stores could impose backpressure on the pipeline when many of them get buffered at the same time (less common out of the two).

- Domain: Slots
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Mem
- Metric group: Backend, TmaL2

```python
Few_Uops_Executed_Threshold = EXE_ACTIVITY.1_PORTS_UTIL + Retiring * EXE_ACTIVITY.2_PORTS_UTIL
Backend_Bound_Cycles = CYCLE_ACTIVITY.STALLS_TOTAL + Few_Uops_Executed_Threshold + EXE_ACTIVITY.BOUND_ON_STORES
Memory_Bound_Fraction = (CYCLE_ACTIVITY.STALLS_MEM_ANY + EXE_ACTIVITY.BOUND_ON_STORES) / Backend_Bound_Cycles
Memory_Bound = Memory_Bound_Fraction * Backend_Bound
```

- [Backend_Bound](#backend_bound)
- EXE_ACTIVITY.BOUND_ON_STORES
- CYCLE_ACTIVITY.STALLS_TOTAL
- [Retiring](#retiring)
- EXE_ACTIVITY.1_PORTS_UTIL
- EXE_ACTIVITY.2_PORTS_UTIL
- CYCLE_ACTIVITY.STALLS_MEM_ANY

### 3.1.1 <a id="l1_bound">L1_Bound</a>

This metric estimates how often the CPU was stalled without loads missing the L1 data cache. The L1 data cache typically has the shortest latency. However; in certain cases like loads blocked on older stores; a load might suffer due to high latency even though it is being satisfied by the L1. Another example is loads who miss in the TLB. These cases are characterized by execution unit stalls; while some non-completed demand load lives in the machine without having that demand load missing the L1 cache.

- Domain: Stalls
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Mem
- Metric group: CacheMisses, MemoryBound, TmaL3mem
- sample: MEM_LOAD_RETIRED.L1_HIT:pp, MEM_LOAD_RETIRED.FB_HIT:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
L1_Bound = max((CYCLE_ACTIVITY.STALLS_MEM_ANY - CYCLE_ACTIVITY.STALLS_L1D_MISS) / CLKS, 0)
```

- CPU_CLK_UNHALTED.THREAD
- CYCLE_ACTIVITY.STALLS_L1D_MISS
- CYCLE_ACTIVITY.STALLS_MEM_ANY

#### 3.1.1.1 <a id="dtlb_load">DTLB_Load</a>

This metric roughly estimates the fraction of cycles where the Data TLB (DTLB) was missed by load accesses. TLBs (Translation Look-aside Buffers) are processor caches for recently used entries out of the Page Tables that are used to map virtual- to physical-addresses by the operating system. This metric approximates the potential delay of demand loads missing the first-level data TLB (assuming worst case scenario with back to back misses to different pages). This includes hitting in the second-level TLB (STLB) as well as performing a hardware page walk on an STLB miss..

- Domain: Clocks_Estimated
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryTLB
- sample: MEM_INST_RETIRED.STLB_MISS_LOADS:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
DTLB_Load = min(Mem_STLB_Hit_Cost * DTLB_LOAD_MISSES.STLB_HIT:c1 + DTLB_LOAD_MISSES.WALK_ACTIVE, max(CYCLE_ACTIVITY.CYCLES_MEM_ANY - CYCLE_ACTIVITY.CYCLES_L1D_MISS, 0)) / CLKS
```

- CYCLE_ACTIVITY.CYCLES_L1D_MISS
- DTLB_LOAD_MISSES.WALK_ACTIVE
- Mem_STLB_Hit_Cost
- CYCLE_ACTIVITY.CYCLES_MEM_ANY
- CPU_CLK_UNHALTED.THREAD
- DTLB_LOAD_MISSES.STLB_HIT:c1

##### 3.1.1.1.1 <a id="load_stlb_hit">Load_STLB_Hit</a>

This metric roughly estimates the fraction of cycles where the (first level) DTLB was missed by load accesses, that later on hit in second-level TLB (STLB)

- Domain: Clocks_Estimated
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryTLB

```python
Load_STLB_Hit = DTLB_Load - Load_STLB_Miss
```

- [DTLB_Load](#dtlb_load)
- [Load_STLB_Miss](#load_stlb_miss)

##### 3.1.1.1.2 <a id="load_stlb_miss">Load_STLB_Miss</a>

This metric estimates the fraction of cycles where the Second-level TLB (STLB) was missed by load accesses, performing a hardware page walk

- Domain: Clocks_Calculated
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryTLB

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Load_STLB_Miss = DTLB_LOAD_MISSES.WALK_ACTIVE / CLKS
```

- DTLB_LOAD_MISSES.WALK_ACTIVE
- CPU_CLK_UNHALTED.THREAD

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
- sample: MEM_INST_RETIRED.LOCK_LOADS:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
ORO_Demand_RFO_C1 = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_RFO', level)), level)
Mem_Lock_St_Fraction = MEM_INST_RETIRED.LOCK_LOADS / MEM_INST_RETIRED.ALL_STORES
Lock_Latency = (12 * max(0, MEM_INST_RETIRED.LOCK_LOADS - L2_RQSTS.ALL_RFO) + Mem_Lock_St_Fraction * (Mem_L2_Store_Cost * L2_RQSTS.RFO_HIT + ORO_Demand_RFO_C1)) / CLKS
```

- L2_RQSTS.ALL_RFO
- MEM_INST_RETIRED.LOCK_LOADS
- MEM_INST_RETIRED.ALL_STORES
- level
- EV
- L2_RQSTS.RFO_HIT
- Mem_L2_Store_Cost
- CPU_CLK_UNHALTED.THREAD

#### 3.1.1.4 <a id="split_loads">Split_Loads</a>

This metric estimates fraction of cycles handling memory load split accesses - load that cross 64-byte cache line boundary. . Consider aligning data or hot structure fields. See the Optimization Manual for more details

- Domain: Clocks_Calculated
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Mem
- sample: MEM_INST_RETIRED.SPLIT_LOADS:pp

```python
Load_Miss_Real_Latency = L1D_PEND_MISS.PENDING / (MEM_LOAD_RETIRED.L1_MISS + MEM_LOAD_RETIRED.FB_HIT)
CLKS = CPU_CLK_UNHALTED.THREAD
Split_Loads = Load_Miss_Real_Latency * LD_BLOCKS.NO_SR / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- LD_BLOCKS.NO_SR
- MEM_LOAD_RETIRED.L1_MISS
- L1D_PEND_MISS.PENDING
- MEM_LOAD_RETIRED.FB_HIT

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
Load_Miss_Real_Latency = L1D_PEND_MISS.PENDING / (MEM_LOAD_RETIRED.L1_MISS + MEM_LOAD_RETIRED.FB_HIT)
CLKS = CPU_CLK_UNHALTED.THREAD
FB_Full = Load_Miss_Real_Latency * L1D_PEND_MISS.FB_FULL:c1 / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- L1D_PEND_MISS.FB_FULL:c1
- MEM_LOAD_RETIRED.L1_MISS
- L1D_PEND_MISS.PENDING
- MEM_LOAD_RETIRED.FB_HIT

### 3.1.2 <a id="l2_bound">L2_Bound</a>

This metric estimates how often the CPU was stalled due to L2 cache accesses by loads. Avoiding cache misses (i.e. L1 misses/L2 hits) can improve the latency and increase performance.

- Domain: Stalls
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: CacheMisses, MemoryBound, TmaL3mem
- sample: MEM_LOAD_RETIRED.L2_HIT:pp

```python
FBHit_per_L1Miss = MEM_LOAD_RETIRED.FB_HIT / MEM_LOAD_RETIRED.L1_MISS
LOAD_L2_HIT = MEM_LOAD_RETIRED.L2_HIT * (1 + FBHit_per_L1Miss)
CLKS = CPU_CLK_UNHALTED.THREAD
L2_Bound_Ratio = (CYCLE_ACTIVITY.STALLS_L1D_MISS - CYCLE_ACTIVITY.STALLS_L2_MISS) / CLKS
L2_Bound = LOAD_L2_HIT / (LOAD_L2_HIT + L1D_PEND_MISS.FB_FULL:c1) * L2_Bound_Ratio
```

- CPU_CLK_UNHALTED.THREAD
- CYCLE_ACTIVITY.STALLS_L1D_MISS
- CYCLE_ACTIVITY.STALLS_L2_MISS
- L1D_PEND_MISS.FB_FULL:c1
- MEM_LOAD_RETIRED.L1_MISS
- MEM_LOAD_RETIRED.FB_HIT
- MEM_LOAD_RETIRED.L2_HIT

### 3.1.3 <a id="l3_bound">L3_Bound</a>

This metric estimates how often the CPU was stalled due to loads accesses to L3 cache or contended with a sibling Core. Avoiding cache misses (i.e. L2 misses/L3 hits) can improve the latency and increase performance.

- Domain: Stalls
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: CacheMisses, MemoryBound, TmaL3mem
- sample: MEM_LOAD_RETIRED.L3_HIT:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
L3_Bound = (CYCLE_ACTIVITY.STALLS_L2_MISS - CYCLE_ACTIVITY.STALLS_L3_MISS) / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- CYCLE_ACTIVITY.STALLS_L3_MISS
- CYCLE_ACTIVITY.STALLS_L2_MISS

#### 3.1.3.1 <a id="contested_accesses">Contested_Accesses</a>

This metric estimates fraction of cycles while the memory subsystem was handling synchronizations due to contested accesses. Contested accesses occur when data written by one Logical Processor are read by another Logical Processor on a different Physical Core. Examples of contested accesses include synchronizations such as locks; true data sharing such as modified locked variables; and false sharing.

- Domain: Clocks_Estimated
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: DataSharing, Offcore, Snoop
- sample: MEM_LOAD_L3_HIT_RETIRED.XSNP_HITM:pp, MEM_LOAD_L3_HIT_RETIRED.XSNP_MISS:pp

```python
LOAD_XSNP_MISS = MEM_LOAD_L3_HIT_RETIRED.XSNP_MISS
CLKS = CPU_CLK_UNHALTED.THREAD
Time = interval-s
Turbo_Utilization = CLKS / CPU_CLK_UNHALTED.REF_TSC
Average_Frequency = Turbo_Utilization * msr/tsc/ / OneBillion / Time
Mem_L2_Hit_Cost = 3.5 * Average_Frequency
FBHit_per_L1Miss = MEM_LOAD_RETIRED.FB_HIT / MEM_LOAD_RETIRED.L1_MISS
FB_Factor = 1 + FBHit_per_L1Miss / 2
Mem_XSNP_HitM_Cost = 22 * Average_Frequency
LOAD_XSNP_HITM = MEM_LOAD_L3_HIT_RETIRED.XSNP_HITM
Mem_XSNP_Hit_Cost = 20 * Average_Frequency
Contested_Accesses = ((Mem_XSNP_HitM_Cost - Mem_L2_Hit_Cost) * LOAD_XSNP_HITM + (Mem_XSNP_Hit_Cost - Mem_L2_Hit_Cost) * LOAD_XSNP_MISS) * FB_Factor / CLKS
```

- CPU_CLK_UNHALTED.REF_TSC
- CPU_CLK_UNHALTED.THREAD
- msr/tsc/
- OneBillion
- interval-s
- MEM_LOAD_L3_HIT_RETIRED.XSNP_HITM
- MEM_LOAD_RETIRED.L1_MISS
- MEM_LOAD_RETIRED.FB_HIT
- MEM_LOAD_L3_HIT_RETIRED.XSNP_MISS

#### 3.1.3.2 <a id="data_sharing">Data_Sharing</a>

This metric estimates fraction of cycles while the memory subsystem was handling synchronizations due to data-sharing accesses. Data shared by multiple Logical Processors (even just read shared) may cause increased access latency due to cache coherency. Excessive data sharing can drastically harm multithreaded performance.

- Domain: Clocks_Estimated
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: Offcore, Snoop
- sample: MEM_LOAD_L3_HIT_RETIRED.XSNP_HIT:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Time = interval-s
Turbo_Utilization = CLKS / CPU_CLK_UNHALTED.REF_TSC
Average_Frequency = Turbo_Utilization * msr/tsc/ / OneBillion / Time
Mem_L2_Hit_Cost = 3.5 * Average_Frequency
FBHit_per_L1Miss = MEM_LOAD_RETIRED.FB_HIT / MEM_LOAD_RETIRED.L1_MISS
FB_Factor = 1 + FBHit_per_L1Miss / 2
LOAD_XSNP_HIT = MEM_LOAD_L3_HIT_RETIRED.XSNP_HIT
Mem_XSNP_Hit_Cost = 20 * Average_Frequency
Data_Sharing = (Mem_XSNP_Hit_Cost - Mem_L2_Hit_Cost) * LOAD_XSNP_HIT * FB_Factor / CLKS
```

- CPU_CLK_UNHALTED.REF_TSC
- CPU_CLK_UNHALTED.THREAD
- msr/tsc/
- OneBillion
- interval-s
- MEM_LOAD_L3_HIT_RETIRED.XSNP_HIT
- MEM_LOAD_RETIRED.L1_MISS
- MEM_LOAD_RETIRED.FB_HIT

#### 3.1.3.3 <a id="l3_hit_latency">L3_Hit_Latency</a>

This metric represents fraction of cycles with demand load accesses that hit the L3 cache under unloaded scenarios (possibly L3 latency limited). Avoiding private cache misses (i.e. L2 misses/L3 hits) will improve the latency; reduce contention with sibling physical cores and increase performance. Note the value of this node may overlap with its siblings.

- Domain: Clocks_Estimated
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryLat
- sample: MEM_LOAD_RETIRED.L3_HIT:pp

```python
Time = interval-s
CLKS = CPU_CLK_UNHALTED.THREAD
Turbo_Utilization = CLKS / CPU_CLK_UNHALTED.REF_TSC
Average_Frequency = Turbo_Utilization * msr/tsc/ / OneBillion / Time
Mem_XSNP_None_Cost = 10 * Average_Frequency
Mem_L2_Hit_Cost = 3.5 * Average_Frequency
FBHit_per_L1Miss = MEM_LOAD_RETIRED.FB_HIT / MEM_LOAD_RETIRED.L1_MISS
FB_Factor = 1 + FBHit_per_L1Miss / 2
LOAD_L3_HIT = MEM_LOAD_RETIRED.L3_HIT
L3_Hit_Latency = (Mem_XSNP_None_Cost - Mem_L2_Hit_Cost) * LOAD_L3_HIT * FB_Factor / CLKS
```

- MEM_LOAD_RETIRED.L3_HIT
- MEM_LOAD_RETIRED.L1_MISS
- MEM_LOAD_RETIRED.FB_HIT
- CPU_CLK_UNHALTED.REF_TSC
- CPU_CLK_UNHALTED.THREAD
- msr/tsc/
- OneBillion
- interval-s

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
- sample: MEM_LOAD_RETIRED.L3_MISS:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
L2_Bound_Ratio = (CYCLE_ACTIVITY.STALLS_L1D_MISS - CYCLE_ACTIVITY.STALLS_L2_MISS) / CLKS
MEM_Bound_Ratio = CYCLE_ACTIVITY.STALLS_L3_MISS / CLKS + L2_Bound_Ratio - L2_Bound
DRAM_Bound = MEM_Bound_Ratio
```

- CPU_CLK_UNHALTED.THREAD
- CYCLE_ACTIVITY.STALLS_L1D_MISS
- CYCLE_ACTIVITY.STALLS_L2_MISS
- CYCLE_ACTIVITY.STALLS_L3_MISS
- [L2_Bound](#l2_bound)

#### 3.1.4.1 <a id="mem_bandwidth">MEM_Bandwidth</a>

This metric estimates fraction of cycles where the core's performance was likely hurt due to approaching bandwidth limits of external memory (DRAM). The underlying heuristic assumes that a similar off-core traffic is generated by all IA cores. This metric does not aggregate non-data-read requests by this logical processor; requests from other IA Logical Processors/Physical Cores/sockets; or other non-IA devices like GPU; hence the maximum external memory bandwidth limits may or may not be approached when this metric is flagged (see Uncore counters for that).. Improve data accesses to reduce cacheline transfers from/to memory. Examples: 1) Consume all bytes of a each cacheline before it is evicted (e.g. reorder structure elements and split non- hot ones), 2) merge computed-limited with BW-limited loops, 3) NUMA optimizations in multi-socket system. Note: software prefetches will not help BW-limited application..

- Domain: Clocks
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryBW, Offcore

```python
CLKS = CPU_CLK_UNHALTED.THREAD
ORO_DRD_BW_Cycles = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('OFFCORE_REQUESTS_OUTSTANDING.ALL_DATA_RD:c4', level)), level)
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
- sample: MEM_INST_RETIRED.ALL_STORES:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Store_Bound = EXE_ACTIVITY.BOUND_ON_STORES / CLKS
```

- EXE_ACTIVITY.BOUND_ON_STORES
- CPU_CLK_UNHALTED.THREAD

#### 3.1.5.1 <a id="store_latency">Store_Latency</a>

This metric estimates fraction of cycles the CPU spent handling L1D store misses. Store accesses usually less impact out-of-order core performance; however; holding resources for longer time can lead into undesired implications (e.g. contention on L1D fill-buffer entries - see FB_Full). Consider to avoid/reduce unnecessary (or easily load-able/computable) memory store.

- Domain: Clocks_Estimated
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryLat, Offcore

```python
Mem_Lock_St_Fraction = MEM_INST_RETIRED.LOCK_LOADS / MEM_INST_RETIRED.ALL_STORES
Store_L2_Hit_Cycles = L2_RQSTS.RFO_HIT * Mem_L2_Store_Cost * (1 - Mem_Lock_St_Fraction)
CLKS = CPU_CLK_UNHALTED.THREAD
ORO_Demand_RFO_C1 = EV(lambda EV, level: min(EV('CPU_CLK_UNHALTED.THREAD', level), EV('OFFCORE_REQUESTS_OUTSTANDING.CYCLES_WITH_DEMAND_RFO', level)), level)
Store_Latency = (Store_L2_Hit_Cycles + (1 - Mem_Lock_St_Fraction) * ORO_Demand_RFO_C1) / CLKS
```

- level
- EV
- MEM_INST_RETIRED.ALL_STORES
- MEM_INST_RETIRED.LOCK_LOADS
- CPU_CLK_UNHALTED.THREAD
- L2_RQSTS.RFO_HIT
- Mem_L2_Store_Cost

#### 3.1.5.2 <a id="false_sharing">False_Sharing</a>

This metric roughly estimates how often CPU was handling synchronizations due to False Sharing. False Sharing is a multithreading hiccup; where multiple Logical Processors contend on different data-elements mapped into the same cache line. . False Sharing can be easily avoided by padding to make Logical Processors access different lines.

- Domain: Clocks_Estimated
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: DataSharing, Offcore, Snoop
- sample: MEM_LOAD_L3_HIT_RETIRED.XSNP_HITM:pp, OFFCORE_RESPONSE.DEMAND_RFO.L3_HIT.SNOOP_HITM

```python
Time = interval-s
CLKS = CPU_CLK_UNHALTED.THREAD
Turbo_Utilization = CLKS / CPU_CLK_UNHALTED.REF_TSC
Average_Frequency = Turbo_Utilization * msr/tsc/ / OneBillion / Time
Mem_XSNP_HitM_Cost = 22 * Average_Frequency
OCR_all_rfo_l3_hit_snoop_hitm = OFFCORE_RESPONSE.DEMAND_RFO.L3_HIT.SNOOP_HITM
False_Sharing = Mem_XSNP_HitM_Cost * OCR_all_rfo_l3_hit_snoop_hitm / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- OFFCORE_RESPONSE.DEMAND_RFO.L3_HIT.SNOOP_HITM
- CPU_CLK_UNHALTED.REF_TSC
- msr/tsc/
- OneBillion
- interval-s

#### 3.1.5.3 <a id="split_stores">Split_Stores</a>

This metric represents rate of split store accesses. Consider aligning your data to the 64-byte cache line granularity.

- Domain: Core_Utilization
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Mem
- sample: MEM_INST_RETIRED.SPLIT_STORES:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Split_Stores = MEM_INST_RETIRED.SPLIT_STORES / CORE_CLKS
```

- MEM_INST_RETIRED.SPLIT_STORES
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
- sample: MEM_INST_RETIRED.STLB_MISS_STORES:pp

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
DTLB_Store = (Mem_STLB_Hit_Cost * DTLB_STORE_MISSES.STLB_HIT:c1 + DTLB_STORE_MISSES.WALK_ACTIVE) / CORE_CLKS
```

- DTLB_STORE_MISSES.STLB_HIT:c1
- Mem_STLB_Hit_Cost
- DTLB_STORE_MISSES.WALK_ACTIVE
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

##### 3.1.5.4.1 <a id="store_stlb_hit">Store_STLB_Hit</a>

This metric roughly estimates the fraction of cycles where the TLB was missed by store accesses, hitting in the second- level TLB (STLB)

- Domain: Clocks_Estimated
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryTLB

```python
Store_STLB_Hit = DTLB_Store - Store_STLB_Miss
```

- [Store_STLB_Miss](#store_stlb_miss)
- [DTLB_Store](#dtlb_store)

##### 3.1.5.4.2 <a id="store_stlb_miss">Store_STLB_Miss</a>

This metric estimates the fraction of cycles where the STLB was missed by store accesses, performing a hardware page walk

- Domain: Clocks_Calculated
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Mem
- Metric group: MemoryTLB

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Store_STLB_Miss = DTLB_STORE_MISSES.WALK_ACTIVE / CORE_CLKS
```

- DTLB_STORE_MISSES.WALK_ACTIVE
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

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
- sample: ARITH.DIVIDER_ACTIVE

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Divider = ARITH.DIVIDER_ACTIVE / CLKS
```

- ARITH.DIVIDER_ACTIVE
- CPU_CLK_UNHALTED.THREAD

### 3.2.2 <a id="ports_utilization">Ports_Utilization</a>

This metric estimates fraction of cycles the CPU performance was potentially limited due to Core computation issues (non divider-related). Two distinct categories can be attributed into this metric: (1) heavy data-dependency among contiguous instructions would manifest in this metric - such cases are often referred to as low Instruction Level Parallelism (ILP). (2) Contention on some hardware execution unit other than Divider. For example; when there are too many multiply operations.. Loop Vectorization -most compilers feature auto-Vectorization options today- reduces pressure on the execution ports as multiple elements are calculated with same uop.

- Domain: Clocks
- Threshold:  > 0.15 and parent over threshold
- Area: BE/Core
- Metric group: PortsUtil

```python
Few_Uops_Executed_Threshold = EXE_ACTIVITY.1_PORTS_UTIL + Retiring * EXE_ACTIVITY.2_PORTS_UTIL
Core_Bound_Cycles = EXE_ACTIVITY.EXE_BOUND_0_PORTS + Few_Uops_Executed_Threshold
CLKS = CPU_CLK_UNHALTED.THREAD
Ports_Utilization = Core_Bound_Cycles / CLKS if ARITH.DIVIDER_ACTIVE < CYCLE_ACTIVITY.STALLS_TOTAL - CYCLE_ACTIVITY.STALLS_MEM_ANY else Few_Uops_Executed_Threshold / CLKS
```

- CYCLE_ACTIVITY.STALLS_TOTAL
- [Retiring](#retiring)
- EXE_ACTIVITY.1_PORTS_UTIL
- EXE_ACTIVITY.2_PORTS_UTIL
- ARITH.DIVIDER_ACTIVE
- CYCLE_ACTIVITY.STALLS_MEM_ANY
- CPU_CLK_UNHALTED.THREAD
- EXE_ACTIVITY.EXE_BOUND_0_PORTS

#### 3.2.2.1 <a id="ports_utilized_0">Ports_Utilized_0</a>

This metric represents fraction of cycles CPU executed no uops on any execution port (Logical Processor cycles since ICL, Physical Core cycles otherwise). Long-latency instructions like divides may contribute to this metric.. Check assembly view and Appendix C in Optimization Manual to find out instructions with say 5 or more cycles latency.. http://www.intel.com/content/www/us/en/architecture-and- technology/64-ia-32-architectures-optimization-manual.html

- Domain: Clocks
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Core
- Metric group: PortsUtil

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Cycles_0_Ports_Utilized = UOPS_EXECUTED.CORE_CYCLES_NONE / 2 if smt_enabled else CYCLE_ACTIVITY.STALLS_TOTAL - CYCLE_ACTIVITY.STALLS_MEM_ANY
Ports_Utilized_0 = Cycles_0_Ports_Utilized / CORE_CLKS
```

- smt_enabled
- CYCLE_ACTIVITY.STALLS_TOTAL
- UOPS_EXECUTED.CORE_CYCLES_NONE
- CYCLE_ACTIVITY.STALLS_MEM_ANY
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- CPU_CLK_UNHALTED.THREAD_ANY

##### 3.2.2.1.1 <a id="serializing_operation">Serializing_Operation</a>

This metric represents fraction of cycles the CPU issue- pipeline was stalled due to serializing operations. Instructions like CPUID; WRMSR or LFENCE serialize the out- of-order execution which may limit performance.

- Domain: Clocks
- Threshold:  > 0.1 and parent over threshold
- Area: BE/Core
- Metric group: PortsUtil
- sample: PARTIAL_RAT_STALLS.SCOREBOARD

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Serializing_Operation = PARTIAL_RAT_STALLS.SCOREBOARD / CLKS
```

- PARTIAL_RAT_STALLS.SCOREBOARD
- CPU_CLK_UNHALTED.THREAD

###### 3.2.2.1.1.1 <a id="slow_pause">Slow_Pause</a>

This metric represents fraction of cycles the CPU was stalled due to PAUSE Instructions.

- Domain: Clocks
- Threshold:  > 0.05 and parent over threshold
- Area: BE/Core
- sample: ROB_MISC_EVENTS.PAUSE_INST

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Slow_Pause = 140 * ROB_MISC_EVENTS.PAUSE_INST / CLKS
```

- CPU_CLK_UNHALTED.THREAD
- ROB_MISC_EVENTS.PAUSE_INST

##### 3.2.2.1.2 <a id="mixing_vectors">Mixing_Vectors</a>

The Mixing_Vectors metric gives the percentage of injected blend uops out of all uops issued. Usually a Mixing_Vectors over 5% is worth investigating. Read more in Appendix B1 of the Optimizations Guide for this topic.

- Domain: Clocks
- Threshold:  > 0.05
- Area: BE/Core

```python
CLKS = CPU_CLK_UNHALTED.THREAD
Mixing_Vectors = CLKS * UOPS_ISSUED.VECTOR_WIDTH_MISMATCH / UOPS_ISSUED.ANY
```

- CPU_CLK_UNHALTED.THREAD
- UOPS_ISSUED.VECTOR_WIDTH_MISMATCH
- UOPS_ISSUED.ANY

#### 3.2.2.2 <a id="ports_utilized_1">Ports_Utilized_1</a>

This metric represents fraction of cycles where the CPU executed total of 1 uop per cycle on all execution ports (Logical Processor cycles since ICL, Physical Core cycles otherwise). This can be due to heavy data-dependency among software instructions; or over oversubscribing a particular hardware resource. In some other cases with high 1_Port_Utilized and L1_Bound; this metric can point to L1 data-cache latency bottleneck that may not necessarily manifest with complete execution starvation (due to the short L1 latency e.g. walking a linked list) - looking at the assembly can be helpful.

- Domain: Clocks
- Threshold:  > 0.2 and parent over threshold
- Area: BE/Core
- Metric group: PortsUtil

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Cycles_1_Port_Utilized = (UOPS_EXECUTED.CORE_CYCLES_GE_1 - UOPS_EXECUTED.CORE_CYCLES_GE_2) / 2 if smt_enabled else EXE_ACTIVITY.1_PORTS_UTIL
Ports_Utilized_1 = Cycles_1_Port_Utilized / CORE_CLKS
```

- smt_enabled
- UOPS_EXECUTED.CORE_CYCLES_GE_1
- EXE_ACTIVITY.1_PORTS_UTIL
- UOPS_EXECUTED.CORE_CYCLES_GE_2
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
Cycles_2_Ports_Utilized = (UOPS_EXECUTED.CORE_CYCLES_GE_2 - UOPS_EXECUTED.CORE_CYCLES_GE_3) / 2 if smt_enabled else EXE_ACTIVITY.2_PORTS_UTIL
Ports_Utilized_2 = Cycles_2_Ports_Utilized / CORE_CLKS
```

- smt_enabled
- UOPS_EXECUTED.CORE_CYCLES_GE_2
- UOPS_EXECUTED.CORE_CYCLES_GE_3
- EXE_ACTIVITY.2_PORTS_UTIL
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
Cycles_3m_Ports_Utilized = UOPS_EXECUTED.CORE_CYCLES_GE_3 / 2 if smt_enabled else UOPS_EXECUTED.CORE_CYCLES_GE_3
Ports_Utilized_3m = Cycles_3m_Ports_Utilized / CORE_CLKS
```

- smt_enabled
- UOPS_EXECUTED.CORE_CYCLES_GE_3
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

This metric represents Core fraction of cycles CPU dispatched uops on execution port 0 ([SNB+] ALU; [HSW+] ALU and 2nd branch)

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

This metric represents Core fraction of cycles CPU dispatched uops on execution port 5 ([SNB+] Branches and ALU; [HSW+] ALU). See section 'Handling Port 5 Pressure' in Optimization Manual:. http://www.intel.com/content/www/us/en /architecture-and-technology/64-ia-32-architectures- optimization-manual.html

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
X87_Use = Retiring * UOPS_EXECUTED.X87 / UOPS_EXECUTED.THREAD
```

- [Retiring](#retiring)
- UOPS_EXECUTED.X87
- UOPS_EXECUTED.THREAD

#### 4.1.1.2 <a id="fp_scalar">FP_Scalar</a>

This metric approximates arithmetic floating-point (FP) scalar uops fraction the CPU has retired. May overcount due to FMA double counting.. Investigate what limits (compiler) generation of vector code.

- Domain: Uops
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- Metric group: Compute, Flops

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
FP_Arith_Scalar = FP_ARITH_INST_RETIRED.SCALAR_SINGLE:u0x03
FP_Scalar = FP_Arith_Scalar / Retired_Slots
```

- FP_ARITH_INST_RETIRED.SCALAR_SINGLE:u0x03
- UOPS_RETIRED.RETIRE_SLOTS

#### 4.1.1.3 <a id="fp_vector">FP_Vector</a>

This metric approximates arithmetic floating-point (FP) vector uops fraction the CPU has retired aggregated across all vector widths. May overcount due to FMA double counting.. Check if vector width is expected

- Domain: Uops
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- Metric group: Compute, Flops

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
FP_Arith_Vector = FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE:u0x3c
FP_Vector = FP_Arith_Vector / Retired_Slots
```

- FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE:u0x3c
- UOPS_RETIRED.RETIRE_SLOTS

##### 4.1.1.3.1 <a id="fp_vector_128b">FP_Vector_128b</a>

This metric approximates arithmetic FP vector uops fraction the CPU has retired for 128-bit wide vectors. May overcount due to FMA double counting.. Try to exploit wider vector length

- Domain: Uops
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- Metric group: Compute, Flops

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
FP_Vector_128b = (FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE + FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE) / Retired_Slots
```

- FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE
- FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE
- UOPS_RETIRED.RETIRE_SLOTS

##### 4.1.1.3.2 <a id="fp_vector_256b">FP_Vector_256b</a>

This metric approximates arithmetic FP vector uops fraction the CPU has retired for 256-bit wide vectors. May overcount due to FMA double counting.. Try to exploit wider vector length

- Domain: Uops
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- Metric group: Compute, Flops

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
FP_Vector_256b = (FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE + FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE) / Retired_Slots
```

- FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE
- FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE
- UOPS_RETIRED.RETIRE_SLOTS

### 4.1.2 <a id="memory_operations">Memory_Operations</a>

This metric represents fraction of slots where the CPU was retiring memory operations -- uops for memory load or store accesses.

- Domain: Slots
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- Metric group: Pipeline

```python
Memory_Operations = Light_Operations * MEM_INST_RETIRED.ANY / INST_RETIRED.ANY
```

- MEM_INST_RETIRED.ANY
- INST_RETIRED.ANY
- [Light_Operations](#light_operations)

### 4.1.3 <a id="fused_instructions">Fused_Instructions</a>

This metric represents fraction of slots where the CPU was retiring fused instructions -- where one uop can represent multiple contiguous instructions. The instruction pairs of CMP+JCC or DEC+JCC are commonly used examples.. See section 'Optimizing for Macro-fusion' in Optimization Manual:

- Domain: Slots
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- Metric group: Pipeline

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
Fused_Instructions = Light_Operations * UOPS_RETIRED.MACRO_FUSED / Retired_Slots
```

- UOPS_RETIRED.MACRO_FUSED
- [Light_Operations](#light_operations)
- UOPS_RETIRED.RETIRE_SLOTS

### 4.1.4 <a id="non_fused_branches">Non_Fused_Branches</a>

This metric represents fraction of slots where the CPU was retiring branch instructions that were not fused. Non- conditional branches like direct JMP or CALL would count here. Can be used to examine fusible conditional jumps that were not fused.

- Domain: Slots
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- Metric group: Pipeline

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
Non_Fused_Branches = Light_Operations * (BR_INST_RETIRED.ALL_BRANCHES - UOPS_RETIRED.MACRO_FUSED) / Retired_Slots
```

- UOPS_RETIRED.MACRO_FUSED
- BR_INST_RETIRED.ALL_BRANCHES
- [Light_Operations](#light_operations)
- UOPS_RETIRED.RETIRE_SLOTS

### 4.1.5 <a id="nop_instructions">Nop_Instructions</a>

This metric represents fraction of slots where the CPU was retiring NOP (no op) instructions. Compilers often use NOPs for certain address alignments - e.g. start address of a function or loop body.. Improve Codegen by correctly placing NOPs outside hot sections (e.g. outside loop body).

- Domain: Slots
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- Metric group: Pipeline
- sample: INST_RETIRED.NOP

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
Nop_Instructions = Light_Operations * INST_RETIRED.NOP / Retired_Slots
```

- INST_RETIRED.NOP
- [Light_Operations](#light_operations)
- UOPS_RETIRED.RETIRE_SLOTS

### 4.1.6 <a id="other_light_ops">Other_Light_Ops</a>

This metric represents the remaining light uops fraction the CPU has executed - remaining means not covered by other sibling nodes. May undercount due to FMA double counting

- Domain: Slots
- Threshold:  > 0.3 and parent over threshold
- Area: RET
- Metric group: Pipeline

```python
Light_Ops_Sum = FP_Arith + Memory_Operations + Fused_Instructions + Non_Fused_Branches + Nop_Instructions
Other_Light_Ops = max(0, Light_Operations - Light_Ops_Sum)
```

- [Light_Operations](#light_operations)
- [Memory_Operations](#memory_operations)
- [Non_Fused_Branches](#non_fused_branches)
- [FP_Arith](#fp_arith)
- [Nop_Instructions](#nop_instructions)
- [Fused_Instructions](#fused_instructions)

## 4.2 <a id="heavy_operations">Heavy_Operations</a>

This metric represents fraction of slots where the CPU was retiring heavy-weight operations -- instructions that require two or more uops or micro-coded sequences. This highly-correlates with the uop length of these instructions/sequences.

- Domain: Slots
- Threshold:  > 0.1
- Area: RET
- Metric group: Retire, TmaL2

```python
Retired_Slots = UOPS_RETIRED.RETIRE_SLOTS
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Heavy_Operations = (Retired_Slots + UOPS_RETIRED.MACRO_FUSED - INST_RETIRED.ANY) / SLOTS
```

- UOPS_RETIRED.MACRO_FUSED
- Pipeline_Width
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- UOPS_RETIRED.RETIRE_SLOTS
- INST_RETIRED.ANY

### 4.2.1 <a id="few_uops_instructions">Few_Uops_Instructions</a>

This metric represents fraction of slots where the CPU was retiring instructions that that are decoder into two or up to ([SNB+] four; [ADL+] five) uops. This highly-correlates with the number of uops in such instructions.

- Domain: Slots
- Threshold:  > 0.05 and parent over threshold
- Area: RET

```python
Few_Uops_Instructions = Heavy_Operations - Microcode_Sequencer
```

- [Microcode_Sequencer](#microcode_sequencer)
- [Heavy_Operations](#heavy_operations)

### 4.2.2 <a id="microcode_sequencer">Microcode_Sequencer</a>

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

#### 4.2.2.1 <a id="assists">Assists</a>

This metric estimates fraction of slots the CPU retired uops delivered by the Microcode_Sequencer as a result of Assists. Assists are long sequences of uops that are required in certain corner-cases for operations that cannot be handled natively by the execution pipeline. For example; when working with very small floating point values (so-called Denormals); the FP units are not set up to perform these operations natively. Instead; a sequence of instructions to perform the computation on the Denormals is injected into the pipeline. Since these microcode sequences might be dozens of uops long; Assists can be extremely deleterious to performance and they can be avoided in many cases.

- Domain: Slots_Estimated
- Threshold:  > 0.1 and parent over threshold
- Area: RET
- sample: OTHER_ASSISTS.ANY

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Assists = Avg_Assist_Cost * (FP_ASSIST.ANY + OTHER_ASSISTS.ANY) / SLOTS
```

- FP_ASSIST.ANY
- OTHER_ASSISTS.ANY
- Pipeline_Width
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- Avg_Assist_Cost

#### 4.2.2.2 <a id="cisc">CISC</a>

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

## 5.1 <a id="metric_iparith_avx128">Metric_IpArith_AVX128</a>

Instructions per FP Arithmetic AVX/SSE 128-bit instruction (lower number means higher occurrence rate). May undercount due to FMA double counting.

- Domain: Inst_Metric
- Threshold:  < 10
- Area: Info.Inst_Mix
- Metric group: Flops, FpVector, InsType

```python
IpArith_AVX128 = INST_RETIRED.ANY / (FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE + FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE)
Metric_IpArith_AVX128 = IpArith_AVX128
```

- FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE
- INST_RETIRED.ANY
- FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE

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

## 5.3 <a id="metric_ipcall">Metric_IpCall</a>

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

## 5.4 <a id="metric_l3_cache_fill_bw">Metric_L3_Cache_Fill_BW</a>

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

## 5.5 <a id="metric_mem_read_latency">Metric_MEM_Read_Latency</a>

Average latency of data read request to external memory (in nanoseconds). Accounts for demand loads and L1/L2 prefetches. ([RKL+]memory-controller only)

- Domain: NanoSeconds
- Max value: 1000
- Threshold: True
- Area: Info.System
- Metric group: Mem, MemoryLat, SoC

```python
Time = interval-s
Socket_CLKS = UNC_CLOCK.SOCKET
MEM_Read_Latency = OneBillion * (UNC_ARB_TRK_OCCUPANCY.DATA_READ / UNC_ARB_TRK_REQUESTS.DATA_READ) / (Socket_CLKS / Time)
Metric_MEM_Read_Latency = MEM_Read_Latency
```

- UNC_ARB_TRK_REQUESTS.DATA_READ
- UNC_ARB_TRK_OCCUPANCY.DATA_READ
- OneBillion
- UNC_CLOCK.SOCKET
- interval-s

## 5.6 <a id="metric_ipstore">Metric_IpStore</a>

Instructions per Store (lower number means higher occurrence rate)

- Domain: Inst_Metric
- Threshold:  < 8
- Area: Info.Inst_Mix
- Metric group: InsType

```python
IpStore = INST_RETIRED.ANY / MEM_INST_RETIRED.ALL_STORES
Metric_IpStore = IpStore
```

- MEM_INST_RETIRED.ALL_STORES
- INST_RETIRED.ANY

## 5.7 <a id="metric_load_stlb_mpki">Metric_Load_STLB_MPKI</a>

STLB (2nd level TLB) data load speculative misses per kilo instruction (misses of any page-size that complete the page walk)

- Domain: Metric
- Threshold: True
- Area: Info.Memory.TLB
- Metric group: Mem, MemoryTLB

```python
Load_STLB_MPKI = 1000 * DTLB_LOAD_MISSES.WALK_COMPLETED / INST_RETIRED.ANY
Metric_Load_STLB_MPKI = Load_STLB_MPKI
```

- INST_RETIRED.ANY
- DTLB_LOAD_MISSES.WALK_COMPLETED

## 5.8 <a id="metric_data_l2_mlp">Metric_Data_L2_MLP</a>

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

## 5.9 <a id="metric_l2hpki_load">Metric_L2HPKI_Load</a>

L2 cache hits per kilo instruction for all demand loads (including speculative)

- Domain: Metric
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, CacheMisses

```python
L2HPKI_Load = 1000 * L2_RQSTS.DEMAND_DATA_RD_HIT / INST_RETIRED.ANY
Metric_L2HPKI_Load = L2HPKI_Load
```

- INST_RETIRED.ANY
- L2_RQSTS.DEMAND_DATA_RD_HIT

## 5.10 <a id="metric_ilp">Metric_ILP</a>

Instruction-Level-Parallelism (average number of uops executed when there is execution) per-core

- Domain: Core_Metric
- Max value: Exe_Ports
- Threshold: True
- Area: Info.Core
- Metric group: Backend, Cor, Pipeline, PortsUtil

```python
Execute_Cycles = UOPS_EXECUTED.CORE_CYCLES_GE_1 / 2 if smt_enabled else UOPS_EXECUTED.CORE_CYCLES_GE_1
ILP = UOPS_EXECUTED.THREAD / Execute_Cycles
Metric_ILP = ILP
```

- smt_enabled
- UOPS_EXECUTED.CORE_CYCLES_GE_1
- UOPS_EXECUTED.THREAD

## 5.11 <a id="metric_fetch_upc">Metric_Fetch_UpC</a>

Average number of Uops issued by front-end when it issued something

- Domain: Metric
- Max value: 6.0
- Threshold: True
- Area: Info.Frontend
- Metric group: Fed, FetchBW

```python
Fetch_UpC = UOPS_ISSUED.ANY / UOPS_ISSUED.ANY:c1
Metric_Fetch_UpC = Fetch_UpC
```

- UOPS_ISSUED.ANY:c1
- UOPS_ISSUED.ANY

## 5.12 <a id="metric_fb_hpki">Metric_FB_HPKI</a>

Fill Buffer (FB) hits per kilo instructions for retired demand loads (L1D misses that merge into ongoing miss- handling entries)

- Domain: Metric
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, CacheMisses

```python
FB_HPKI = 1000 * MEM_LOAD_RETIRED.FB_HIT / INST_RETIRED.ANY
Metric_FB_HPKI = FB_HPKI
```

- INST_RETIRED.ANY
- MEM_LOAD_RETIRED.FB_HIT

## 5.13 <a id="metric_gflops">Metric_GFLOPs</a>

Giga Floating Point Operations Per Second. Aggregate across all supported options of: FP precisions, scalar and vector instructions, vector-width and AMX engine.

- Domain: Metric
- Max value: 200
- Threshold: True
- Area: Info.System
- Metric group: Cor, Flops, HPC

```python
Time = interval-s
FLOP_Count = 1 * (FP_ARITH_INST_RETIRED.SCALAR_SINGLE + FP_ARITH_INST_RETIRED.SCALAR_DOUBLE) + 2 * FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE + 4 * (FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE + FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE) + 8 * FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE
GFLOPs = FLOP_Count / OneBillion / Time
Metric_GFLOPs = GFLOPs
```

- FP_ARITH_INST_RETIRED.SCALAR_DOUBLE
- FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE
- FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE
- FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE
- FP_ARITH_INST_RETIRED.SCALAR_SINGLE
- FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE
- OneBillion
- interval-s

## 5.14 <a id="metric_iparith_scalar_sp">Metric_IpArith_Scalar_SP</a>

Instructions per FP Arithmetic Scalar Single-Precision instruction (lower number means higher occurrence rate). May undercount due to FMA double counting.

- Domain: Inst_Metric
- Threshold:  < 10
- Area: Info.Inst_Mix
- Metric group: Flops, FpScalar, InsType

```python
IpArith_Scalar_SP = INST_RETIRED.ANY / FP_ARITH_INST_RETIRED.SCALAR_SINGLE
Metric_IpArith_Scalar_SP = IpArith_Scalar_SP
```

- FP_ARITH_INST_RETIRED.SCALAR_SINGLE
- INST_RETIRED.ANY

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

## 5.17 <a id="metric_ipbranch">Metric_IpBranch</a>

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

## 5.18 <a id="metric_coreipc">Metric_CoreIPC</a>

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

## 5.19 <a id="metric_average_frequency">Metric_Average_Frequency</a>

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

## 5.20 <a id="metric_bptkbranch">Metric_BpTkBranch</a>

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

## 5.21 <a id="metric_execute_per_issue">Metric_Execute_per_Issue</a>

The ratio of Executed- by Issued-Uops. Ratio > 1 suggests high rate of uop micro-fusions. Ratio < 1 suggest high rate of "execute" at rename stage.

- Domain: Metric
- Threshold: True
- Area: Info.Thread
- Metric group: Cor, Pipeline

```python
Execute_per_Issue = UOPS_EXECUTED.THREAD / UOPS_ISSUED.ANY
Metric_Execute_per_Issue = Execute_per_Issue
```

- UOPS_ISSUED.ANY
- UOPS_EXECUTED.THREAD

## 5.22 <a id="metric_ipmispredict">Metric_IpMispredict</a>

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

## 5.23 <a id="metric_iparith_avx256">Metric_IpArith_AVX256</a>

Instructions per FP Arithmetic AVX* 256-bit instruction (lower number means higher occurrence rate). May undercount due to FMA double counting.

- Domain: Inst_Metric
- Threshold:  < 10
- Area: Info.Inst_Mix
- Metric group: Flops, FpVector, InsType

```python
IpArith_AVX256 = INST_RETIRED.ANY / (FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE + FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE)
Metric_IpArith_AVX256 = IpArith_AVX256
```

- FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE
- INST_RETIRED.ANY
- FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE

## 5.24 <a id="metric_uptb">Metric_UpTB</a>

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

## 5.25 <a id="metric_mispredictions">Metric_Mispredictions</a>

Total pipeline cost of Branch Misprediction related bottlenecks

- Domain: Scaled_Slots
- Threshold:  > 20
- Area: Info.Bottleneck
- Metric group: Bad, BadSpec, BrMispredicts

```python
Mispredictions = 100 * (Branch_Mispredicts + Fetch_Latency * Mispredicts_Resteers / (LCP + ICache_Misses + DSB_Switches + Branch_Resteers + MS_Switches + ITLB_Misses))
Metric_Mispredictions = Mispredictions
```

- [Mispredicts_Resteers](#mispredicts_resteers)
- [DSB_Switches](#dsb_switches)
- [LCP](#lcp)
- [Branch_Mispredicts](#branch_mispredicts)
- [ITLB_Misses](#itlb_misses)
- [ICache_Misses](#icache_misses)
- [Fetch_Latency](#fetch_latency)
- [MS_Switches](#ms_switches)
- [Branch_Resteers](#branch_resteers)

## 5.26 <a id="metric_cond_nt">Metric_Cond_NT</a>

Fraction of branches that are non-taken conditionals

- Domain: Fraction
- Max value: 1.0
- Threshold: True
- Area: Info.Branches
- Metric group: Bad, Branches, CodeGen, PGO

```python
Cond_NT = BR_INST_RETIRED.NOT_TAKEN / BR_INST_RETIRED.ALL_BRANCHES
Metric_Cond_NT = Cond_NT
```

- BR_INST_RETIRED.NOT_TAKEN
- BR_INST_RETIRED.ALL_BRANCHES

## 5.27 <a id="metric_memory_bandwidth">Metric_Memory_Bandwidth</a>

Total pipeline cost of (external) Memory Bandwidth related bottlenecks

- Domain: Scaled_Slots
- Threshold:  > 20
- Area: Info.Bottleneck
- Metric group: Mem, MemoryBW, Offcore

```python
Memory_Bandwidth = 100 * Memory_Bound * (DRAM_Bound / (L1_Bound + L3_Bound + DRAM_Bound + Store_Bound + L2_Bound) * (MEM_Bandwidth / (MEM_Latency + MEM_Bandwidth)) + L3_Bound / (L1_Bound + L3_Bound + DRAM_Bound + Store_Bound + L2_Bound) * (SQ_Full / (L3_Hit_Latency + Contested_Accesses + SQ_Full + Data_Sharing))) + L1_Bound / (L1_Bound + L3_Bound + DRAM_Bound + Store_Bound + L2_Bound) * (FB_Full / (Store_Fwd_Blk + DTLB_Load + G4K_Aliasing + Lock_Latency + Split_Loads + FB_Full))
Metric_Memory_Bandwidth = Memory_Bandwidth
```

- [Split_Loads](#split_loads)
- [Store_Fwd_Blk](#store_fwd_blk)
- [Memory_Bound](#memory_bound)
- [G4K_Aliasing](#g4k_aliasing)
- [Store_Bound](#store_bound)
- [MEM_Latency](#mem_latency)
- [Contested_Accesses](#contested_accesses)
- [MEM_Bandwidth](#mem_bandwidth)
- [L3_Hit_Latency](#l3_hit_latency)
- [L3_Bound](#l3_bound)
- [L1_Bound](#l1_bound)
- [SQ_Full](#sq_full)
- [DTLB_Load](#dtlb_load)
- [DRAM_Bound](#dram_bound)
- [L2_Bound](#l2_bound)
- [Lock_Latency](#lock_latency)
- [Data_Sharing](#data_sharing)
- [FB_Full](#fb_full)

## 5.28 <a id="metric_uoppi">Metric_UopPI</a>

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

## 5.29 <a id="metric_l2hpki_all">Metric_L2HPKI_All</a>

L2 cache hits per kilo instruction for all request types (including speculative)

- Domain: Metric
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, CacheMisses

```python
L2HPKI_All = 1000 * (L2_RQSTS.REFERENCES - L2_RQSTS.MISS) / INST_RETIRED.ANY
Metric_L2HPKI_All = L2HPKI_All
```

- L2_RQSTS.MISS
- INST_RETIRED.ANY
- L2_RQSTS.REFERENCES

## 5.30 <a id="metric_l2mpki">Metric_L2MPKI</a>

L2 cache true misses per kilo instruction for retired demand loads

- Domain: Metric
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, Backend, CacheMisses

```python
L2MPKI = 1000 * MEM_LOAD_RETIRED.L2_MISS / INST_RETIRED.ANY
Metric_L2MPKI = L2MPKI
```

- MEM_LOAD_RETIRED.L2_MISS
- INST_RETIRED.ANY

## 5.31 <a id="metric_ipunknown_branch">Metric_IpUnknown_Branch</a>

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

## 5.32 <a id="metric_store_stlb_mpki">Metric_Store_STLB_MPKI</a>

STLB (2nd level TLB) data store speculative misses per kilo instruction (misses of any page-size that complete the page walk)

- Domain: Metric
- Threshold: True
- Area: Info.Memory.TLB
- Metric group: Mem, MemoryTLB

```python
Store_STLB_MPKI = 1000 * DTLB_STORE_MISSES.WALK_COMPLETED / INST_RETIRED.ANY
Metric_Store_STLB_MPKI = Store_STLB_MPKI
```

- INST_RETIRED.ANY
- DTLB_STORE_MISSES.WALK_COMPLETED

## 5.33 <a id="metric_kernel_utilization">Metric_Kernel_Utilization</a>

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

## 5.34 <a id="metric_ipfarbranch">Metric_IpFarBranch</a>

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

## 5.35 <a id="metric_flopc">Metric_FLOPc</a>

Floating Point Operations Per Cycle

- Domain: Core_Metric
- Max value: 10.0
- Threshold: True
- Area: Info.Core
- Metric group: Ret, Flops

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
FLOP_Count = 1 * (FP_ARITH_INST_RETIRED.SCALAR_SINGLE + FP_ARITH_INST_RETIRED.SCALAR_DOUBLE) + 2 * FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE + 4 * (FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE + FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE) + 8 * FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE
FLOPc = FLOP_Count / CORE_CLKS
Metric_FLOPc = FLOPc
```

- FP_ARITH_INST_RETIRED.SCALAR_DOUBLE
- FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE
- FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE
- FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE
- FP_ARITH_INST_RETIRED.SCALAR_SINGLE
- FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

## 5.36 <a id="metric_instructions">Metric_Instructions</a>

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

## 5.37 <a id="metric_kernel_cpi">Metric_Kernel_CPI</a>

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

## 5.38 <a id="metric_iparith_scalar_dp">Metric_IpArith_Scalar_DP</a>

Instructions per FP Arithmetic Scalar Double-Precision instruction (lower number means higher occurrence rate). May undercount due to FMA double counting.

- Domain: Inst_Metric
- Threshold:  < 10
- Area: Info.Inst_Mix
- Metric group: Flops, FpScalar, InsType

```python
IpArith_Scalar_DP = INST_RETIRED.ANY / FP_ARITH_INST_RETIRED.SCALAR_DOUBLE
Metric_IpArith_Scalar_DP = IpArith_Scalar_DP
```

- INST_RETIRED.ANY
- FP_ARITH_INST_RETIRED.SCALAR_DOUBLE

## 5.39 <a id="metric_mem_request_latency">Metric_MEM_Request_Latency</a>

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

## 5.40 <a id="metric_dsb_switch_cost">Metric_DSB_Switch_Cost</a>

Average number of cycles of a switch from the DSB fetch-unit to MITE fetch unit - see DSB_Switches tree node for details.

- Domain: Metric
- Threshold: True
- Area: Info.Frontend
- Metric group: DSBmiss

```python
DSB_Switch_Cost = DSB2MITE_SWITCHES.PENALTY_CYCLES / DSB2MITE_SWITCHES.COUNT
Metric_DSB_Switch_Cost = DSB_Switch_Cost
```

- DSB2MITE_SWITCHES.PENALTY_CYCLES
- DSB2MITE_SWITCHES.COUNT

## 5.41 <a id="metric_callret">Metric_CallRet</a>

Fraction of branches that are CALL or RET

- Domain: Fraction
- Max value: 1.0
- Threshold: True
- Area: Info.Branches
- Metric group: Bad, Branches

```python
CallRet = (BR_INST_RETIRED.NEAR_CALL + BR_INST_RETIRED.NEAR_RETURN) / BR_INST_RETIRED.ALL_BRANCHES
Metric_CallRet = CallRet
```

- BR_INST_RETIRED.NEAR_CALL
- BR_INST_RETIRED.ALL_BRANCHES
- BR_INST_RETIRED.NEAR_RETURN

## 5.42 <a id="metric_clks">Metric_CLKS</a>

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

## 5.43 <a id="metric_dsb_coverage">Metric_DSB_Coverage</a>

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

## 5.44 <a id="metric_dsb_misses">Metric_DSB_Misses</a>

Total pipeline cost of DSB (uop cache) misses - subset of the Instruction_Fetch_BW Bottleneck.

- Domain: Scaled_Slots
- Threshold:  > 10
- Area: Info.Botlnk.L2
- Metric group: DSBmiss, Fed

```python
DSB_Misses = 100 * (Fetch_Latency * DSB_Switches / (LCP + ICache_Misses + DSB_Switches + Branch_Resteers + MS_Switches + ITLB_Misses) + Fetch_Bandwidth * MITE / (LSD + MITE + DSB))
Metric_DSB_Misses = DSB_Misses
```

- [DSB_Switches](#dsb_switches)
- [LSD](#lsd)
- [LCP](#lcp)
- [Fetch_Bandwidth](#fetch_bandwidth)
- [ITLB_Misses](#itlb_misses)
- [ICache_Misses](#icache_misses)
- [Fetch_Latency](#fetch_latency)
- [MITE](#mite)
- [MS_Switches](#ms_switches)
- [DSB](#dsb)
- [Branch_Resteers](#branch_resteers)

## 5.45 <a id="metric_time">Metric_Time</a>

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

## 5.47 <a id="metric_iparith">Metric_IpArith</a>

Instructions per FP Arithmetic instruction (lower number means higher occurrence rate). May undercount due to FMA double counting. Approximated prior to BDW.

- Domain: Inst_Metric
- Threshold:  < 10
- Area: Info.Inst_Mix
- Metric group: Flops, InsType

```python
FP_Arith_Vector = FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE:u0x3c
FP_Arith_Scalar = FP_ARITH_INST_RETIRED.SCALAR_SINGLE:u0x03
IpArith = INST_RETIRED.ANY / (FP_Arith_Scalar + FP_Arith_Vector)
Metric_IpArith = IpArith
```

- FP_ARITH_INST_RETIRED.SCALAR_SINGLE:u0x03
- INST_RETIRED.ANY
- FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE:u0x3c

## 5.48 <a id="metric_retire">Metric_Retire</a>

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

## 5.49 <a id="metric_l3mpki">Metric_L3MPKI</a>

L3 cache true misses per kilo instruction for retired demand loads

- Domain: Metric
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, CacheMisses

```python
L3MPKI = 1000 * MEM_LOAD_RETIRED.L3_MISS / INST_RETIRED.ANY
Metric_L3MPKI = L3MPKI
```

- MEM_LOAD_RETIRED.L3_MISS
- INST_RETIRED.ANY

## 5.50 <a id="metric_cpi">Metric_CPI</a>

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

## 5.51 <a id="metric_l2mpki_load">Metric_L2MPKI_Load</a>

L2 cache ([RKL+] true) misses per kilo instruction for all demand loads (including speculative)

- Domain: Metric
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, CacheMisses

```python
L2MPKI_Load = 1000 * L2_RQSTS.DEMAND_DATA_RD_MISS / INST_RETIRED.ANY
Metric_L2MPKI_Load = L2MPKI_Load
```

- L2_RQSTS.DEMAND_DATA_RD_MISS
- INST_RETIRED.ANY

## 5.52 <a id="metric_ipload">Metric_IpLoad</a>

Instructions per Load (lower number means higher occurrence rate)

- Domain: Inst_Metric
- Threshold:  < 3
- Area: Info.Inst_Mix
- Metric group: InsType

```python
IpLoad = INST_RETIRED.ANY / MEM_INST_RETIRED.ALL_LOADS
Metric_IpLoad = IpLoad
```

- INST_RETIRED.ANY
- MEM_INST_RETIRED.ALL_LOADS

## 5.53 <a id="metric_l2_cache_fill_bw_1t">Metric_L2_Cache_Fill_BW_1T</a>

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

## 5.54 <a id="metric_l1d_cache_fill_bw_1t">Metric_L1D_Cache_Fill_BW_1T</a>

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

## 5.55 <a id="metric_ic_misses">Metric_IC_Misses</a>

Total pipeline cost of Instruction Cache misses - subset of the Big_Code Bottleneck.

- Domain: Scaled_Slots
- Threshold:  > 5
- Area: Info.Botlnk.L2
- Metric group: Fed, FetchLat, IcMiss

```python
IC_Misses = 100 * (Fetch_Latency * ICache_Misses / (LCP + ICache_Misses + DSB_Switches + Branch_Resteers + MS_Switches + ITLB_Misses))
Metric_IC_Misses = IC_Misses
```

- [DSB_Switches](#dsb_switches)
- [LCP](#lcp)
- [ITLB_Misses](#itlb_misses)
- [ICache_Misses](#icache_misses)
- [Fetch_Latency](#fetch_latency)
- [MS_Switches](#ms_switches)
- [Branch_Resteers](#branch_resteers)

## 5.56 <a id="metric_code_stlb_mpki">Metric_Code_STLB_MPKI</a>

STLB (2nd level TLB) code speculative misses per kilo instruction (misses of any page-size that complete the page walk)

- Domain: Metric
- Threshold: True
- Area: Info.Memory.TLB
- Metric group: Fed, MemoryTLB

```python
Code_STLB_MPKI = 1000 * ITLB_MISSES.WALK_COMPLETED / INST_RETIRED.ANY
Metric_Code_STLB_MPKI = Code_STLB_MPKI
```

- ITLB_MISSES.WALK_COMPLETED
- INST_RETIRED.ANY

## 5.57 <a id="metric_ipswpf">Metric_IpSWPF</a>

Instructions per Software prefetch instruction (of any type: NTA/T0/T1/T2/Prefetch) (lower number means higher occurrence rate)

- Domain: Inst_Metric
- Max value: 1000
- Threshold:  < 100
- Area: Info.Inst_Mix
- Metric group: Prefetches

```python
IpSWPF = INST_RETIRED.ANY / SW_PREFETCH_ACCESS.T0:u0xF
Metric_IpSWPF = IpSWPF
```

- SW_PREFETCH_ACCESS.T0:u0xF
- INST_RETIRED.ANY

## 5.58 <a id="metric_memory_data_tlbs">Metric_Memory_Data_TLBs</a>

Total pipeline cost of Memory Address Translation related bottlenecks (data-side TLBs)

- Domain: Scaled_Slots
- Threshold:  > 20
- Area: Info.Bottleneck
- Metric group: Mem, MemoryTLB, Offcore

```python
Memory_Data_TLBs = 100 * Memory_Bound * (L1_Bound / max(Memory_Bound, L1_Bound + L3_Bound + DRAM_Bound + Store_Bound + L2_Bound) * (DTLB_Load / max(L1_Bound, Store_Fwd_Blk + DTLB_Load + G4K_Aliasing + Lock_Latency + Split_Loads + FB_Full)) + Store_Bound / (L1_Bound + L3_Bound + DRAM_Bound + Store_Bound + L2_Bound) * (DTLB_Store / (Split_Stores + DTLB_Store + Store_Latency + False_Sharing)))
Metric_Memory_Data_TLBs = Memory_Data_TLBs
```

- [Split_Loads](#split_loads)
- [Store_Fwd_Blk](#store_fwd_blk)
- [Memory_Bound](#memory_bound)
- [G4K_Aliasing](#g4k_aliasing)
- [Store_Bound](#store_bound)
- [False_Sharing](#false_sharing)
- [L1_Bound](#l1_bound)
- [L3_Bound](#l3_bound)
- [DTLB_Load](#dtlb_load)
- [DRAM_Bound](#dram_bound)
- [L2_Bound](#l2_bound)
- [Lock_Latency](#lock_latency)
- [FB_Full](#fb_full)
- [DTLB_Store](#dtlb_store)
- [Store_Latency](#store_latency)
- [Split_Stores](#split_stores)

## 5.59 <a id="metric_turbo_utilization">Metric_Turbo_Utilization</a>

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

## 5.60 <a id="metric_jump">Metric_Jump</a>

Fraction of branches that are unconditional (direct or indirect) jumps

- Domain: Fraction
- Max value: 1.0
- Threshold: True
- Area: Info.Branches
- Metric group: Bad, Branches

```python
Br_DoI_Jumps = BR_INST_RETIRED.NEAR_TAKEN - (BR_INST_RETIRED.CONDITIONAL - BR_INST_RETIRED.NOT_TAKEN) - 2 * BR_INST_RETIRED.NEAR_CALL
Jump = Br_DoI_Jumps / BR_INST_RETIRED.ALL_BRANCHES
Metric_Jump = Jump
```

- BR_INST_RETIRED.NEAR_CALL
- BR_INST_RETIRED.CONDITIONAL
- BR_INST_RETIRED.NOT_TAKEN
- BR_INST_RETIRED.NEAR_TAKEN
- BR_INST_RETIRED.ALL_BRANCHES

## 5.61 <a id="metric_page_walks_utilization">Metric_Page_Walks_Utilization</a>

Utilization of the core's Page Walker(s) serving STLB misses triggered by instruction/Load/Store accesses

- Domain: Core_Metric
- Max value: 1.0
- Threshold:  > 0.5
- Area: Info.Memory.TLB
- Metric group: Mem, MemoryTLB

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
Page_Walks_Utilization = (ITLB_MISSES.WALK_PENDING + DTLB_LOAD_MISSES.WALK_PENDING + DTLB_STORE_MISSES.WALK_PENDING + EPT.WALK_PENDING) / (2 * CORE_CLKS)
Metric_Page_Walks_Utilization = Page_Walks_Utilization
```

- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- DTLB_LOAD_MISSES.WALK_PENDING
- DTLB_STORE_MISSES.WALK_PENDING
- ITLB_MISSES.WALK_PENDING
- EPT.WALK_PENDING

## 5.62 <a id="metric_l1mpki">Metric_L1MPKI</a>

L1 cache true misses per kilo instruction for retired demand loads

- Domain: Metric
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, CacheMisses

```python
L1MPKI = 1000 * MEM_LOAD_RETIRED.L1_MISS / INST_RETIRED.ANY
Metric_L1MPKI = L1MPKI
```

- MEM_LOAD_RETIRED.L1_MISS
- INST_RETIRED.ANY

## 5.63 <a id="metric_cond_tk">Metric_Cond_TK</a>

Fraction of branches that are taken conditionals

- Domain: Fraction
- Max value: 1.0
- Threshold: True
- Area: Info.Branches
- Metric group: Bad, Branches, CodeGen, PGO

```python
Cond_TK = (BR_INST_RETIRED.CONDITIONAL - BR_INST_RETIRED.NOT_TAKEN) / BR_INST_RETIRED.ALL_BRANCHES
Metric_Cond_TK = Cond_TK
```

- BR_INST_RETIRED.CONDITIONAL
- BR_INST_RETIRED.ALL_BRANCHES
- BR_INST_RETIRED.NOT_TAKEN

## 5.64 <a id="metric_branching_overhead">Metric_Branching_Overhead</a>

Total pipeline cost of branch related instructions (used for program control-flow including function calls)

- Domain: Scaled_Slots
- Threshold:  > 10
- Area: Info.Bottleneck
- Metric group: Ret

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Br_DoI_Jumps = BR_INST_RETIRED.NEAR_TAKEN - (BR_INST_RETIRED.CONDITIONAL - BR_INST_RETIRED.NOT_TAKEN) - 2 * BR_INST_RETIRED.NEAR_CALL
Branching_Retired = (BR_INST_RETIRED.CONDITIONAL + 3 * BR_INST_RETIRED.NEAR_CALL + Br_DoI_Jumps) / SLOTS
Branching_Overhead = 100 * Branching_Retired
Metric_Branching_Overhead = Branching_Overhead
```

- BR_INST_RETIRED.NEAR_CALL
- BR_INST_RETIRED.CONDITIONAL
- BR_INST_RETIRED.NOT_TAKEN
- BR_INST_RETIRED.NEAR_TAKEN
- Pipeline_Width
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

## 5.65 <a id="metric_cpu_utilization">Metric_CPU_Utilization</a>

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

## 5.66 <a id="metric_mem_parallel_reads">Metric_MEM_Parallel_Reads</a>

Average number of parallel data read requests to external memory. Accounts for demand loads and L1/L2 prefetches

- Domain: SystemMetric
- Max value: 100
- Threshold: True
- Area: Info.System
- Metric group: Mem, MemoryBW, SoC

```python
MEM_Parallel_Reads = UNC_ARB_TRK_OCCUPANCY.DATA_READ / UNC_ARB_TRK_OCCUPANCY.DATA_READ:c1
Metric_MEM_Parallel_Reads = MEM_Parallel_Reads
```

- UNC_ARB_TRK_OCCUPANCY.DATA_READ:c1
- UNC_ARB_TRK_OCCUPANCY.DATA_READ

## 5.67 <a id="metric_mlp">Metric_MLP</a>

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

## 5.68 <a id="metric_l2mpki_code_all">Metric_L2MPKI_Code_All</a>

L2 cache speculative code cacheline misses per kilo instruction

- Domain: Metric
- Threshold: True
- Area: Info.Frontend
- Metric group: IcMiss

```python
L2MPKI_Code_All = 1000 * L2_RQSTS.CODE_RD_MISS / INST_RETIRED.ANY
Metric_L2MPKI_Code_All = L2MPKI_Code_All
```

- INST_RETIRED.ANY
- L2_RQSTS.CODE_RD_MISS

## 5.69 <a id="metric_ipflop">Metric_IpFLOP</a>

Instructions per Floating Point (FP) Operation (lower number means higher occurrence rate). Reference: Tuning Performance via Metrics with Expectations. https://doi.org/10.1109/LCA.2019.2916408

- Domain: Inst_Metric
- Threshold:  < 10
- Area: Info.Inst_Mix
- Metric group: Flops, InsType

```python
FLOP_Count = 1 * (FP_ARITH_INST_RETIRED.SCALAR_SINGLE + FP_ARITH_INST_RETIRED.SCALAR_DOUBLE) + 2 * FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE + 4 * (FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE + FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE) + 8 * FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE
IpFLOP = INST_RETIRED.ANY / FLOP_Count
Metric_IpFLOP = IpFLOP
```

- INST_RETIRED.ANY
- FP_ARITH_INST_RETIRED.SCALAR_DOUBLE
- FP_ARITH_INST_RETIRED.128B_PACKED_SINGLE
- FP_ARITH_INST_RETIRED.256B_PACKED_SINGLE
- FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE
- FP_ARITH_INST_RETIRED.SCALAR_SINGLE
- FP_ARITH_INST_RETIRED.256B_PACKED_DOUBLE

## 5.70 <a id="metric_l1mpki_load">Metric_L1MPKI_Load</a>

L1 cache true misses per kilo instruction for all demand loads (including speculative)

- Domain: Metric
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, CacheMisses

```python
L1MPKI_Load = 1000 * L2_RQSTS.ALL_DEMAND_DATA_RD / INST_RETIRED.ANY
Metric_L1MPKI_Load = L1MPKI_Load
```

- INST_RETIRED.ANY
- L2_RQSTS.ALL_DEMAND_DATA_RD

## 5.71 <a id="metric_core_bound_likely">Metric_Core_Bound_Likely</a>

Probability of Core Bound bottleneck hidden by SMT-profiling artifacts. Tip: consider analysis with SMT disabled

- Domain: Metric
- Max value: 1.0
- Threshold:  > 0.5
- Area: Info.Botlnk.L0
- Metric group: Cor, SMT

```python
SMT_2T_Utilization = 1 - CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / (CPU_CLK_UNHALTED.REF_XCLK_ANY / 2) if smt_enabled else 0
Core_Bound_Likely = 100 * (1 - Core_Bound / Ports_Utilization if Core_Bound < Ports_Utilization else 1) if SMT_2T_Utilization > 0.5 else 0
Metric_Core_Bound_Likely = Core_Bound_Likely
```

- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- smt_enabled
- CPU_CLK_UNHALTED.REF_XCLK_ANY
- [Core_Bound](#core_bound)
- [Ports_Utilization](#ports_utilization)

## 5.72 <a id="metric_iptb">Metric_IpTB</a>

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

## 5.73 <a id="metric_execute">Metric_Execute</a>

- Domain: Metric
- Max value: Exe_Ports
- Threshold: True
- Area: Info.Pipeline
- Metric group: Cor, Pipeline, PortsUtil, SMT

```python
Execute = UOPS_EXECUTED.THREAD / UOPS_EXECUTED.THREAD:c1
Metric_Execute = Execute
```

- UOPS_EXECUTED.THREAD:c1
- UOPS_EXECUTED.THREAD

## 5.74 <a id="metric_slots">Metric_SLOTS</a>

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

## 5.75 <a id="metric_big_code">Metric_Big_Code</a>

Total pipeline cost of instruction fetch related bottlenecks by large code footprint programs (i-side cache; TLB and BTB misses)

- Domain: Scaled_Slots
- Threshold:  > 20
- Area: Info.Bottleneck
- Metric group: BigFoot, Fed, Frontend, IcMiss, MemoryTLB

```python
Big_Code = 100 * Fetch_Latency * (ITLB_Misses + ICache_Misses + Unknown_Branches) / (LCP + ICache_Misses + DSB_Switches + Branch_Resteers + MS_Switches + ITLB_Misses)
Metric_Big_Code = Big_Code
```

- [DSB_Switches](#dsb_switches)
- [LCP](#lcp)
- [Unknown_Branches](#unknown_branches)
- [ICache_Misses](#icache_misses)
- [ITLB_Misses](#itlb_misses)
- [Fetch_Latency](#fetch_latency)
- [MS_Switches](#ms_switches)
- [Branch_Resteers](#branch_resteers)

## 5.76 <a id="metric_l3_cache_access_bw_1t">Metric_L3_Cache_Access_BW_1T</a>

- Domain: Metric
- Threshold: True
- Area: Info.Memory.Thread
- Metric group: Mem, MemoryBW, Offcore

```python
Time = interval-s
L3_Cache_Access_BW = 64 * OFFCORE_REQUESTS.ALL_REQUESTS / OneBillion / Time
L3_Cache_Access_BW_1T = L3_Cache_Access_BW
Metric_L3_Cache_Access_BW_1T = L3_Cache_Access_BW_1T
```

- OFFCORE_REQUESTS.ALL_REQUESTS
- OneBillion
- interval-s

## 5.77 <a id="metric_smt_2t_utilization">Metric_SMT_2T_Utilization</a>

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

## 5.78 <a id="metric_load_l2_miss_latency">Metric_Load_L2_Miss_Latency</a>

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

## 5.79 <a id="metric_fp_arith_utilization">Metric_FP_Arith_Utilization</a>

Actual per-core usage of the Floating Point non-X87 execution units (regardless of precision or vector-width). Values > 1 are possible due to ([BDW+] Fused-Multiply Add (FMA) counting - common; [ADL+] use all of ADD/MUL/FMA in Scalar or 128/256-bit vectors - less common).

- Domain: Core_Metric
- Max value: 2.0
- Threshold: True
- Area: Info.Core
- Metric group: Cor, Flops, HPC

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
FP_Arith_Vector = FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE:u0x3c
FP_Arith_Scalar = FP_ARITH_INST_RETIRED.SCALAR_SINGLE:u0x03
FP_Arith_Utilization = (FP_Arith_Scalar + FP_Arith_Vector) / (2 * CORE_CLKS)
Metric_FP_Arith_Utilization = FP_Arith_Utilization
```

- FP_ARITH_INST_RETIRED.SCALAR_SINGLE:u0x03
- FP_ARITH_INST_RETIRED.128B_PACKED_DOUBLE:u0x3c
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY

## 5.80 <a id="metric_core_clks">Metric_CORE_CLKS</a>

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

## 5.81 <a id="metric_icache_miss_latency">Metric_ICache_Miss_Latency</a>

Average Latency for L1 instruction cache misses

- Domain: Metric
- Threshold: True
- Area: Info.Frontend
- Metric group: Fed, FetchLat, IcMiss

```python
ICache_Miss_Latency = ICACHE_16B.IFDATA_STALL / ICACHE_16B.IFDATA_STALL:c1:e1 + 2
Metric_ICache_Miss_Latency = ICache_Miss_Latency
```

- ICACHE_16B.IFDATA_STALL
- ICACHE_16B.IFDATA_STALL:c1:e1

## 5.82 <a id="metric_l2mpki_code">Metric_L2MPKI_Code</a>

L2 cache true code cacheline misses per kilo instruction

- Domain: Metric
- Threshold: True
- Area: Info.Frontend
- Metric group: IcMiss

```python
L2MPKI_Code = 1000 * FRONTEND_RETIRED.L2_MISS / INST_RETIRED.ANY
Metric_L2MPKI_Code = L2MPKI_Code
```

- INST_RETIRED.ANY
- FRONTEND_RETIRED.L2_MISS

## 5.83 <a id="metric_ipdsb_miss_ret">Metric_IpDSB_Miss_Ret</a>

Instructions per non-speculative DSB miss (lower number means higher occurrence rate)

- Domain: Inst_Metric
- Threshold:  < 50
- Area: Info.Frontend
- Metric group: DSBmiss, Fed

```python
IpDSB_Miss_Ret = INST_RETIRED.ANY / FRONTEND_RETIRED.ANY_DSB_MISS
Metric_IpDSB_Miss_Ret = IpDSB_Miss_Ret
```

- INST_RETIRED.ANY
- FRONTEND_RETIRED.ANY_DSB_MISS

## 5.84 <a id="metric_l3_cache_access_bw">Metric_L3_Cache_Access_BW</a>

Average per-core data access bandwidth to the L3 cache [GB / sec]

- Domain: Core_Metric
- Threshold: True
- Area: Info.Memory.Core
- Metric group: Mem, MemoryBW, Offcore

```python
Time = interval-s
L3_Cache_Access_BW = 64 * OFFCORE_REQUESTS.ALL_REQUESTS / OneBillion / Time
Metric_L3_Cache_Access_BW = L3_Cache_Access_BW
```

- OFFCORE_REQUESTS.ALL_REQUESTS
- OneBillion
- interval-s

## 5.85 <a id="metric_l2_cache_fill_bw">Metric_L2_Cache_Fill_BW</a>

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

## 5.86 <a id="metric_branch_misprediction_cost">Metric_Branch_Misprediction_Cost</a>

Branch Misprediction Cost: Fraction of TMA slots wasted per non-speculative branch misprediction (retired JEClear)

- Domain: Core_Metric
- Max value: 300
- Threshold: True
- Area: Info.Bad_Spec
- Metric group: Bad, BrMispredicts

```python
CLKS = CPU_CLK_UNHALTED.THREAD
CORE_CLKS = CPU_CLK_UNHALTED.THREAD / 2 * (1 + CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE / CPU_CLK_UNHALTED.REF_XCLK) if ebs_mode else CPU_CLK_UNHALTED.THREAD_ANY / 2 if smt_enabled else CLKS
SLOTS = Pipeline_Width * CORE_CLKS
Branch_Misprediction_Cost = (Branch_Mispredicts + Fetch_Latency * Mispredicts_Resteers / (LCP + ICache_Misses + DSB_Switches + Branch_Resteers + MS_Switches + ITLB_Misses)) * SLOTS / BR_MISP_RETIRED.ALL_BRANCHES
Metric_Branch_Misprediction_Cost = Branch_Misprediction_Cost
```

- [Mispredicts_Resteers](#mispredicts_resteers)
- [DSB_Switches](#dsb_switches)
- [LCP](#lcp)
- [Branch_Mispredicts](#branch_mispredicts)
- [ITLB_Misses](#itlb_misses)
- [ICache_Misses](#icache_misses)
- [Fetch_Latency](#fetch_latency)
- [MS_Switches](#ms_switches)
- BR_MISP_RETIRED.ALL_BRANCHES
- Pipeline_Width
- ebs_mode
- CPU_CLK_UNHALTED.THREAD
- CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE
- CPU_CLK_UNHALTED.REF_XCLK
- smt_enabled
- CPU_CLK_UNHALTED.THREAD_ANY
- [Branch_Resteers](#branch_resteers)

## 5.87 <a id="metric_mem_parallel_requests">Metric_MEM_Parallel_Requests</a>

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

## 5.88 <a id="metric_l2mpki_all">Metric_L2MPKI_All</a>

L2 cache ([RKL+] true) misses per kilo instruction for all request types (including speculative)

- Domain: Metric
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, CacheMisses, Offcore

```python
L2MPKI_All = 1000 * L2_RQSTS.MISS / INST_RETIRED.ANY
Metric_L2MPKI_All = L2MPKI_All
```

- L2_RQSTS.MISS
- INST_RETIRED.ANY

## 5.89 <a id="metric_load_miss_real_latency">Metric_Load_Miss_Real_Latency</a>

Actual Average Latency for L1 data-cache miss demand load operations (in core cycles)

- Domain: Clocks_Latency
- Max value: 1000
- Threshold: True
- Area: Info.Memory
- Metric group: Mem, MemoryBound, MemoryLat

```python
Load_Miss_Real_Latency = L1D_PEND_MISS.PENDING / (MEM_LOAD_RETIRED.L1_MISS + MEM_LOAD_RETIRED.FB_HIT)
Metric_Load_Miss_Real_Latency = Load_Miss_Real_Latency
```

- MEM_LOAD_RETIRED.L1_MISS
- L1D_PEND_MISS.PENDING
- MEM_LOAD_RETIRED.FB_HIT

## 5.90 <a id="metric_l3_cache_fill_bw_1t">Metric_L3_Cache_Fill_BW_1T</a>

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

## 5.91 <a id="metric_instruction_fetch_bw">Metric_Instruction_Fetch_BW</a>

Total pipeline cost of instruction fetch bandwidth related bottlenecks

- Domain: Scaled_Slots
- Threshold:  > 20
- Area: Info.Bottleneck
- Metric group: Fed, FetchBW, Frontend

```python
Big_Code = 100 * Fetch_Latency * (ITLB_Misses + ICache_Misses + Unknown_Branches) / (LCP + ICache_Misses + DSB_Switches + Branch_Resteers + MS_Switches + ITLB_Misses)
Instruction_Fetch_BW = 100 * (Frontend_Bound - Fetch_Latency * Mispredicts_Resteers / (LCP + ICache_Misses + DSB_Switches + Branch_Resteers + MS_Switches + ITLB_Misses)) - Big_Code
Metric_Instruction_Fetch_BW = Instruction_Fetch_BW
```

- [Mispredicts_Resteers](#mispredicts_resteers)
- [DSB_Switches](#dsb_switches)
- [Frontend_Bound](#frontend_bound)
- [LCP](#lcp)
- [ITLB_Misses](#itlb_misses)
- [ICache_Misses](#icache_misses)
- [Fetch_Latency](#fetch_latency)
- [Unknown_Branches](#unknown_branches)
- [MS_Switches](#ms_switches)
- [Branch_Resteers](#branch_resteers)

## 5.92 <a id="metric_load_l2_mlp">Metric_Load_L2_MLP</a>

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

## 5.93 <a id="metric_memory_latency">Metric_Memory_Latency</a>

Total pipeline cost of Memory Latency related bottlenecks (external memory and off-core caches)

- Domain: Scaled_Slots
- Threshold:  > 20
- Area: Info.Bottleneck
- Metric group: Mem, MemoryLat, Offcore

```python
Memory_Latency = 100 * Memory_Bound * (DRAM_Bound / (L1_Bound + L3_Bound + DRAM_Bound + Store_Bound + L2_Bound) * (MEM_Latency / (MEM_Latency + MEM_Bandwidth)) + L3_Bound / (L1_Bound + L3_Bound + DRAM_Bound + Store_Bound + L2_Bound) * (L3_Hit_Latency / (L3_Hit_Latency + Contested_Accesses + SQ_Full + Data_Sharing)) + L2_Bound / (L1_Bound + L3_Bound + DRAM_Bound + Store_Bound + L2_Bound))
Metric_Memory_Latency = Memory_Latency
```

- [Memory_Bound](#memory_bound)
- [Contested_Accesses](#contested_accesses)
- [Store_Bound](#store_bound)
- [MEM_Latency](#mem_latency)
- [L3_Hit_Latency](#l3_hit_latency)
- [MEM_Bandwidth](#mem_bandwidth)
- [L3_Bound](#l3_bound)
- [SQ_Full](#sq_full)
- [L1_Bound](#l1_bound)
- [DRAM_Bound](#dram_bound)
- [L2_Bound](#l2_bound)
- [Data_Sharing](#data_sharing)

## 5.94 <a id="metric_lsd_coverage">Metric_LSD_Coverage</a>

Fraction of Uops delivered by the LSD (Loop Stream Detector; aka Loop Cache)

- Domain: Metric
- Max value: 1.0
- Threshold: True
- Area: Info.Frontend
- Metric group: Fed, LSD

```python
Fetched_Uops = IDQ.DSB_UOPS + LSD.UOPS + IDQ.MITE_UOPS + IDQ.MS_UOPS
LSD_Coverage = LSD.UOPS / Fetched_Uops
Metric_LSD_Coverage = LSD_Coverage
```

- LSD.UOPS
- IDQ.MS_UOPS
- IDQ.MITE_UOPS
- IDQ.DSB_UOPS
