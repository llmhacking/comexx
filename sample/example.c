#include <stdio.h>
#include <stdlib.h>

// 定义链表节点结构体
typedef struct Node {
    int value;
    struct Node *next;
} Node;

// 动态分配一个新节点，测试内存分配和指针操作的DFG
Node* create_node(int value) {
    Node *node = (Node*) malloc(sizeof(Node));
    if (!node) {
        fprintf(stderr, "内存分配失败\n");
        exit(EXIT_FAILURE);
    }
    node->value = value;
    node->next = NULL;
    return node;
}

// 将新节点追加到链表尾部
void append_node(Node **head, int value) {
    Node *new_node = create_node(value);
    if (*head == NULL) {
        *head = new_node;
    } else {
        Node *current = *head;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = new_node;
    }
}

// 递归计算Fibonacci数列，用于测试AST和CFG的递归调用分支
int fibonacci(int n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

// 使用递归打印数字，增加控制流复杂度
void recursive_print(int n) {
    if (n <= 0)
        return;
    printf("%d ", n);
    recursive_print(n - 1);
}

int main() {
    // 1. 简单的算术运算与条件分支 (AST和CFG示例)
    int a = 10, b = 20, max = 0;
    if (a > b) {
        max = a;
    } else {
        max = b;
    }
    printf("较大的数字是: %d\n", max);

    // 2. 循环与数组操作 (AST, CFG, DFG示例)
    int arr[5] = {1, 2, 3, 4, 5};
    int sum = 0;
    for (int i = 0; i < 5; i++) {
        sum += arr[i];
    }
    printf("数组的和为: %d\n", sum);

    // 3. 指针与链表操作 (DFG示例)
    Node *head = NULL;
    for (int i = 0; i < 5; i++) {
        append_node(&head, i * 10);
    }
    printf("链表节点值: ");
    Node *current = head;
    while (current != NULL) {
        printf("%d ", current->value);
        current = current->next;
    }
    printf("\n");

    // 4. 使用递归函数计算Fibonacci (AST与CFG示例)
    int fib = fibonacci(6);
    printf("Fibonacci(6) = %d\n", fib);

    // 5. 递归打印 (增加CFG复杂度)
    printf("递归打印: ");
    recursive_print(5);
    printf("\n");

    // 清理链表内存
    current = head;
    while (current != NULL) {
        Node *temp = current;
        current = current->next;
        free(temp);
    }

    return 0;
}