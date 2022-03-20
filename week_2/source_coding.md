# Source coding

## Source code

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

## Prefix codes

&emsp;***非奇***（non-singular）:任何一个字母表中的符号的映射都是不同的。

&emsp;***可独特编码***（uniquely decodable）:每个符号序列都可以映射为一个不同的比特流，也就是说，对于一串符号序列，有且仅有一个对应的比特流。

&emsp;***前缀编码***（Prefix code）:如果codebook里任何一个codeword都不是另一个codeword的前缀，那么编码被称为前缀编码。  

<center><img src=".\image\code.png" height ="50%" width="50%"\></center>  

&emsp;下图是关于前缀编码的解码的伪代码。

<center><img src=".\image\prefix_decoding.png" height="50%" weight="50%"\></center>

## Kraft Inequality

&emsp;对于任何具有$N$个codeword的前缀编码，它的编码长度$l_1,l_2,...,l_N$一定符合下述不等式，

<center>$$\sum_{i=1}^{N}{2^{-l_i}\le1}$$</center>  

## 2.4 Minimum Encoding Bit Rate 

&emsp;平均比特率（average bit rate）用于衡量针对源代码C数据压缩的表现。假定字母表里第$i$个字符的概率为$p_i$，且其对应的codeword的长度为$l_i$，那么我们有，

<center>$$L(C)=\sum_{i=1}^{N}{p_il_i}$$</center> 

&emsp;任何随机变量的前缀编码的平均比特率都大于随机变量的熵，  

<center>$$L(C)\ge H(X)$$</cenetr>  

&emsp;***证明思路***：将不等式转换为$L(C)-H(X)\ge0$，然后带入$L(C)=\sum_{i=1}^{N}{p_il_i}$，$H(X)=-\sum_{i=1}^{N}{p_ilog_2{p_i}}$，合并两个式子，接着使用Jensen Inequality得到最终的结果。  

## Huffman Codes  

&emsp;霍夫曼编码的执行的思路就是依据每个codeword的可能性由高到低进行排序，每轮选择可能性最低的两个codeword进行合并，并且标记合并的两个枝干，上面的枝干为0，下面的枝干为1，直到所有的codeword被合并。

<center><img src=".\image\Huffman_codes.png" height="50%" width="50%"/></center>
