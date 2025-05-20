# Consolidated Mapping of OpenSSF Scorecard Check to SLSA Threats

## Scorecard Check: Code Review

**Risk:** High

**Description:** This check determines whether the project requires human code review before pull requests (merge requests) are merged.

---

## Individual Mappings

### Rebecca Beyer

**Mapping:**

- **Threat A:** Increases chance of finding malware
- **Threat B:** Bot, no review, copy reviewed change to another context
- **Threat C:** Platform Admin Abuses Privileges

**Notes:**

- [Note 1]
- [Note 2]

### Richard Hegewald

**Mapping:**

- **Threat B:** Submit change without review.
- **Threat H:** Malicious package use through developer inattention.

**Notes:**

- [Note 1]
- [Note 2]

---

## Discussion

---

## Consolidated Mapping

**Final Mapping:**

- **Threat A:** High numbers of users / reviewers may increase likelihood that bad code is detected during review.
- **Threat B:** Submit change without review.

---

**Note:** Replace placeholders (e.g., `[Check Name]`, `[Justification]`, `[Note]`) with actual content based on the collaborators' inputs and discussions.
