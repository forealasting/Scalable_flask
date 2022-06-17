"# **Scalable_flask**" : 

***Building a Scalable Flask Application using Docker***


### Scenario 1

First scenario we focus on a single container .
We use flask to build our web service. 

![](https://i.imgur.com/6bpSfNc.png)

• **Set the single container CPUs = 0.3** 

(We let the system have less cpu resource first. We expect to see the impact of different request rates with limited resources.)

•	**Set container fixed replica = 1**

(We let the system have only one container first.)

•     **Agent is only responsible for forwarding requests in this scenario**


### Second scenario 

we let system scalable .
We use static threshold-based approach by setting the maximum tolerance response time T_max=25ms /T_max=30ms.

##### i.Horizontal elasticity
1. If the maximum tolerance response time is violated, agent should take action to increase a container(service).

2. Every 1 increase in container with CPUs 0.3
##### ii.Vertical elasticity

1. If the maximum tolerance response time is violated, agent should take action to increase CPUs resources.
2. Every 0.1 increase in CPU resources




***REFERENCES***:

[1]	Jie-Yong Yang, “Design and Analysis of Multiple Level Elasticity Policy in Microservice-based M2M Platform,”2021

[2]	Vindeep Singh and Sateesh K Peddoju, “Container-based Microservice Architecture for Cloud Applications,” International Conference on Computing, Communication and Automation, 2017

[3]	F. Rossi, M. Nardelli and V. Cardellini, "Horizontal and Vertical Scaling of Container-Based Applications Using Reinforcement Learning," 2019 IEEE 12th International Conference on Cloud Computing (CLOUD) , pp. 329-338, 2019.

[4]	Y. Al-Dhuraibi, F. Paraiso, N. Djarallah and P. Merle, "Elasticity in Cloud Computing: State of the Art and Research Challenges," in IEEE Transactions on Services Computing, vol. 11, no. 2, pp. 430-447, 1 March-April 2018.

[5]	F. Rossi, V. Cardellini and F. L. Presti, "Self-adaptive Threshold-based Policy for Microservices Elasticity," 2020 28th International Symposium on Modeling, Analysis, and Simulation of Computer and Telecommunication Systems (MASCOTS) , pp. 1-8, 2020.

[6]	S. Zhang, T. Wu, M. Pan, C. Zhang and Y. Yu, "A-SARSA: A Predictive Container Auto-Scaling Algorithm Based on Reinforcement Learning," 2020 IEEE International Conference on Web Services (ICWS) , pp. 489-497, 2020.7
[7]	Wenzheng Li, Xiaoping Li and Ruben´ Ruiz, "Scheduling Microservice-based Workflows to Containers in On-demand Cloud Resources," 2021 IEEE 24th International Conference on Computer Supported Cooperative Work in Design , pp. 61-66, 2021.

[8]	Liu, Guozhi, et al. "Microservices: architecture, container, and challenges." 2020 IEEE 20th International Conference on Software Quality, Reliability and Security Companion (QRS-C). IEEE, pp. 629-635,2020.

[9]	Y. Al-Dhuraibi, F. Paraiso, N. Djarallah and P. Merle, "Autonomic Vertical Elasticity of Docker Containers with ELASTICDOCKER," 2017 IEEE 10th International Conference on Cloud Computing (CLOUD) , pp. 472-479, 2017.

[10]	Docker. Available on June 16,2022: https://www.docker.com/ .
