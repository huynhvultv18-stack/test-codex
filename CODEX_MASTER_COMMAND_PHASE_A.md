# CODEX MASTER COMMAND — PHASE A
# MATH CORE THCS V1.0
# AUDIT + IMPLEMENTATION DESIGN ONLY
# DO NOT IMPLEMENT — DO NOT PATCH — DO NOT PRODUCTION

## 0. BASELINE AUTHORITY

Normative frozen baseline:

`MATH_CORE_THCS_MASTER_SPEC_V1.0.md`

Required status:

```text
MASTER_SPEC_VERSION = 1.0
MASTER_SPEC_STATUS = FROZEN
BASELINE_STATUS = LOCKED
```

The frozen MASTER SPEC is the highest-authority source for this task.

Codex MUST NOT:
- modify the frozen MASTER SPEC;
- silently reinterpret or weaken a frozen rule;
- add a subsystem outside the approved scope without reporting it;
- remove a rule because implementation is difficult;
- change the frozen baseline in place.

If Codex detects a specification problem:

```text
SPEC_ISSUE_REPORT
→ STOP THE AFFECTED DESIGN
→ DO NOT PATCH THE SPEC
```

---

## 1. PHASE A PURPOSE

Perform only:

```text
AUDIT EXISTING ASSETS
→ MAP MASTER SPEC TO IMPLEMENTATION
→ IDENTIFY REUSABLE COMPONENTS
→ IDENTIFY MISSING COMPONENTS
→ DESIGN IMPLEMENTATION ARCHITECTURE
→ DESIGN CANONICAL LESSON MODEL
→ DESIGN VALIDATION
→ DESIGN TEST STRATEGY
→ DESIGN WEB LIVE P12.1 PACKAGE ADAPTER
→ PRODUCE REQUIRED REPORTS
```

Phase A is analysis/design only.

```text
DO NOT IMPLEMENT
DO NOT PATCH CORE
DO NOT CREATE RC1
DO NOT PROMOTE PRODUCTION
```

---

## 2. INPUT AUTHORITY ORDER

Use the following priority:

```text
PRIORITY 1
MATH_CORE_THCS_MASTER_SPEC_V1.0.md
→ NORMATIVE SOURCE OF TRUTH

PRIORITY 2
CURRENT ALGEBRA + GEOMETRY PREP SOURCE
→ REUSE / AUDIT TARGET

PRIORITY 3
WEB_LIVE_LESSON_LIBRARY_P12_1_CANDIDATE.zip
→ COMPATIBILITY TARGET

PRIORITY 4
SGK + PPCT REFERENCE MATERIAL, IF PROVIDED
→ READ-ONLY CURRICULUM EVIDENCE

PRIORITY 5
KNOWN-GOOD OUTPUT/PACKAGE SAMPLES, IF PROVIDED
→ OUTPUT / RUNTIME EVIDENCE
```

If inputs conflict:

```text
DO NOT GUESS
DO NOT SILENTLY FIX
REPORT THE CONFLICT
```

Do not treat older source behavior as authority over the frozen MASTER SPEC.

---

## 3. HARD SCOPE LOCK

Preserve:

```text
PPCT_SCOPE_LOCK
SGK_STRUCTURE_LOCK
NO_TEACH_AHEAD
NO_GUESS

ONE_RULE_ONE_SOURCE_OF_TRUTH
WORK_DOES_NOT_PATCH_CORE
CODEX_DOES_NOT_EDIT_SGK_PPCT_SBT
WEB_LIVE_DOES_NOT_REWRITE_PEDAGOGY

SOAN_TRUOC_TOTAL_TIME <= 45 MIN

OFFLINE_PACKAGE_FIRST
NO_DIRECT_LIVE_DEPENDENCY

FROZEN_MEANS_IMMUTABLE
```

No refactor outside approved scope.

---

## 4. EXISTING-ASSET-FIRST POLICY

Audit existing source before proposing new implementation.

Required preference:

```text
REUSE
>
REUSE WITH ADAPTER
>
PATCH
>
EXTEND
>
REPLACE
>
CREATE NEW
```

For every relevant existing component, classify it as exactly one of:

```text
REUSE_AS_IS
REUSE_WITH_ADAPTER
PATCH_REQUIRED
EXTEND_REQUIRED
REPLACE_REQUIRED
NEW_COMPONENT_REQUIRED
```

For every PATCH / EXTEND / REPLACE / NEW decision, provide:
- component;
- existing evidence;
- reason;
- affected MASTER SPEC requirement;
- risk;
- proposed boundary.

Do not rebuild merely to normalize style or architecture.

---

## 5. REQUIRED TARGET ARCHITECTURE

The implementation design MUST preserve:

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
 ┌───────────┬───────────┬─────────────────────┐
 ↓           ↓           ↓
BẢN HS     BẢN GV     P12.1 PACKAGE ADAPTER
                            ↓
                       manifest.json
                       lesson.json
                       images/assets
                            ↓
                       *_LIVE.zip
                            ↓
                    VALIDATE + FREEZE
══════════════════ SYSTEM BOUNDARY ══════════════════
                            ↓
                     USER MANUAL IMPORT
                            ↓
                      WEB LIVE P12.1
```

Prohibited architecture:

```text
MATH CORE → DIRECT LIVE CONTROL
```

WEB LIVE P12.1 is an existing consumer, not a subsystem to rebuild inside Math Core.

---

## 6. LOGICAL COMPONENTS TO AUDIT AND MAP

Audit and create an implementation map for at least:

```text
CURRICULUM_GUARD
OBJECTIVE_MODEL

DOMAIN_ENGINE
├── ALGEBRA
└── GEOMETRY

LESSON_TYPE_ENGINE
DIFFERENTIATION_ENGINE
ASSESSMENT_ENGINE
TASK_ENGINE

SUPPORT_MODEL
├── SCAFFOLD
├── HINT
└── TEACHER_INTERVENTION

DIAGNOSTIC_MODEL
TIME_ENGINE
LESSON_STATE_MACHINE

MATH_REPRESENTATION_STANDARD
GEOMETRY_FIGURE_STANDARD
REASONING_REPRESENTATION

CANONICAL_LESSON_MODEL
OUTPUT_CONTRACT
VALIDATION_ENGINE

WEB_LIVE_P12_1_PACKAGE_ADAPTER
```

These are logical ownership boundaries.

Do NOT assume each logical component requires a separate package/plugin/folder.

---

## 7. CURRICULUM RESPONSIBILITY

Codex builds:
- rules;
- schemas;
- validators;
- engines;
- tests;
- adapters.

Codex does NOT invent actual:
- PPCT scope;
- SGK section order;
- curriculum progress;
- SGK exercise attribution;
- SBT attribution.

Actual curriculum grounding is populated by Work from real source material.

If evidence is missing or ambiguous:

```text
BLOCK
REPORT
DO NOT GUESS
```

SGK / PPCT / SBT are read-only external sources.

---

## 8. CANONICAL LESSON MODEL DESIGN

Design one authoritative Canonical Lesson Model.

Required relationship:

```text
              CANONICAL LESSON
                     │
        ┌────────────┼─────────────┐
        ↓            ↓             ↓
   STUDENT VIEW  TEACHER VIEW  LIVE PACKAGE
```

Required invariant:

```text
TEACHER_VIEW
=
STUDENT_VIEW
+
TEACHER_LAYER
```

Do not design three independent lessons.

Canonical model must remain independent from P12.1 legacy field duplication.

If P12.1 requires legacy aliases/duplicates, map them in the Package Adapter.

---

## 9. WEB LIVE P12.1 AUDIT

Treat:

`WEB_LIVE_LESSON_LIBRARY_P12_1_CANDIDATE.zip`

as the compatibility target.

Audit relevant actual runtime/source, including where present:
- lesson/subject loader;
- ZIP importer;
- manifest handling;
- lesson.json handling;
- asset/image handling;
- subject profiles;
- Algebra/Geometry handling;
- geometry scenes;
- analysis diagram/analysis steps;
- progressive disclosure;
- teacher/TV separation;
- package safety checks;
- package examples/tests.

Do not assume compatibility from documentation alone when runtime/source evidence is available.

Do NOT patch P12.1 in Phase A.

---

## 10. P12.1 PACKAGE ADAPTER DESIGN

Design:

```text
WEB_LIVE_P12_1_PACKAGE_ADAPTER
```

Its responsibility:

```text
CANONICAL LESSON
→ MAP METADATA
→ MAP SCREENS
→ MAP QUESTION / HINT / ANSWER
→ MAP FORMALIZATION
→ MAP GEOMETRY
→ MAP REASONING / ANALYSIS
→ COLLECT ASSETS
→ BUILD manifest.json
→ BUILD lesson.json
→ BUILD *_LIVE.zip
```

Adapter MUST NOT create new pedagogy or alter mathematical meaning.

Official package model:

```text
*_LIVE.zip
├── manifest.json
├── lesson.json
└── images/assets/
```

Delivery model:

```text
GENERATE
→ VALIDATE
→ PACKAGE
→ FREEZE
→ USER MANUAL IMPORT
```

No direct-live dependency.

---

## 11. PACKAGE VALIDATION DESIGN

Design validation for at least:

```text
PACKAGE_SCHEMA
MANIFEST_VALID
LESSON_JSON_VALID
ASSET_EXISTS
ASSET_SUPPORTED
ASSET_SIZE
ZIP_STRUCTURE
P12_1_COMPATIBILITY

NO_STUDENT_ANSWER_LEAK
NO_TEACHER_METADATA_LEAK

MATH_RENDER_CONTRACT
FIGURE_ASSET_CONTRACT
TRACEABILITY
```

Math Core/Work performs strict pedagogical/semantic validation before packaging.

WEB LIVE importer remains a compatibility/runtime safety layer; it is not the authoritative pedagogy validator.

---

## 12. VALIDATION SEVERITY DESIGN

Use exactly:

```text
HARD_FAIL
QUALITY_FAIL
WARNING
INFO
```

HARD_FAIL blocks the affected official candidate/package.

Do not allow Work or WEB LIVE to bypass a Core HARD_FAIL.

Severity is consequence-aware:

```text
SEMANTIC ERROR
→ may escalate to HARD_FAIL

COSMETIC/PRESENTATION ERROR
→ QUALITY_FAIL or WARNING unless meaning/readability is destroyed
```

Design clear phase-aware behavior for:
- design-time validation;
- package validation;
- runtime monitoring;
- release gates.

Do not confuse runtime state with validator failure.

---

## 13. TRACEABILITY DESIGN

Required logical chain:

```text
PPCT_REF
→ SGK_REF
→ OBJECTIVE_ID
→ ACTIVITY_ID
→ TASK_ID
→ OUTPUT/PACKAGE STEP
```

Design fields and propagation so generated output can be traced back to curriculum and objective.

Internal trace/audit metadata must not leak to students.

---

## 14. VERSION / COMPATIBILITY / IMMUTABILITY

Design at least:

```text
CORE_VERSION
CANONICAL_SCHEMA_VERSION
PACKAGE_CONTRACT_VERSION
TARGET_WEB_LIVE_VERSION
GENERATED_WITH_CORE_VERSION
PACKAGE_HASH
```

Required rules:

```text
FROZEN_MEANS_IMMUTABLE

SEMANTIC_EDIT_AFTER_VALIDATION
→ VALIDATION_STALE
→ REVALIDATE

CONTRACT_VERSION_MISMATCH
→ BLOCK BUILD/IMPORT AS APPROPRIATE
```

Do not modify a frozen artifact under the same version/hash.

---

## 15. TIME ENGINE DESIGN

Preserve:

```text
SOAN_TRUOC_TOTAL_TIME <= 45 MIN
NO_AUTO_TIME_FILL
NO_HIDDEN_TIME
NO_NEGATIVE_TIME
```

Design time handling around:
- lesson type;
- SGK structure;
- objective;
- student profile;
- minimum valid lesson;
- activity priority;
- compression.

If minimum valid lesson cannot fit within 45 minutes:

```text
TIME_DESIGN_FAIL
```

Do not fabricate time compliance.

---

## 16. TEST STRATEGY DESIGN

Phase A does not implement or execute the future Core test suite.

Design a test matrix covering:

```text
UNIT TESTS
CURRICULUM GUARD TESTS
NO_TEACH_AHEAD TESTS
OBJECTIVE TESTS
ALGEBRA TESTS
GEOMETRY TESTS
LESSON TYPE TESTS
DIFFERENTIATION TESTS
ASSESSMENT TESTS
TASK TESTS
SUPPORT / DIAGNOSTIC TESTS
TIME TESTS
STATE MACHINE TESTS
MATH REPRESENTATION TESTS
FIGURE / REASONING TESTS
OUTPUT CONTRACT TESTS
HS/GV PARITY TESTS
PACKAGE ADAPTER TESTS
P12.1 COMPATIBILITY TESTS
TRACEABILITY TESTS
FREEZE / REVALIDATION TESTS
REGRESSION TESTS
```

Propose approximately 10–16 representative Golden Lesson cases.

Do not use a full Cartesian product unless evidence shows it is necessary.

Golden cases must cover meaningful boundaries/edge conditions.

---

## 17. RISK REGISTER

For each implementation risk record:

```text
RISK_ID
DESCRIPTION
SEVERITY
AFFECTED_COMPONENT
EVIDENCE
MITIGATION
BLOCKING_STATUS
```

Explicitly inspect for:
- duplicate Source of Truth;
- Core/Work ownership leak;
- curriculum assumptions;
- hidden teach-ahead;
- fake SGK/SBT attribution;
- schema coupling;
- P12.1 legacy coupling;
- HS/GV divergence;
- answer/metadata leakage;
- validation bypass;
- frozen artifact mutation;
- unjustified rebuild/refactor.

---

## 18. REQUIRED PHASE A REPORTS

Produce all 10:

```text
01_MATH_CORE_EXISTING_ASSET_AUDIT.md

02_MASTER_SPEC_IMPLEMENTATION_MAP.md

03_REUSE_PATCH_NEW_MATRIX.md

04_PROPOSED_IMPLEMENTATION_ARCHITECTURE.md

05_CANONICAL_LESSON_MODEL_DESIGN.md

06_VALIDATION_SEVERITY_DESIGN.md

07_TEST_AND_GOLDEN_PLAN.md

08_P12_1_PACKAGE_ADAPTER_DESIGN.md

09_IMPLEMENTATION_RISK_REGISTER.md

10_PHASE_B_IMPLEMENTATION_PLAN.md
```

Reports must reference actual evidence from supplied assets where applicable.

Do not report PASS merely from intent or comments if runtime/source evidence is required.

---

## 19. REQUIRED DECISION SUMMARY

At the end provide:

```text
REUSE_AS_IS = [...]
REUSE_WITH_ADAPTER = [...]
PATCH_REQUIRED = [...]
EXTEND_REQUIRED = [...]
REPLACE_REQUIRED = [...]
NEW_COMPONENT_REQUIRED = [...]

BLOCKERS = [...]
SPEC_ISSUES = [...]
P12_1_COMPATIBILITY_RISKS = [...]
```

Then exactly one Phase A status:

```text
PHASE_A_STATUS = READY_FOR_REVIEW
```

or:

```text
PHASE_A_STATUS = BLOCKED
```

Recommendation:

```text
RECOMMENDATION = PROCEED_TO_PHASE_B
```

or:

```text
RECOMMENDATION = HOLD_FOR_SPEC_OR_ASSET_RESOLUTION
```

Phase A recommendation is not authorization to implement.

---

## 20. PHASE A EXIT GATE

`READY_FOR_REVIEW` requires:

```text
AUDIT_COMPLETE = YES
MASTER_SPEC_MAPPING_COMPLETE = YES

OWNERSHIP_AMBIGUITY = 0
UNJUSTIFIED_REBUILD = 0
DIRECT_LIVE_DEPENDENCY = 0

CANONICAL_LESSON_MODEL_DESIGN_COMPLETE = YES
P12_1_PACKAGE_ADAPTER_DESIGN_COMPLETE = YES
VALIDATION_DESIGN_COMPLETE = YES
TEST_PLAN_COMPLETE = YES

BLOCKING_RISKS_IDENTIFIED_WITH_EVIDENCE = YES
```

If any required evidence is unavailable, state the limitation explicitly.

Do not manufacture evidence to satisfy the exit gate.

---

## 21. STOP CONDITIONS

Stop the affected design and report if:

- the frozen MASTER SPEC contains an unresolved contradiction that rule precedence cannot resolve;
- required audit source is missing;
- P12.1 compatibility cannot be determined from supplied evidence;
- existing assets differ materially from the stated assumptions;
- continuing would require modifying WEB LIVE P12.1;
- continuing would require modifying SGK/PPCT/SBT;
- continuing would require changing the frozen MASTER SPEC;
- a required decision would depend on guessing curriculum/source facts.

Required response:

```text
REPORT
→ IDENTIFY BLOCKER
→ PRESERVE EVIDENCE
→ DO NOT GUESS
→ DO NOT PATCH
```

---

## 22. ABSOLUTE PROHIBITIONS FOR PHASE A

```text
DO NOT IMPLEMENT MATH CORE

DO NOT PATCH EXISTING CORE

DO NOT REFACTOR SOURCE

DO NOT CREATE RC1

DO NOT MODIFY MASTER SPEC V1.0

DO NOT MODIFY SGK
DO NOT MODIFY PPCT
DO NOT MODIFY SBT

DO NOT PATCH WEB LIVE P12.1

DO NOT CREATE DIRECT LIVE CONNECTION

DO NOT PROMOTE PRODUCTION

DO NOT CLAIM RUNTIME PASS WITHOUT EVIDENCE
```

---

# FINAL INSTRUCTION

Audit first.

Design second.

Stop after the 10 required reports and decision summary.

Do not begin Phase B until the project owner explicitly issues a separate:

```text
APPROVE PHASE B
```
