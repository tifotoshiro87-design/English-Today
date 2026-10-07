# English-Today

**Khung sườn (hiếm khi sửa):** `index.html` (giao diện + code), `fetch_podcast.py`, `.github/workflows/update.yml`.

**Phần cập nhật (chỉ sửa phần này khi thêm bài):**
- `data/lessons/<CẤP>-<CHỦ ĐỀ>.json` — mỗi file là một danh sách bài (vd. `B1-SOCIAL.json`).
- `data/meta.json` — mục tiêu, cấp độ, chủ đề, danh sách file bài học.
- `CAPNHAT.md` — nhật ký số bài.

**Thêm bài:** `python tools/add_lessons.py bai_moi.json` (tự ghi đúng file, tự cập nhật meta + nhật ký).
Sau đó chỉ cần đưa các file trong `data/` đã đổi lên GitHub; không cần đụng `index.html`.

**Cập nhật 1 chạm:** tải `bai_moi.json` từ Claude → bấm đúp `CAPNHAT.bat`. File vào `inbox/`, GitHub Action (`.github/workflows/them-bai.yml`) tự gộp vào `data/`. Xem `HUONGDAN.md`.
