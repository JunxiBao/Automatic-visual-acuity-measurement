from sklearn.neighbors import NearestNeighbors
import face_recognition
import os
import json
import numpy as np

def save_to_json(encodings, names, json_file):
    """保存人脸特征和名字到 JSON 文件"""
    # 将 numpy.ndarray 转换为列表
    data = [{"name": name, "encoding": encoding.tolist()} for name, encoding in zip(names, encodings)]
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json(json_file):
    """从 JSON 文件加载人脸特征和名字"""
    if not os.path.exists(json_file):
        return [], []

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    encodings = [np.array(item["encoding"]) for item in data]  # 转回 numpy.ndarray
    names = [item["name"] for item in data]
    return encodings, names

def load_known_faces_with_knn(known_faces_dir, data_file="data/faces.json"):
    """加载已知人脸，构建 KD-Tree，支持增量更新和同步删除"""
    print("Loading known faces...")
    os.makedirs(os.path.dirname(data_file), exist_ok=True)

    # 加载已保存的特征和名称
    known_encodings, known_names = load_from_json(data_file)

    # 获取目录中的实际文件名（去掉扩展名）
    current_files = {os.path.splitext(filename)[0] for filename in os.listdir(known_faces_dir) if filename.endswith((".jpg", ".jpeg", ".png"))}

    # 找到需要移除的文件
    removed_files = set(known_names) - current_files
    if removed_files:
        print(f"Removing deleted files from cache: {removed_files}")
        indices_to_keep = [i for i, name in enumerate(known_names) if name not in removed_files]
        known_encodings = [known_encodings[i] for i in indices_to_keep]
        known_names = [known_names[i] for i in indices_to_keep]

    # 处理新文件
    for filename in current_files - set(known_names):
        print(f"Processing {filename}...")
        image_path = os.path.join(known_faces_dir, filename + ".jpg")  # 默认扩展名为 .jpg
        if not os.path.exists(image_path):  # 检查其他扩展名
            image_path = os.path.join(known_faces_dir, filename + ".jpeg")
        if not os.path.exists(image_path):  # 检查其他扩展名
            image_path = os.path.join(known_faces_dir, filename + ".png")

        if os.path.exists(image_path):
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:  # 确保图片中有检测到人脸
                known_encodings.append(encodings[0])
                known_names.append(filename)

    # 保存更新后的特征和名称
    save_to_json(known_encodings, known_names, data_file)

    knn = NearestNeighbors(n_neighbors=1, algorithm="ball_tree").fit(known_encodings)
    return knn, np.array(known_encodings), known_names

def recognize_faces_with_knn(input_image_path, knn, known_names, tolerance=0.6):
    """使用 KD-Tree 识别人脸"""
    print("Recognizing faces in image...")
    input_image = face_recognition.load_image_file(input_image_path)
    face_encodings = face_recognition.face_encodings(input_image)
    recognized_names = []

    for face_encoding in face_encodings:
        distances, indices = knn.kneighbors([face_encoding])
        if distances[0][0] < tolerance:
            recognized_names.append(known_names[indices[0][0]])
        else:
            recognized_names.append("Unknown")
    return recognized_names

def main():
    print("Starting...")
    known_faces_dir = "./data/image"  # 存放已知人脸图片的目录
    input_image_path = "./data/output.jpeg"  # 要识别的图片路径

    knn, known_encodings, known_names = load_known_faces_with_knn(known_faces_dir)
    print("Known names (without extensions):", known_names)
    recognized_names = recognize_faces_with_knn(input_image_path, knn, known_names)
    print("**********************")
    print("Recognized names:", recognized_names)
    print("**********************")
