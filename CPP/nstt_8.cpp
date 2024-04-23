#include <string>
#include <stdexcept>
#include <iostream>
#include <fstream>
#include <utility>

class IO {
protected:
    virtual unsigned char read_byte() = 0;

    virtual void write_byte(unsigned char input) = 0;

    void throw_closed() {
        if (!is_open()) {
            throw std::runtime_error("Closed error");
        }
    }

    void throw_EOF() {
        if (is_EOF()) {
            throw std::runtime_error("EOF error");
        }
    }


public:

    virtual void open(char mode) = 0;

    virtual void close() = 0;

    virtual bool is_open() = 0;

    virtual bool is_EOF() = 0;
};

class Reader : virtual public IO {
public:
    template<typename T>
    T read_primitive() {
        throw_closed();
        uint size = sizeof(T);

        if (size == 1) {
            throw_EOF();
            return static_cast<T>(read_byte());
        }

        T out;
        auto *bytes_out = (unsigned char *) &out;

        for (uint i = 0; i < size; i++) {
            throw_EOF();
            bytes_out[i] = read_byte();
        }
        return out;
    }

    std::string read_string() {
        if (!is_open()) {
            throw std::runtime_error("Closed error");
        }
        std::string out;
        if (is_EOF()) {
            return out;
        }

        auto just_read = static_cast<char>(read_byte());
        while (just_read != '\0' && !is_EOF()) {
            out.push_back(just_read);
            just_read = static_cast<char>(read_byte());
        }
        if (just_read) {
            out.push_back(just_read);
        }

        return out;
    }

};

class Writer : virtual public IO {
public:
    template<typename T>
    void write_primitive(T input) {
        throw_closed();
        uint size = sizeof(T);

        if (size == 1) {
            write_byte(static_cast<unsigned char>(input));
            return;
        }

        auto *out = (unsigned char *) &input;
        for (uint i = 0; i < size; i++) {
            write_byte(out[i]);
        }


    }

    void write_string(std::string input) {
        if (input[input.length()-1]) {
            input.push_back('\0');
        }
        for (uint i = 0; i < input.length(); i++) {
            write_byte(static_cast<unsigned char>(input[i]));
        }
    }
};

class ReaderWriter : public Reader, public Writer {

};

class FileReaderWriter : public ReaderWriter {
    std::string filename;
    std::fstream file;
    char mode = 'n';


    void copy(FileReaderWriter const &other) {
        filename = other.filename;
        mode = 'n';
    }

    void move(FileReaderWriter &&other) {
        filename = other.filename;
        file = std::move(other.file);
        mode = other.mode;
        other.filename = nullptr;
        other.mode = 'n';
    }

protected:
    unsigned char read_byte() override {
        if (mode != 'r') {
            throw std::runtime_error("Mode should be set to 'r");
        }
        return static_cast<unsigned char>(file.get());
    }

    void write_byte(unsigned char input) override {
        if (mode != 'w') {
            throw std::runtime_error("Mode should be set to 'w");
        }
        file << input;
    }

public:
    explicit FileReaderWriter(std::string in_filename) {
        this->filename = std::move(in_filename);
    }

    FileReaderWriter(FileReaderWriter const &other) {
        copy(other);
    }

    FileReaderWriter(FileReaderWriter &&other) noexcept {
        move(std::move(other));
    }

    FileReaderWriter &operator=(FileReaderWriter const &other) {
        if (this == &other) {
            return *this;
        }
        copy(other);
        return *this;
    }

    FileReaderWriter &operator=(FileReaderWriter &&other) noexcept {
        if (this == &other) {
            return *this;
        }
        move(std::move(other));
        return *this;
    }


    void open(char in_mode) override {
        switch (in_mode) {
            case 'r':
                file.open(filename.c_str(), std::ios::in | std::ios::binary);
                break;
            case 'w':
                file.open(filename.c_str(), std::ios::out | std::ios::binary);
                break;
            default:
                throw std::runtime_error("Only 'w' or 'r' modes are allowed");
        }
        mode = in_mode;
    }

    void close() override {
        file.close();
        mode = 'n';
    }

    bool is_open() override {
        return file.is_open();
    }

    bool is_EOF() override {
        return file.eof();
    }

    char get_mode() const {
        return mode;
    }

};


class StringReaderWriter : public ReaderWriter {
    std::string *line;
    size_t pos;
    char mode = 'n';

    void copy(StringReaderWriter const &other) {
        line = other.line;
        mode = 'n';
        pos = 0;
    }

    void move(StringReaderWriter &&other) {
        line = other.line;
        mode = other.mode;
        pos = other.pos;

        other.line = nullptr;
        other.mode = 'n';
        other.pos = 0;
    }

protected:
    unsigned char read_byte() override {
        if (mode != 'r') {
            throw std::runtime_error("Mode should be set to 'r");
        }
        return static_cast<unsigned char>((*line)[pos++]);
    }

    void write_byte(unsigned char input) override {
        if (mode != 'w') {
            throw std::runtime_error("Mode should be set to 'w");
        }
        line->push_back(static_cast<char>(input));
    }

public:
    explicit StringReaderWriter(std::string *in_line) {
        line = in_line;
        mode = 'n';
        pos = 0;
    }

    StringReaderWriter(StringReaderWriter const &other) {
        copy(other);
    }

    StringReaderWriter(StringReaderWriter &&other) noexcept {
        move(std::move(other));
    }

    StringReaderWriter &operator=(StringReaderWriter const &other) {
        if (this == &other) {
            return *this;
        }
        copy(other);
        return *this;
    };

    StringReaderWriter &operator=(StringReaderWriter &&other) noexcept {
        if (this == &other) {
            return *this;
        }
        move(std::move(other));
        return *this;
    };

    void open(char in_mode) override {
        pos = 0;
        switch (in_mode) {
            case 'r':
                break;
            case 'w':
                *line = std::string();
                break;
            default:
                throw std::runtime_error("Only 'w' or 'r' modes are allowed");
        }
        mode = in_mode;
    }

    void close() override {
        mode = 'n';
    }

    bool is_open() override {
        return mode == 'r' || mode == 'w';
    }

    bool is_EOF() override {
        return mode != 'w' && pos == line->length();
    }

    char get_mode() const {
        return mode;
    }

};

template<class C, typename T>//base class and source datatype
class BufferReaderWriter : public C {
    unsigned char *buffer = nullptr;
    bool main_file_eof = false;
    int buffer_size;
    int read_into_buffer;
    int pos;

    void copy(BufferReaderWriter const &other) {
        buffer = new unsigned char[other.buffer_size];
        buffer_size = other.buffer_size;
        read_into_buffer = 0;
        pos = 0;
    }

    void move(BufferReaderWriter &&other) {
        buffer = other.buffer;
        buffer_size = other.buffer_size;
        read_into_buffer = other.read_into_buffer;
        pos = other.pos;

        other.buffer = nullptr;
        other.buffer_size = 0;
        other.pos = 0;
    }

    void read_to_buffer() {
        for (read_into_buffer = 0; read_into_buffer < buffer_size; read_into_buffer++) {
            if (C::is_EOF()) {
                main_file_eof = true;
                break;
            }
            buffer[read_into_buffer] = C::read_byte();
        }
        pos = 0;
    }

    void write_from_buffer() {
        for (int i = 0; i < pos; i++) {
            C::write_byte(buffer[i]);
        }
        pos = 0;
    }

public:
    explicit BufferReaderWriter(int size, T source) : C(source) {
        buffer = new unsigned char[size];
        buffer_size = size;
        read_into_buffer = 0;
        pos = 0;
    }

    BufferReaderWriter(BufferReaderWriter &other) : C(other) {
        copy(other);
    };

    BufferReaderWriter(BufferReaderWriter &&other) : C(std::move(other)) {
        move(std::move(other));
    }

    BufferReaderWriter &operator=(BufferReaderWriter const &other) {
        if (this == &other) {
            return *this;
        }

        delete buffer;

        copy(other);
        C::operator=(other);
        return *this;
    };

    BufferReaderWriter &operator=(BufferReaderWriter &&other) noexcept {
        if (this == &other) {
            return *this;
        }

        delete buffer;

        move(std::move(other));
        C::operator=(std::move(other));
        return *this;
    };

    ~BufferReaderWriter() {
        delete buffer;
    };

    unsigned char read_byte() override {
        if (pos == read_into_buffer) {
            read_to_buffer();
        }
        return buffer[pos++];
    }

    void write_byte(unsigned char input) override {
        if (pos == buffer_size) {
            write_from_buffer();
        }
        buffer[pos++] = input;
    }

    bool is_EOF() override {
        return main_file_eof && pos == read_into_buffer;
    }

    void close() override {
        if (C::get_mode() == 'w') {
            write_from_buffer();
        }

//        read_into_buffer = 0;
//        pos = 0;

        C::close();

    }
};

template
class BufferReaderWriter<FileReaderWriter, std::string>;

template
class BufferReaderWriter<StringReaderWriter, std::string *>;

using BufferFileReaderWriter = BufferReaderWriter<FileReaderWriter, std::string>;
using BufferStringReaderWriter = BufferReaderWriter<StringReaderWriter, std::string *>;