import re 


def get_lines_from_file(path):
    with open(path, 'r+', encoding='utf-8') as f:
        lines = f.readlines() 
        f.close()
    return [x.split('\n')[0] for x in lines]



if __name__ == '__main__':
    all_rule_sids = get_lines_from_file('/root/suricata/all_sids.txt')
    
    trand_lines = get_lines_from_file('/root/suricata/trans.txt')

    _kv = {} 
    for x in trand_lines:
        matchd = re.match('(\d+),(.*)', x)
        if matchd:
            sid, signature = matchd.group(1), matchd.group(2)
            _kv[sid]  = signature 
    
    print_lines = [_kv[x] if x in _kv.keys() else '-'*10 for x in all_rule_sids]

    with open('output.txt', 'w+', encoding='utf-8') as f:
        f.write( '\n'.join(print_lines) )
        f.close() 
