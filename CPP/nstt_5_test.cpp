#include "gtest/gtest.h"
#include "nstt_5.cpp"



TEST(ScopePointerFirst, deep_copyng) {
    ScopedPointerFirst sp1{new Triple{13, 42, 1}};
    ScopedPointerFirst sp2 = sp1;
    sp2->x = 42;
    EXPECT_FALSE(sp1 == sp2);
}

TEST(ScopePointerFirst, transferring_an_ownership) {
    ScopedPointerFirst sp1{new Triple{13, 42, 1}};
    ScopedPointerFirst sp2 = std::move(sp1);
    EXPECT_TRUE(sp1.get() == nullptr);
}

TEST(ScopePointerSecond, transferring_an_ownership) {
    ScopedPointerSecond sp1{new Triple{13, 42, 1}};
    ScopedPointerSecond sp2 = std::move(sp1);
    std::cout<<sp1.get()<<std::endl;
    EXPECT_TRUE(sp1.get() == nullptr);
}