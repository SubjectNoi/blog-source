---
title: >-
  Review Log: QIG: Quantifying the Importance and Interaction of GPGPU
  Architecture Parameters (TCAD VOL.37, NO.6, 2018)
date: 2022-05-05 12:22:47
tags: Paper Review
---

# 0. 开始之前及总体感想
* 文章标题：Review Log: QIG: Quantifying the Importance and Interaction of GPGPU Architecture Parameters

* 期刊/会议：TCAD VOL.37, NO.6, 2018

* 这篇文章和我下一个想做的工作有重合，所以会以较为aggressive的态度来写review log（

* 本文主要介绍了一种用于GPU设计过程中设计空间探索（Design Space Explore，DSE）的系统，通过将设计参数与GPU Kernel的运行性能数据输入给一个*可解释*的机器学习模型（有点类似随机森林的决策树算法）来衡量不同任务下不同设计参数的优劣。当然这篇文章最重要的贡献我认为不在于模型准确率活着加速GPU架构设计等等，而在于其挖掘的GPU设计参数对于计算任务的影响，以及参数之间互相影响的模式。
* 本文采用可解释的机器学习模型，在获得高预测准确率的同时能够解释数据与硬件之间的关系。然而有些解释在我看来并不能真实反应硬件设计参数对性能的影响，也许是将相关性解释为了因果性，详见Review Log正文。
# 1. Summary
This work proposed an explainable performance model of GPGPUs, based on which the authors first predict the performance of a given kernel on giver hardware with high accuracy, then explain the relation between GPGPU behaviors and design parameters. 
# 2. Strength
+ The paper is well organized and well-motivated. 
+ The performance model they use is highly explainable with considerable accuracy.
+ Some important design insights are revealed via their model.
+ The performance model can be easily generalized to other hardware and other performance metrics (from IPS to Power consumption).
# 3. Weakness
- Some findings are misleading, which will be datailed in questions and comments.
# 4. Questions and Comments to Authors
0. The problem this work target is emerging and important, and the authors explain their motivation well.
1. In the analysis of importance analysis, the *core frequency* is treated as the most important design factor. While this parameter is not the most challenging factor the hardware designers concerned. It's trival that with higher frequency the performance and power of a GPGPU kernel will increase. So is the *instruction replay overhead* which is a factor related to the profiler itself. I think it's necessary to filter out the influence of these parameters other wise some misleading findings will be given. (For example, execute all the kernels at a fixed core frequency or fixed power budget)
2.  I think the benchmark amount and the problem size are limited, and the register per thread is always sufficient. While for some recent applications with very heavy computation burdens, there may exist other patterns. (这点其实有点时空警察，但是2018年应该也是有那些很大的模型、很大的计算任务了)
3. GPUWattch is available for power estimated with higher explainable. 
4. Overall, the findings and hardware patterns proposed in this work is reasonable and insightful. 
# 5. Paper Writting (1-5)
4
# 6. Overall Merit (1-5)
4 - Weak Accept
# 7. Confidence (1-4)
3 - Knowledgeable
