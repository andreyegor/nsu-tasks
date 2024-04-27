#include <algorithm>
#include <stdexcept>
#include <vector>

class Matrix {
    class ReturnableLine {
        double *line;
        int line_size;
    public:
        ReturnableLine(double *in_line, int in_line_size) : line(in_line), line_size(in_line_size) {

        }

        ReturnableLine(const ReturnableLine &other) = delete;

        double operator[](int index) {
            if (0 <= index && index < line_size) {
                return line[index];
            } else {
                throw std::out_of_range("Index is out of range");
            }
        }

    };

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
        this->matrix = std::exchange(matrix.matrix, nullptr);
        this->size = std::exchange(matrix.size, 0);
    }

    Matrix &operator=(const Matrix &other) {
        if (this == &other) {
            return *this;
        }
        this->matrix = copy_matrix(other.matrix, other.size);
        this->size = other.size;
        return *this;
    }

    Matrix &operator=(Matrix &&other) noexcept {
        if (this == &other) {
            return *this;
        }
        delete this->matrix;
        this->matrix = std::exchange(other.matrix, nullptr);
        this->size = std::exchange(other.size, 0);
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
            throw std::runtime_error("Matrices are different sizes");
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

    friend Matrix operator+(double scal, Matrix &other) {
        return other + scal;
    }

    friend Matrix operator*(double scal, Matrix &other) {
        return other * scal;
    }


    ~Matrix() {
        delete_matrix(matrix, size);
    }

    bool operator==(const Matrix &other) {
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

    ReturnableLine operator[](int index) {
        if (0 <= index && index < size) {
            return {matrix[index], size};
        } else {
            throw std::out_of_range("Index is out of range");
        }
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


