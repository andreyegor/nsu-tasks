#include <utility>
#include <stdexcept>

template<typename KeyT, typename ValT>
class AvlTree {
    class Node {
        void copy(Node &other) {//copy other node and tree under
            left = other.left ? new Node(*other.left) : nullptr;
            right = other.right ? new Node(*other.right) : nullptr;

            key = other.key;
            val = other.val;
            height = other.height;
        }

        void move(Node &&other) {//move other node and tree under to this position and not change parent
            left = std::exchange(other.left, nullptr);
            right = std::exchange(other.right, nullptr);

            val = std::move(other.val);// there are no default value for val and key
            key = std::move(other.key);
            height = std::exchange(other.height, 0);

        }

    public:
        KeyT key;
        ValT val;
        int height = 1;

        Node *parent = nullptr;
        Node *left = nullptr;
        Node *right = nullptr;

        Node(KeyT key_in, ValT val_in, Node *parent_in = nullptr) : key(key_in), val(val_in), parent(parent_in) {}

        Node(Node &other) {
            copy(other);
        }

        Node(Node &&other) noexcept {
            move(std::move(other));
        }

        Node &operator=(Node const &other) {
            if (this == &other) {
                return *this;
            }
            left = nullptr;
            right = nullptr;
            parent = nullptr;

            copy(other);
            return *this;
        }

        Node &operator=(Node &&other) noexcept {
            if (this == &other) {
                return *this;
            }
            left = nullptr;
            right = nullptr;

            move(std::move(other));
            return *this;
        }

        ~Node() {
            delete left;
            delete right;
        }
    };

    Node *root = nullptr;

    void update_height(Node *now) {
        now->height = (now->right ? now->right->height : 0) + (now->left ? now->left->height : 0) + 1;
    }

    int diff(Node *now) {
        return (now->right ? now->right->height : 0) - (now->left ? now->left->height : 0);
    }

    template<bool IS_RIGHT>
    Node *rotation(Node *now) {
        Node *new_now = (IS_RIGHT ? now->left : now->right);

        new_now->parent = now->parent;
        now->parent = new_now;

        (IS_RIGHT ? now->left : now->right) = (IS_RIGHT ? new_now->right : new_now->left);
        (IS_RIGHT ? new_now->right : new_now->left) = now;

        if (IS_RIGHT ? now->left : now->right) {
            (IS_RIGHT ? now->left->parent : now->right->parent) = now;
        }
        update_height(now);
        update_height(new_now);

        if (!new_now->parent) {
            root = new_now;
        } else if ((IS_RIGHT ? new_now->parent->right : new_now->parent->left) == now) {
            (IS_RIGHT ? new_now->parent->right : new_now->parent->left) = new_now;
        } else {
            (IS_RIGHT ? new_now->parent->left : new_now->parent->right) = new_now;
        }

        return new_now;
    }

    Node *sr_rotation(Node *now) {
        return rotation<true>(now);
    }

    Node *sl_rotation(Node *now) {
        return rotation<false>(now);
    }

    Node *bl_rotation(Node *now) {
        sr_rotation(now->right);
        return sl_rotation(now);
    }

    Node *br_rotation(Node *now) {
        sl_rotation(now->left);
        return sr_rotation(now);
    }

    void balance(Node *now, bool only_sr = false) {
        while (true) {
            update_height(now);
            int df = diff(now);
            if (df == -2) {
                if (!only_sr && now->left && diff(now->left) == 1) {
                    now = br_rotation(now);
                } else {
                    now = sr_rotation(now);
                }
            } else if (df == 2) {
                if (!only_sr && now->right and diff(now->right) == -1) {
                    now = bl_rotation(now);
                } else {
                    now = sl_rotation(now);
                }
            }
            if (now->parent) {
                now = now->parent;
                continue;
            }
            break;
        }
    }

    Node *local_min(Node *now) {
        while (now->left) {
            now = now->left;
        }
        return now;
    }

    Node *peek_node(KeyT key) {
        Node *now = root;
        while (now and now->key != key) {
            if (now->key < key) {
                now = now->right;
                continue;
            }
            now = now->left;
        }
        return now;
    }

    void kill_child(Node *child) {
        if (!(child->left || child->right || child->parent)) {
            return;
        }
        if (child->left and child->right) {
            throw std::runtime_error("Too many alive grandsons");
        }
        Node *alive_grandson = child->left ? child->left : child->right;
        if (alive_grandson) {
            *child = std::move(*alive_grandson);
            delete alive_grandson;
            return;
        } else if (child->parent->left == child) {
            child->parent->left = nullptr;
        } else if (child->parent->right == child) {
            child->parent->right = nullptr;
        } else if (child == root) {
            root = nullptr;
        } else {
            throw std::runtime_error("Something went wrong");
        }
        delete child;
    }

public:
    AvlTree() = default;

    AvlTree(AvlTree &other) {
        root = new Node(*other.root);
    }

    AvlTree(AvlTree &&other) noexcept {
        root = std::exchange(other.root, nullptr);
    }

    AvlTree &operator=(AvlTree const &other) {
        if (this == &other) {
            return *this;
        }
        delete root;
        root = new Node(*other.root);
        return *this;
    }

    AvlTree &operator=(AvlTree &&other) noexcept {
        if (this == &other) {
            return *this;
        }
        delete root;
        root = std::exchange(other.root, nullptr);
        return *this;
    }

    ~AvlTree() {
        delete root;
    }

    void insert(KeyT key, ValT val) {
        if (!root) {
            root = new Node(key, val);
            return;
        }

        Node *now = root;
        while (true) {
            if (now->key < key) {
                if (!now->right) {
                    now->right = new Node(key, val, now);
                    break;
                }
                now = now->right;
            } else if (now->key > key) {
                if (!now->left) {
                    now->left = new Node(key, val, now);
                    break;
                }
                now = now->left;
            } else {
                throw std::runtime_error("This key is already in tree");
            }
        }
        balance(now, true);
    }

    ValT peek(KeyT key) {
        Node *res = peek_node(key);
        if (res) {
            return res->val;
        }
        throw std::runtime_error("This tree does not contain the key you are looking for");
    }

    ValT extract(KeyT key) {
        Node *extractable = peek_node(key);
        if (!extractable) {
            throw std::runtime_error("This tree does not contain the key you are looking for");
        }
        ValT out = extractable->val;
        if (extractable->left && extractable->right) {
            Node *swap = local_min(extractable->right);
            std::swap(swap->key, extractable->key);
            std::swap(swap->val, extractable->val);
            Node *balance_node = swap->parent;
            kill_child(swap);
            balance(balance_node);
            if (root == swap) {
                root = extractable;
            }
        } else if (root == extractable) {
            root = extractable->left ? extractable->left : extractable->right;
            kill_child(extractable);
        } else {
            Node *balance_node = extractable->parent;
            kill_child(extractable);
            balance(balance_node);
        }
        return out;
    }
};