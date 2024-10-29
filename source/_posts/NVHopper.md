---
title: NVHopper
date: 2022-05-18 12:11:02
tags:
---

# `NVIDIA Hopper` 架构GPU浅析

[原文地址(2022.03.22)](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/)

## 0. 引言

2022年GTC大会，老黄介绍了基于`NVIDIA`最新`Hopper`架构的`NVIDIA H100 Tensor Core GPU`。本文将带你深入`Hopper`架构并介绍Hopper架构的一些重要新特性。

## 1. `NVIDIA H100 Tensor Core GPU`简介
`NVIDIA H100 Tensor Core GPU`是`NVIDIA`发行的第九代数据中心GPU，该GPU被设计用来在大规模人工智能应用以及高性能计算应用中提供相较于前代商品`NVIDIA A100 Tensor Core GPU`数量级级别的提升。`H100`继承了`A100`上为提升人工智能及高性能计算性能的设计特点，且显著提高了架构效率。图1展示了基于新`SXM5`板卡的`NVIDIA H100 Tensor Core GPU`。

![Fig1](http://subjectnoi.github.io/2022/05/18/NVHopper/Fig1.png)

对于如今主流的人工智能以及高性能计算任务，配备有`InfiniBand`互联技术的`H100`相比`A100`能提供最多30倍的性能提升（译者：可能类似`AMD Infinity Fabric`，致力于提升设备、节点间的带宽）。最新的`NVLink`互联系统主要着眼于如今最具挑战性的、需要大量GPU计算节点提供加速进行模型并行的任务。基于`InifniBand`的加持，这些任务在`H100`上的性能又一次得到了飞跃。图2展示了`A100`, `H100`, `H100+InfiniBand`在高性能计算、AI训练与推理任务中的性能。

![Fig2](http://subjectnoi.github.io/2022/05/18/NVHopper/Fig2.png)

在本次GTC上，NVIDIA发布了新的`NVIDIA Grace Hopper Superchip`产品。 `NVIDIA Hopper H100 Tensor Core GPU`将为`NVIDIA Grace Hopper Superchip CPU+GPU`架构提供动力，该架构专为TB级加速计算而打造，并能在大型人工智能模型以及高性能计算任务重提供超10倍的性能。
`NVIDIA Grace Hopper Superchip`利用`Arm`架构的灵活性从头开始设计用于加速计算de CPU和服务器架构。 `H100`与`NVIDIA Grace CPU`通过`NVIDIA`的芯片互联技术连接，提供`900 GB/s`的总带宽，比`PCIe Gen5`快7倍。 与当今最快的服务器相比，这种创新设计可提供高达30倍的总带宽，并为使用巨量数据的应用提供超10倍的性能提升。

下面是`NVIDIA H100 Tensor Core GPU`新特性的简要总结：
* 新设计的流多处理器(SM)提供了许多性能及效率上的提升，具体如下：
  * 第四代张量核心：若将每个SM的提升、SM数量的提升以及频率的提升结合考虑，`H100`相比`A100`能提供超6倍的性能提升。在每个SM层面，`H100`相比`A100`在每种数据类型上能提供2倍的矩阵乘加(`MMA`)性能，在`FP8`数据类型上，相比于`FP16`数据类型则能提供4倍于`A100`的性能。而张量核心的稀疏特性能够利用深度学习中的细粒度结构化稀疏，提供2倍于稠密张量计算的性能。
  * 新的`DPX`指令：该指令能够加速动态规划算法，相比`A100`提升7倍的性能。例如基因组处理中的`Smith-Waterman`算法以及为机器人队伍寻找最优路径的`Floyd-Warshall`算法。
  * 3倍性能的IEEE标准浮点处理性能：相比`A100`，SM同频浮点性能为2倍。而得益于更高的频率以及更多的SM，总体性能为3倍。
  * 新的抽象层`Thread block Cluster`：这一特性能够使程序员能够显式地以大于运行在一个SM上的一个线程块`Thread block`的粒度控制程序的局部性。这一特性通过增加一个抽象层扩展了`CUDA`编程模型，现在的编程模型包括`thread`, `thread block`, `thread block cluster`, `grid`。`Thread block cluster`能够使多个线程块同时运行于多个SM，并支持同步、集合通信以及数据交换。
  * 分布式共享内存：这一机制允许SM之间点对点横跨多个SM的共享内存地进行包含`load`, `store`以及源自操作在内的通信。
  * 新的异步执行模型：通过张量存储加速器`TMA`能够在全剧内存以及共享内存间进行更高效的大规模数据通信。TMA同样还支持`thread block cluster`内的`thread block`进行异步数据拷贝。为保证数据原子移动以及同步，TMA还加入了新的异步事物屏障(`asynchronous transaction barrier`)。
* 新的Transformer引擎：该引擎结合张量核心以及软件特性专门加速Transformer模型的训练与推理。该引擎能够智能地管理计算过程，动态地在FP8以及FP16精度之间选择，自动处理层之间不同数据精度地重用和缩放。在大型语言模型上相比`A100`能获得9倍训练性能和30倍推理性能地提升。
* `HBM3`显存子系统：相比前代产品这一系统能提供将近2倍地带宽。`H100 SXM5 GPU`是世界上第一款配备了`HBM3`显存并提供领先的`3 TB/s`显存带宽地GPU。
* `50MB`的L2缓存：缓存更多的数据、模型，以减少访存`HBM3`。
* 第二代多实例GPU技术(`Multi-Instance GPU`)：相比`A100`，每个GPU实例能提供3倍的计算能力以及2倍的访存带宽。且本代产品开始每个GPU实例能够提供加密保密计算。`H100`最多能够提供7个GPU实例，每个实例都有各自的图像视频解码单元(`NVDEC`,`NVJPG`)。现在每个GPU实例都有独立的性能监视器。
* 新的隐私计算支持：新机制能够保证在虚拟机或GPU实例中的用户数据具有更高的安全性，防止硬件、软件的攻击，更好地隔离资源。`H100`实现了世界上第一个原生的GPU配合CPU的加密计算以及高可信运行环境，并且完全匹配PCIe标准。
* 第四代`NVLink`：相比前代产品，`H100`在All-Reduce运算中能够提供3倍的带宽，而各种应用平均能提升50%的带宽。`NVLink`能提供7倍于`PCIe Gen5`的带宽(`900 GB/s`)。
* 第三代`NVSwitch`：这一技术同时包含节点内部以及节点外部用于互联在服务器、集群及数据中心中多个GPU的网络。节点内部每个`NVSwitch`提供64个`NVLink`端口以加速多GPU互联速率。相比前代产品，整个互联网络的吞吐量从`7.2 Tbits/s`提升到`13.6 Tbits/s`。新一代互联网络同时在硬件上加速了包含多播、归约等集合通信。
* 新的硬件互联系统：基于`NVLink`以及`NVSwitch`技术，新的互联系统支持32个节点或256个GPU以2:1胖树拓扑相连接。这一连接方式能够提供`57.6 TB/s`的互联带宽从而达到在`FP8`精度下`1 exaFLOP`的稀疏计算性能。
* `PCIe Gen5`：相比`Gen4`，能够提供双向共`128 GB/s`的带宽。`PCIe Gen5`使得`H100`能够以最高的性能与`x86 CPU，SmartNICs`以及`DPU`连接

除上文提到的信特性外，还有许多新细节能够提升性能、减小延迟和开销、提升编程便利性。

## 2. 深入`NVIDIA H100 GPU`架构
