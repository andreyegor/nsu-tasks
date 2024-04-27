#include "tuple"
#include "iostream"

template<typename T>
class ScopedPointerFirst {
    T *pointer = nullptr;
public:
    explicit ScopedPointerFirst(T *inp) : pointer(inp) {}

    ScopedPointerFirst(const ScopedPointerFirst &other) : pointer(new T(*other.pointer)) {}

    ScopedPointerFirst &operator=(const ScopedPointerFirst &other) {
        if (this == &other) {
            return *this;
        }
        pointer = new T(*other.pointer);
        return *this;
    }

    ScopedPointerFirst(ScopedPointerFirst &&other) noexcept {
        std::swap(pointer, other.pointer);
    }

    ScopedPointerFirst &operator=(ScopedPointerFirst &&other) noexcept {
        if (this == &other) {
            return *this;
        }
        delete pointer;
        pointer = std::exchange(other.pointer, nullptr);
        return *this;
    }

    ~ScopedPointerFirst() {
        delete pointer;
    }

    T &operator*() {
        return *pointer;
    }

    const T &operator*() const {
        return *pointer;
    }

    T *operator->() {
        return pointer;
    }

    const T *operator->() const {
        return pointer;
    }

    bool operator==(ScopedPointerFirst other) const {
        return pointer == other.pointer;
    }

    T *get() {
        return pointer;
    }

};

template<typename T>
class ScopedPointerSecond : public ScopedPointerFirst<T> {
public:
    explicit ScopedPointerSecond(T *inp) : ScopedPointerFirst<T>(inp) {}

    ScopedPointerSecond(const ScopedPointerSecond &other) = delete;

    ScopedPointerSecond &operator=(const ScopedPointerSecond &other) = delete;

    ScopedPointerSecond(ScopedPointerSecond &&other) noexcept: ScopedPointerFirst<T>(std::move(other)) {}
};


struct Triple {
    int x;
    int y;
    int z;

    bool operator==(Triple &other) const {
        return x == other.x && y == other.y && z == other.z;
    }
};