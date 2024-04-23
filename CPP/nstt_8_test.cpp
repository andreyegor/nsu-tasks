#include "gtest/gtest.h"
#include "nstt_8.cpp"

void test_RW(ReaderWriter &file) {
    file.open('w');
    file.write_primitive<int>(123);
    file.write_primitive<bool>(true);
    file.write_primitive<float>(-1.0);
    file.write_primitive<int>(42);
    file.write_primitive<int>(24);
    file.write_string("first_string");
    file.write_string("second_string");
    file.write_primitive<int>(1);
    EXPECT_FALSE(file.is_EOF());
    file.close();

    file.open('r');
    EXPECT_EQ(file.read_primitive<int>(), 123);
    EXPECT_EQ(file.read_primitive<bool>(), true);
    EXPECT_EQ(file.read_primitive<float>(), -1.0);
    EXPECT_EQ(file.read_primitive<int>(), 42);
    EXPECT_EQ(file.read_primitive<int>(), 24);
    EXPECT_EQ(file.read_string(), "first_string");
    EXPECT_EQ(file.read_string(), "second_string");
    EXPECT_EQ(file.read_primitive<int>(), 1);
    file.close();
}

TEST(nstt_8, BufferStringReaderWriter) {
    std::string string;
    auto file = BufferStringReaderWriter(16, &string);
    test_RW(file);
}

TEST(nstt_8, BufferFileReaderWriter) {
    auto file = BufferFileReaderWriter(16, "aboba");
    test_RW(file);
}

TEST(nstt_8, StringReaderWriter) {
    std::string string;
    auto file = StringReaderWriter(&string);
    test_RW(file);
}

TEST(nstt_8, FileReaderWriter) {
    auto file = FileReaderWriter("aboba");
    test_RW(file);
}

//"{\000\000\000\001\000\000\200\277*\000\000\000\030\000\000\000first_string\000second_string\000\001\000\000"
//"{\000\000\000\001\000\000\200\277*\000\000\000\030\000\000\000first_string\000second_string\000\001\000\000"