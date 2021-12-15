def get_list(str_):
    li_ = []
    for i in str_.split():
        try:
            li_.append(float(i))
        except ValueError:
            print("В списке присутствует нечисловое значение")
    return li_

def sort_list(l_):
    return sorted(l_)

def search_lower(array, element, left, right):
    if len(array) < 2:
        print("Слишком короткий массив")
        return False
    if left > right:
        return False
    if element <= array[0]:
        print("Нет элементов, удовлетворящих условиям. Элемент является минимальным")
        return False
    if element > array[-1]:
        print("Нет элементов, удовлетворящих условиям. Элемент является максимальным")
        return False
    middle = (right + left) // 2
    if array[middle] < element and array[middle+1]>=element:
        return middle
    elif element <= array[middle]:
        return search_lower(array, element, left, middle - 1)
    else:
        return search_lower(array, element, middle + 1, right)

string="153 45 78 69 452 158 12 45 12 4.56 36 258 14 159 265 126 12 14 18 19 16 147 56 89 57 45 -17"
array = sort_list(get_list(string))
l = input('Что нужно найти? ')
try:
    element = (float(l))
except ValueError:
    print("Введено недопустимое значение")
    exit()
print(search_lower(array, element, 0, len(array)))
print(array)