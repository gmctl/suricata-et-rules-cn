import re 


def get_lines_from_file(path):
    with open(path, 'r+', encoding='utf-8') as f:
        lines = f.readlines() 
        f.close()
    return [x.split('\n')[0] for x in lines]


def get_file_strs(path):
    with open(path, 'r+', encoding='utf-8') as f:
        result = f.read() 
        f.close()
    return result 


if __name__ == '__main__':
    outputs = get_file_strs('/root/suricata/output.txt')
    reps = get_lines_from_file('/root/suricata/sid_slugs.txt')
    
    for x in reps:
        outputs = outputs.replace(x, '') 

    with open('r0.txt', 'w+', encoding='utf-8') as f:
        f.write(outputs)
        f.close() 
