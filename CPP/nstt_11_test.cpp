#include "gtest/gtest.h"
#include "nstt_11.cpp"

TEST(lonley_test_suite, lonley_test_case) {

    const int primes[16] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53};

    const int test_primes[16] = {n_prime<1>::value, n_prime<2>::value, n_prime<3>::value, n_prime<4>::value,
                             n_prime<5>::value, n_prime<6>::value, n_prime<7>::value, n_prime<8>::value,
                             n_prime<9>::value, n_prime<10>::value, n_prime<11>::value, n_prime<12>::value,
                             n_prime<13>::value, n_prime<14>::value, n_prime<15>::value, n_prime<16>::value};

    for (int i = 0; i < 16; i++) {
        EXPECT_EQ(test_primes[i], primes[i]);
    }
}