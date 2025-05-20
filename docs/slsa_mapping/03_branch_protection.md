# Consolidated Mapping of OpenSSF Scorecard Check to SLSA Threats

## Scorecard Check: Branch Protection

**Risk:** High

**Description:** This check determines whether a project's default and release branches are protected with GitHub's branch protection or repository rules settings. Branch protection allows maintainers to define rules that enforce certain workflows for branches, such as requiring review or passing certain status checks before acceptance into a main branch, or preventing rewriting of public history.

---

## Individual Mappings

### Rebecca Beyer

**Mapping:**

- **Threat B:** Directly Submit without review, Highly-permissioned actors bypasses or disables controls

**Notes:**

- [Note 1]
- [Note 2]

### Richard Hegewald

**Mapping:**

- **Threat B:** Unauthorized merges or pushes.
- **Threat C:** Platform admin abuses privileges.

**Notes:**

- [Note 1]
- [Note 2]

---

## Discussion

---

## Consolidated Mapping

**Final Mapping:**

- **Threat B:** Directly Submit without review. Highly-permissioned actors bypasses or disables controls

---

**Note:** Replace placeholders (e.g., `[Check Name]`, `[Justification]`, `[Note]`) with actual content based on the collaborators' inputs and discussions.
