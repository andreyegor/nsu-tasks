#include <vector>
#include <cassert>
#include <cstddef>

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
        delete left; // TODO a nuzna li proverka na nullptr? vrode kak net
        delete right;
    }

    TreapNode *getRoot() {//TODO vozmozno stoit ubrat v private
        TreapNode *now = this;
        while (now->parent) {
            now = now->parent;
        }
        return now;
    }

};

int main() {
    int keys[8] = {8, 12, 14, 15, 18, 23, 24, 25};
    int values[8] = {10, 8, 14, 4, 9, 6, 15, 11};
    std::vector<TreapVal> aaa;

    for (int i = 0; i < 8; i++) {
        aaa.emplace_back(TreapVal{keys[i], values[i]});
    }

    auto *treap = (new TreapNode(aaa))->getRoot();

    return 0;
};