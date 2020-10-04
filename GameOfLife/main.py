max_x = 1920
max_y = 1080


class Field():
    def __init__(self, array):
        self.__field = array

    def change_field(self, array):
        self.__field = array

    def get_field(self):
        return self.__field


def move(field):
    field_array = field.get_field()
    new_field_array = []
    for i in range(len(field_array)):
        new_field_array.append([])
        for j in range(len(field_array[i])):
            new_field_array[i].append(field_array[i][j])
    return new_field_array


arr = [[1, 2, 3], [1, 2, 3]]
a = Field(arr)
print(move(a))

if __name__ == '__main__':
    print(1)
