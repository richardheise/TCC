#include "jngen.h"
using namespace std;

int main(int argc, char *argv[]) {
    // Tree t = Tree::random(50);
    // cout << t.add1().printN() << endl;

    cout << Graph::random(50, 100).connected() << endl;
}