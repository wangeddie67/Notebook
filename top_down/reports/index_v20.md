# Decision Tree

| Metrics | adl_grt | ehl |
| ---- | :----: | :----: |
| 1 Frontend_Bound | [:heavy_check_mark:](adl_grt_ratios.md#frontend_bound) | [:heavy_check_mark:](ehl_ratios.md#frontend_bound) |
| 1.1 Frontend_Latency | [:heavy_check_mark:](adl_grt_ratios.md#frontend_latency) |  |
| 1.1.1 Icache | [:heavy_check_mark:](adl_grt_ratios.md#icache) |  |
| 1.1.2 ITLB | [:heavy_check_mark:](adl_grt_ratios.md#itlb) |  |
| 1.1.3 Branch_Detect | [:heavy_check_mark:](adl_grt_ratios.md#branch_detect) |  |
| 1.1.4 Branch_Resteer | [:heavy_check_mark:](adl_grt_ratios.md#branch_resteer) |  |
| 1.2 Frontend_Bandwidth | [:heavy_check_mark:](adl_grt_ratios.md#frontend_bandwidth) |  |
| 1.2.1 Cisc | [:heavy_check_mark:](adl_grt_ratios.md#cisc) |  |
| 1.2.2 Decode | [:heavy_check_mark:](adl_grt_ratios.md#decode) |  |
| 1.2.3 Predecode | [:heavy_check_mark:](adl_grt_ratios.md#predecode) |  |
| 1.2.4 Other_FB | [:heavy_check_mark:](adl_grt_ratios.md#other_fb) |  |
| 2 Bad_Speculation | [:heavy_check_mark:](adl_grt_ratios.md#bad_speculation) | [:heavy_check_mark:](ehl_ratios.md#bad_speculation) |
| 2.1 Branch_Mispredicts | [:heavy_check_mark:](adl_grt_ratios.md#branch_mispredicts) | [:heavy_check_mark:](ehl_ratios.md#branch_mispredicts) |
| 2.2 Machine_Clears | [:heavy_check_mark:](adl_grt_ratios.md#machine_clears) | [:heavy_check_mark:](ehl_ratios.md#machine_clears) |
| 2.2.1 Nuke | [:heavy_check_mark:](adl_grt_ratios.md#nuke) |  |
| 2.2.1.1 SMC | [:heavy_check_mark:](adl_grt_ratios.md#smc) |  |
| 2.2.1.2 Memory_Ordering | [:heavy_check_mark:](adl_grt_ratios.md#memory_ordering) |  |
| 2.2.1.3 FP_Assist | [:heavy_check_mark:](adl_grt_ratios.md#fp_assist) |  |
| 2.2.1.4 Disambiguation | [:heavy_check_mark:](adl_grt_ratios.md#disambiguation) |  |
| 2.2.1.5 Page_Fault | [:heavy_check_mark:](adl_grt_ratios.md#page_fault) |  |
| 2.2.2 Fast_Nuke | [:heavy_check_mark:](adl_grt_ratios.md#fast_nuke) | [:heavy_check_mark:](ehl_ratios.md#fast_nuke) |
| 3 Backend_Bound | [:heavy_check_mark:](adl_grt_ratios.md#backend_bound) | [:heavy_check_mark:](ehl_ratios.md#backend_bound) |
| 3.1 Core_Bound | [:heavy_check_mark:](adl_grt_ratios.md#core_bound) |  |
| 3.2 Load_Store_Bound | [:heavy_check_mark:](adl_grt_ratios.md#load_store_bound) | [:heavy_check_mark:](ehl_ratios.md#load_store_bound) |
| 3.2.1 Store_Bound | [:heavy_check_mark:](adl_grt_ratios.md#store_bound) |  |
| 3.2.2 L1_Bound | [:heavy_check_mark:](adl_grt_ratios.md#l1_bound) |  |
| 3.2.2.1 Store_Fwd | [:heavy_check_mark:](adl_grt_ratios.md#store_fwd) |  |
| 3.2.2.2 STLB_Hit | [:heavy_check_mark:](adl_grt_ratios.md#stlb_hit) |  |
| 3.2.2.3 STLB_Miss | [:heavy_check_mark:](adl_grt_ratios.md#stlb_miss) |  |
| 3.2.2.4 Other_L1 | [:heavy_check_mark:](adl_grt_ratios.md#other_l1) |  |
| 3.2.3 L2_Bound | [:heavy_check_mark:](adl_grt_ratios.md#l2_bound) | [:heavy_check_mark:](ehl_ratios.md#l2_bound) |
| 3.2.4 L3_Bound | [:heavy_check_mark:](adl_grt_ratios.md#l3_bound) | [:heavy_check_mark:](ehl_ratios.md#l3_bound) |
| 3.2.5 DRAM_Bound | [:heavy_check_mark:](adl_grt_ratios.md#dram_bound) | [:heavy_check_mark:](ehl_ratios.md#dram_bound) |
| 4 Retiring | [:heavy_check_mark:](adl_grt_ratios.md#retiring) | [:heavy_check_mark:](ehl_ratios.md#retiring) |
| 4.1 Base | [:heavy_check_mark:](adl_grt_ratios.md#base) | [:heavy_check_mark:](ehl_ratios.md#base) |
| 4.1.1 FP_uops | [:heavy_check_mark:](adl_grt_ratios.md#fp_uops) | [:heavy_check_mark:](ehl_ratios.md#fp_uops) |
| 4.1.2 Other_Ret | [:heavy_check_mark:](adl_grt_ratios.md#other_ret) | [:heavy_check_mark:](ehl_ratios.md#other_ret) |
| 4.2 MS_uops | [:heavy_check_mark:](adl_grt_ratios.md#ms_uops) | [:heavy_check_mark:](ehl_ratios.md#ms_uops) |
# General Metrics

| Metrics | adl_grt | ehl |
| ---- | :----: | :----: |
| 5.1 Metric_CPI | [:heavy_check_mark:](adl_grt_ratios.md#metric_cpi) | [:heavy_check_mark:](ehl_ratios.md#metric_cpi) |
| 5.2 Metric_Inst_Miss_Cost_L3Hit_Percent | [:heavy_check_mark:](adl_grt_ratios.md#metric_inst_miss_cost_l3hit_percent) |  |
| 5.3 ST_Buffer | [:heavy_check_mark:](adl_grt_ratios.md#st_buffer) |  |
| 5.4 Metric_IpCall | [:heavy_check_mark:](adl_grt_ratios.md#metric_ipcall) | [:heavy_check_mark:](ehl_ratios.md#metric_ipcall) |
| 5.5 Metric_IpLoad | [:heavy_check_mark:](adl_grt_ratios.md#metric_ipload) | [:heavy_check_mark:](ehl_ratios.md#metric_ipload) |
| 5.6 Metric_IDiv_Uop_Ratio | [:heavy_check_mark:](adl_grt_ratios.md#metric_idiv_uop_ratio) | [:heavy_check_mark:](ehl_ratios.md#metric_idiv_uop_ratio) |
| 5.7 Metric_Cycles_per_Demand_Load_DRAM_Hit | [:heavy_check_mark:](adl_grt_ratios.md#metric_cycles_per_demand_load_dram_hit) | [:heavy_check_mark:](ehl_ratios.md#metric_cycles_per_demand_load_dram_hit) |
| 5.8 Metric_Estimated_Pause_Cost | [:heavy_check_mark:](adl_grt_ratios.md#metric_estimated_pause_cost) |  |
| 5.9 Metric_SLOTS | [:heavy_check_mark:](adl_grt_ratios.md#metric_slots) | [:heavy_check_mark:](ehl_ratios.md#metric_slots) |
| 5.10 Metric_Microcode_Uop_Ratio | [:heavy_check_mark:](adl_grt_ratios.md#metric_microcode_uop_ratio) | [:heavy_check_mark:](ehl_ratios.md#metric_microcode_uop_ratio) |
| 5.11 Register | [:heavy_check_mark:](adl_grt_ratios.md#register) | [:heavy_check_mark:](ehl_ratios.md#register) |
| 5.12 Reorder_Buffer | [:heavy_check_mark:](adl_grt_ratios.md#reorder_buffer) | [:heavy_check_mark:](ehl_ratios.md#reorder_buffer) |
| 5.13 Metric_Load_Splits | [:heavy_check_mark:](adl_grt_ratios.md#metric_load_splits) | [:heavy_check_mark:](ehl_ratios.md#metric_load_splits) |
| 5.14 Metric_IpStore | [:heavy_check_mark:](adl_grt_ratios.md#metric_ipstore) | [:heavy_check_mark:](ehl_ratios.md#metric_ipstore) |
| 5.15 Metric_Turbo_Utilization | [:heavy_check_mark:](adl_grt_ratios.md#metric_turbo_utilization) | [:heavy_check_mark:](ehl_ratios.md#metric_turbo_utilization) |
| 5.16 Non_Mem_Scheduler | [:heavy_check_mark:](adl_grt_ratios.md#non_mem_scheduler) | [:heavy_check_mark:](ehl_ratios.md#non_mem_scheduler) |
| 5.17 Backend_Bound_Aux | [:heavy_check_mark:](adl_grt_ratios.md#backend_bound_aux) | [:heavy_check_mark:](ehl_ratios.md#backend_bound_aux) |
| 5.18 Metric_UPI | [:heavy_check_mark:](adl_grt_ratios.md#metric_upi) | [:heavy_check_mark:](ehl_ratios.md#metric_upi) |
| 5.19 Metric_MemLoadPKI | [:heavy_check_mark:](adl_grt_ratios.md#metric_memloadpki) | [:heavy_check_mark:](ehl_ratios.md#metric_memloadpki) |
| 5.20 Metric_FPDiv_Uop_Ratio | [:heavy_check_mark:](adl_grt_ratios.md#metric_fpdiv_uop_ratio) | [:heavy_check_mark:](ehl_ratios.md#metric_fpdiv_uop_ratio) |
| 5.21 LD_Buffer | [:heavy_check_mark:](adl_grt_ratios.md#ld_buffer) |  |
| 5.22 Metric_Cycles_per_Demand_Load_L3_Hit | [:heavy_check_mark:](adl_grt_ratios.md#metric_cycles_per_demand_load_l3_hit) | [:heavy_check_mark:](ehl_ratios.md#metric_cycles_per_demand_load_l3_hit) |
| 5.23 Metric_Store_Fwd_Blocks | [:heavy_check_mark:](adl_grt_ratios.md#metric_store_fwd_blocks) | [:heavy_check_mark:](ehl_ratios.md#metric_store_fwd_blocks) |
| 5.24 Metric_IpFarBranch | [:heavy_check_mark:](adl_grt_ratios.md#metric_ipfarbranch) | [:heavy_check_mark:](ehl_ratios.md#metric_ipfarbranch) |
| 5.25 Metric_Kernel_Utilization | [:heavy_check_mark:](adl_grt_ratios.md#metric_kernel_utilization) | [:heavy_check_mark:](ehl_ratios.md#metric_kernel_utilization) |
| 5.26 Metric_CPU_Utilization | [:heavy_check_mark:](adl_grt_ratios.md#metric_cpu_utilization) | [:heavy_check_mark:](ehl_ratios.md#metric_cpu_utilization) |
| 5.27 Metric_Branch_Mispredict_Ratio | [:heavy_check_mark:](adl_grt_ratios.md#metric_branch_mispredict_ratio) | [:heavy_check_mark:](ehl_ratios.md#metric_branch_mispredict_ratio) |
| 5.28 Metric_CLKS_P | [:heavy_check_mark:](adl_grt_ratios.md#metric_clks_p) | [:heavy_check_mark:](ehl_ratios.md#metric_clks_p) |
| 5.29 Metric_IPC | [:heavy_check_mark:](adl_grt_ratios.md#metric_ipc) | [:heavy_check_mark:](ehl_ratios.md#metric_ipc) |
| 5.30 RSV | [:heavy_check_mark:](adl_grt_ratios.md#rsv) |  |
| 5.31 Metric_Inst_Miss_Cost_L2Hit_Percent | [:heavy_check_mark:](adl_grt_ratios.md#metric_inst_miss_cost_l2hit_percent) |  |
| 5.32 Resource_Bound | [:heavy_check_mark:](adl_grt_ratios.md#resource_bound) | [:heavy_check_mark:](ehl_ratios.md#resource_bound) |
| 5.33 Metric_Cycles_per_Demand_Load_L2_Hit | [:heavy_check_mark:](adl_grt_ratios.md#metric_cycles_per_demand_load_l2_hit) | [:heavy_check_mark:](ehl_ratios.md#metric_cycles_per_demand_load_l2_hit) |
| 5.34 Metric_Branch_Mispredict_to_Unknown_Branch_Ratio | [:heavy_check_mark:](adl_grt_ratios.md#metric_branch_mispredict_to_unknown_branch_ratio) | [:heavy_check_mark:](ehl_ratios.md#metric_branch_mispredict_to_unknown_branch_ratio) |
| 5.35 Metric_IpBranch | [:heavy_check_mark:](adl_grt_ratios.md#metric_ipbranch) | [:heavy_check_mark:](ehl_ratios.md#metric_ipbranch) |
| 5.36 Serialization | [:heavy_check_mark:](adl_grt_ratios.md#serialization) | [:heavy_check_mark:](ehl_ratios.md#serialization) |
| 5.37 Metric_X87_Uop_Ratio | [:heavy_check_mark:](adl_grt_ratios.md#metric_x87_uop_ratio) |  |
| 5.38 Metric_CLKS | [:heavy_check_mark:](adl_grt_ratios.md#metric_clks) | [:heavy_check_mark:](ehl_ratios.md#metric_clks) |
| 5.39 Mem_Scheduler | [:heavy_check_mark:](adl_grt_ratios.md#mem_scheduler) | [:heavy_check_mark:](ehl_ratios.md#mem_scheduler) |
| 5.40 Metric_Inst_Miss_Cost_DRAMHit_Percent | [:heavy_check_mark:](adl_grt_ratios.md#metric_inst_miss_cost_dramhit_percent) |  |
| 5.41 Metric_IpMispredict | [:heavy_check_mark:](adl_grt_ratios.md#metric_ipmispredict) | [:heavy_check_mark:](ehl_ratios.md#metric_ipmispredict) |
| 5.42 Metric_Address_Alias_Blocks | [:heavy_check_mark:](adl_grt_ratios.md#metric_address_alias_blocks) | [:heavy_check_mark:](ehl_ratios.md#metric_address_alias_blocks) |
| 5.43 Alloc_Restriction | [:heavy_check_mark:](adl_grt_ratios.md#alloc_restriction) | [:heavy_check_mark:](ehl_ratios.md#alloc_restriction) |
| 5.44 Store_Buffer |  | [:heavy_check_mark:](ehl_ratios.md#store_buffer) |
| 5.45 Frontend_Bound | [:heavy_check_mark:](adl_grt_ratios.md#frontend_bound) | [:heavy_check_mark:](ehl_ratios.md#frontend_bound) |
