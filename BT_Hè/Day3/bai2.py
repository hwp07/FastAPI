students = [
    {"name": "An", "gpa": 7.2},
    {"name": "Bình", "gpa": 9.5},
    {"name": "Cường", "gpa": 6.8},
    {"name": "Dũng", "gpa": 8.4}
]

for i in range(len(students)):
    for j in range(0, len(students) - i - 1):
        if students[j]["gpa"] < students[j + 1]["gpa"]:
            students[j], students[j + 1] = students[j + 1], students[j]


print("BẢNG XẾP HẠNG SINH VIÊN (BUBBLE SORT - GPA GIẢM DẦN)")
for rank, i in enumerate(students, start=1):
    print(f"Top {rank}: {i["name"]} - {i["gpa"]} điểm")