#!/usr/bin/env python3
"""
Face Finder - Simple CLI tool to find and crop specific faces from images
"""

import os
import sys
import argparse
from face_finder import process_folder


def main():
    parser = argparse.ArgumentParser(
        description='Find and crop specific faces from a collection of images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic usage - find faces matching reference.jpg in photos/ folder
  python find_faces.py reference.jpg photos/

  # Specify output directory
  python find_faces.py reference.jpg photos/ -o output/person1/

  # Adjust similarity threshold (0.3-0.5 recommended)
  python find_faces.py reference.jpg photos/ -t 0.45

  # Change crop scale factor (2.0 = 2x face size)
  python find_faces.py reference.jpg photos/ -s 2.5

  # Full example with all options
  python find_faces.py face.jpg photos/ -o results/ -t 0.42 -s 2.0
        ''')

    parser.add_argument(
        'reference_image',
        help='Path to reference image containing the face to find'
    )
    parser.add_argument(
        'input_folder',
        help='Path to folder containing images to search'
    )
    parser.add_argument(
        '-o', '--output',
        default='output',
        help='Output directory for cropped faces (default: output/)'
    )
    parser.add_argument(
        '-s', '--scale',
        type=float,
        default=2.0,
        help='Bounding box scale factor (default: 2.0, range: 1.0-3.0)'
    )
    parser.add_argument(
        '-t', '--threshold',
        type=float,
        default=0.4,
        help='Similarity threshold (default: 0.4, range: 0.3-0.6, higher=stricter)'
    )

    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.reference_image):
        print(f"❌ Error: Reference image not found: {args.reference_image}")
        sys.exit(1)

    if not os.path.isdir(args.input_folder):
        print(f"❌ Error: Input folder not found: {args.input_folder}")
        sys.exit(1)

    if args.scale < 1.0 or args.scale > 3.0:
        print(f"⚠️  Warning: Scale factor {args.scale} is outside recommended range (1.0-3.0)")

    if args.threshold < 0.2 or args.threshold > 0.7:
        print(f"⚠️  Warning: Threshold {args.threshold} is outside recommended range (0.3-0.6)")

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    print("=" * 60)
    print("🔍 Face Finder")
    print("=" * 60)
    print(f"📷 Reference: {args.reference_image}")
    print(f"📁 Input folder: {args.input_folder}")
    print(f"💾 Output folder: {args.output}")
    print(f"📏 Scale factor: {args.scale}x")
    print(f"🎯 Similarity threshold: {args.threshold}")
    print("=" * 60)
    print()

    # Process folder
    try:
        process_folder(
            args.input_folder,
            args.reference_image,
            args.output,
            args.scale,
            args.threshold
        )
        print()
        print("=" * 60)
        print("✅ Processing complete!")
        print(f"📂 Results saved to: {os.path.abspath(args.output)}")
        print("=" * 60)
    except KeyboardInterrupt:
        print("\n\n⚠️  Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
