# Trò chơi cờ Caro AI (9×9) – Minimax & Alpha‑Beta Pruning

## 1. Giới thiệu tổng quan
Dự án mô phỏng trò chơi cờ Caro đối kháng giữa **Người chơi (Human)** và **Máy tính (AI)** trên bàn cờ kích thước **9×9**.  
Đây là sản phẩm của bài thực hành môn **Cơ sở trí tuệ nhân tạo**, tập trung vào các thuật toán tìm kiếm có đối thủ trong trò chơi hai người tổng bằng không (zero‑sum game).

AI được xây dựng với hai thuật toán chính:
- **Minimax thuần (Pure Minimax):** Duyệt toàn bộ cây trò chơi đến độ sâu giới hạn.
- **Alpha‑Beta Pruning:** Cải tiến cắt tỉa nhánh giúp giảm số lượng trạng thái phải duyệt, tăng tốc độ phản hồi đáng kể.

Giao diện đồ hoạ được thiết kế trực quan bằng **Pygame**, mô phỏng bàn cờ giấy ô ly quen thuộc với hai quân **X** (đỏ) và **O** (xanh) đúng chuẩn Caro Việt Nam.

---

## 2. Tính năng nổi bật
1. **Launcher cấu hình trước khi vào game** – Menu Terminal cho phép chọn chế độ chơi một cách chuyên nghiệp.
2. **Ba mức độ khó (độ sâu tìm kiếm)**:
   - *Easy (Depth = 1)* – AI phản xạ nhanh, chỉ tính nước đi tức thời.
   - *Medium (Depth = 2)* – AI bắt đầu thiết lập bẫy và chuỗi tấn công ngắn.
   - *Hard (Depth = 3)* – AI tính toán sâu, chủ động phòng ngự từ xa, phá bẫy nước đôi.
3. **Lựa chọn thuật toán linh hoạt** – Có thể chọn **Minimax** hoặc **Alpha‑Beta** để so sánh hiệu năng.
4. **Giới hạn không gian tìm kiếm (Search Boundary)** – AI chỉ xét các ô trống lân cận quân đã đánh, tránh duyệt thừa.
5. **Log hiệu năng thời gian thực** – Sau mỗi nước đi, Terminal in ra **thời gian chạy**, **số nút đã xét** và **số nhánh bị cắt tỉa** (đối với Alpha‑Beta).

---

## 3. Cấu trúc thư mục dự án

```text
mssv1_mssv2_mssv3_CaroAI/
│
├── source_code/
│   ├── play.py               # File khởi chạy chính (Launcher & vòng lặp game)
│   ├── AI.py                 # Lõi thuật toán Minimax, Alpha‑Beta và hàm đánh giá
│   ├── gomoku.py             # Điều phối lượt chơi, đo thời gian suy nghĩ
│   ├── utils.py              # Tiện ích: Zobrist hashing, pattern dictionary cho heuristic
│   │
│   ├── gui/
│   │   ├── interface.py      # Giao diện Pygame (vẽ bàn cờ, quân X/O, bảng kết quả)
│   │   └── button.py         # Class Button xử lý tương tác chuột
│   │
│   └── assets/
│       ├── black_piece.png   # Hình quân X (đỏ, nền trong suốt)
│       ├── white_piece.png   # Hình quân O (xanh, nền trong suốt)
│       ├── menu_board.png    # Nền cho popup kết quả
│       └── button.png        # Nền cho các nút chức năng
│
├── benchmark.py              # Script chạy thực nghiệm tự động trên 5 thế cờ
├── requirements.txt          # Danh sách thư viện Python cần cài đặt
└── README.md                 # Hướng dẫn này
```

---

## 4. Hướng dẫn cài đặt và chạy

### Yêu cầu môi trường
- Hệ điều hành: Windows, macOS hoặc Linux
- Python **3.8** trở lên
- PIP (trình quản lý gói của Python)

## Các bước triển khai
**Bước 1: Tải mã nguồn về máy hoặc clone từ repository**
```bash
git clone [https://github.com/OEDUyZs/22026200_CaroAI.git](https://github.com/OEDUyZs/22026200_CaroAI.git)
cd 22026200_CaroAI
```

**Bước 2 – Cài đặt thư viện**
```bash
pip install -r requirements.txt
```

**Bước 3 – Khởi chạy trò chơi**
```bash
python source_code/play.py
```

### Trải nghiệm trò chơi
1. **Terminal** hiện menu:
   - Nhập `1`, `2` hoặc `3` để chọn độ khó (độ sâu tìm kiếm).
   - Nhập `1` (Minimax) hoặc `2` (Alpha‑Beta) để chọn thuật toán.
2. **Cửa sổ Pygame** xuất hiện:
   - Chọn quân đi trước: **BLACK (X)** – người đi trước, hoặc **WHITE (O)** – máy đi trước.
   - Click chuột trái vào giao điểm ô ly để đánh quân của bạn.
3. Theo dõi cửa sổ Terminal để xem thông số hiệu năng của AI.
4. Khi có 4 quân liên tiếp, popup thông báo thắng/hòa hiện ra. Nhấn **YES** để chơi lại, **NO** để thoát.

---

## 5. Chạy thực nghiệm tự động (Benchmark)

Để thu thập số liệu cho báo cáo (Level 3) mà không cần chơi tay, nhóm đã xây dựng script `benchmark.py`.

**Cách chạy:**
```bash
python benchmark.py
```

Hệ thống sẽ tự động giả lập 5 trạng thái thế cờ đặc trưng (khởi đầu, giữa ván, tấn công, phòng thủ, bẫy kép) với **cả hai thuật toán** và **ba mức độ sâu (1, 2, 3)**. Kết quả được in dưới dạng bảng so sánh chi tiết:
- Số trạng thái đã xét (Nodes visited)
- Thời gian suy nghĩ (giây)
- Nước đi được chọn

---

## 6. Thông tin nhóm
- Lê Khánh Duy - 22026200

---

## 7. Tài liệu tham khảo
- Thuật toán Minimax và Alpha‑Beta Pruning – Tài liệu môn học.
- Thư viện Pygame: https://www.pygame.org/
- Các repository mẫu được cung cấp (chỉ tham khảo ý tưởng tổ chức code, không sao chép thuật toán chính).
```