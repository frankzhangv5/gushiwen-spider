# _*_ coding:utf8 _*_

from w3lib.html import remove_tags


def join_url(suffix, prefix='https://www.gushiwen.org'):
    url = prefix
    if suffix is not None:
        url = prefix + suffix
        url = url.strip()
    return url


def write_for_debug(path, something):
    f = open(path, 'w')
    try:
        f.write(something)
    finally:
        f.close()


def load_script(path):
    script = ''
    if path is not None:
        f = open(path)
        try:
            script = f.read()
        finally:
            f.close()
    return script


def eat_header_and_extract(text, tag='<div class="hr"></div>'):
    start = text.find(tag) + len(tag)
    text = text[start:-1]
    text = extract_text(text)
    end = text.find('\n赏析内容整理自网络')
    return text[0:end]


def extract_text(text):
    """
    调用w3lib.html.remove_tags()处理正文
    部分作品的文本内容放在了p标签外面通过<br>分隔
    <br>标签不是完整标签，在remove_tags()函数中会被去掉，无法通过keep保留
    先remove其他标签（div，a，span，p...） 再用'\n'替换<br>
    """
    text = text.replace('</p>', '<br></p>')
    text = text.replace('<strong>', '<br><strong>')
    text = remove_tags(
        text=text, which_ones=('div', 'a', 'span', 'p', 'strong'))
    text = text.replace(' ', '').replace('\n', '',
                                         16).replace('<br>',
                                                     '\n').replace('▲', '')
    return text.strip('\n')
