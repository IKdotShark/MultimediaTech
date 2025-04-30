import numpy as np

# Исходный массив
arr = np.array([[1, 2, 3],
                [2, -1, 4],
                [-20, 4, 10]])

# Маска для отрицательных значений
negative_mask = arr < 0

# Маска для положительных значений
positive_mask = arr > 0

# Создаем массивы, где отрицательные и положительные значения заменяются на 0, соответственно
arr_negatives = np.where(negative_mask, arr, 0)
arr_positives = np.where(positive_mask, arr, 0)
sum_negatives = np.sum(arr_negatives, axis=0)
sum_positives = np.sum(arr_positives, axis=0)

print("Сумма отрицательных значений:")
print(sum_negatives)

print("\nСумма положительных значений:")
print(sum_positives)



column = np.array([-5, -3, -5, -1])  # индексы: 0, 1, 2, 3
neg_indices = np.where(column < 0)[0]
neg_indices = sorted(neg_indices, key=lambda i: (column[i], i))
print(neg_indices)



