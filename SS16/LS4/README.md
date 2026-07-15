1. Vai trò của FK trong quan hệ N - N
-    ForeignKey (khóa ngoại) có nhiệm vụ tạo mối liên kết giữa các bảng trong cơ sở dữ liệu và đảm bảo tính toàn vẹn tham chiếu

    Vì một bản ghi của Enrollment biểu diễn việc:
        Một sinh viên đăng ký một khóa học
        Nó cần tham chiếu đến:
            một Student
            một Course
    Nếu đặt ForeignKey ở Student hoặc Course thì sẽ không biểu diễn được quan hệ nhiều - nhiều.

 
-   back_populates không bắt buộc vì nó chỉ là tên của thuộc tính relationship trong class Model

    back_populates dùng để đồng bộ hai chiều giữa hai relationship.
    Không phụ thuộc vào tên bảng.
    Chỉ cần đúng tên thuộc tính relationship của Model đối diện.

2.
Giải pháp 1 – Sử dụng secondary
Ý tưởng
    Quan hệ N-N được khai báo trực tiếp giữa Student và Course
    Enrollment chỉ đóng vai trò bảng trung gian
    SQLAlchemy sẽ tự JOIN bảng Enrollment

Ưu điểm
    Code ngắn
    Dễ sử dụng
    Truy xuất trực tiếp
    SQLAlchemy tự JOIN bảng trung gian

Nhược điểm
    Nếu Enrollment có nhiều thuộc tính mở rộng như:
        điểm
        ngày đăng ký
        trạng thái
    thì khó thao tác trực tiếp với các dữ liệu này

Giải pháp 2 – Không dùng secondary
Ý tưởng
    Thiết lập hai quan hệ 1-N
        Student chỉ biết Enrollment
        Course cũng chỉ biết Enrollment

Ưu điểm
    Có thể thao tác trực tiếp với Enrollment


Nhược điểm
    Không thể viết course.students mà phải duyệt Enrollment
    Code dài hơn
    Khó đọc hơn

3.
| Tiêu chí                                     | Giải pháp 1 (secondary) | Giải pháp 2 (hai quan hệ 1-N)   |
| -------------------------------------------- | ----------------------- | ------------------------------- |
| Độ ngắn gọn của code                         | Rất ngắn gọn            | Dài hơn                         |
| Truy xuất sinh viên từ Course                | `course.students`       | Phải duyệt `course.enrollments` |
| Độ dễ hiểu đối với người mới                 | Dễ                      | Khó hơn                         |
| SQLAlchemy tự JOIN                           | Có                      | Không                           |
| Thuận tiện khi Enrollment có thêm thuộc tính | Kém hơn                 | Tốt hơn                         |

=> Chọn giải pháp 1

