#include <vector>
#include <tuple>
#include <iostream>

typedef struct {
    int key;
    int priority;
} TreapVal;

class TreapNode {

    TreapNode *parent = nullptr;
    TreapNode *left = nullptr;
    TreapNode *right = nullptr;
    TreapVal value;


    bool removeChild(TreapNode *node) {
        if (left == node) {
            left = nullptr;
            return true;
        }
        if (right == node) {
            right = nullptr;
            return true;
        }
        return false;
    }

    void fromSortedArray(const std::vector<TreapVal> &values, size_t id, TreapNode *previous) {
        if (id == values.size()) {
            return;
        }

        if (value.priority < values[id].priority && value.key < values[id].key) {
            right = new TreapNode(values[id], nullptr); // TODO setright
            right->parent = this;
            if (previous) {
                previous->parent->removeChild(previous);
                previous->parent = right;
                right->left = previous;
            }
            right->fromSortedArray(values, id + 1, nullptr);
        } else if (parent != nullptr) {
            parent->fromSortedArray(values, id, this);
        } else {
            parent = new TreapNode(values[id]);
            parent->left = this;
            parent->fromSortedArray(values, id + 1, nullptr);
        }


    }

public:
    TreapNode(const TreapVal &in_value) {
        value = in_value;
    }

    TreapNode(const TreapVal &in_value, TreapNode *in_parent) : TreapNode(in_value) {
        parent = in_parent;
    }

    TreapNode(const std::vector<TreapVal> &values) : TreapNode(values[0]) {
        fromSortedArray(values, 1, this);

    }

    ~TreapNode() {
        delete left;
        delete right;
    }

    TreapNode *getNoParents() {
        TreapNode *now = this;
        while (now->parent) {
            now = now->parent;
        }
        return now;
    }

    std::pair<TreapNode *, TreapNode *> split(int key) {
        if (key > this->value.key) {
            if (this->right != nullptr) {
                auto splt = right->split(key);
                this->right = splt.first;
                if (splt.first != nullptr) splt.first->parent = this;
                if (splt.second != nullptr) splt.second->parent = nullptr;
                return {this, splt.second};
            } else {
                return {this, nullptr};
            }
        } else {
            if (this->left != nullptr) {
                auto splt = left->split(key);
                this->left = splt.second;
                if (splt.first != nullptr) splt.first->parent = nullptr;
                if (splt.second != nullptr) splt.second->parent = this;
                return {splt.first, this};
            } else {
                return {nullptr, this};
            }
        }
    };

    TreapNode *merge(TreapNode *other) {
        if (other == nullptr) return this;

        if (this->value.priority < other->value.priority) {
            if (this->right != nullptr) {
                this->right = this->right->merge(other);
            } else {
                this->right = other;
            }
            this->right->parent = this;
            return this;
        } else {
            if (other->left != nullptr) {
                other->left = other->left->merge(this);
            } else {
                other->left = this;
            }
            other->left->parent = other;
            return other;

        }
    }

    TreapNode *insert(TreapVal in_val) {
        auto half = this->split(in_val.key);
        auto *new_node = new TreapNode(in_val);
        return half.second->merge(half.first->merge(new_node));
    }

    TreapNode *remove(int key) {
        auto half = this->split(key);
        TreapNode *root = half.second;
        if (half.second->left != nullptr)half.second = half.second->left->merge(half.second->right);
        else half.second = half.second->right;
        if (half.second != nullptr) half.second->parent = nullptr;
        delete root;
        return half.first->merge(half.second);
    }

    bool includes(int key) {
        auto pair = split(key);
        bool out = pair.second->value.key == key;
        pair.first->merge(pair.second);
        return out;
    }

};


int main() {
    int keys[8] = {8, 12, 14, 15, 18, 23, 24, 25};
    int values[8] = {10, 8, 14, 4, 9, 6, 15, 11};
    std::vector<TreapVal> aaa;

    for (int i = 0; i < 8; i++) {
        aaa.emplace_back(TreapVal{keys[i], values[i]});
    }

    auto *treap = (new TreapNode(aaa))->getNoParents();

    auto trps = treap->split(20);
    TreapNode *trp = trps.first->merge(trps.second);
    trp = trp->insert(TreapVal{20, 7});
    std::cout << trp->includes(20) << std::endl;
    trp = trp->remove(20);
    delete trp;
    return 0;
};