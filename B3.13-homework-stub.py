""""

Таким образом:

В коде должно быть минимум три основных класса HTML, TopLevelTag и Tag.
Класс HTML определяет, куда сохранять вывод: на экран через print или в файл.
Объекты класса TopLevelTag скорее всего не содержат внутреннего текста и всегда парные.
Объекта класса Tag могут быть непарные или быть парные и содержать текст внутри себя.
Должна быть возможность задать атрибуты в Tag, но в данном задании для TopLevelTag это необязательное условие.
Это задание имеет очень гибкие варианты решения, и в первую очередь в решении оценивается результат (получился или не получился HTML как на фрагменте выше). Код, приведенный выше, — просто вариант решения. Возможно, вам проще будет решить задание с другим форматом ввода или создания документа.

То есть:

Для решения задания не обязательно использовать контекстный менеджер
Можно использовать или не использовать наследование
Можно использовать или не использовать специальные методы
Можно использовать или не использовать *args/**kwargs для указания решения
В этом задании обязательно использовать классы. Хотя решение можно получить и просто на функциях, в данном задании использование классов предпочтительней.
"""

class HTML:

    def __init__(self, output):
        self.output = output
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        html = '<html>\n'
        for child in self.children:
            html += str(child)
        html += '</html>'
        return html

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.output is None:
            print(self)
        else:
            with open(self.output, 'w', encoding='utf-8') as f:
                f.write(str(self))


class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        opening = f'<{self.tag}>\n'
        if self.children:
            for child in self.children:
                internal = str(child)
        else:
            internal = ''
        ending = f'</{self.tag}>\n'
        return opening + internal + ending

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Tag(TopLevelTag):
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        super().__init__(tag)
        self.text = ''
        self.is_single = is_single
        self.attributes = {}

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if self.attributes:
            attrs = ' ' + attrs

        if len(self.children) > 0:
            opening = "<{tag}{attrs}>".format(tag=self.tag, attrs=attrs) + "\n"
            if self.text:
                internal = "%s" % self.text
            else:
                internal = ""
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag + "\n"
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag}{attrs}/>".format(tag=self.tag, attrs=attrs) + "\n"
            else:
                return "<{tag}{attrs}>{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text) + "\n"


if __name__ == "__main__":
    with HTML(output='index.html') as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "Домашние задание"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Че кого е? Выходи раз на раз!"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "Тоби ббида придет!"
                    div += paragraph

                with Tag("img", is_single=True, src="/img.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body