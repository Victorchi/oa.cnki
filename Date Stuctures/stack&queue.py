# coding:utf8
# Author:Victor Chi

class StackUnderflow(ValueError):  # 栈下溢 (空栈访问)
    pass


class SStack():
    '''
    基于顺序表技术实现的栈类
    用list对象 _elems存储栈中的元素
    所有栈的操作映射到list操作
    '''
    def __init__(self):
        self._elems = []

    def is_empty(self):
        return self._elems == []

    def top(self):
        if self._elems == []:
            raise StackUnderflow('in SStack.top()')
        return self._elems[-1]

    def push(self, elem):
        self._elems.append(elem)

    def pop(self):
        if self._elems == []:
            raise StackUnderflow('in SStack.pop()')
        return self._elems.pop()

if __name__ == '__main__':

    st1 = SStack()
    st1.push(1)
    st1.push(2)
    while not st1.is_empty():
        print(st1.pop())