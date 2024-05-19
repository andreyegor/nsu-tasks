template<typename Checker, typename... Args>
int getIndexOfFirstMatch(Checker check, Args... args) {
    int i = 0;
    int ans = -1;
    ([&] {
        if (check(args)) {
            ans = i;
            return true;
        }
        i++;
        return false;
    }()|| ...);
    return ans;
}