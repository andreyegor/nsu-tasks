#include <type_traits>
#include <iostream>

template<int a, int b = a - 1>
struct is_prime : std::conditional<
        b == 1, std::true_type,
        std::conditional<static_cast<bool>(a % b), is_prime<a, b - 1>, std::false_type>>::type::type {
};

template<int n, int now = 1>
struct n_prime : std::conditional<
        n == 0, std::integral_constant<int, now>, std::conditional<is_prime<now + 1>::value, n_prime<
                n - 1, now + 1>, n_prime<n, now + 1>>>::type::type {
};
