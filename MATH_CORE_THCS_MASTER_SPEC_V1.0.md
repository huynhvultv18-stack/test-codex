# MATH CORE THCS — MASTER SPEC V1.0

**Status:** FROZEN  
**Baseline:** LOCKED  
**Final Review:** PASS  
**Integrated Spec Patches:** 18/18  
**Codex implementation:** NOT STARTED  
**Production:** PROHIBITED until explicit approval

> This document is the normative Source of Truth for MATH CORE THCS V1.0.  
> Codex/Work/WEB LIVE must not silently reinterpret, weaken, or modify this frozen baseline.

---

## 0. PURPOSE AND SYSTEM BOUNDARY

MATH CORE THCS supports lower-secondary Mathematics (grades 6–9), with Algebra and Geometry as domain engines. Its purpose is to generate curriculum-grounded, pedagogically valid lesson packages while preserving SGK/PPCT progression.

Official delivery model:

```text
SGK + PPCT
    ↓
WORK — CURRICULUM GROUNDING
    ↓
LESSON CONTEXT
    ↓
MATH CORE THCS
    ↓
CANONICAL LESSON MODEL
    ↓
STRICT VALIDATION
    ↓
BẢN HS / BẢN GV / P12.1 PACKAGE ADAPTER
    ↓
manifest.json + lesson.json + images/assets
    ↓
*_LIVE.zip
    ↓
VALIDATE + FREEZE
════════════════ SYSTEM BOUNDARY ════════════════
    ↓
USER MANUAL IMPORT
    ↓
WEB LIVE P12.1
```

**OFFLINE_PACKAGE_FIRST.** There is no required direct-live connection between MATH CORE and WEB LIVE.

### Immutable architecture principles

1. `ONE_RULE_ONE_SOURCE_OF_TRUTH`
2. `WORK_DOES_NOT_PATCH_CORE`
3. `CODEX_DOES_NOT_EDIT_SGK_PPCT_SBT`
4. `WEB_LIVE_DOES_NOT_REWRITE_PEDAGOGY`
5. `NO_DIRECT_LIVE_DEPENDENCY`
6. `NO_GUESS`: uncertain source/scope → BLOCK/REPORT
7. `FROZEN_MEANS_IMMUTABLE`
8. `SOAN_TRUOC_TOTAL_TIME <= 45 MIN`

---

# LAYER 1 — FOUNDATION

## 1. Teaching philosophy

Mathematics learning targets four levels:

**KIẾN THỨC → KỸ NĂNG → TƯ DUY TOÁN HỌC → NĂNG LỰC GIẢI QUYẾT VẤN ĐỀ**

For each new knowledge item, the lesson should answer:
1. Why learn it?
2. How can the knowledge be discovered/constructed?
3. What can it be used for?

Reference learning path:

**NHU CẦU → KHÁM PHÁ → KIẾN THỨC → SỬ DỤNG**

Reference student activity chain:

**Tò mò → Quan sát → Suy nghĩ → Dự đoán → Trao đổi → Phát hiện → GV chuẩn hóa → Kiểm tra hiểu → Vận dụng**

Student role may include:
**Quan sát → Suy nghĩ → Dự đoán → Thử → Trao đổi → Phát hiện → Giải thích → Vận dụng → Tự kiểm tra**

Teacher role includes: designing the learning path, creating learning need, selecting situations/data, questioning, controlling scaffolds, diagnosing misconceptions, intervening when needed, formalizing knowledge, checking understanding, and connecting knowledge.

Rules:
- `DO_NOT_TELL_IF_DISCOVERABLE`
- `TEACHER_INTERVENTION_IF_NEEDED`

Teacher intervention is justified when prerequisites are missing, misconceptions persist, discovery is taking too long, content is unsuitable for discovery, or exact formalization is required.

### Mathematical understanding model

A correct answer alone is insufficient evidence of understanding.

Reference dimensions:
`RECOGNIZE → UNDERSTAND_MEANING → REPRESENT → EXPLAIN/REASON → APPLY → DETECT_ERROR → TRANSFER`

Assessment evidence may use:
- U1 Recognition
- U2 Meaning
- U3 Representation
- U4 Apply
- U5 Explain
- U6 Analyze/fix error
- U7 Transfer

## 2. Objective Model

Every core learning objective must be measurable and traceable.

Minimum fields:
- `OBJECTIVE_ID`
- `KNOWLEDGE`
- `EXPECTED_ACTION`
- `UNDERSTANDING_LEVEL`
- `SUCCESS_EVIDENCE`
- `MINIMUM_STANDARD`

Trace:
`OBJECTIVE → SUCCESS_CRITERIA → EXPECTED_EVIDENCE`

## 3. Rule precedence

When valid rules compete, use:

1. MATHEMATICAL CORRECTNESS
2. CURRICULUM / PPCT / NO_TEACH_AHEAD
3. SGK STRUCTURE / KNOWLEDGE DEPENDENCY
4. LEARNING OBJECTIVE
5. STUDENT UNDERSTANDING / PEDAGOGY
6. DIFFERENTIATION
7. TIME OPTIMIZATION
8. WEB LIVE PRESENTATION
9. VISUAL / MOTION / AESTHETICS

The 45-minute limit remains a hard constraint; precedence determines what is modified/cut to remain valid.

---

# LAYER 2 — CURRICULUM & PEDAGOGY

## 4. Curriculum Guard

Source of truth:

`PPCT + SGK + ACTUAL PROGRESS → CURRENT_LESSON_SCOPE`

Required lesson context includes:
- GRADE
- DOMAIN
- WEEK
- PERIOD
- LESSON
- LESSON_TYPE
- STUDENT_PROFILE
- CURRENT_SCOPE
- PREVIOUS_SCOPE
- NEXT_SCOPE
- PRIOR_KNOWLEDGE
- CURRENT_SGK_SCOPE
- SGK_SECTION_ORDER
- LEARNING_OBJECTIVES
- ALLOWED_KNOWLEDGE
- FORBIDDEN_KNOWLEDGE
- HOME_PREP_CONTEXT
- TIME = 45

### Locks

`PPCT_SCOPE_LOCK`  
`SGK_STRUCTURE_LOCK`  
`NO_TEACH_AHEAD`  
`KNOWLEDGE_BOUNDARY_CHECK`  
`SOLUTION_METHOD_BOUNDARY`  
`SOURCE_INTEGRITY`

Pedagogy may enrich the SGK path but must not replace its knowledge dependency/order or current scope.

If source/scope/figure relation is uncertain:
`BLOCKED → REPORT → DO NOT GUESS`

SBT is supplementary, not curriculum Source of Truth.

## 5. Prerequisite Dependency

Distinguish:
- `REQUIRED_PREREQUISITE`
- `HELPFUL_PRIOR_KNOWLEDGE`

Flow:
`CURRENT_KNOWLEDGE → REQUIRED_PREREQUISITES → READINESS_CHECK → READY/PARTIAL_READY/NOT_READY`

Only required prerequisites trigger repair.

Small gap:
`MICRO_REPAIR → RETRY → VERIFY`

Large gap:
`PREREQUISITE_GAP_TOO_LARGE`

## 6. Domain Engine — Algebra

Reference path:

`CONTEXT → REPRESENT → OBSERVE_STRUCTURE → COMPARE → PREDICT_PATTERN → TEST → GENERALIZE → FORMALIZE → TRANSFORM → CHECK_EQUIVALENCE → APPLY`

Algebra-specific error extensions may include:
- SIGN
- TRANSFORMATION
- EQUIVALENCE

## 7. Domain Engine — Geometry

Reference path:

`VISUAL_PROBLEM/FIGURE → OBSERVE → MANIPULATE/MEASURE/COMPARE → PREDICT → TEST → IDENTIFY_RELATION → REASON → PROVE/JUSTIFY → FORMALIZE → APPLY_ON_FIGURE`

Principle:

**HÌNH → QUAN SÁT → DỰ ĐOÁN → LẬP LUẬN → KẾT LUẬN → VẬN DỤNG TRỞ LẠI HÌNH**

`FIGURE_FIRST` does not mean `FIGURE_ONLY`.

A figure may support conjecture but visual appearance is never proof.

Figure lifecycle:
`FIGURE_CREATE → OBSERVE → MARK_GIVEN → PREDICT → ADD_VERIFIED/DERIVED_RELATION → REASON → FORMALIZE → SOLVE`

## 8. Lesson Type Engine

### NEW_KNOWLEDGE
`PRIOR_KNOWLEDGE → WHY_LEARN → PROBLEM/CURIOSITY → OBSERVE → THINK → PREDICT → EXPLORE → DISCUSS → DISCOVER → TEACHER_FORMALIZE → CHECK_UNDERSTANDING → PRACTICE → TRANSFER → SELF_ASSESS`

Not every node is mandatory if SGK/content does not support it.

### PRACTICE
`QUICK_RECALL → KNOWLEDGE_MAP/RECOGNIZE_PROBLEM → SELECT_METHOD → SOLVE → EXPLAIN_WHY → ERROR_ANALYSIS → COMPARE_METHODS → VARIATION → TRANSFER → SELF_ASSESS`

### CHAPTER_REVIEW
`RETRIEVE → CONNECT → KNOWLEDGE_MAP → COMPARE → CLASSIFY → SELECT_TOOL → INTEGRATED_PROBLEM → ERROR_DIAGNOSIS → KNOWLEDGE_GAP → REPAIR`

### SEMESTER_REVIEW
`GLOBAL_RETRIEVAL → KNOWLEDGE_NETWORK → CORE_KNOWLEDGE → DIAGNOSTIC_CHECK → GAP_DETECTION → TARGETED_REPAIR → MIXED_PROBLEMS → STRATEGY_SELECTION → EXAM_TRANSFER → SELF_EVALUATION`

Future extensibility:
`ASSESSMENT_REPAIR: RESULT → ERROR_CLASSIFICATION → ROOT_CAUSE → KNOWLEDGE_GAP → TARGETED_RETEACH → RETRY → VERIFY`

## 9. Minimum Valid Lesson

Each lesson type defines `NON_NEGOTIABLE_COMPONENTS`.

For NEW_KNOWLEDGE, minimum normally includes:
- entry/prior connection
- core discovery/knowledge formation appropriate to SGK
- formalization
- core understanding check
- independent attempt
- final evidence/check

If emergency compression would remove a non-negotiable component:
`LESSON_DESIGN_FAIL`

## 10. Differentiation Engine

Rule:

**DIFFERENTIATE THE PATH — NOT THE CURRICULUM**

Dimensions are separate:
- STUDENT_PROFILE
- COGNITIVE_DEPTH
- SCAFFOLD_LEVEL
- OPENNESS

Cognitive depth:
D1 Recognize; D2 Understand; D3 Apply; D4 Analyze; D5 Justify; D6 Generalize; D7 Create.

Scaffold:
S3 High; S2 Medium; S1 Low; S0 Independent.

Reference profiles:

**YẾU:** small steps → concrete/visual → guided → partial worked support → try → feedback → independent retry. Scaffold must fade.

**TB:** observe → think → guided discovery → formalize → basic practice → variation → independent application.

**KHÁ:** problem → predict → self-discovery → explain → multiple methods → error analysis → variation → transfer.

**GIỎI:** open problem → conjecture → multiple strategies → justification → generalization → counterexample → condition change → create problem.

Advanced students are challenged by depth, justification, openness, multiple methods, condition change and generalization — not future-grade curriculum.

Mixed class:
`CORE TASK → SUPPORT / STANDARD / CHALLENGE`

Do not publicly label students on WEB LIVE.

## 11. Assessment Engine

Assessment is embedded, not additive:
`ASSESSMENT_IS_EMBEDDED_NOT_ADDITIVE`

Possible checkpoints:
- PRIOR
- DISCOVERY
- FORMALIZATION
- PRACTICE
- TRANSFER/EXIT

Not all are mandatory in every lesson.

Evidence loop:
`QUESTION → RESPONSE → EVIDENCE → DIAGNOSIS → INTERVENTION → RETRY → VERIFY`

Discovery check:
`OBSERVATION + PREDICTION + EVIDENCE`

Practice should distinguish:
- CAN_EXECUTE
- CAN_SELECT_METHOD

Reference independence progression:
`GUIDED → SEMI_GUIDED → NO_METHOD_HINT`

Error analysis:
`LOCATE → EXPLAIN → CORRECT`

Mastery:
- MASTERED → continue
- PARTIAL → targeted support
- NOT_YET → repair/retry

AI diagnosis safety:
`OBSERVE → HYPOTHESIZE_ERROR → VERIFY → INTERVENE`

Never diagnose a misconception from one wrong answer without verification.

## 12. Task Engine

Every task has `TASK_PURPOSE`.

Source priority:
1. SGK
2. SGK_VARIATION
3. SBT
4. CORE_GENERATED_TASK

Never fake SGK/SBT attribution.

Reference task taxonomy:
- T0 PRIOR_KNOWLEDGE
- T1 DISCOVERY
- T2 CONCEPT_CHECK
- T3 WORKED_EXAMPLE
- T4 GUIDED_PRACTICE
- T5 INDEPENDENT_PRACTICE
- T6 ERROR_ANALYSIS
- T7 VARIATION
- T8 TRANSFER
- T9 CHALLENGE
- T10 EXIT_CHECK

Not all are mandatory.

Task metadata:
- TASK_ID
- SOURCE
- SOURCE_REFERENCE
- TASK_TYPE
- TASK_PURPOSE
- REQUIRED_KNOWLEDGE
- ALLOWED_METHODS
- FORBIDDEN_METHODS
- COGNITIVE_DEPTH
- SCAFFOLD_LEVEL
- EXPECTED_TIME
- ANSWER
- SOLUTION_PATH
- COMMON_ERRORS

Geometry may add:
- FIGURE_REQUIRED
- FIGURE_SOURCE
- FIGURE_RELATIONS

Task Selection:
`OBJECTIVE + LESSON_TYPE + PROFILE + SGK_STRUCTURE + KNOWLEDGE_BOUNDARY + TIME → CANDIDATES → CHECKS → SELECT`

## 13. Support Model

Scaffold, hint and intervention are related but not identical.

### Hint ladder
H0 NONE → H1… → H5 PARTIAL STEP

### Intervention ladder
I0 WAIT  
I1 REPEAT/FOCUS  
I2 QUESTION  
I3 HINT  
I4 PARTIAL STRUCTURE  
I5 WORKED STEP  
I6 EXPLICIT TEACHER EXPLANATION

Use the lowest effective intervention.

## 14. Diagnostic Model

Common error taxonomy:
- CONCEPT
- REPRESENTATION
- METHOD
- LOGIC
- CALCULATION
- CONDITION

Algebra extensions:
- SIGN
- TRANSFORMATION
- EQUIVALENCE

Geometry extensions:
- FIGURE_READING
- RELATION
- PROOF_LOGIC

Error ≠ misconception.

Flow:
`ERROR_TYPE → MISCONCEPTION_HYPOTHESIS → VERIFY → REPAIR → RETRY`

Misconception record:
- MISCONCEPTION_ID
- KNOWLEDGE_ID
- LIKELY_WRONG_IDEA
- OBSERVABLE_RESPONSE
- DIAGNOSTIC_QUESTION
- REPAIR_STRATEGY
- VERIFY_TASK

---

# LAYER 3 — LESSON EXECUTION MODEL

## 15. Lesson State Machine

Reference runtime logic:

`ACTIVITY → CHECKPOINT → MASTERED/PARTIAL/NOT_YET`

- MASTERED → NEXT
- PARTIAL → SCAFFOLD → RETRY
- NOT_YET → MICRO_REPAIR → RETRY
- then VERIFY

Invalid state transitions that claim mastery/completion without evidence are not permitted.

## 16. 45-Minute Time Engine

Hard rules:
- SOẠN_TRƯỚC total time ≤ 45 minutes
- WEB LIVE lesson plan target = 45 minutes
- NO_AUTO_TIME_FILL
- NO_HIDDEN_TIME
- NO_NEGATIVE_TIME

No universal rigid split.

Time plan derives from:
`LESSON_TYPE + SGK_STRUCTURE + OBJECTIVE + PROFILE`

Each activity may carry:
- ACTIVITY_ID
- MIN_TIME
- TARGET_TIME
- MAX_TIME
- PRIORITY
- FLEXIBILITY
- CAN_COMPRESS
- CAN_SKIP
- CAN_MOVE_TO_HOME
- COMPRESSION_STRATEGY

Priority:
P0 ESSENTIAL  
P1 IMPORTANT  
P2 EXTENSION  
P3 OPTIONAL

Cut order:
optional → extension → repetition → shorten discussion.

Protect:
core knowledge/discovery, formalization, core practice, core understanding check.

Compression:
C0 NORMAL  
C1 LIGHT  
C2 MODERATE  
C3 EMERGENCY

C3 must retain:
- core knowledge
- formalization
- one core practice
- one core check

If minimum valid lesson cannot fit:
`TIME_DESIGN_FAIL`

## 17. Teacher Override Governance

Teacher may:
- skip optional work
- select support/standard/challenge
- repeat
- reveal/delay hints
- extend within available time
- pause/navigate

Teacher runtime authority is not spec rewrite authority.

An override cannot remain “spec valid” if it:
- teaches ahead
- changes mathematical meaning
- bypasses required core formalization while claiming completion
- leaks teacher-only data
- uses a forbidden method

Runtime adaptation is recorded as evidence; the system does not grade the teacher.

## 18. Lesson Completion Evidence

`LESSON_COMPLETED ≠ ALL_SLIDES_SHOWN`

`PEDAGOGICAL_COMPLETION > DISPLAY_COMPLETION`

Completion record:
- OBJECTIVES_COVERED
- CORE_KNOWLEDGE_FORMALIZED
- CORE_TASK_COMPLETED
- UNDERSTANDING_EVIDENCE
- UNRESOLVED_GAPS
- HOME_FOLLOWUP
- TIME_ACTUAL

A design can be valid while a runtime lesson remains incomplete.

---

# LAYER 4 — REPRESENTATION & OUTPUT

## 19. Math Representation Standard

Canonical mathematical meaning comes first; renderers display it.

Required support includes:
- vertical fractions
- superscripts
- radicals covering full radicand
- wide-angle notation
- systems
- inequalities
- sets
- absolute value
- parallel/perpendicular
- congruent/similar triangles
- units
- equivalence/implication where curriculum allows

Current SGK notation has priority for the current lesson.

Semantic notation errors that change meaning may be HARD_FAIL. Cosmetic presentation issues are lower severity.

## 20. Geometry Figure Standard

If SGK supplies a figure, its named points and mathematical relations are Source of Truth.

Do not rename points or alter relations merely for aesthetics.

Markers:
- right-angle square
- equal-segment ticks
- parallel arrows
- equal-angle arcs
- distinguish separate angle groups

`NO_DECORATIVE_GEOMETRY_MARKS`

A marker may represent only a relation that is GIVEN, VERIFIED or PROVED at the current state.

`NO_FIGURE_SPOILER`

## 21. Reasoning Representation

Proof analysis diagram:

`KẾT LUẬN ⇑ Ý CHÍNH ⇑ DỮ KIỆN`

Direction: UP / DOUBLE / CENTER / KEY_REASONING.

Calculation guidance:

`DỮ KIỆN ⇓ QUAN HỆ/CÔNG THỨC ⇓ KẾT QUẢ`

Direction: DOWN / DOUBLE / CENTER.

Default display is minimal:
`KEY_REASONING_ONLY`

Supporting reasoning may be revealed as scaffold.

Reasoning representation is not the Hint Engine; Support Model controls how much is revealed.

## 22. Canonical Lesson Model

One authoritative lesson source generates all views.

Metadata:
- GRADE
- DOMAIN
- WEEK
- PERIOD
- LESSON
- LESSON_TYPE
- STUDENT_PROFILE
- SGK_SCOPE
- PRIOR_KNOWLEDGE
- TIME_BUDGET

Learning Contract:
- LEARNING_OBJECTIVES
- CORE_KNOWLEDGE
- CORE_SKILLS
- MATHEMATICAL_THINKING
- EXPECTED_STUDENT_PRODUCT
- SUCCESS_CRITERIA

HOME_PREP:
- READ
- OBSERVE
- TRY
- PREDICT
- QUESTION
- PREP_TO_CLASS_LINK

Each activity may contain:
- ACTIVITY_ID
- PURPOSE
- TIME
- SGK_REFERENCE
- TEACHER_ACTION
- STUDENT_ACTION
- QUESTION
- EXPECTED_RESPONSE
- MISCONCEPTION
- SCAFFOLD
- FORMALIZATION
- STUDENT_PRODUCT
- CHECK_UNDERSTANDING

Do not fabricate irrelevant fields.

## 23. BẢN HS

Student View may contain:
- situation
- question
- figure
- data
- task
- response area
- permitted hints/diagram
- suitable self-check

Must not leak:
- ANSWER
- TEACHER_NOTE
- EXPECTED_RESPONSE
- INTERNAL_VALIDATION
- audit/debug metadata

## 24. BẢN GV

`TEACHER_VIEW = STUDENT_VIEW + TEACHER_LAYER`

Teacher layer may add:
- ANSWER
- SOLUTION
- EXPECTED_RESPONSE
- MISCONCEPTION
- QUESTIONING_PATH
- SCAFFOLD_PATH
- TEACHER_INTERVENTION
- FORMALIZATION
- TIME_CONTROL

`HS_GV_STRUCTURE_PARITY` is required.

ANSWER ≠ SOLUTION ≠ FORMALIZATION.

## 25. WEB LIVE Lesson Package / Import Contract

WEB LIVE P12.1 is an existing consumer.

Official delivery unit:
`WEB_LIVE_LESSON_PACKAGE (.zip)`

Target structure:

```text
*_LIVE.zip
├── manifest.json
├── lesson.json
└── images/assets/
```

The Package Adapter maps the Canonical Lesson Model to P12.1-compatible fields.

The adapter may map canonical fields to legacy duplicates if required for compatibility, but legacy duplication must not pollute the Canonical Model.

Math Core does not own:
- TV layout ratios
- TV typography
- focus implementation
- animation implementation
- BroadcastChannel
- localStorage
- TTS
- Launcher
- Word/GeoGebra demo runtime
- browser-specific controls

WEB LIVE owns import, storage, lesson selection, rendering, reveal/focus/navigation, TV sync, drawing/demo/runtime UI.

Core owns mathematical/pedagogical semantics. WEB LIVE must not change mathematical meaning.

### Progressive disclosure contract

Core/package may provide semantic states/data for:
`QUESTION → THINK/WAIT → HINT → RESPONSE → ANSWER → FORMALIZATION`

WEB LIVE owns hide/reveal/focus behavior.

### Geometry package mapping

Canonical geometry semantics/lifecycle may map to P12.1 constructs such as:
- sceneId
- visualRole
- geometry
- analysisSteps
- analysisDiagram
- image/assets

Reuse the existing P12.1 geometry/runtime capabilities where compatible; do not rebuild them in Math Core.

## 26. Package Validation

Math Core/Work validation is strict before packaging.

Package validation includes:
- PACKAGE_SCHEMA
- MANIFEST_VALID
- LESSON_JSON_VALID
- ASSET_EXISTS
- ASSET_SUPPORTED
- ASSET_SIZE
- ZIP_STRUCTURE
- P12_1_COMPATIBILITY
- NO_STUDENT_ANSWER_LEAK
- NO_TEACHER_METADATA_LEAK
- MATH_RENDER_CONTRACT
- FIGURE_ASSET_CONTRACT

WEB LIVE importer remains backward-compatible and protects import/runtime; it is not responsible for re-running full pedagogy validation.

`PACKAGE_READY = YES` only after required validation passes.

## 27. Offline Package First

`OFFLINE_PACKAGE_FIRST`

MATH CORE/Work must not require a direct connection to WEB LIVE.

The lesson must be independently:
`GENERATED → VALIDATED → PACKAGED → FROZEN`

before the user manually imports it into WEB LIVE.

`NO_DIRECT_LIVE_DEPENDENCY`

---

# LAYER 5 — GOVERNANCE

## 28. Validation Severity

Exactly four levels:

### HARD_FAIL
Blocks candidate/package/release.

Typical causes:
- false mathematical statement
- wrong answer/invalid proof
- false geometry relation
- PPCT scope violation
- teach-ahead
- forbidden knowledge/method
- fake SGK/SBT attribution
- student answer leak
- teacher/internal metadata leak
- semantic notation corruption
- time design >45 / impossible minimum lesson
- invalid mastery/completion claim
- forbidden write
- frozen artifact mutation
- canonical rule conflict

### QUALITY_FAIL
Must be revised/reviewed before official readiness according to release policy.

Examples:
- lesson type mismatch
- student profile mismatch
- weak objective alignment in auxiliary content
- insufficient assessment evidence
- bad/no scaffold fade
- disconnected home prep
- unrealistic time estimate
- reasoning overload
- poor readability

### WARNING
Non-blocking review item.

### INFO
Runtime/audit/telemetry only.

Severity may escalate based on consequence:
`SEMANTIC CONSEQUENCE > ERROR LABEL`

## 29. Release Gates

Lesson validation, RC release and Production release are distinct.

RC:
- HARD_FAIL = 0
- quality issues documented/controlled according to policy

Production:
- HARD_FAIL = 0
- OPEN_CRITICAL_QUALITY_FAIL = 0
- GOLDEN_REGRESSION = PASS
- WORK_PILOT = PASS
- explicit project-owner approval

Never auto-promote Production.

## 30. Ownership

### CODEX / CORE owns standards/rules
- MATH_PEDAGOGY_SPEC
- CURRICULUM_GUARD
- OBJECTIVE_MODEL
- DOMAIN_ENGINE
- LESSON_TYPE_ENGINE
- DIFFERENTIATION_ENGINE
- ASSESSMENT_ENGINE
- TASK_ENGINE
- SUPPORT_MODEL
- DIAGNOSTIC_MODEL
- TIME_ENGINE
- LESSON_STATE_MACHINE
- MATH_REPRESENTATION_STANDARD
- GEOMETRY_FIGURE_STANDARD
- REASONING_REPRESENTATION
- OUTPUT_CONTRACT
- VALIDATION_ENGINE
- GOLDEN/REGRESSION TESTS

Codex builds the system, not hundreds of actual curriculum lessons.

### WORK owns actual curriculum application/instances
- curriculum mapping process
- PPCT map
- SGK structure map
- lesson context
- current scope
- actual prior-knowledge context
- actual home-prep content
- lesson composition
- BẢN HS
- BẢN GV
- WEB LIVE output package
- pilot evidence
- Core issue reports

Work may edit a lesson instance if Core validation still passes. Work may not weaken/bypass Core rules.

### WEB LIVE owns presentation/runtime
- import
- storage
- layout
- typography
- focus/reveal/navigation
- zoom/fullscreen
- figure display state
- animation/transitions
- teacher controls
- runtime display state
- TV synchronization and application-specific runtime features

### Teacher runtime
May control the real lesson, but runtime authority does not rewrite the frozen specification.

## 31. Write Authority Matrix

Allowed:
- Codex → CORE SOURCE / SCHEMA / TESTS / VALIDATORS
- Work → CURRICULUM MAP / LESSON INSTANCE / HS-GV OUTPUT / PACKAGE / PILOT REPORT / CORE ISSUE REPORT
- WEB LIVE → UI/DISPLAY/RUNTIME STATE / PRESENTATION SETTINGS

Forbidden:
- WORK → CORE SOURCE
- WEB_LIVE → CORE CONTENT
- WEB_LIVE → MATH SEMANTICS
- CORE → SGK/PPCT/SBT SOURCE
- WORK → SGK/PPCT/SBT SOURCE
- RUNTIME → FROZEN CANDIDATE

## 32. Traceability

Required chain:

`PPCT_REF → SGK_REF → OBJECTIVE_ID → ACTIVITY_ID → TASK_ID → OUTPUT/PACKAGE STEP`

Representative fields:
- TRACE_ID
- PPCT_REF
- SGK_REF
- OBJECTIVE_ID
- ACTIVITY_ID
- TASK_ID
- DISPLAY/PACKAGE_STEP_ID

P12.1 package preserves traceability where the contract permits; internal trace data must not leak to students.

## 33. Version Compatibility

Track independently:
- CORE_VERSION
- CANONICAL_SCHEMA_VERSION
- PACKAGE_CONTRACT_VERSION
- TARGET_WEB_LIVE_VERSION
- GENERATED_WITH_CORE_VERSION
- PACKAGE_HASH

WEB LIVE and Core versions are independent.

A package adapter targets a specific compatible contract, e.g. P12.1.

Contract mismatch:
`CONTRACT_VERSION_MISMATCH → BLOCK IMPORT/BUILD as appropriate`

## 34. Immutability and Revalidation

`FROZEN_MEANS_IMMUTABLE`

After freeze, any semantic modification requires a new artifact/version/hash.

Semantic edit after validation:
`VALIDATION_STALE → REVALIDATE`

Examples of semantic edits:
- question
- task
- answer
- solution
- figure relation
- formalization
- method

Pure cosmetic presentation edits may use narrower render/UI validation if mathematical meaning is unchanged.

## 35. Fail-safe / No Guess

If required PPCT, SGK scope/structure, source attribution, figure relation, or compatibility contract is missing/ambiguous:

`BLOCKED → REPORT → DO NOT GUESS`

No silent source fabrication or inferred curriculum progression.

## 36. Core Issue Workflow

When Work finds a Core defect:

`CORE_ISSUE_REPORT → CODEX REPRODUCE → PATCH → UNIT TEST → GOLDEN TEST → REGRESSION → NEW RC`

CORE_ISSUE_REPORT minimum:
- ISSUE_ID
- CORE_VERSION
- INPUT
- CURRICULUM_CONTEXT
- EXPECTED
- ACTUAL
- EVIDENCE
- SEVERITY
- AFFECTED_COMPONENT
- REPRODUCIBLE

Work does not patch Core.

## 37. Golden and Regression Strategy

Use approximately 10–16 representative Golden Lesson cases covering meaningful edge conditions rather than a full Cartesian product.

Golden tests are Core-owned. Work pilot lessons provide runtime evidence and may later be proposed as Golden candidates.

Patch workflow:
`PATCH TEST → RELATED TESTS → GOLDEN SET → REGRESSION`

---

# HOME PREP CROSS-CUTTING RULES

HOME_PREP may ask students to:
- read a specified SGK section
- observe
- try using known knowledge
- predict
- bring a question to class

It must not:
- formalize untaught new knowledge
- require memorizing an untaught rule
- expose a full solution that removes class discovery
- teach ahead

Every meaningful home-prep task requires `PREP_TO_CLASS_BRIDGE`.

---

# MASTER SPEC PATCH INTEGRATION REGISTER

All 18 approved patch candidates are integrated into their authoritative owners:

1. Measurable Learning Objective → Objective Model
2. Prerequisite Dependency Map → Curriculum/Readiness
3. Misconception Library → Diagnostic Model
4. Lesson State Machine → Execution Model
5. Minimum Valid Lesson → Lesson Type + Time
6. Traceability Chain → Governance
7. Teacher Override Governance → Runtime Governance
8. Lesson Completion Evidence → Completion Model
9. Rule Priority Matrix → Foundation
10. Single Source of Truth Rule → Architecture Governance
11. Write Authority Matrix → Governance
12. Immutability & Version Trace → Governance
13. Severity Escalation Rule → Validation
14. Release Gate Policy → Governance
15. Fail-safe / No Guess → Curriculum + Validation
16. Contract Version Compatibility → Output/Package
17. Revalidate After Semantic Edit → Validation Lifecycle
18. Offline Lesson Package Contract → WEB LIVE Package Adapter

No patch remains as an unowned parallel rule.

---

# FROZEN BASELINE STATUS

```text
PROJECT = MATH_CORE_THCS

MASTER_SPEC_VERSION = 1.0
MASTER_SPEC_STATUS = FROZEN
BASELINE_STATUS = LOCKED

GAP_CHECK = PASS
CONFLICT_CHECK = PASS
DUPLICATION_CHECK = PASS
OWNERSHIP_CHECK = PASS
SEVERITY_CHECK = PASS
END_TO_END_SIMULATION = PASS
WEB_LIVE_P12_1_COMPATIBILITY_REVIEW = PASS
FINAL_REVIEW_6_GATES = PASS

SPEC_PATCHES = 18
PATCHES_INTEGRATED = 18

ARCHITECTURE_REBUILD_REQUIRED = NO
WEB_LIVE_P12_1_REBUILD_REQUIRED = NO

CODEX_IMPLEMENTATION = NOT_STARTED
WORK_PILOT = NOT_STARTED
PRODUCTION = PROHIBITED
```

## Change control after freeze

This V1.0 document must not be silently edited.

Any future specification change requires:

`SPEC_ISSUE_REPORT → PATCH_PROPOSAL → REVIEW → NEW_SPEC_VERSION`

Codex must not modify or reinterpret this baseline during implementation.

---

# NEXT AUTHORIZED PHASE

The next phase is:

**CODEX PHASE A — AUDIT + IMPLEMENTATION DESIGN ONLY**

Phase A must audit existing Algebra/Geometry assets and WEB LIVE P12.1 compatibility before any implementation.

Phase A is explicitly:
- DO NOT IMPLEMENT
- DO NOT PATCH MASTER SPEC
- DO NOT PATCH WEB LIVE P12.1
- DO NOT MODIFY SGK/PPCT/SBT
- DO NOT CREATE RC1
- DO NOT PROMOTE PRODUCTION
