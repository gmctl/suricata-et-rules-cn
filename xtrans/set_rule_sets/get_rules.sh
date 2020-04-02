#!/bin/bash 

wget http://rules.emergingthreats.net/open-nogpl/suricata-5.0/emerging.rules.tar.gz && tar xf emerging.rules.tar.gz 
git clone https://github.com/ptresearch/AttackDetection
git clone https://github.com/suricata-rules/suricata-rules
git clone https://github.com/travisbgreen/hunting-rules

# 删除 dns 和 加密的指纹的规则
