# 2 Source coding

## 2.1 Source code

&emsp;***codeword***:字母到二进制字符串的映射。  

&emsp;***codebook***:字母表中所有的符号的codeword的集合。 



&emsp;假定$C$是codeword，字符串为$x_1x_2...x_n$， 
$$
C(x_1x_2...x_n)=C(x_1)C(x_2)...C(x_n)
$$
&emsp; 假定离散随机变量$/mathcal{X}$的分布为$p(x)$，每个字符对应的长度为$l(x)$，codeword的平均长度为 $L(C)$，我们有  
$$
L(C)=\sum_{x\in\mathcal{X}}{p(x)l(x)}
$$
