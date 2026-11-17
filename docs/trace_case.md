# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Case M1 — ticket ghi đè dữ liệu DB

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`; run ID dạng `R-seeded_regression-C-002-s11` |
| Triệu chứng | Lab 8 grader fail `status resolved != denied`; ledger ghi `20000` và 1 refund, nhãn yêu cầu 0 và denied. |
| Bước sai đầu tiên | Event 3 `model_override`: `delay_days` bị đổi thành 5. |
| Vì sao là bước *đầu tiên* | Event 1 chỉ handoff allowlist; event 2 đọc order và thấy DB `delay_days=2`; sai lệch bắt đầu ở event 3. |
| Failure mode | `FM-03 ticket_trust` |
| Đối chứng | `fixed C-002@11` giữ `delay_days=2`, quote bằng 0, không gọi refund và trả denied. |
| Regression test | `tests/test_swarm_reference.py::test_reference_weakness_is_visible_on_public_t02`; variant lỗi fail ở C-002@55, `fixed` giữ đúng kết quả. |
| Chưa chắc chắn | Trace chứng minh quyết định sai trong trial này; chưa chứng minh tần suất tương tự trên model thật. |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
