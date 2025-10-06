# Face Finder 對話紀錄

**日期**: 2025-10-06  
**專案**: Face Finder - 人臉識別與裁剪工具

---

## 執行任務摘要

### 1. YC 資料集處理
**指令**:
```bash
python3 find_faces.py /Users/hjc/Downloads/FaceSwap/_raw_yc_only/20250911_132858.jpg /Users/hjc/Downloads/FaceSwap/_raw_yc_only/ -t 0.45 -o /Users/hjc/Downloads/FaceSwap/yc_crop
```

**結果**:
- 處理圖片: 275 張
- 找到匹配: 148 個臉部
- 相似度閾值: 0.45 (較嚴格)
- 輸出資料夾: `/Users/hjc/Downloads/FaceSwap/yc_crop`
- 最高相似度: 1.000 (參考圖片本身)
- 其他高分: 0.943, 0.941, 0.893, 0.886, 0.831, 0.814
- 最低通過: 0.453

---

### 2. HM 資料集處理
**指令**:
```bash
python3 find_faces.py _raw_hm_only/IMG_4022.JPG _raw_hm_only/ -o crophm/
```

**結果**:
- 處理圖片: 44 張
- 找到匹配: 33 個臉部
- 相似度閾值: 0.4 (預設值)
- 輸出資料夾: `/Users/hjc/Downloads/FaceSwap/crophm/`
- 最高相似度: 1.000 (參考圖片 IMG_4022.JPG)
- 其他高分: 0.629, 0.595, 0.576, 0.575, 0.567, 0.560, 0.556
- 最低通過: 0.404

**備註**: 初次執行時參考圖片路徑錯誤，已修正為 `_raw_hm_only/IMG_4022.JPG`

---

### 3. LG 資料集處理
**指令**:
```bash
python3 find_faces.py _raw_lg_only/DSC_0170.JPG _raw_lg_only/ -o croplg/
```

**結果**:
- 處理圖片: 87 張
- 找到匹配: 87 個臉部 (100% 命中率！)
- 相似度閾值: 0.4 (預設值)
- 輸出資料夾: `/Users/hjc/Downloads/FaceSwap/croplg/`
- 最高相似度: 1.000 (參考圖片 DSC_0170.JPG)
- 其他高分: 0.887, 0.874, 0.844, 0.837, 0.830, 0.829, 0.828, 0.827
- 最低通過: 0.401

---

## 技術細節

### 使用的模型
- **InsightFace buffalo_l 模型**
- **ArcFace (w600k_r50)**: 人臉識別，512維特徵向量
- **RetinaFace (det_10g)**: 人臉偵測
- **執行環境**: CPU (CPUExecutionProvider)

### 參數說明
- **Scale factor**: 2.0x (裁剪框為臉部的2倍大小)
- **Similarity threshold**: 
  - YC 資料集: 0.45 (更嚴格的匹配)
  - HM & LG 資料集: 0.4 (預設值)
- **相似度計算**: Cosine similarity (餘弦相似度)

### 專案位置
- **主程式**: `/Users/hjc/Downloads/FaceSwap/find_faces.py`
- **核心模組**: `/Users/hjc/Downloads/FaceSwap/face_finder.py`
- **GitHub**: https://github.com/r90941022/face-finder

---

## 整體統計

| 資料集 | 處理圖片 | 找到臉部 | 命中率 | 閾值 |
|--------|---------|---------|--------|------|
| YC     | 275     | 148     | 53.8%  | 0.45 |
| HM     | 44      | 33      | 75.0%  | 0.4  |
| LG     | 87      | 87      | 100%   | 0.4  |
| **總計** | **406** | **268** | **66.0%** | - |

---

## 備註
- 所有任務均成功完成
- LG 資料集達到 100% 命中率，顯示參考圖片品質良好且資料集內該人物出現頻率高
- YC 資料集使用較高閾值 (0.45)，確保更高的匹配準確度
- 模型已預先載入，無需重新下載

---

**存檔時間**: $(date '+%Y-%m-%d %H:%M:%S')
