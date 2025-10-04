# Face Finder - 技術文件

## 📋 目錄

- [專案結構](#專案結構)
- [核心技術](#核心技術)
- [演算法原理](#演算法原理)
- [效能分析](#效能分析)
- [進階使用](#進階使用)
- [開發維護](#開發維護)

---

## 專案結構

### 檔案說明

```
FaceSwap/
├── find_faces.py          # CLI 介面，處理命令列參數
├── face_finder.py         # 核心功能：人臉檢測、識別、裁剪
├── requirements.txt       # Python 依賴
├── test_installation.py   # 安裝測試腳本
├── example.sh            # Bash 使用範例
├── .gitignore            # Git 忽略規則
├── README.md             # 使用手冊
└── TECHNICAL.md          # 本文件
```

### 核心模組

**find_faces.py** - 使用者介面層
```python
main()
  ├── argparse.parse_args()    # 解析 CLI 參數
  ├── 驗證輸入檔案與資料夾
  └── process_folder()         # 呼叫核心功能
```

**face_finder.py** - 核心邏輯層
```python
process_folder()
  ├── 初始化 FaceAnalysis()
  ├── get_reference_face_embedding()  # 提取參考人臉特徵
  └── 遍歷圖片
      └── crop_matching_faces()       # 檢測、比對、裁剪
```

---

## 核心技術

### InsightFace 深度學習框架

使用 [InsightFace](https://github.com/deepinsight/insightface) buffalo_l 模型套件：

| 模型 | 功能 | 架構 |
|------|------|------|
| **det_10g** | 人臉檢測 | RetinaFace |
| **w600k_r50** | 人臉識別 | ArcFace (ResNet-50) |

### 技術指標

- **特徵維度**: 512 維向量（L2 正規化）
- **相似度計算**: Cosine Similarity
- **檢測閾值**: 0.5（內建）
- **訓練資料**: WebFace600K (600萬張臉)
- **準確度**: LFW 99.86%

---

## 演算法原理

### 1. 人臉檢測

```python
# 使用 RetinaFace 檢測人臉
faces = app.get(image)

# 每個 face 包含:
# - bbox: [x1, y1, x2, y2] 邊界框
# - embedding: 512 維特徵向量
# - det_score: 檢測置信度
```

### 2. 特徵提取

```python
# ArcFace 模型自動提取 512 維特徵
embedding = face.embedding  # shape: (512,)

# 特徵已經過 L2 正規化
# ||embedding|| = 1
```

### 3. 相似度計算

使用**餘弦相似度** (Cosine Similarity)：

```python
def calculate_similarity(emb1, emb2):
    emb1 = emb1 / np.linalg.norm(emb1)  # 正規化
    emb2 = emb2 / np.linalg.norm(emb2)
    return np.dot(emb1, emb2)  # 範圍: [-1, 1]
```

**相似度解讀**:
- `> 0.6`: 高度相似，很可能是同一人
- `0.4 - 0.6`: 中度相似
- `0.3 - 0.4`: 低度相似
- `< 0.3`: 不相似

### 4. 邊界框擴大

```python
# 計算中心點
center_x = (x1 + x2) // 2
center_y = (y1 + y2) // 2

# 擴大到 scale 倍（預設 2.0）
new_width = int((x2 - x1) * scale)
new_height = int((y2 - y1) * scale)

# 保持中心不變，計算新邊界框
new_x1 = center_x - new_width // 2
new_y1 = center_y - new_height // 2

# 確保在圖片範圍內
new_x1 = max(0, new_x1)
new_y1 = max(0, new_y1)
```

### 完整流程

```
1. 初始化 InsightFace 模型
2. 讀取參考圖片 → 檢測人臉 → 提取特徵向量
3. For each 目標圖片:
   ├── 檢測所有人臉
   ├── For each 檢測到的人臉:
   │   ├── 提取特徵向量
   │   ├── 計算與參考人臉的相似度
   │   └── If 相似度 >= threshold:
   │       ├── 擴大邊界框
   │       └── 裁剪並儲存
4. 輸出統計結果
```

---

## 效能分析

### 時間複雜度

- **初始化**: O(1) - 載入模型
- **處理 n 張圖片**: O(n × m) - m 為平均每張圖片的人臉數
- **單張人臉**: ~0.05s（特徵提取）+ <0.001s（相似度計算）

### 效能基準 (MacBook Pro M1)

| 任務 | 時間 |
|------|------|
| 模型載入 | 3-5s |
| 單張圖片檢測 | 0.2-0.5s |
| 500 張圖片處理 | 5-10 分鐘 |

### 優化建議

**1. 使用 GPU 加速**
```python
# 編輯 face_finder.py
app = FaceAnalysis(providers=['CUDAExecutionProvider'])
```

**2. 調整檢測尺寸**
```python
# 更快但較不準確
app.prepare(ctx_id=0, det_size=(320, 320))

# 預設
app.prepare(ctx_id=0, det_size=(640, 640))

# 更準確但較慢
app.prepare(ctx_id=0, det_size=(1024, 1024))
```

**3. 批次處理與平行化**
```python
# 可使用 multiprocessing 平行處理多張圖片
from multiprocessing import Pool

with Pool(4) as p:
    p.map(process_image, image_list)
```

---

## 進階使用

### 同時搜尋多人

```python
from face_finder import process_folder

people = {
    'person1': 'ref1.jpg',
    'person2': 'ref2.jpg',
}

for name, ref_img in people.items():
    process_folder(
        'photos/', ref_img, f'output/{name}/',
        scale=2.0, threshold=0.4
    )
```

### 作為 Python 模組使用

```python
from face_finder import get_reference_face_embedding, crop_matching_faces
from insightface.app import FaceAnalysis

# 初始化
app = FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

# 提取參考特徵
ref_emb = get_reference_face_embedding(app, 'reference.jpg')

# 處理單張圖片
matches = crop_matching_faces(
    app, 'photo.jpg', ref_emb, 'output/',
    scale=2.0, threshold=0.4
)
```

### 自訂模型參數

```python
# face_finder.py 中修改

# 使用小型模型（更快）
app = FaceAnalysis(name='buffalo_sc')

# 使用大型模型（更準確，預設）
app = FaceAnalysis(name='buffalo_l')

# 啟用 GPU
app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
```

---

## 開發維護

### 測試流程

```bash
# 1. 測試安裝
python3 test_installation.py

# 2. 功能測試
python3 find_faces.py test_ref.jpg test_photos/ -o test_output/

# 3. 檢查結果
ls -lh test_output/
```

### 常見修改

**調整預設參數** (find_faces.py):
```python
parser.add_argument('-t', '--threshold', default=0.35)  # 改閾值
parser.add_argument('-s', '--scale', default=2.5)       # 改縮放
```

**啟用除錯日誌** (face_finder.py):
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 版本控制

```bash
# 初始化
git init
git add .
git commit -m "Initial commit"

# 開發分支
git checkout -b feature/new-feature
# ... 修改 ...
git commit -m "Add feature"
git checkout main
git merge feature/new-feature

# 打標籤
git tag -a v1.0 -m "Version 1.0"
```

### 部署建議

**打包專案**:
```bash
tar -czf face_finder.tar.gz \
    find_faces.py face_finder.py \
    requirements.txt README.md TECHNICAL.md \
    test_installation.py example.sh
```

**Docker 化** (選用):
```dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py .
ENTRYPOINT ["python3", "find_faces.py"]
```

---

## 故障排除

### 安裝問題

**numpy 版本衝突**:
```bash
pip3 install "numpy<2"
```

**InsightFace 無法安裝**:
```bash
pip3 install --upgrade pip
pip3 install insightface onnxruntime
```

### 效能問題

1. **處理太慢**: 降低 `det_size` 或使用 GPU
2. **記憶體不足**: 分批處理圖片
3. **找不到人臉**: 降低 `threshold` 或檢查圖片品質

### 除錯技巧

**查看相似度分數**:
程式執行時會顯示每張臉的相似度，觀察這些數值來調整 threshold

**測試單張圖片**:
```bash
# 先用單張圖片測試
python3 find_faces.py ref.jpg single_image_folder/
```

---

## 參考資料

- [InsightFace GitHub](https://github.com/deepinsight/insightface)
- [ArcFace Paper](https://arxiv.org/abs/1801.07698) - Deng et al., CVPR 2019
- [RetinaFace Paper](https://arxiv.org/abs/1905.00641) - Deng et al., CVPR 2020

---

**版本**: 1.0
**最後更新**: 2025-10-04
**測試狀態**: ✅ 已測試（501 張圖片，找到 419 + 383 張匹配人臉）
