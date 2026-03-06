#include <stdio.h>
#include <string.h>

int main() {
    char buffer[10];
    char *input = "This is a very long string that will cause a buffer overflow";
    
    // Vulnerability: Buffer Overflow
    strcpy(buffer, input);
    
    // Vulnerability: Format String
    printf(input);
    
    return 0;
}
