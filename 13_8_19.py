q = int(input("Введите кол-во билетов\n"))
s = 0
for n in range(1,q+1):
    a = int(input("Возраст " + str(n) + "-го посетителя:\n"))
    if a >= 25:
        s += 1390
    elif 18 <= a < 25:
        s += 990
if q > 3:
    s *= 0.9
print("Сумма к оплате: ", s)
