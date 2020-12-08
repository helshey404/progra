
class Node:
    def __init__(self, contained_object, next_object=None):
        self.contained_object = contained_object
        self.next_object = next_object


class MyQueue:
    def __init__(self):
        self.head = None

    def add(self, obj):
        if self.head is None:
            self.head = Node(obj, None)
        else:
            new_obj = self.head
            while new_obj.next_object is not None:
                new_obj = new_obj.next_object
            new_obj.next_object = Node(new_obj, None)

    def remove(self, index_obj):
        if index_obj != 0:
            queue = Node(None, self.head)
            new_queue = queue
            next_queue = new_queue.next_object
            index_obj1 = 0
            while next_queue is not None:
                if index_obj == index_obj1:
                    new_queue.next_object = next_queue.next_object
                    next_queue.next_object = None
                index_obj1 += 1
                new_queue = next_queue
                next_queue = next_queue.next_object
        else:
            self.head = self.head.next_object

    def clear(self):
        self.__init__()

    def convert_array(self):
        queue_arr = []
        if self.head is not None:
            queue_head = self.head
            queue_arr.append(queue_head.contained_object)
            while queue_head.next_object is not None:
                queue_head = queue_head.next_object
                queue_arr.append(queue_head.contained_object)
            return queue_arr

    def __str__(self):
        if self.head is not None:
            temp_head = self.head
            print_queue = str(temp_head.contained_object) + '\n'
            while temp_head.next_object is not None:
                temp_head = temp_head.next_object
                print_queue += str(temp_head.contained_object) + '\n'
            return print_queue


class Country:

    def __init__(self, capital, population, currency):
        self._population = str(population)
        self._currency = str(currency)
        self._capital = str(capital)

    @property
    def capital(self):
        return self._capital

    @property
    def currency(self):
        return self._currency

    @property
    def population(self):
        return self._population

    def __str__(self):
        return 'Country( \n    Population: ' + str(
            self._population) + ',\n    Capital: ' + self._capital + ',\n    Local currency: ' + self._currency + '\n)\n'

    @population.setter
    def population(self, value):
        self._population = value

    @capital.setter
    def capital(self, value):
        self._capital = value

    @currency.setter
    def currency(self, value):
        self._currency = value


"""         TESTS           """

Russia = Country(Москва, 146630227, RUB)
USA = Country(Washington, 328239523, USD)
Polska = Country(Warszawa, 38382576, PLN)


queue = MyQueue()

for i in range(6):
    queue.add(2 ** i)

queue.remove(0)
print(queue.convert_array())


country_queue = MyQueue()
country_queue.add(Russia)
country_queue.add(USA)
country_queue.add(Polska)
print(country_queue)
