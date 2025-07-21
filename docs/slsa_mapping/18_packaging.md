# Consolidated Mapping of OpenSSF Scorecard Check to SLSA Threats

## Scorecard Check: Packaging

**Risk:** Medium

**Description:** Does the project build and publish official packages from CI/CD, e.g. GitHub Publishing?

---

## Individual Mappings

### Rebecca Beyer

**Mapping:**

- **Threat A:** validating official package registries? (metadata documents provenance?)
- **Threat I:** easier patching of bugs with updates?

### Richard Hegewald

**Mapping:**

- **Threat E:** Tamper with artifact during build.
- **Threat F:** Tamper with artifact after CI/CD.

---

## Discussion

---

## Consolidated Mapping

**Final Mapping:**

- **Threat E:** Tamper with artifact during build.
- **Threat F:** Tamper with artifact after CI/CD.
