# Socrates

## 创意简介：
	苏格拉底反问法，就是通过反问的方式强迫自己思考，从而最终找到正确答案。在思考的过程中我们先假设对话的双方是理性的且不含偏见的，因此能在一来一回的辩论中通过问答的方式帮助人产生新思想。
	本产品替代了苏格拉底，采用回合制对话的方式，对提出的问题进行巧妙地反问，引导用户进行思考。用户也可以通过“一键总结”功能，生成辩论的纲领思想。

## 创意背景：
	新冠疫情、中美关系、内卷，当下青年人生活在百年未有之大变局中，各类思想的激烈碰撞让人不由得感到迷茫。苏格拉底，作为先贤们的一员，在繁重的学习生活之余，为现代人的思考提供一些指导。
	终极目标是实现元宇宙中复刻先贤成为NPC。通过模型的模拟，生成孔孟、老子、牛顿等对话虚拟人格，在游戏中对话，在对话中学习，另辟一条教育道路。

## 解决方案：
	demo中已经初步展示了一些有意思的反问样例，如若对该结果进行优化，我们可以使用NER和阅读理解对输入进行分析，生成反问语句；同时可以将提问转换为同义陈述句后作为问答任务的答案，从候选问题中寻找合适的提问。最终可以使用语义相似度计算问题和反问之间的相似度，将其作为损失函数的一部分进行模型优化。
	在内存中记载用户的每次提问和反问，最终使用NLU生成一篇可读的总结报告。

## 预期效果：
	作为一款偏树洞类app，可以通过知识付费和广告进行盈利。通过用户的提问，可以向其推荐知识类课程进行学习、或是相关产品。例如：“我是否应该辞职？”可以适当推荐理财、创业、财富自由相关课程；“考研记笔记iPad好用吗？”根据对话可能关注到用户存在视力方面的顾虑，因此可以向其推荐水墨屏的pad。


## How to start

1. generate project using `nb create` .
2. writing your plugins under `socrates/plugins` folder.
3. run your bot using `nb run` .

## Note:

This is a simple chatbot build based on Nonebot (https://nonebot2-vercel-mirror.vercel.app/).  
A quick demo is showed on BilliBilli (https://www.bilibili.com/video/BV1e44y157AT).  
However this bot is NOT WORKING, this is because:  
a) I cannot afford a server.  
b) Backend ERNIE model is supported by Baidu, which they no longer release related APIs.