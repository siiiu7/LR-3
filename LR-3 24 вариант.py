'''
Лабораторная работа №3
С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, 
B,C,D,E заполняется случайным образом целыми числами в интервале [-10,10]. Для тестирования использовать не случайное заполнение, а целенаправленное.

Вариант 24
Формируется матрица F следующим образом: если в Е количество чисел, больших К в четных столбцах в области 2 больше,
чем произведение чисел в нечетных строках в области 4, то поменять в С симметрично области 1 и 4 местами, иначе С и В поменять местами несимметрично.
При этом матрица А не меняется. После чего вычисляется выражение: К*(A*F)+ K* F T . Выводятся по мере формирования А, F и все матричные операции последовательно.
Матрица:
B C
D E
  
Вид матрицы:
  2  
1   3
  4 
'''
import numpy as np
import random
from copy import deepcopy

#Реализуем класс для работы с матрицами, переопределив класс list 
class Matrix(list):
    def generate(self, N):
        '''метод для генерации матрицы случайными числами в диапазоне [-10, 10]'''
        self.clear() #если объект уже заполнен, то очищаем его
        return self.__init__([[random.randint(-10, 10) for _ in range(N)]  for _ in range(N)]) #С помощью list comprehension генерируем двумерный список и передаем в унаследованный конструктор класса
        
    @property
    def size(self):
        '''Определение размерности матрицы'''
        return len(self)

    def max_str(self):
        '''Метод определяет max длину символьного представления чисел в матрице. Необходимо для форматированного вывода матрицы'''
        return max(map(len,(map(str, sum(self,[]) ))))
            
    def __str__(self):
        '''Переопределение метода для форматированного вывода матрицы'''
        m = self.max_str()
        return '\n'.join(' '.join(map(lambda x: f'{x:{m}}', row)) for row in self)
        
    def __mul__(self, other):
        '''Реализация метода для умножения матриц'''
        res = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    res[i][j] += self[i][k]*other[k][j]
        return Matrix(res)

    def __rmul__(self, value):
        '''Реализация метода для умножения числа на матрицу. Число должно стоять перед матрицей'''
        res = deepcopy(self)
        for i in range(res.size):
            for j in range(res.size):
                res[i][j] *= value
        return res
        
    def T(self):
        '''Метод для траспонирования матрицы'''
        res = deepcopy(self)
        for i in range(res.size):
            for j in range(i+1):
                res[i][j], res[j][i] = res[j][i], res[i][j]
        return res

    def __add__(self, other):
        '''Реализация метода для сложения матриц'''
        return Matrix([[self[i][j]+other[i][j] for j in range(self.size)] for i in range(self.size)])

    def __sub__(self, other):
        '''Реализация метода для вычитания матриц'''
        return Matrix([[self[i][j]-other[i][j] for j in range(self.size)] for i in range(self.size)])
        
def check_area(area, i, j, N):
    '''Проверяет входят ли элемент с заданными индексами в заданную область матрицы размерностью NxN;
    area - область матрицы
    i, j - индексы элемента
    N - размер матрицы'''
    if area == 1 and j<=i and N-j > i:    return True
    if area == 2 and j>=i and N-j > i:    return True
    if area == 3 and j>=i and N-j-1 <= i: return True
    if area == 4 and j<=i and N-j-1 <= i: return True
    return False

def area_perimetr(area, i, j, N):
    '''Проверяет принадлежит ли элемент по заданным индексам к элемнтам периметра заданной области'''
    if area == 1 and j<N//2+N%2 and (j==i or i==N-j-1 or j==0): return True
    if area == 2 and i<N//2+N%2 and (j==i or i==N-j-1 or i==0): return True
    if area == 3 and j>N//2+N%2 and (j==i or i==N-j-1 or j==N): return True
    if area == 4 and i>N//2+N%2 and (j==i or i==N-j-1 or i==N): return True
    return False
    
def mirror_area(matrix, sub, area_1, area_2):
    '''
    Зеркально отражает элементы области матрицы относительно диагонали между этими областями
    matrix - исходная матрица;
    sub_matrix_name - имя подматрицы
    area_1, area_2 - области для замены элементов
    '''
    #согласно варианту задания определяем относительно главной или побочной диагонали, вертикальной или горизонтальной оси менять элементы
    res = deepcopy(matrix) 
    mid = len(res)//2 
    for row, col in sub: 
        if check_area(area_1, row%mid, col%mid, mid): 
            if (area_1 == 1 and area_2 == 2) or (area_1 == 2 and area_2 == 1) or (area_1 == 4 and area_2 == 3) or (area_1 == 3 and area_2 == 4):
                ki = ((0, -mid), (mid, 0))[row//mid][col//mid]
                kj = ((0, mid), (-mid, 0))[row//mid][col//mid]
                res[row][col], res[col+ki][row+kj] = res[col+ki][row+kj], res[row][col]
            elif (area_1 == 1 and area_2 == 4) or (area_1 == 4 and area_2 == 1) or (area_1 == 2 and area_2 == 3) or (area_1 == 3 and area_2 == 2): 
                res[row][col], res[mid-col-1+(col//mid+row//mid)*mid][mid-row-1+(col//mid+row//mid)*mid] = res[mid-col-1+(col//mid+row//mid)*mid][mid-row-1+(col//mid+row//mid)*mid], res[row][col]
            elif (area_1 == 1 and area_2 == 3) or (area_2 == 3 and area_1 == 1): 
                res[row][col], res[row][mid*(1+col//mid)-col%mid-1] = res[row][mid*(1+col//mid)-col%mid-1], res[row][col] 
            elif (area_1 == 2 and area_2 == 4) or (area_2 == 4 and area_1 == 2): 
                res[row][col], res[mid*(1+row//mid)-row%mid-1][col] = res[mid*(1+row//mid)-row%mid-1][col], res[row][col]
    return res

def not_mirror_sub(matrix, sub_1, sub_2):
    '''Меняет подматрицы местами
    matrix - исходная матрица
    sub_1, sub_2 - индексы элементов подматриц'''
    res = deepcopy(matrix) #копируем исходную матрицу
    for indx1, indx2 in zip(sub_1, sub_2):
        res[indx1[0]][indx1[1]], res[indx2[0]][indx2[1]] = res[indx2[0]][indx2[1]], res[indx1[0]][indx1[1]]
    return res
                

if __name__ == '__main__'    :
    #Ввод исходных данных
    K, N = (int(item) for item in input('Press values K and N: ').split())
    mid = N//2
    
    #Для удобства определяем переменные для хранения индексов элементов подматриц
    B = list((i, j) for j in range(mid) for i in range(mid))
    C = list((i, j) for j in range(mid, N) for i in range(mid))
    D = list((i, j) for j in range(mid) for i in range(mid,N))
    E = list((i, j) for j in range(mid,N) for i in range(mid,N))
    
    #Генерация и вывод матрицы A
    A = Matrix()
    A.generate(N)
    print('\nМатрица A:', A, sep='\n')
    
    #Проверка условий по заданию
    c1 = 0
    c2 = 1    
    for row, col in E:
        if check_area(2, row%mid, col%mid, mid) and (col%mid)%2 == 1 and A[row][col]>K:
            c1 += 1
        if check_area(4, row%mid, col%mid, mid) and (row%mid)%2 == 0:
            c2 *= A[row][col]
    print(f'\nВ Е количество чисел, больших К в четных столбцах в области 2 = {c1}')
    print(f'В Е произведение чисел в нечетных строках в области 4         = {c2}')

    #согласно условиям задания создаем матрицу F
    if c1>c2:
        F = mirror_area(A, C, 1, 4)
    else:
        F = not_mirror_sub(A, B, C)
        #for sub1_indx, sub2_indx in zip(sub_indx(B, N),sub_indx(C, N)):
        #    A[sub1_indx], A[sub2_indx] = A[sub2_indx], A[sub1_indx]

    print('\nМатрица F:', F, sep='\n')
    print('\nРезультат A*F: ', A*F, sep='\n')
    print('\nРезультат K*(A*F): ', K*(A*F), sep='\n')
    print('\nРезультат Ft: ', F.T() , sep='\n')
    print('\nРезультат K*Ft: ', K*F.T(), sep='\n')
    print('\nРезультат K*(A*F) + K*Ft: ', K*(A*F)+ K*F.T(), sep='\n')
