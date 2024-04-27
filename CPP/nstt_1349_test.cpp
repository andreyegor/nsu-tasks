#include "gtest/gtest.h"
#include "nstt_1349.cpp"

const int DEMO_TEST_KEYS[8] = {15, 18, 14, 8, 23, 12, 25, 24};
const int DEMO_TEST_VALUES[8] = {10, 8, 14, 4, 9, 6, 15, 11};

AvlTree<int, int> get_test_data() {
    AvlTree<int, int> tree;

    for (int i = 0; i < 8; i++) {
        tree.insert(DEMO_TEST_KEYS[i], DEMO_TEST_VALUES[i]);
    }

    return tree;
}

TEST(base, create_peek_test) {
    AvlTree<int, int> tree = get_test_data();

    for (int i = 7; i >= 0; i--) {
        EXPECT_EQ(tree.peek(DEMO_TEST_KEYS[i]), DEMO_TEST_VALUES[i]);
    }
}

TEST(base, extract_test) {
    AvlTree<int, int> tree = get_test_data();

    for (int i = 0; i < 8; i += 2) {
        EXPECT_EQ(tree.extract(DEMO_TEST_KEYS[i]), DEMO_TEST_VALUES[i]);
    }
    for (int i = 1; i < 8; i += 2) {
        EXPECT_EQ(tree.peek(DEMO_TEST_KEYS[i]), DEMO_TEST_VALUES[i]);
    }
}

TEST(copy, copy_test) {
    AvlTree<int, int> tree = get_test_data();
    auto other = tree;
    for (int i = 0; i < 8; i += 1) {
        EXPECT_EQ(tree.extract(DEMO_TEST_KEYS[i]), DEMO_TEST_VALUES[i]);
    }

    for (int i = 7; i >= 0; i--) {
        EXPECT_EQ(other.peek(DEMO_TEST_KEYS[i]), DEMO_TEST_VALUES[i]);
    }
}

TEST(move, move_test) {
    AvlTree<int, int> tree = get_test_data();
    auto other = std::move(tree);
    for (int i = 0; i < 8; i += 1) {
        EXPECT_THROW({
                         try { tree.extract(DEMO_TEST_KEYS[i]); } catch (const std::runtime_error &msg) {
                             EXPECT_STREQ(msg.what(), "This tree does not contain the key you are looking for");
                             throw;
                         }
                     }, std::runtime_error);
    }

    for (int i = 7; i >= 0; i--) {
        EXPECT_EQ(other.peek(DEMO_TEST_KEYS[i]), DEMO_TEST_VALUES[i]);
    }
}
