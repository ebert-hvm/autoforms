
with open('num.txt', 'r', encoding="utf-8") as f:
    for num in f.readlines():
        num = num.strip()
        n=0
        name = ''
        with open('names.txt', 'r', encoding="utf-8") as g:
            for l in g.readlines():
                n, name = l.strip().split(',')
                if n == num:
                    with open('output.txt', 'a', encoding="utf-8") as h:
                        h.write(f'{n},{name},C\n')
                        break
        
