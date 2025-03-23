#include<stdio.h>
void main(){
    float a,b,c;
    char op;
    printf("enter two numbers with space :");
    scanf("%f%f",&a,&b);
    fflush(stdin); //used to flush numbers for entering operator
    printf("enter operator :");
    scanf("%c",&op);
    switch(op){
        case'+': 
        c=a+b;
        printf("Addition=%f",c);
        break;
        case'-':
        c=a-b;
        break;
        printf("Subtraction=%f",c);
        break;
        case'*':
        c=a*b;
        printf("Multiplication=%f",c);
        break;
        case'/':
        c=a/b;
        printf("division=%f",c);
        break;
        default:printf("invalid operator");
        break;
    }
}