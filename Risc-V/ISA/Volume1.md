# 简介

$\triangle$ Our goals in RISC-V include:

- A completely *open* ISA that is freely available to academic and industry.
- A *real* ISA suitable for direct native hardware implementation, not just simulation or binary translation.
- An ISA that avoids "over-architecting" for a particular microarchitecture style, but which allows efficient implementation in any of these.
- An ISA seperated into a *small* base integer ISA, usable by itself as a base for customized accelerators or for eduacational purposes, and optional standard extensions, to support general purpose software development.
- Support for the revised 2008 IEEE-754 floating-point standard.
- An ISA supporting extensive ISA extensions and specialized variants.
- Both 32-bit and 64-bit address space variants for applications, operating system kernels, and hardware implementations.
- An ISA with support for highly-parallel multicore or manycore implementations, including heterogenous multiprocessors.
- Optional *variable-length* instructions to both expand availabe instruction encoding space and to support an optional *dense instruction encoding* for improved performance, static code size, and energy efficiency.
- A fully virtualizable ISA to easy hypervisor development.
- An ISA that simplifies experiements with new privileged architecture designs.

$\triangle$ The RISC-V ISA is defined avoiding implementation details as much as possibleand should be read as the software-visiable interface to a wide variety of implementations rather than as the design of a particular hardware artifact.

## 1.1 RISC-V硬件平台术语

$\triangle$ A component is termed as a *core* if it contains an independent instruction fetch unit.

$\triangle$ A RISC-V-compatible core might support multiple RISC-V-compatible hardware threads, or *harts*, through multithreading.

$\triangle$ We use the term *coprocessor* to refer to a unit that is attached to a RISC-V core and is mostly sequenced by a RISC-V instruction stream, but which contains additional architectural state and instruction-set extensions, and possibly some limited autonomy relative to the primary RISC-V instruction stream.  

$\triangle$ We use the term *accelerator* to refer to either a non-programmable fixed-function unit or a core that can operate autonomously but is specialized for certain tasks.

## 1.2 RISC-V软件执行环境和Hart

$\triangle$​​ A RISC-V execution environment interface (EEI) defines:

- the initial state of the program
- the number and type of harts in the environment including the privilege modes supported by the harts,
- the accessibility and attributes of memory and I/O regions,
- the behavior of all legal instructions executed on each hart, and
- the handling of any interrupts or exceptions raised during execution including environment calls.

$\triangle$ From the perspective of software running in a given execution environment, a hart is a resource that autonomously fetches and executes RISC-V instructions within that execution environment.   

## 1.3 RISC-V ISA简介

$\triangle$ RISCV-ISA is actually a family of related ISAs:

- RV32I and RV64I, two primary base integer variants (XLEN);
- RV32E subset variant of the RV32I base instruction set, to support small microcontrollers, and which has half the number of integer registers (XLEN=64).
- RV128I variant of the base integer instruction set supporting a flat 128-bit address space (XLEN=128).

$\triangle$ We use the term XLEN to refer to the width of an integer register in bits (either 32 or 64).  

$\triangle$ We divide each RISC-V instruction-set encoding space into three disjoint categories: *standard*, *reserved*, and *custom*.

- Standard encoding are defined by the Foundation.
- Reserved encoding are currently not defined but are saved for future standard extension.
  - *non-standard*: an extension that is not defined by Foundation.
- Custom encoding shall never be used for standard extensions and are made available for vendor-specific non-standard extension.
  - *non-conforming*: non-standard extension that uses either a standard or a reserved encoding.

$\triangle$ Extension:

- "I": base integer ISA
- "M": standard integer multiplication and division extension
- "A": standard atomic instruction extension.
- "F": standard single-precision floating-point extension.
- "D": standard double-precision floating-point extension.
- "C": instruction extension provides narrower 16-bit forms of common instructions.

## 1.4 访存

$\triangle$​​ RISC-V hart总共的内存空间为2^XLEN^字节，可以单比特寻址。

$\triangle$​​ 访存宽度定义：

- *halfword*：16比特（2字节），
- *word*：32比特（4字节），
- *doubleword*：64比特（8字节），
- *quadword*：128比特（16字节）。

$\triangle$​​​ 内存地址计算忽略溢出，而是模2^XLEN^。

$\triangle$​​​ 读写I/O设置会引起副作用，访问主存不会。

$\triangle$ 内存访问分为隐式访问（*implicit*）和显式方式（*explicit*）。

- 隐式访问：指令取值。
- 显式访问：load/store指令。

$\triangle$ 执行环境定义：

- 指令的其他隐式访问。
- 内存空间分配。

$\triangle$​ 指令访问不可访问的地址，触发异常。

- 隐式读不引起异常，而且没有副作用。

$\triangle$​ RISC-V的默认内存一致性模型为RISC-V Weak Memory Ordering (RVWMO)。提议替换为强模型Total Store Ordering。

- 需要软件配合使用fence或者cache控制指令保证内存访问的顺序。

## 1.5 基础指令长度编码

$\triangle$​ 基础RISC-V ISA的指令编码为固定长度的32比特。

$\triangle$ 标准编码机制支持不同长度指令的ISA扩展。

$\triangle$ IALIGN（以字节为单位），指令地址对齐约束。

$\triangle$ ILEN（以字节为单位），最大指令长度，总是IALIGN的倍数。

### 扩展指令长度编码

$\triangle$ RISC-V的标准编码是32比特，但是预留了其他编码的格式。编码为16比特对齐。

$\triangle$ 以低地址的低位表示指令长度：

- 16比特：[1:0]不等于11。
- 32比特：[1:0]=11，[4:2]不等于111。
- 48比特：[5:0]=011111。
- 64比特：[6:0]=0111111。
- 80比特：[14:12]不等与111，[6:0]=1111111。
- 176比特：[14:12]=111，[6:0]=11111111。

$\triangle$ 全0和全1都是非法编码。

$\triangle$ 支持大端或小端。

## 1.6 异常、陷阱和中断

$\triangle$ *异常*：运行时出现的非常规条件。*中断*：外部异步时间，使得hard执行非常规的条件。

- 与IEEE-754定义兼容。

$\triangle$ 陷阱的作用：

- 包含陷阱：软件可见的陷阱，由执行环境中的软件处理。
- 请求陷阱：同步异常，向执行环境请求行为。例如：系统调用。
- 不可见陷阱：陷阱处理对于软件是透明的，在trap处理后继续。
- Fatal陷阱：表示fatal失效，执行环境中止。

|              | 包含陷阱 | 请求陷阱 | 不可见陷阱 | Fatal陷阱 |
| ------------ | -------- | -------- | ---------- | --------- |
| 执行中止     | No       | No       | No         | Yes       |
| 软件不可见   | No       | No       | Yes        | Yes       |
| 执行环境处理 | No       | Yes      | Yes        | Yes       |

## 1.7 未指明的行为

$\triangle$ 未指明的行为：没有约束的行为或值。对于扩展集、平台标准和实现开放。



# 2 RV32I基础整形指令集

版本2.1

$\triangle$ RV32I包含40条指令。

- 其中ECALL/EBREAK可以用SYSTEM指令实现，FENCE可以用NOP实现。

## 2.1 基础整形ISA的编程环境

$\triangle$ 编程环境：

- 32个x寄存器，每个32比特。
  - x0固定为全0，x1-x31为通用寄存器。
  - XLEN=32。
- pc维护指令指针。

$\triangle$ 没有专门的栈针寄存器和返回寄存器，可以利用任意寄存器。

$\triangle$​​ **疑问**：Although 16 registers would arguably be sufficient for an integer ISA running compiled code, it is impossible to encode a complete ISA with 16 registers in 16-bit instructions using a 3-address format. Although a 2-address format would be possible, it would increase instruction count and lower efficiency.

## 2.2 基础指令格式

$\triangle$ 四种指令格式都是32比特长度，但是可以16比特对齐。

$\triangle$ 四种指令格式：R/I/S/U

- R格式：两源操作数格式rs2、rs1、rd，
- I格式：单源操作数+12比特立即数格式rs1、imm、rd，
- S格式：两源操作数+12比特立即数格式rs2、rs1、imm，
- U格式：20比特立即数格式imm、rd。

$\triangle$ 编码规则：

- 操作数位置相同。
- 除了CSR指令，立即数总是符号扩展。

## 2.3 立即数编码变种

$\triangle$ 除了上面四种指令格式，还有两种指令格式：B/J

- B格式：两源操作数+12比特立即数格式rs1、rs2、imm。立即数编码乱序。
- J格式：20比特立即数格式imm、rd。立即数编码乱序。

$\triangle$ 立即数用来保存地址偏移，所以不需要保留最低位。

## 2.4 整数计算指令

$\triangle$ 不提供专门的flag检查指令，而是在分支指令中完成。

### 整数寄存器-立即数指令

$\triangle$​ ADDI: adds the sign-extended 12-bit immediate to register *rs1*.

$\triangle$​​ SLTI: places the value 1 in register *rd* if register *rs1* is less than the sign-extended immediate when both are treated as signed numbers, else 0 is written to *rd*.

$\triangle$ SLTIU: is similar but compares the values are unsigned numbers.

$\triangle$​ ANDI/ORI/XORI: are logical operations that perform bitwise AND, OR, and XOR on register *rs1* and the sign-extended 12-bit immediate and place the result in *rd*.

$\triangle$ SLLI/SRLI/SRAI: Shifts by a constant. The operand to be shifted is in *rs1*, and the shift amount is encoded in the lower 5 bits of the I-immediate field.

$\triangle$ LUI: is used to build 32-bit constants. LUI places the 32-bit U-immediate value into the destination register *rd*, filling in the lowest 12 bits with zeros.

$\triangle$ AUIPC: is used to build pc-relative addresses. 

### 整数寄存器-寄存器操作

$\triangle$ ADD: performs the addition of *rs1* and *rs2*.

$\triangle$ SUB: performs the subtraction of *rs2* form *rs1*. 忽略溢出。

$\triangle$ SLT and SLTU: perform signed and unsigned compares respectively, write 1 to *rd* if *rs1 < rs2*, 0 otherwise.

$\triangle$ AND/OR/XOR: perform bitwise logical operations.

$\triangle$ SLL/SRL/SRA perform logical left, logical right, and arithmetic right shifts on the value in register *rs1* by the shift amount held in the lower 5 bits of register *rs2*.

### NOP指令

$\triangle$ NOP: does not change any architecturally visible state, except for advancing the pc and incrementing any applicable performance counters.

$\triangle$ 复用`ADDI x0, x0, 0`编码。

## 2.5 控制转移指令

### 无条件跳转

$\triangle$ JAL stores the address of the instruction following the jump (pc+4) into register *rd*.

- 偏移是有符号的，跳转范围是$\pm$1MiB范围。

$\triangle$​ JALR: target address is obtained by adding the sign-extended 12-bit I-immediate to the register *rs1*, then setting the least-significant bit of the result to zero.

## 2.6 Load和Store指令





