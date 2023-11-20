from django import template

register = template.Library()

dwords = ['сука', 'хер', 'дебил']


@register.filter('censor')
def char_to_asterisk(value):
    words = value.split()
    nwords = []
    for word in words:
        nword = word
        for cw in dwords:
            if word.strip().lower().replace('-', '').startswith(cw):
                nword = ''
                bf = False
                i = 0
                for char in word:
                    if char == '&':
                        bf = True
                    if char.isalpha() and not bf and i:
                        nword += '*'
                    else:
                        nword += char
                    i += 1
        nwords.append(nword)
    nvalue = ' '.join(nwords)
    return f'{nvalue}'
