/*
Прочитать статью Андрея Александреску:
"Триумфальное возвращение Ломуто"

Оригинал:
https://dlang.org/blog/2020/05/14/lomutos-comeback/

Перевод:
https://habr.com/ru/post/512106/

Разобраться в версии разбиения Ломуто без ветвлений и
провести собственный эксперимент, сравнив эту версию,
обычное разбиение Ломуто и разбиение Хоара. (use C)
*/


#include <cassert>
#include <functional>
#include <iostream>
#include <chrono>
#include <vector>
#include <map>
#include <string>
#include <cmath>

using std::swap;


long *lomuto_partition_branchfree(long *first, long *last) {
//    assert(first <= last);
    if (last - first < 2)
        return first; // nothing interesting to do
    --last;
    if (*first > *last)
        swap(*first, *last);
    auto pivot_pos = first;
    auto pivot = *first;
    do {
        ++first;
//        assert(first <= last);
    } while (*first < pivot);
    for (auto read = first + 1; read < last; ++read) {
        auto x = *read;
        auto smaller = -int(x < pivot);
        auto delta = smaller & (read - first);
        first[delta] = *first;
        read[-delta] = x;
        first -= smaller;
    }
//    assert(*first >= pivot);
    --first;
    *pivot_pos = *first;
    *first = pivot;
    return first;
}

long *hoare_partition(long *first, long *last) {
//    assert(first <= last);
    if (last - first < 2)
        return first; // nothing interesting to do
    --last;
    if (*first > *last)
        swap(*first, *last);
    auto pivot_pos = first;
    auto pivot = *pivot_pos;
    for (;;) {
        ++first;
        auto f = *first;
        while (f < pivot)
            f = *++first;
        auto l = *last;
        while (pivot < l)
            l = *--last;
        if (first >= last)
            break;
        *first = l;
        *last = f;
        --last;
    }
    --first;
    swap(*first, *pivot_pos);
    return first;
}

long *lomuto_partition_naive(long *first, long *last) {
//    assert(first <= last);
    if (last - first < 2)
        return first; // nothing interesting to do
    auto pivot_pos = first;
    auto pivot = *first;
    ++first;
    for (auto read = first; read < last; ++read) {
        if (*read < pivot) {
            swap(*read, *first);
            ++first;
        }
    }
    --first;
    swap(*first, *pivot_pos);
    return first;
}

class bench {
private:
    std::map<std::string, std::function<long *(long *, long *)>> funcs;

public:
    // TODO ?
    template<typename Function>
    void add(std::string name, Function &&func) {
        funcs.insert(std::make_pair(name, func));
    }

    std::map<std::string, long long> run_all() {
        std::map<std::string, long long> out;
        long test_array[1 << 15];
        for (long &e: test_array) {
            e = rand();
        }
        for (auto &&func: funcs) {
            auto start = std::chrono::steady_clock::now();
            long *result = func.second(&test_array[0], &test_array[(1 << 15) - 1]);
            auto end = std::chrono::steady_clock::now();
            long long time = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
            out.insert(std::make_pair(func.first, time));
        }
        return out;
    }

};

int main() {
    bench test{};
    test.add("hoar", hoare_partition);
    test.add("lomuto", lomuto_partition_naive);
    test.add("better lomuto", lomuto_partition_branchfree);
    std::map<std::string, long long> sample_mean{{"hoar",          0},
                                                 {"lomuto",        0},
                                                 {"better lomuto", 0}};
    std::map<std::string, long long> geometric_mean{{"hoar",          1},
                                                    {"lomuto",        1},
                                                    {"better lomuto", 1}};

    int iterations = 5;
    for (int i = 0; i < iterations; i++) {
        std::map<std::string, long long> results = test.run_all();
        for (auto &e: results) {
            sample_mean[e.first] += e.second;
            geometric_mean[e.first] *= e.second;
        }
    }

    std::cout << "sample mean:" << std::endl;
    for (auto &mean: sample_mean) {
        std::cout << " " << mean.first << ": " << mean.second / iterations << std::endl;
    }

    std::cout << std::endl << "geometric mean:" << std::endl;
    for (auto &mean: geometric_mean) {
        std::cout << " " << mean.first << ": " << std::pow(mean.second, 1.0 / iterations) << std::endl;
    }
    return 0;
}
/*
по неясным мне причинам разбиение из статьи работает медленнее даже обычного ломуто (ну или я криво измеряю)
sample mean:
 better lomuto: 126
 hoar: 48
 lomuto: 122

geometric mean:
 better lomuto: 125.484
 hoar: 44.2055
 lomuto: 84.4247
 */