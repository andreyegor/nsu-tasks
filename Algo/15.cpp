#include <cstdlib>
#include <stdexcept>
#include <cassert>
#include <iostream>

template<typename type>
class DArray {
    size_t size = sizeof(type);
    type *just_an_array_itself;

    const unsigned long int DEFAULT_CAP = 1;
    unsigned long int length;
    unsigned long int capacity;

public:
    DArray() {
        just_an_array_itself = (type *) std::malloc(size * DEFAULT_CAP);
        if (just_an_array_itself == nullptr)
            throw std::bad_alloc();
        capacity = DEFAULT_CAP;
        length = 0;
    }

    ~DArray() {
        std::free(just_an_array_itself);
    }

    unsigned long int getLen() {
        return length;
    }

    type operator[](unsigned long int index) {
        if (index < length)
            return just_an_array_itself[index];
        else
            throw std::out_of_range("Index is out of range");
    }

    void add(type value) {
        just_an_array_itself[length] = value;
        if (capacity == ++length) {
            capacity *= 2;
            void *not_a_list_itself = realloc(just_an_array_itself, capacity * size);

            if (not_a_list_itself == nullptr)
                throw std::bad_alloc();
            just_an_array_itself = (type *) not_a_list_itself;
        }
    }

    type pop() {
        if (length == 0) {
            throw std::out_of_range("Index is out of range");
        }
        length--;

        if (length * 3 <= capacity && length >= DEFAULT_CAP) {
            capacity = length;
            just_an_array_itself = (type *) realloc(just_an_array_itself, capacity * size);

            if (just_an_array_itself == nullptr)
                throw std::bad_alloc();
        }
    }

};


int main() {
    DArray<int> arr;
    for (int i = 0; i < 30; i++) {
        arr.add(i);
    }

    for (int i = 0; i < 30; i++) {
        assert(arr[i] == i);
    }

    for (int i = 29; i >= 0; i--) {
        arr.pop();
        assert(arr.getLen() == i);
    }

    try {
        arr.pop();
    } catch (const std::out_of_range &out) {
        std::cout << out.what() << std::endl;
    }

    try {
        arr[0];
    } catch (const std::out_of_range &out) {
        std::cout << out.what() << std::endl;
    }


}