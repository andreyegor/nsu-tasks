#include <algorithm>
#include <stdexcept>
#include "gtest/gtest.h"

class Matrix {
    double **matrix;
    int size{};

    double **new_matrix(int this_size) {
        auto this_matrix = new double *[this_size];
        for (int i = 0; i < this_size; i++) {
            this_matrix[i] = new double[this_size]{0.};
        }
        return this_matrix;
    }

    double **copy_matrix(double **this_matrix, int this_size) {
        double **out = new_matrix(this_size);
        for (int i = 0; i < this_size; i++) {
            for (int j = 0; j < this_size; j++) {
                out[i][j] = this_matrix[i][j];
            }
        }
        return out;
    }

    void delete_matrix(double **this_matrix, int this_size) {
        for (int i = 0; i < this_size; i++) {
            delete[] this_matrix[i];
        }
        delete[] this_matrix;
    }

    double **add_matrix_first(double **first, double **other, int this_size) {//change first
        for (int i = 0; i < this_size; i++) {
            for (int j = 0; j < this_size; j++) {
                first[i][j] += other[i][j];
            }
        }
        return first;
    }

    double **add_scal_first(double **first, double scal, int this_size) {//change first
        for (int i = 0; i < this_size; i++) {
            for (int j = 0; j < this_size; j++) {
                first[i][j] += scal;
            }
        }
        return first;
    }

    double **mul_matrix_new(double **first, double **other, int this_size) {//return new
        double **out = new_matrix(this_size);
        for (int i = 0; i < this_size; i++) {
            for (int j = 0; j < this_size; j++) {
                for (int k = 0; k < this_size; k++) {
                    out[i][j] += first[i][k] * other[k][j];
                }
            }
        }
        return out;
    }

    double **mul_scal_first(double **first, double scal, int this_size) {//change first
        for (int i = 0; i < this_size; i++) {
            for (int j = 0; j < this_size; j++) {
                first[i][j] *= scal;
            }
        }
        return first;
    }

public:
    explicit Matrix(int size) {
        this->matrix = new_matrix(size);
        this->size = size;
    }

    Matrix(std::initializer_list<std::initializer_list<double>> this_list, int this_size) {
        matrix = new_matrix(this_size);
        auto this_matrix = this_list.begin();
        for (int i = 0; i < this_size; i++) {
            auto this_line = this_matrix[i].begin();
            for (int j = 0; j < this_size; j++) {
                matrix[i][j] = this_line[j];
            }
        }
        size = this_size;
    }

    Matrix(double **this_matrix, int this_size) {
        matrix = this_matrix;
        size = this_size;
    }

    explicit Matrix(std::vector<double> diag) {
        matrix = new_matrix(diag.size());
        size = diag.size();
        for (int i = 0; i < size; i++) {
            matrix[i][i] = diag[i];
        }
    }

    Matrix(const Matrix &matrix) {
        this->matrix = copy_matrix(matrix.matrix, matrix.size);
        this->size = matrix.size;
    }

    Matrix(Matrix &&matrix) noexcept {
        std::swap(this->matrix, matrix.matrix);
        std::swap(this->size, matrix.size);
    }

    Matrix &operator=(const Matrix &other) {
        this->matrix = copy_matrix(other.matrix, other.size);
        this->size = other.size;
        return *this;
    }

    Matrix &operator=(Matrix &&other) noexcept {
        std::swap(this->matrix, other.matrix);
        std::swap(this->size, other.size);
        return *this;
    }

    Matrix operator+(const Matrix &other) {
        if (size != other.size) {
            throw std::range_error("Matrices are different sizes");
        }
        Matrix out{*this};
        add_matrix_first(out.matrix, other.matrix, size);
        return out;
    }

    const Matrix &operator+(const Matrix &other) const {};

    Matrix &operator+=(const Matrix &other) {
        if (size != other.size) {
            throw std::range_error("Matrices are different sizes");
        }
        add_matrix_first(this->matrix, other.matrix, size);
        return *this;
    }

    Matrix operator*(const Matrix &other) {
        if (size != other.size) {
            throw std::range_error("Matrices are different sizes");
        }
        Matrix out{mul_matrix_new(this->matrix, other.matrix, size), size};
        return out;
    }

    Matrix &operator*=(const Matrix &other) {
        if (size != other.size) {
            throw std::range_error("Matrices are different sizes");
        }
        auto result = mul_matrix_new(this->matrix, other.matrix, size);
        delete_matrix(matrix, size);
        matrix = result;
        return *this;
    }

    Matrix operator+(const double &scal) {
        Matrix out{*this};
        add_scal_first(out.matrix, scal, size);
        return out;
    }

    Matrix &operator+=(double scal) {
        add_scal_first(this->matrix, scal, size);
        return *this;
    }

    Matrix operator*(double scal) {
        Matrix out{*this};
        mul_scal_first(out.matrix, scal, size);
        return out;
    }

    Matrix &operator*=(double scal) {
        mul_scal_first(this->matrix, scal, size);
        return *this;
    }

    ~Matrix() {
        delete_matrix(matrix, size);
    }

    bool operator==(Matrix &other) {
        if (size != other.size) {
            return false;
        }
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if (matrix[i][j] != other.matrix[i][j]) {
                    return false;
                }
            }
        }
        return true;
    }

    bool operator!=(Matrix &other) {
        return not(*this == other);
    }

    double *operator[](int index) {
        return matrix[index];
    }

    explicit  operator double() const {
        double out;
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                out += matrix[i][j];
            }
        }
        return out;
    }

};


TEST(FirstCase, from_vector) {
    Matrix first{std::vector<double>{1, 2}};
    Matrix second{{{1., 0.}, {0., 2.}}, 2};
    EXPECT_TRUE(first == second);
};

TEST(SecondCase, conversion_to_double) {
    Matrix first{{{1., 0.}, {0., 2.}}, 2};
    EXPECT_TRUE((double) first == 3.);
}

TEST(ThirdCase, Overloaded_operators_add) {
    Matrix first{{{1., 1.}, {2., 0.}}, 2};
    Matrix second{{{0., 1.}, {1., 4.}}, 2};
    Matrix expected{{{1., 2.}, {3., 4.}}, 2};

    EXPECT_TRUE(first + second == expected);
    second += first;
    EXPECT_TRUE(second == expected);

    Matrix expected_scalar{{{2., 2.}, {3., 1.}}, 2};
    EXPECT_TRUE(first + 1. == expected_scalar);
    first += 1.;
    EXPECT_TRUE(first == expected_scalar);
}

TEST(ThirdCase, Overloaded_operators_mul) {
    Matrix first{{{1, 2}, {3, 4}}, 2};
    Matrix second{{{5, 6}, {7, 8}}, 2};
    Matrix expected{{{19, 22}, {43, 50}}, 2};

    EXPECT_TRUE(first * second == expected);
    first *= second;
    EXPECT_TRUE(first == expected);

    Matrix expected_scalar{{{10, 12}, {14, 16}}, 2};
    EXPECT_TRUE(second * 2 == expected_scalar);
    second *= 2;
    EXPECT_TRUE(second == expected_scalar);
}

TEST(FourthCase, double_indexing) {
    Matrix first{{{1, 2}, {3, 4}}, 2};
    EXPECT_TRUE(first[0][0]==1);
    EXPECT_TRUE(first[0][1]==2);
    EXPECT_TRUE(first[1][0]==3);
    EXPECT_TRUE(first[1][1]==4);
}