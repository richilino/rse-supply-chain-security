# Consolidated Mapping of OpenSSF Scorecard Check to SLSA Threats

## Scorecard Check: Dangerous Workflow

**Risk:** Critical

**Description:** This check determines whether the project's GitHub Action workflows has dangerous code patterns. Some examples of these patterns are untrusted code checkouts, logging github context and secrets, or use of potentially untrusted inputs in scripts.

---

## Individual Mappings

### Rebecca Beyer

**Mapping:**

- **Threat D & E:** With the PR checkout, PR authors may compromise the repository, for example, by using build scripts controlled by the author of the PR or reading token in memory; pattern detects whether a workflow's inline script may execute untrusted input from attackers

### Richard Hegewald

**Mapping:**

- **Threat D:** Possible Build from unofficial parameters.
- **Threat E:** Possible tampering with artifact during build.

---

## Discussion

---

## Consolidated Mapping

**Final Mapping:**

- **Threat D:** Possible Build from unofficial parameters.
- **Threat E:** Possible tampering with artifact during build.
