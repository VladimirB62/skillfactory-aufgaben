per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}
procent = dict.values(per_cent)
money = float(input("Введите сумму вклада\n"))
deposit = [i*money/100 for i in procent]
print(deposit)
print("Максимальная сумма, которую вы можете заработать —", max(deposit))