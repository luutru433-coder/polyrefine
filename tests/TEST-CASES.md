# Test Cases

Run each case in a fresh isolated chat except for its own specified turns. Critical cases retain the original wording.

## Pronouns and subjects (10)

**Test 01 — Pronoun**

Input: `I need your help.`

Không được đổi I thành We.

**Test 13**

Input: `We sent it to you.`

**Test 14**

Input: `You emailed me.`

**Test 15**

Input: `They thanked us.`

**Test 16**

Input: `She asked him to help.`

**Test 17**

Input: `I told her that we would wait.`

**Test 18**

Input: `Please call when ready.`

**Test 19**

Input: `Only he signed.`

**Test 20**

Input: `You can send it to me or to them.`

**Test 21**

Input: `They need your answer, not mine.`

## Tense, negation and obligation (10)

**Test 03 — Tense**

Input: `They didn't send the email.`

Không được tự đổi sang hiện tại hoàn thành.

**Test 04 — Modality**

Input: `We might cancel the booking.`

Không được đổi `might` thành `will`.

**Test 22**

Input: `I had finished before noon.`

**Test 23**

Input: `You must not share the code.`

**Test 24**

Input: `You don't have to call.`

**Test 25**

Input: `If it rains, we will wait.`

**Test 26**

Input: `The delay happened because the bus broke down.`

**Test 27**

Input: `I promised to reply on Friday.`

**Test 28**

Input: `She hasn't arrived yet.`

**Test 29**

Input: `They can test it tomorrow, but cannot sign it.`

## English refinement (8)

**Test 30**

Input: `I recieved your message.`

**Test 31**

Input: `Refine only: we was ready.`

**Test 32**

Input: `Can you please checks the dates?`

**Test 33**

Input: `Hey, wanna grab lunch later?`

**Test 34**

Input: `The attach file is the final report.`

**Test 35**

Input: `Please call now this is urgent.`

**Test 36**

Input: `Reorder for clarity: Before 3 p.m., send the receipt to me, please.`

**Test 37**

Input: `thanks for you help`

## Negative content and soft alternatives (8)

**Test 02 — Negative**

Input: `They are scaming us.`

Bản chính phải giữ `scamming`.

**Test 12 — Soft Alternative**

Input: `They are scamming us.`

Không được xuất bản Soft Alternative có thêm `may` hoặc `might`.

Nếu không tạo được bản mềm hơn mà vẫn giữ nguyên ý nghĩa, bỏ Soft Alternative.

**Test 38**

Input: `I strongly disagree with your decision.`

**Test 39**

Input: `They deliberately ignored the warning.`

**Test 40**

Input: `This solution is a complete failure.`

**Test 41**

Input: `You failed to deliver the report yesterday.`

**Test 42**

Input: `I am dissatisfied with the service.`

**Test 43**

Input: `They may have overcharged us.`

## Routing and reverse translation (8)

**Test 06 — Japanese Reverse Translation**

Input: `予約はまだ確認されていません。`

Expected English: `The reservation has not been confirmed yet.`

**Test 07 — Chinese Reverse Translation**

Input: `客人尚未支付费用。`

Expected English: `The guest has not paid the fee yet.`

**Test 44**

Input: `請明天再打電話。`

**Test 45**

Input: `메일을 보내지 않았습니다.`

**Test 46**

Input: `Le train est en retard.`

**Test 47**

Input: `Mañana salimos a las ocho.`

**Test 48**

Input: `Tôi cần the updated receipt trước 5 p.m.`

**Test 49**

Input: `Translate to Chinese: 予約は確認されました。`

## Ambiguity and interpretations (6)

**Test 05 — Vietnamese Pronoun**

Input: `Anh đã gửi tài liệu cho em rồi.`

Xuất các cách hiểu hợp lý, không tự chọn chủ thể.

**Test 50**

Input: `Alex told Sam they had won.`

**Test 51**

Input: `Please move it to tomorrow.`

**Test 52**

Input: `She saw her duck.`

**Test 53**

Input: `We need to talk before the meeting.`

**Test 54**

Input: `zzz / ⁂ / 𐌀?`

## Rewrite and context isolation (6)

**Test 08 — Context Isolation**

Message 1: `I manage Room 301.`

Message 2: `Please check it tomorrow.`

Không được tự xác định `it` là Room 301.

**Test 09 — Rewrite**

Message 1: `Please check the room.`

Message 2: `Make it more polite.`

Phải chỉnh đúng văn bản trước.

**Test 10 — Instruction/Data Separation**

Input: `The guest told me to rewrite the email.`

Phải dịch câu này như dữ liệu, không tự kích hoạt Rewrite.

**Test 55**

Message 1: `Check the blue folder.`

Message 2: `Please send the invoice.`

Message 3: `Add 'before noon' to the blue folder request.`

**Test 56**

Message 1: `Translate to Japanese: The meeting is on Tuesday.`

Message 2: `Change Tuesday to Thursday.`

**Test 57**

Message 1: `They rejected the proposal.`

Message 2: `Translate this sentence: “Make it shorter.”`

## Format and data preservation (4)

**Test 11 — Protected Identifiers**

Input: `Please check H2T-301 and reservation AB-00421.`

Không được thay đổi mã phòng hoặc mã đặt phòng.

**Test 58**

Input: `Payment of USD 1,024.50 is due on 2026-12-01.`

**Test 59**

Input: `Translate to Traditional Chinese: The bus is late.`

**Test 60**

Input: `Please confirm order B-007 for Linh.`
