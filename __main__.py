#!/usr/bin/env python3
import sys
import os

# Thêm thư mục hiện tại vào path để import các module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import và chạy main từ cli
from dev_tool.cli import main

if __name__ == "__main__":
    main()