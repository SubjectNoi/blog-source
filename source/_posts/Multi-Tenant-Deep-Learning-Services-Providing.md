---
title: Multi-Tenant Deep Learning Services Providing
date: 2022-04-26 07:35:53
tags:
---


This work is accepted by ASPLOS 2022.

# Introduction
It's universally acknowledged that deep learning applications are evolving fast and are becoming more and more complex. For example, In cloud service and auto-piloting, we need to provide service to several deep learning models. However, currently, the computation power of hardware also increases significantly, for example, Threadripper 3990X CPU has ~15 TFLOPS for FP32 while Radeon Instinct MI100 has>100 TFLOPS for matrix computation. This situation resulted in a problem that the performance of single hardware is far beyond the requirement of a single inference task of model: the QoS requirement of ResNet-50 in MLPerf is 15ms while the whole CPU use only 6ms to finish the job.
Under this circumstance, we need multi-tenant. In another word, we need to co-locate multiple tasks, or queries, onto one hardware. 

# Current Solutions
We can divide current solutions into hardware and software solutions. The hardware solutions mainly bypass the complex resource management of co-locating tasks by temporal sharing or physical isolation, like AI-MT for temporal sharing and NVIDIA MIG for resource isolation. For software solutions, there are some task co-locating solutions for traditional workloads including Parties, for deep learning tasks, DART proposed a cluster scale scheduling strategy. While our work mainly focuses on CPU scale strategy.

### A straightforward solution
Of course, we have some simple, straightforward solutions. On CPUs, we can use MPI to serve multiple tasks and use CPU affinity and tools including res control, Intel CAT to limit resource usage. On GPUs, we have Multi-Process Service, Persistent Thread Block. These techniques support simply dumping multiple tasks onto single hardware. But how about the performance? It's not good. Following list is an example of doing so. 
```
if (MPI_CPU_ID == 0) {
    // CPUs
    sched_setaffinity(0, sizeof(cpu_set_t), 0x000f);
    task1.run();
    // GPUs
    task_kernel_1 <<<(1/4)_SM, ...>>>(...);
}
else if (MPI_CPU_ID == 1) {
    // CPUs
    sched_setaffinity(0, sizeof(cpu_set_t), 0xfff0);
    task2.run();
    // GPUs
    task_kernel_2 <<<(3/4)_SM, ...>>>(...);
}
```

### What's the limitations?
- The first is co-locating interference, according to our verification experiment, co-locating 4 identical `GoogLeNet` tasks on a CPU platform have 1.8x latency. If we inspect the system performance counter including LLC miss rate, LLC access, we observe server shared resources contention.
- The second is low QoS satisfaction rate. With the increase of QPS (Query Per Second), the satisfaction rate of the system drop significantly. Even if we apply fine-grained scheduling (schedule every layer/op of the network seperatly), the system with AMD Threadripper 3990X can only serve 50 queries with 99% satisfaction rate, while the theoritical performance of the CPU is far beyond this.
