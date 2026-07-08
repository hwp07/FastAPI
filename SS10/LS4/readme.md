Phần 1: Phân tích
INPUT: shipment_id:
    kiểu dữ liệu: interger
    ràng buộc: primary_key = True, 

OUTPUT: 
    output thành công (shipment_id tồn tại trong database):http status code 200, response
    output thất bại (shipment_id không tồn tại): http status code 404, response


Phần 2: So sánh 2 giải pháp
| Tiêu chí                     | Giải pháp 1 `.all()` + lọc Python | Giải pháp 2 `.filter().first()`              |
| ---------------------------- | --------------------------------- | -------------------------------------------- |
| Số lượng bản ghi lấy từ DB   | 100.000 bản ghi                   | Tối đa 1 bản ghi                             |
| RAM sử dụng                  | Rất lớn                           | Rất nhỏ                                      |
| SQL sinh ra                  | `SELECT * FROM shipments`         | `SELECT * FROM shipments WHERE id=? LIMIT 1` |
| Có LIMIT không               | Không                             | Có (`LIMIT 1`)                               |
| CPU Python                   | Phải duyệt toàn bộ danh sách      | Hầu như không phải duyệt                     |
| Lưu lượng truyền DB → Server | Rất lớn                           | Rất nhỏ                                      |
| Tốc độ khi dữ liệu tăng      | Giảm mạnh                         | Ổn định                                      |
| Khả năng mở rộng             | Kém                               | Rất tốt                                      |
| Trường hợp nên dùng          | Khi thật sự cần toàn bộ dữ liệu   | Khi chỉ cần một bản ghi                      |

Kết luận: Lựa chọn giải pháp 2:
    Database được tối ưu để tìm kiếm dữ liệu
    SQL có WHERE và LIMIT 1
    Không phải tải toàn bộ bảng lên RAM
    Tiết kiệm CPU và bộ nhớ
    Hệ thống vẫn hoạt động tốt khi dữ liệu tăng lên hàng trăm nghìn hoặc hàng triệu bản ghi

