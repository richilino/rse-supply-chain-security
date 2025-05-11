# Consolidated Mapping of OpenSSF Scorecard Check to SLSA Threats

## Scorecard Check: Pinned Dependencies

**Risk:** Medium

**Description:** This check tries to determine if the project pins dependencies used during its build and release process. A "pinned dependency" is a dependency that is explicitly set to a specific hash instead of allowing a mutable version or range of versions.

---

## Individual Mappings

### Rebecca Beyer

**Mapping:**

- **Threat D:** Compromised Dependency
- **Threat G:** Build with manipulated dependencies
- **Threat H:** Dependency Confusion

**Notes:**

- [Note 1]
- [Note 2]

### Richard Hegewald

**Mapping:**

- **Threat D:** Build from unofficial paramters.
- **Threat H:** Unintentional use of malicious dependency version.

**Notes:**

- [Note 1]
- [Note 2]

---

## Discussion

---

## Consolidated Mapping

**Final Mapping:**

- **Threat A:** [Consolidated Justification]
- **Threat B:** [Consolidated Justification]
- **Threat C:** [Consolidated Justification]
- **Threat D:** [Consolidated Justification]
- **Threat E:** [Consolidated Justification]
- **Threat F:** [Consolidated Justification]
- **Threat G:** [Consolidated Justification]
- **Threat H:** [Consolidated Justification]
- **Threat I:** [Consolidated Justification]

---

**Note:** Replace placeholders (e.g., `[Check Name]`, `[Justification]`, `[Note]`) with actual content based on the collaborators' inputs and discussions.
