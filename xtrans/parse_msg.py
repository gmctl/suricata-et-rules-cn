# coding:utf-8 

import re 

Orgs = ['ET', 'GPL', 'TGI']

def parse_msg(full_msg):

    matchd_org = re.match( '((' + '|'.join(Orgs) + ')\s+([0-9A-Z_]+))\s+(.*)', full_msg)
    if matchd_org:
        slug, msg = matchd_org.group(1), matchd_org.group(4)
        return slug, msg 
    
    matchd_thirty = re.match('([_0-9A-Z]+) (.*)', full_msg)
    if matchd_thirty:
        slug, msg = matchd_thirty.group(1), matchd_thirty.group(2) 
    else:
        slug, msg = 'RZX', full_msg 
    return slug, msg 


def get_txt_lines(path):
    with open(path, 'r+', encoding='utf-8') as f:
        s_lines = [x.split('\n')[0] for x in  f.readlines()] 
        f.close()
    return s_lines 


if __name__ == '__main__':
    en_full_msgs = get_txt_lines('./en_sids.txt')

    slug_sets = []
    for x in en_full_msgs:
        _slug, _msg = parse_msg(x)
        _pre_txt = _slug + ',' + _msg 
        slug_sets.append(_pre_txt)

    with open('sid_zap.txt', 'w+', encoding='utf-8' ) as f:
        f.write('\n'.join(slug_sets))
        f.close() 
