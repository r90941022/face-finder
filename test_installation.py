#!/usr/bin/env python3
"""
測試 Face Finder 安裝是否正確
"""

import sys

def test_imports():
    """測試必要的套件是否已安裝"""
    print("正在測試套件安裝...")

    required_packages = {
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'insightface': 'insightface',
        'onnxruntime': 'onnxruntime',
    }

    missing_packages = []

    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {pip_name}")
        except ImportError:
            print(f"  ❌ {pip_name} - 未安裝")
            missing_packages.append(pip_name)

    return missing_packages


def test_model_download():
    """測試模型是否可以載入"""
    print("\n正在測試 InsightFace 模型...")

    try:
        from insightface.app import FaceAnalysis
        print("  ✅ InsightFace 導入成功")

        # 嘗試初始化（會自動下載模型）
        print("  📥 初始化模型（首次執行會下載，約 200MB）...")
        app = FaceAnalysis(providers=['CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))
        print("  ✅ 模型載入成功")

        return True
    except Exception as e:
        print(f"  ❌ 模型載入失敗: {e}")
        return False


def main():
    print("=" * 60)
    print("Face Finder - 安裝測試")
    print("=" * 60)
    print()

    # 測試套件
    missing = test_imports()

    if missing:
        print("\n❌ 缺少以下套件，請執行:")
        print(f"   pip3 install {' '.join(missing)}")
        sys.exit(1)

    # 測試模型
    if not test_model_download():
        print("\n❌ 模型載入失敗")
        print("   請檢查網路連線，模型會在首次執行時自動下載")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✅ 所有測試通過！Face Finder 已準備就緒")
    print("=" * 60)
    print()
    print("下一步:")
    print("  python3 find_faces.py reference.jpg photos/")
    print()


if __name__ == "__main__":
    main()
