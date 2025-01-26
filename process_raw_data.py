import json
import re

from cleantext import clean


def preprocess_text(text, **kwargs):
    cleaned_text = clean(
        text,
        no_emoji=True,  # Remove emojis
        no_urls=True,  # Remove URLs
        to_ascii=False,
        # no_numbers=False,        # Remove numbers
        # no_currency_symbols=True,  # Remove currency symbols
        # replace_with_punct="",  # Replace punctuation with nothing
        # replace_with_url="<URL>",  # Replace URLs with <URL>
        # replace_with_number="<NUM>",  # Replace numbers with <NUM>
        # lower=True,
        **kwargs
    )
    return cleaned_text.replace('‍', '')


def remove_lines(text, lines_triggers):
    for l in lines_triggers:
        text = re.sub(l, '', text, flags=re.MULTILINE | re.UNICODE)
    return text


with open('data/parsed.txt', encoding='utf-8') as f:
    a = f.read().replace('ru:', '')

b = a.split('>>>>>>>')


def remove_non_alphabetic_lines(text):
    lines = text.splitlines()
    cleaned_lines = [
        line for line in lines
        if re.search(r'[a-zA-Zа-яА-Я]', line)
    ]
    return "\n".join(cleaned_lines)


io = dict()
for i in b:
    if not 'input:' in i:
        continue
    texts = i.split('input:')[1].split('output')[0], i.split('output')[1]

    texts = [remove_lines(t, [r'^#event.*$', r'^choyxona.*$', r'^Посмотреть ещё.*$']) for t in texts]

    inp, out = texts
    out = remove_lines(out, [r'Посмотреть ещё мероприятия', 'Мероприятия для стартапов и инвесторов в Центральной Азии',
                             'startupchoyxona', 'К мероприятию', 'Построить маршрут', 'Перейти к регистрации'])

    out = remove_non_alphabetic_lines(preprocess_text(out, no_punct=False,
                                                      lower=False,
                                                      replace_with_url=''))
    io[preprocess_text(inp, no_punct=False, replace_with_punct='', lower=False)] = out

with open('data/dataset.json', 'w+', encoding='utf-8') as f:
    json.dump([{'input': k, 'output': v} for k, v in io.items()], f, ensure_ascii=False)
