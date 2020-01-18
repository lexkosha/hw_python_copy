# -*- coding: utf-8 -*-
import os
fb = os.path.join('some','folder')
print(fb)


params = {}
params["file"] = "my_file1.txt"
params["mode"] = "w"
params["encoding"] = "utf-8"

with open(**params) as fp:
    fp.write("example string")
print(params)
"""
Пишим свой контекстный менеджер для создания
HTML документа.
"""


class Tag:
    def __init__(self, tag, is_single=False):
        self.tag = tag
        self.text = ''
        self.attributes = {}
        self.is_single = is_single

    def __enter__(self):
        """Отдаем себя при старте"""
        return self

    def __exit__(self, type, value, traceback):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = ' '.join(attrs)

        if self.is_single:
            print('<{tag} {attrs}/>'.format(tag=self.tag, attrs=attrs))
        else:
            print('<{tag} {attrs}>{text}</{tag}>'.format(tag=self.tag, attrs=attrs, text=self.text))


# with Tag('H1') as tag:
#     tag.text = 'Привет нига'
#     tag.attributes['class'] = 'my_analizing_class'
#
# with Tag('img') as tag:
#     tag.attributes['class'] = 'my_analizing_class'
#     tag.attributes['src'] = '/tmp/my-logo.png'
