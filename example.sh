#!/bin/bash
# Face Finder - 使用範例

echo "=================================="
echo "Face Finder - 使用範例"
echo "=================================="
echo ""

# 檢查是否有參考圖片和資料夾
if [ $# -lt 2 ]; then
    echo "用法: ./example.sh <參考圖片> <圖片資料夾>"
    echo ""
    echo "範例:"
    echo "  ./example.sh reference.jpg photos/"
    echo ""
    exit 1
fi

REFERENCE=$1
FOLDER=$2

# 檢查檔案是否存在
if [ ! -f "$REFERENCE" ]; then
    echo "❌ 錯誤: 找不到參考圖片 '$REFERENCE'"
    exit 1
fi

if [ ! -d "$FOLDER" ]; then
    echo "❌ 錯誤: 找不到資料夾 '$FOLDER'"
    exit 1
fi

echo "📷 參考圖片: $REFERENCE"
echo "📁 搜尋資料夾: $FOLDER"
echo ""
echo "開始處理..."
echo ""

# 執行 Face Finder
python3 find_faces.py "$REFERENCE" "$FOLDER" -o output/

echo ""
echo "✅ 完成！請查看 output/ 資料夾"
