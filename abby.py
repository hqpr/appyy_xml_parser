import json
import re

with open('abbyy_result.json') as abby_file:
    content = abby_file.read()
json_content = json.loads(content)


def save_to_db(objects):
    attrs_lst = []
    char_lst = []
    for obj in objects:
        if isinstance(obj, dict):
            attrs_lst.append(obj['@attributes'])
        else:
            char_lst.append(obj)
    string_ = ''.join(char_lst)
    splitted_words = re.sub(r"([A-Z])", r" \1", string_).split()
    data = {}
    for w, a in zip(splitted_words, attrs_lst):
        word_l = a['l']
        word_t = a['t']
        word_b = a['b']
        word_r = a['r']
        data.update({'word': w, 'word_l': word_l, 'word_t': word_t, 'word_b': word_b, 'word_r': word_r})
    return data


for block in json_content['page']['block']:
    block_type = block['@attributes']['blockType']
    block_b = block['@attributes']['b']
    block_l = block['@attributes']['l']
    block_t = block['@attributes']['t']
    block_r = block['@attributes']['r']

    if block_type == 'Text':
        if not isinstance(block['text']['par'], list):
            if not isinstance(block['text']['par']['line'], list):
                baseline = block['text']['par']['line']['@attributes']['baseline']
                if not isinstance(block['text']['par']['line']['formatting'], list):
                    char_params = block['text']['par']['line']['formatting']['charParams']
                    save_to_db(char_params)
                else:
                    for line in block['text']['par']['line']['formatting']:
                        save_to_db(line['charParams'])
            else:
                for line in block['text']['par']['line']:
                    baseline = line['@attributes']['baseline']
        else:
            for par in block['text']['par']:
                if not isinstance(par['line']['formatting'], list):
                    save_to_db(par['line']['formatting']['charParams'])
                else:
                    for line in par['line']['formatting']:
                        save_to_db(line['charParams'])

    elif block_type == 'Table':
        for row in block['row']:
            for cell in row['cell']:
                if isinstance(cell, dict):
                    cell_width = cell['@attributes']['width']
                    cell_height = cell['@attributes']['height']
                    if not isinstance(cell['text']['par'], list):
                        if cell['text']['par'].get('line'):
                            if isinstance(cell['text']['par']['line'], list):
                                for line in cell['text']['par']['line']:
                                    save_to_db(line['formatting']['charParams'])
                            else:
                                if cell['text']['par']['line'].get('formatting'):
                                    if not isinstance(cell['text']['par']['line']['formatting'], list):
                                        save_to_db(cell['text']['par']['line']['formatting']['charParams'])
                print(cell['@attributes'])
                print()

    elif block_type == 'Picture':
        pass
        # print('PICTURE')
    elif block_type == 'SeparatorsBox':
        pass
        # print('SeparatorsBox')
    elif block_type == 'Separator':
        pass
        # print('Separator')
    else:
        print('NEW SHIT: {}'.format(block_type))
