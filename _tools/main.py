import os 
import sys
import re

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DefaultRulePath = os.path.join(PROJECT_DIR, *['docs', 'suricata_home', 'emerging.rules', 'rules'])
AutoTakeRulePath = os.path.join(PROJECT_DIR, *list("docs/suricata_home/suricata-5.0.0/rules".split('/')))
EmergingRulePath = DefaultRulePath
FedoraRulePath =  os.path.join(PROJECT_DIR, *['docs', 'suricata_home', 'suricata.rules'])

# ClassificationMappingPath = os.path.join(PROJECT_DIR, *[DefaultRulePath, 'classification.config'])
ClassificationMappingPath = os.path.join(PROJECT_DIR, *['apps', 'xrule', 'docs', 'classification.config'])
Add_RuleTxt = True

from parse_rule import parse_rule_line


def get_filestrs_from_txtfile(filename, file_dir=DefaultRulePath):
    """
    通过文件获取文件的txt内容; 这里由于是脚本控制，所以没有用锁
    :param filename: 文件
    :param file_dir: 目录
    :return:
    """
    with open(os.path.join(file_dir, filename), "r", encoding='utf-8') as f:
        filestrs = f.readlines()
        f.close()
    return filestrs


def list_all_rulefiles(file_dir=DefaultRulePath):
    return [x for x in os.listdir(file_dir) if re.match(".*?\.rules", x)]


def get_rules_parsed_by_filename(filename, file_dir=DefaultRulePath):
    # from .parse_rule import parse_rule_line
    rule_lines = get_filestrs_from_txtfile(filename, file_dir)
    res = []
    for line in rule_lines:
        line_parsed = parse_rule_line(line, detail=Add_RuleTxt)
        if line_parsed:
            if "classtype" not in line_parsed.keys():
                # 修改默认没有归类的规则到这里。
                line_parsed['classtype'] = 'protocol-command-decode'
            res.append(line_parsed)
            # 增加所属文件的这个内容
            line_parsed['belong_file'] = filename

    return res


def get_emerging_classes():
    """
    TODO: 获取规则的分类类别; 其中官方规则已经给了这个文件;
    务必保证文件格式中,前后没有空格！！！
    config classification:shortname,short description,priority
    :return: [*dict, ]
    注意如果要逐条翻译, 这里可以调用翻译脚本翻译出来 `cn_name` 写入
    """
    with open(ClassificationMappingPath, "r", encoding='utf-8') as f:
        lines = f.readlines()
        f.close()
    classifications = []
    for line in lines:
        matched = re.match("config classification: (.*?),(.*?),(\d+).*?", line)
        if matched:
            classifications.append(dict(
                shortname=matched.group(1).strip(),
                short_description=matched.group(2).strip(),
                priority=int(matched.group(3).strip()),
            ))
    return classifications


def get_emerging_rules(file_dir=EmergingRulePath, *args, **kwargs):
    res = []
    for x in list_all_rulefiles(file_dir=file_dir):
        res.extend(get_rules_parsed_by_filename(file_dir=file_dir, filename=x))
    return res


def parse_file_path_abs_dir(dirpath='E:\\workspace\\ids_project\docs\\suricata_home'):
    collect_rule_files = []
    for x in os.listdir(dirpath):
        _path = os.path.join(dirpath, x)
        if os.path.isdir(_path):
            collect_rule_files.extend(parse_file_path_abs_dir(_path))
            continue
        matched_rule_file = re.match('.*?.rules$', x)
        if matched_rule_file:
            collect_rule_files.append(_path)
    return collect_rule_files


class RuleManager:
    """
    规则管理合一测试的管理。
    """
    @staticmethod
    def get_all_rules_based_dir(file_dir):
        res = []
        for x in list_all_rulefiles(file_dir=file_dir):
            res.extend(get_rules_parsed_by_filename(file_dir=file_dir, filename=x))
        return res

    @staticmethod
    def push__all_in_one_file(file_dir, saved_path='all_in_one_rule.rules'):
        rules = RuleManager.get_all_rules_based_dir(file_dir)
        with open(saved_path, "w+", encoding='utf-8') as f:
            for _rule in rules:
                f.write(_rule['rule_line'])
            f.close()
        return

    @staticmethod
    def parse_sigle_rulefile(path=FedoraRulePath):
        return get_rules_parsed_by_filename(file_dir='', filename=path)

    @staticmethod
    def collected_rules_by_dirpath(dirpath='E:\\workspace\\ids_project\docs\\suricata_home'):
        paths = parse_file_path_abs_dir(dirpath=dirpath)
        res = []
        for x in paths:
            _current_rule_sets = get_rules_parsed_by_filename(x)
            res.extend(_current_rule_sets)
        return res

    @staticmethod
    def get_not_collected_rules(dirpath='E:\\workspace\\ids_project\docs\\suricata_home'):
        current_rules = RuleManager.collected_rules_by_dirpath(dirpath=dirpath)
        from xrule.models import IpsRule
        have_collected = set([x.sid for x in IpsRule.objects.all()])
        current = set([x['sid'] for x in current_rules])
        _need_ids = current - (current | have_collected)
        _self_check_duplicates = []  # 本地去重验证.
        return [x for x in current_rules if x['sid'] not in _need_ids]


if __name__ == '__main__':
    rules = get_rules_parsed_by_filename('/root/suricata/suricata.rules')
    _logtxt = ['{sid},{signature}'.format(sid=x['sid'], signature=x['msg']) for x in rules]
    
    with open('tran.txt', 'w+', encoding='utf-8') as f:
        f.write('\n'.join(_logtxt))
        f.close() 


