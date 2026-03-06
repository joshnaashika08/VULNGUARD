import re

class LanguageDetector:
    def __init__(self):
        # Weighted keywords for detection
        self.keywords = {
            "python": {
                "keywords": ["def ", "import ", "from ", "class ", "print(", "if __name__ == \"__main__\":"],
                "weight": 0
            },
            "c": {
                "keywords": ["#include <stdio.h>", "int main(", "printf(", "#include <stdlib.h>", "void "],
                "weight": 0
            },
            "cpp": {
                "keywords": ["#include <iostream>", "using namespace std;", "std::cout", "int main(", "class ", "public:"],
                "weight": 0
            },
            "java": {
                "keywords": ["public class ", "public static void main", "System.out.println", "import java.", "package "],
                "weight": 0
            }
        }

    def detect(self, code):
        """
        Detects the programming language of the provided code snippet.
        Returns 'python', 'c', 'cpp', 'java', or 'unknown'.
        """
        code = code.strip()
        scores: dict[str, int] = {lang: 0 for lang in self.keywords}

        # Check for specific signatures first (strong indicators)
        if "public static void main" in code or "System.out.println" in code:
            scores["java"] += 10
        if "#include <iostream>" in code or "std::" in code:
            scores["cpp"] += 10
        if "def " in code and ":" in code and "import " in code:
            scores["python"] += 10
        
        # Keyword counting
        for lang, data in self.keywords.items():
            keywords = data.get("keywords")
            if isinstance(keywords, list):
                for keyword in keywords:
                    if keyword in code:
                        scores[lang] += 1

        # Heuristics for C vs C++
        if scores["c"] > 0 and scores["cpp"] > 0:
            # If it has classes or namespaces, it's likely C++
            if "class " in code or "namespace " in code or "std::" in code:
                return "cpp"
            
        # Return the language with the highest score
        best_lang = max(scores, key=lambda k: scores[k])
        
        if scores[best_lang] == 0:
            return "unknown"
            
        return best_lang
