# Face Finder

一個基於深度學習的人臉識別工具，可以從大量圖片中自動找出並裁剪特定人物的臉部照片。

## ✨ 特色功能

- 🎯 **高準確度**：使用 InsightFace 深度學習模型進行人臉識別
- 🚀 **簡單易用**：一行指令即可完成批次處理
- 📦 **自動裁剪**：智能裁剪人臉區域，可調整邊界框大小
- 🔧 **彈性設定**：可調整相似度閾值和裁剪範圍
- 📁 **批次處理**：支援處理整個資料夾的圖片

## 🚀 快速開始

### 安裝依賴

```bash
pip3 install -r requirements.txt
```

### 基本使用

1. **準備參考人臉圖片**：選擇一張包含目標人物臉部的清晰照片
2. **執行搜尋**：

```bash
python3 find_faces.py reference.jpg photos/
```

就這麼簡單！程式會自動：
- 載入深度學習模型
- 從 `photos/` 資料夾中的所有圖片搜尋匹配的人臉
- 將找到的人臉裁剪並儲存到 `output/` 資料夾

### 完整範例

```bash
# 基本使用
python3 find_faces.py my_face.jpg photos/

# 指定輸出資料夾
python3 find_faces.py my_face.jpg photos/ -o results/person1/

# 調整相似度閾值（更嚴格的匹配）
python3 find_faces.py my_face.jpg photos/ -t 0.45

# 調整裁剪範圍（2.5 倍臉部大小）
python3 find_faces.py my_face.jpg photos/ -s 2.5

# 組合使用
python3 find_faces.py my_face.jpg photos/ -o output/ -t 0.42 -s 2.0
```

## 📖 參數說明

| 參數 | 簡寫 | 預設值 | 說明 |
|------|------|--------|------|
| `reference_image` | - | *必填* | 參考人臉圖片路徑 |
| `input_folder` | - | *必填* | 要搜尋的圖片資料夾 |
| `--output` | `-o` | `output/` | 輸出資料夾路徑 |
| `--scale` | `-s` | `2.0` | 裁剪邊界框縮放倍數 (1.0-3.0) |
| `--threshold` | `-t` | `0.4` | 相似度閾值 (0.3-0.6) |

### 參數調整建議

**相似度閾值 (threshold)**
- `0.3-0.35`：寬鬆匹配，會找到更多可能的臉，但可能有誤判
- `0.4`：**推薦值**，平衡準確度和召回率
- `0.45-0.5`：嚴格匹配，只找到非常相似的臉
- 相似度分數通常在 0.5-0.9 之間表示是同一個人

**縮放倍數 (scale)**
- `1.5`：緊密裁剪，主要包含臉部
- `2.0`：**推薦值**，包含臉部和部分周圍區域
- `2.5-3.0`：寬鬆裁剪，包含更多背景

## 📁 專案結構

```
FaceSwap/
├── find_faces.py          # 主程式（使用者友善介面）
├── face_finder.py         # 核心功能模組
├── requirements.txt       # Python 依賴套件
├── README.md             # 本文件
├── TECHNICAL.md          # 技術文件
├── examples/             # 範例圖片（可選）
├── output/               # 預設輸出資料夾
└── cy/                   # 你的圖片資料夾
```

## 💡 使用技巧

1. **選擇好的參考圖片**
   - 人臉清晰、正面、光線充足
   - 避免模糊、側臉或被遮擋的照片
   - 建議解析度至少 200x200 像素

2. **調整參數以獲得最佳結果**
   - 如果找不到某些人臉：降低 threshold（如 0.35）
   - 如果有誤判：提高 threshold（如 0.45）
   - 如果裁剪太緊：增加 scale（如 2.5）

3. **處理大量圖片**
   - 程式會顯示進度，耐心等待
   - 可以隨時按 Ctrl+C 中斷
   - 支援的圖片格式：JPG, JPEG, PNG

## ⚙️ 系統需求

- Python 3.7 或更高版本
- 至少 2GB RAM
- 支援的作業系統：macOS, Linux, Windows

## 🔧 故障排除

### 安裝問題

如果安裝 `insightface` 時遇到問題：

```bash
# macOS
pip3 install --upgrade pip
pip3 install insightface onnxruntime

# 如果 numpy 版本衝突
pip3 install "numpy<2"
```

### 記憶體不足

如果處理大量圖片時記憶體不足，可以：
1. 分批處理圖片
2. 關閉其他應用程式
3. 降低模型 det_size（需修改 `face_finder.py` 中的 `det_size=(640, 640)`）

### 找不到人臉

如果程式找不到人臉：
1. 確認參考圖片中人臉清晰可見
2. 降低 threshold 到 0.35 或更低
3. 檢查輸入圖片是否包含該人物

## 📚 技術細節

詳見 [TECHNICAL.md](TECHNICAL.md) 了解：
- 使用的深度學習模型
- 人臉識別原理
- 程式架構設計
- 效能優化建議

## 📝 授權

本專案僅供個人學習和研究使用。使用時請遵守相關隱私和肖像權法律。

## 🤝 貢獻

歡迎提出問題和改進建議！

---

Made with ❤️ using InsightFace
