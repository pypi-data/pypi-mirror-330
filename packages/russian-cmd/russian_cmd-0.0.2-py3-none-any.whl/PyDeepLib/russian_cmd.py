целое_число = int
дробное_число = float
строка = str
список = list
диапозон = range
ноль = 0
один = 1
два = 2
три = 3
четыре = 4
пять = 5
шесть = 6
семь = 7
восемь = 8
девять = 9
ввести = input
вывести = print
сумма = sum
минимум = min
максимум = max
открыть = open
длина = len
истина = True
ложь = False
def среднеареф(a = []):
    if длина(a) == 0:
        return 'Error'
    else:
        return сумма(a)/длина(a)
def добавить(l, a):
    if l != l[0:len(l)]:
        return l
    else:
        return l.append(a)
def н_регистр(a):
    if a != str(a):
        return a
    else:
        return a.lower()
def в_регистр(a):
    if a !=  str(a):
        return a
    else:
        return a.upper()
