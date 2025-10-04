#!/usr/bin/env python3
"""
Face cropping script using InsightFace (accurate face recognition)
Crops matching faces with a bounding box 2x the size of the detected face
"""

import cv2
import os
import sys
import glob
import numpy as np
from insightface.app import FaceAnalysis


def get_reference_face_embedding(app, reference_image_path):
    """
    Extract face embedding from reference image using InsightFace

    Args:
        app: FaceAnalysis app
        reference_image_path: Path to reference image

    Returns:
        embedding or None if no face found
    """
    print(f"Loading reference image: {reference_image_path}")

    # Load image
    image = cv2.imread(reference_image_path)
    if image is None:
        print(f"Error: Cannot read image from {reference_image_path}")
        return None

    # Detect faces
    faces = app.get(image)

    if len(faces) == 0:
        print("Error: No face found in reference image")
        return None

    if len(faces) > 1:
        print(f"Warning: Multiple faces found in reference image, using the largest one")
        # Use the largest face
        faces = sorted(faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]), reverse=True)

    reference_embedding = faces[0].embedding
    print(f"Reference face extracted successfully")
    return reference_embedding


def calculate_similarity(emb1, emb2):
    """
    Calculate cosine similarity between two embeddings

    Args:
        emb1: First embedding
        emb2: Second embedding

    Returns:
        Similarity score (0-1, higher is more similar)
    """
    # Normalize embeddings
    emb1 = emb1 / np.linalg.norm(emb1)
    emb2 = emb2 / np.linalg.norm(emb2)

    # Cosine similarity
    similarity = np.dot(emb1, emb2)

    return similarity


def crop_matching_faces(app, image_path, reference_embedding, output_dir, scale_factor=2.0, threshold=0.4):
    """
    Detect and crop faces that match the reference face

    Args:
        app: FaceAnalysis app
        image_path: Path to input image
        reference_embedding: Reference face embedding to match against
        output_dir: Directory to save cropped faces
        scale_factor: Multiplier for bounding box size (default 2.0)
        threshold: Similarity threshold (higher is stricter, default 0.4)

    Returns:
        Number of matching faces found
    """
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"  Error: Cannot read image from {image_path}")
            return 0

        height, width, _ = image.shape

        # Detect faces
        faces = app.get(image)

        if len(faces) == 0:
            print(f"  No faces detected in {os.path.basename(image_path)}")
            return 0

        print(f"  Found {len(faces)} face(s) in {os.path.basename(image_path)}")

        matching_count = 0

        # Check each detected face
        for idx, face in enumerate(faces):
            # Get face embedding
            embedding = face.embedding

            # Calculate similarity with reference
            similarity = calculate_similarity(reference_embedding, embedding)

            if similarity >= threshold:
                matching_count += 1
                print(f"    ✓ Face {idx + 1} matches! (similarity: {similarity:.3f})")

                # Get face bounding box
                bbox = face.bbox.astype(int)
                x1, y1, x2, y2 = bbox

                # Calculate face dimensions
                face_width = x2 - x1
                face_height = y2 - y1

                # Calculate center of the face
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # Calculate new dimensions (scale_factor x larger)
                new_w = int(face_width * scale_factor)
                new_h = int(face_height * scale_factor)

                # Calculate new bounding box (centered on face)
                new_x1 = center_x - new_w // 2
                new_y1 = center_y - new_h // 2
                new_x2 = new_x1 + new_w
                new_y2 = new_y1 + new_h

                # Ensure coordinates are within image bounds
                new_x1 = max(0, new_x1)
                new_y1 = max(0, new_y1)
                new_x2 = min(width, new_x2)
                new_y2 = min(height, new_y2)

                # Crop the face
                cropped_face = image[new_y1:new_y2, new_x1:new_x2]

                # Generate output filename
                input_filename = os.path.basename(image_path)
                name, ext = os.path.splitext(input_filename)
                output_filename = f"{name}_face_{matching_count}{ext}"
                output_path = os.path.join(output_dir, output_filename)

                # Save cropped face
                cv2.imwrite(output_path, cropped_face)
                print(f"    Saved to: {output_filename}")
            else:
                print(f"    ✗ Face {idx + 1} does not match (similarity: {similarity:.3f})")

        return matching_count

    except Exception as e:
        print(f"  Error processing {os.path.basename(image_path)}: {e}")
        return 0


def process_folder(folder_path, reference_image_path, output_dir, scale_factor=2.0, threshold=0.4):
    """
    Process all images in a folder

    Args:
        folder_path: Path to folder containing images
        reference_image_path: Path to reference image
        output_dir: Directory to save cropped faces
        scale_factor: Multiplier for bounding box size
        threshold: Similarity threshold for face matching
    """
    # Initialize InsightFace
    print("Initializing InsightFace model...")
    app = FaceAnalysis(providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))
    print("Model loaded successfully")

    # Get reference face embedding
    reference_embedding = get_reference_face_embedding(app, reference_image_path)
    if reference_embedding is None:
        return

    # Get all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.png', '*.PNG']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))

    image_files.sort()

    if len(image_files) == 0:
        print(f"No images found in {folder_path}")
        return

    print(f"\nFound {len(image_files)} images to process")
    print(f"Scale factor: {scale_factor}x")
    print(f"Similarity threshold: {threshold}")
    print("-" * 60)

    # Process each image
    total_matches = 0
    processed_count = 0

    for image_path in image_files:
        print(f"\nProcessing: {os.path.basename(image_path)}")
        matches = crop_matching_faces(app, image_path, reference_embedding, output_dir, scale_factor, threshold)
        total_matches += matches
        processed_count += 1

    print("\n" + "=" * 60)
    print(f"Processing complete!")
    print(f"Processed: {processed_count} images")
    print(f"Found: {total_matches} matching faces")
    print(f"Output directory: {output_dir}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python crop_face_v2.py <reference_image> <folder_path> [output_dir] [scale_factor] [threshold]")
        print("Example: python crop_face_v2.py cy/IMG_1004.JPG cy cropped_faces_v2 2.0 0.4")
        print("\nParameters:")
        print("  reference_image: Image containing the face to match")
        print("  folder_path: Folder containing images to process")
        print("  output_dir: Output directory (default: cropped_faces_v2)")
        print("  scale_factor: Bounding box scale factor (default: 2.0)")
        print("  threshold: Similarity threshold, 0-1 (default: 0.4, higher is stricter)")
        sys.exit(1)

    reference_image = sys.argv[1]
    folder_path = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "cropped_faces_v2"
    scale_factor = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
    threshold = float(sys.argv[5]) if len(sys.argv) > 5 else 0.4

    # Validate inputs
    if not os.path.exists(reference_image):
        print(f"Error: Reference image not found: {reference_image}")
        sys.exit(1)

    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found: {folder_path}")
        sys.exit(1)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Process folder
    process_folder(folder_path, reference_image, output_dir, scale_factor, threshold)


if __name__ == "__main__":
    main()
