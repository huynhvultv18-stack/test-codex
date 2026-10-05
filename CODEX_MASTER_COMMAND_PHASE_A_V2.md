# CODEX MASTER COMMAND --- PHASE A V2

## MATH CORE THCS V1.0 --- AUDIT + IMPLEMENTATION DESIGN ONLY

**MASTER SPEC:** `MATH_CORE_THCS_MASTER_SPEC_V1.0.md`\
**MASTER SPEC STATUS:** FROZEN / IMMUTABLE\
**PHASE:** A --- AUDIT + IMPLEMENTATION DESIGN ONLY\
**IMPLEMENTATION:** NOT STARTED\
**PRODUCTION:** PROHIBITED

## 1. Mục tiêu

Chỉ thực hiện **PHASE A**: audit toàn bộ evidence thực tế, ánh xạ MASTER
SPEC V1.0 sang kiến trúc có thể triển khai, xác định
REUSE/PATCH/EXTEND/CREATE NEW và lập kế hoạch Phase B.

**Không implement. Không tạo RC. Không Production.**

Kết thúc bằng đúng một trạng thái: -
`PHASE_A_STATUS = READY_FOR_REVIEW` - `PHASE_A_STATUS = BLOCKED`

Không chuyển Phase B nếu chưa có lệnh riêng:
`APPROVE PHASE B IMPLEMENTATION`.

## 2. Input thực tế và vai trò

### Normative Source of Truth

`MATH_CORE_THCS_MASTER_SPEC_V1.0.md`

-   Là Source of Truth đã FROZEN.
-   Không sửa, không làm yếu, không tự diễn giải lại.
-   Nếu phát hiện vấn đề:
    `ISSUE → SPEC_ISSUE_REPORT → PATCH PROPOSAL → REVIEW → NEW SPEC VERSION`.

### Curriculum evidence --- READ ONLY

-   `PPCT TOÁN 8.docx`
-   `SGK TOÁN 8 TẬP 1.pdf`

Không sửa PPCT/SGK. Không bịa scope, cấu trúc SGK, nguồn bài hay kiến
thức.

### Algebra reference evidence

`DAI_SO_8_TUAN_05_TIET_09_LIVE_RC3.zip`

Vai trò: `ALGEBRA_LIVE_REFERENCE_EVIDENCE`.

Không coi đây là Algebra SOẠN_TRƯỚC Core hay nguồn sư phạm chuẩn thay
MASTER SPEC.

### Geometry reference evidence

`HINH8_W05_TIET10_WEB_LIVE_PREP_PACKET_REVIEW_A2_1.zip`

Vai trò: `GEOMETRY_REFERENCE_EVIDENCE`.

Không mặc định đây là Geometry SOẠN_TRƯỚC Core. Chỉ dùng làm evidence về
lesson/figure/reasoning/package hiện có.

### WEB LIVE compatibility target

`WEB_LIVE_LESSON_LIBRARY_P12_1_CANDIDATE.zip`

Vai trò: `WEB_LIVE_COMPATIBILITY_TARGET`.

Audit contract thực tế. Không redesign/rebuild/patch P12.1 trong Phase
A. Ưu tiên adapter.

### README

`README.md` chỉ là repository metadata, không phải normative Math Core
input.

## 3. Baseline fact bắt buộc

``` text
EXISTING_ALGEBRA_SOAN_TRUOC_CORE = NOT_AVAILABLE
EXISTING_GEOMETRY_SOAN_TRUOC_CORE = NOT_AVAILABLE
```

Hai PREP Core này **không phải input bắt buộc của Phase A**.

Do đó: - Không tìm vô hạn. - Không báo hồ sơ thiếu chỉ vì chúng không
tồn tại. - Không đồng nhất LIVE package với PREP Core. - Không tự tạo
giả một baseline PREP. - Thiết kế Math Core/SOẠN_TRƯỚC mới từ MASTER
SPEC; LIVE/PREP packet hiện có chỉ là reference evidence.

Target:

`SGK + PPCT → WORK/CURRICULUM CONTEXT → MATH CORE → SOẠN_TRƯỚC → CANONICAL LESSON → BẢN HS / BẢN GV / LIVE PACKAGE → WEB LIVE P12.1`

## 4. Nguyên tắc kiến trúc

Áp dụng: - `REUSE > PATCH > EXTEND > CREATE_NEW` -
`ONE_RULE → ONE_SOURCE_OF_TRUTH` - `WORK_DOES_NOT_PATCH_CORE` -
`WEB_LIVE_DOES_NOT_REWRITE_PEDAGOGY` - `OFFLINE_PACKAGE_FIRST` -
`NO_DIRECT_LIVE_DEPENDENCY` -
`IF_SOURCE_OR_SCOPE_IS_UNCERTAIN → BLOCK/REPORT → DO_NOT_GUESS` -
`PPCT/SGK/SBT = READ_ONLY` - `FROZEN_SPEC = IMMUTABLE`

Không rebuild downstream system đang hoạt động nếu adapter giải quyết
được compatibility.

## 5. Audit và mapping bắt buộc

Map MASTER SPEC vào các logical components:

1.  Curriculum Guard
2.  Objective Model
3.  Domain Engine --- Algebra / Geometry
4.  Lesson Type Engine
5.  Differentiation Engine
6.  Assessment Engine
7.  Task Engine
8.  Support Model
9.  Diagnostic Model
10. Time Engine
11. Lesson State Machine
12. Math Representation Standard
13. Geometry Figure Standard
14. Reasoning Representation
15. Canonical Lesson Model
16. Output Contract
17. Validation Engine
18. P12.1 Package Adapter
19. Golden Tests
20. Regression Tests
21. Governance / Version / Freeze / Traceability

Với mỗi component xác định: owner, inputs, outputs, dependencies,
validation responsibility, evidence hiện có, reuse status,
implementation recommendation, risks và test strategy.

## 6. Curriculum Guard

Thiết kế phải hỗ trợ: - `PPCT_SCOPE_LOCK` - `SGK_STRUCTURE_LOCK` -
`NO_TEACH_AHEAD` - `ALLOWED_KNOWLEDGE` - `FORBIDDEN_KNOWLEDGE` -
prerequisite dependency - home-prep-to-class bridge - source integrity -
solution method boundary

Toán 8 chỉ là evidence Phase A; kiến trúc phải mở rộng được THCS 6--9.

## 7. Canonical Lesson Model

Thiết kế **một** Canonical Lesson Model làm semantic source cho: - BẢN
HS - BẢN GV - WEB LIVE PACKAGE

Không tạo ba lesson sources độc lập.

Model phải hỗ trợ metadata/scope, objective, prerequisite/readiness,
lesson type, domain, student profile, activities, tasks, questions,
expected evidence, misconceptions, scaffold/intervention, formalization,
assessment checkpoints, time contract, student product, completion
evidence, math/geometry semantics, reasoning, traceability, version và
validation state.

Teacher-only data phải tách được khỏi Student View.

## 8. P12.1 Package Adapter

Thiết kế:

`CANONICAL LESSON MODEL → WEB_LIVE_PACKAGE_ADAPTER → *_LIVE.zip`

Kiểm chứng contract thực tế của P12.1, gồm khi phù hợp: -
`manifest.json` - `lesson.json` - assets/images - metadata/screens -
question/hint/answer - teacher note - geometry - analysisSteps /
analysisDiagram - scene persistence - progressive disclosure

Không ép Canonical Model dùng legacy schema của P12.1. Adapter chỉ map
semantics sang consumer contract.

Ngoài phạm vi Math Core: TV sync, BroadcastChannel, TTS, drawing
runtime, launcher, Word/GeoGebra demo, animation, browser storage,
Chrome behavior, teacher modal.

## 9. Validation + Severity

Thiết kế 2 tầng:

**Tier 1 --- Math Core Semantic Validation:** math correctness,
PPCT/SGK/no-teach-ahead, source integrity, objectives, prerequisite,
pedagogy, lesson type, differentiation, assessment, tasks/method
boundaries, time ≤45, math representation, geometry relations, HS/GV
leakage, traceability, state/completion, freeze/version.

**Tier 2 --- Package/P12.1 Validation:** ZIP structure, manifest,
lesson.json, required fields/schema, assets, safe paths, verified
size/format constraints, contract version và import compatibility.

Severity: - `HARD_FAIL = BLOCK` - `QUALITY_FAIL = REVISE` -
`WARNING = REVIEW` - `INFO = LOG`

HARD_FAIL không được Work/P12.1 waive.

## 10. Version / Freeze / Traceability

Thiết kế: - `CORE_VERSION` - `LESSON_SCHEMA_VERSION` -
`WEB_LIVE_CONTRACT_VERSION` - `PACKAGE_CONTRACT_VERSION` - RC/candidate
identity - hashes - frozen state - semantic revalidation

Semantic edit ở task/answer/question/formalization/method/geometry
relation phải làm validation cũ thành stale.

Traceability:
`DISPLAY/PACKAGE STEP ← ACTIVITY ← OBJECTIVE ← SGK SECTION ← PPCT SCOPE`

## 11. Test Design

Lập kế hoạch trước khi implementation: unit, schema, validator,
curriculum guard, math representation, geometry, leakage, time engine,
package adapter, P12.1 compatibility và regression tests.

Thiết kế 10--16 Golden Lessons tương lai bao phủ Algebra/Geometry, new
knowledge/practice/review, profiles, prerequisite gap, misconception
repair, figure/reasoning, compression, no-teach-ahead và package
generation.

Không tạo citation SGK giả để hoàn thành Golden Lessons.

## 12. 10 báo cáo bắt buộc

1.  `01_MATH_CORE_EXISTING_ASSET_AUDIT.md`
2.  `02_MASTER_SPEC_IMPLEMENTATION_MAP.md`
3.  `03_REUSE_PATCH_NEW_MATRIX.md`
4.  `04_PROPOSED_IMPLEMENTATION_ARCHITECTURE.md`
5.  `05_CANONICAL_LESSON_MODEL_DESIGN.md`
6.  `06_VALIDATION_SEVERITY_DESIGN.md`
7.  `07_TEST_AND_GOLDEN_PLAN.md`
8.  `08_P12_1_PACKAGE_ADAPTER_DESIGN.md`
9.  `09_IMPLEMENTATION_RISK_REGISTER.md`
10. `10_PHASE_B_IMPLEMENTATION_PLAN.md`

Report 01 phải ghi rõ:

``` text
MASTER_SPEC_FOUND = YES/NO
MASTER_SPEC_FROZEN = YES/NO
PPCT_EVIDENCE_FOUND = YES/NO
SGK_EVIDENCE_FOUND = YES/NO
ALGEBRA_LIVE_REFERENCE_FOUND = YES/NO
GEOMETRY_REFERENCE_FOUND = YES/NO
WEB_LIVE_P12_1_FOUND = YES/NO
EXISTING_ALGEBRA_SOAN_TRUOC_CORE = NOT_AVAILABLE
EXISTING_GEOMETRY_SOAN_TRUOC_CORE = NOT_AVAILABLE
```

## 13. REUSE/PATCH/NEW Matrix

Mỗi component phải được phân loại: `REUSE`, `PATCH`, `EXTEND`,
`CREATE_NEW`, `EXTERNAL`, `REFERENCE_ONLY`, hoặc `NOT_APPLICABLE`.

Mỗi phân loại phải có evidence. Không đánh dấu REUSE chỉ vì LIVE có
field cùng tên.

## 14. Stop conditions

`BLOCKED` nếu: không đọc được frozen spec; critical spec conflict cần
sửa spec; evidence cần thiết bị hỏng/không đọc được; P12.1 contract
không thể kiểm chứng đủ; cần đoán curriculum/math; cần sửa PPCT/SGK/SBT;
cần sửa frozen spec; cần sửa P12.1; hoặc architecture không thể đáp ứng
HARD rule.

**Sự vắng mặt của Algebra/Geometry SOẠN_TRƯỚC Core không phải blocker.**

Khi BLOCKED: nêu blocker chính xác, evidence cần bổ sung, không tự
workaround.

## 15. Hành động bị cấm

Trong Phase A không: - implement production code; - refactor ngoài phạm
vi; - tạo RC/Production; - patch frozen Master Spec; - sửa
PPCT/SGK/SBT; - patch WEB LIVE P12.1; - bịa curriculum/SGK references; -
bịa PREP baseline; - silently resolve spec conflict; - redesign WEB
LIVE; - tạo direct runtime dependency Core↔Live; - suy luận quan hệ hình
học từ hình vẽ; - hạ HARD_FAIL vì tiện triển khai.

## 16. Exit Gate

Trước `READY_FOR_REVIEW`, xác nhận:

``` text
MASTER_SPEC_MUTATED = NO
PPCT_MUTATED = NO
SGK_MUTATED = NO
WEB_LIVE_P12_1_MUTATED = NO

IMPLEMENTATION_CODE_CREATED = NO
PRODUCTION_CREATED = NO
RC_CREATED = NO

ALL_10_REPORTS_CREATED = YES
ARCHITECTURE_MAPPED = YES
OWNERSHIP_MAPPED = YES
VALIDATION_DESIGNED = YES
TEST_PLAN_DESIGNED = YES
CANONICAL_MODEL_DESIGNED = YES
P12_1_ADAPTER_DESIGNED = YES

UNRESOLVED_CRITICAL_CONFLICTS = 0
UNRESOLVED_HARD_ARCHITECTURE_BLOCKERS = 0
```

Nếu đạt: `PHASE_A_STATUS = READY_FOR_REVIEW`

Nếu không: `PHASE_A_STATUS = BLOCKED`

## 17. Final Handoff

Cuối Phase A báo cáo ngắn: - status; - repository/commit inspected; -
input inventory; - 10 reports produced; - major reuse decisions; - major
create-new decisions; - unresolved risks; - proposed Phase B scope; -
xác nhận không implementation/production change.

**STOP.**

Chờ lệnh riêng:

`APPROVE PHASE B IMPLEMENTATION`
