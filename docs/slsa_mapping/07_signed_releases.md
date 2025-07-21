# Consolidated Mapping of OpenSSF Scorecard Check to SLSA Threats

## Scorecard Check: Signed Releases

**Risk:** High

**Description:** This check tries to determine if the project cryptographically signs release artifacts. It is currently limited to repositories hosted on GitHub, and does not support other source hosting repositories (i.e., Forges).

---

## Individual Mappings

### Rebecca Beyer

**Mapping:**

- **Threat F:** Tamper with artifact
- **Threat G:** Replace package

### Richard Hegewald

**Mapping:**

- **Threat F:** Tamper with artifact after CI/CD.
- **Threat G:** Tamper with artifact after upload.

---

## Discussion

---

## Consolidated Mapping

**Final Mapping:**

- **Threat F:** Tamper with artifact after CI/CD.
- **Threat G:** Tamper with artifact after upload.
