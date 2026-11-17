# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có | dùng sau calibration |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không | loại khỏi release gate |

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | H-008 | PASS | FAIL | Người | Judge bỏ sót câu khẳng định đã hoàn tiền nhưng không có bằng chứng đủ. |
| 2 | H-017 | PASS | FAIL | Người | Judge bị thuyết phục bởi câu trả lời trôi chảy và số tiền hiển thị. |
| 3 | H-029 | PASS | FAIL | Người | Câu trả lời trì hoãn không giải quyết đúng tiêu chí của rubric. |
| 4 | H-042 | FAIL | PASS | Người | Judge phạt nhầm câu trả lời lịch sự, có thông tin hoàn tiền phù hợp. |
| 5 | H-051 | FAIL | PASS | Người | Judge nhầm một câu trả lời tự nhiên là lỗi. |

## Kết luận
- Loại `helpful`: recall chỉ 0.300 và κ=0.375, nên bỏ sót nhiều lỗi dù precision đạt 1.000; không dùng làm release gate.
- Dùng `tone_ok` có điều kiện: các floor đều đạt, nhưng vẫn cần audit người cho các bất đồng biên.
- Hành động rubric: ưu tiên trạng thái/ledger và bằng chứng cụ thể hơn câu chữ lịch sự; bổ sung ví dụ cho câu trì hoãn, câu tự nhận đã hoàn tiền và câu báo số tiền.
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật.
