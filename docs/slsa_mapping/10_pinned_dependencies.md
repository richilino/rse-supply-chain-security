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

### Richard Hegewald

**Mapping:**

- **Threat D:** Build from unofficial paramters.
- **Threat H:** Unintentional use of malicious dependency version.

---

## Discussion

---

## Consolidated Mapping

**Final Mapping:**

- **Threat D:** Build from unofficial paramters.
- **Threat H:** Dependency Confusion

---

**Note:** FAIR Criterion
