1. Phân tích
INPUT: student_id: int
OUTPUT: status_code, thông báo, dữ liệu

2. Giải pháp
Giải pháp 1:
    Tìm học viên theo student_id.
    Nếu không tồn tại → báo lỗi 404
    Nếu tồn tại:
        Lưu thông tin cần trả về
        db.delete(student)
        db.commit()
        Trả về dữ liệu vừa xóa

Giải pháp 2:
Xóa trực tiếp bằng Query, sau đó kiểm tra số dòng bị ảnh hưởng


3. So sánh
| Tiêu chí               | Giải pháp 1 | Giải pháp 2        |
| ---------------------- | ----------- | ------------------ |
| Độ dễ hiểu             | Cao         | Trung bình         |
| Số lượng code          | Nhiều hơn   | Ít hơn             |
| Kiểm soát lỗi          | Rất tốt     | Khó hơn            |
| Kiểm tra tồn tại       | Có          | Phải kiểm tra thêm |
| Phù hợp SQLAlchemy ORM | Rất phù hợp | Ít phù hợp hơn     |
| Dễ tách Service        | Có          | Có                 |

=> Chọn giải pháp 1:
    Đúng phong cách SQLAlchemy ORM
    Kiểm tra được dữ liệu tồn tại
    Dễ xử lý Exception
    Có thể trả lại thông tin học viên đã xóa
    Dễ mở rộng nghiệp vụ sau này

