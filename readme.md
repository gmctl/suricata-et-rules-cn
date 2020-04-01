# 代码说明


- `_tools` 是我一直自己用的规则拆解的套件，要比官方的好用
    - 核心程序就是 `main.py` 修改 `__main__` 里面的路径为自己规则的路径可以生成 `trans.txt` 
- `push_txt.py` 是将 `trans.txt` 结合我们现有的excel的顺序 `all_sis.txt` 转化为 `output.txt` ;
- `*.txt` 是运行 py 文件后生成的一系列文件
- `replace_end.py` 是最终的产物，其中需要注意的是这里面有个替换列表是手动增加的
    - 替换列表 `sid_slug,txt` 这个文件是提取出规则里面的 msg 后进行替换删除前缀(ET DOS)这样的关键字 


