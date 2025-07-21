# Consolidated Mapping of OpenSSF Scorecard Check to SLSA Threats

## Scorecard Check: Token Permissions

**Risk:** High

**Description:** This check determines whether the project's automated workflows tokens follow the principle of least privilege. This is important because attackers may use a compromised token with write access to, for example, push malicious code into the project.

---

## Individual Mappings

### Rebecca Beyer

**Mapping:**

- **Threat B:** not authorized code changes
- **Threat C:** platform admin abuse
- **Threat F & G:** upload malicious package or provenance

### Richard Hegewald

**Mapping:**

- **Threat C:** Unauthorized workflow triggering.

---

## Discussion

---

## Consolidated Mapping

**Final Mapping:**

- **Threat B:** Use bot account to submit change
- **Threat C:** Unauthorized workflow triggering.
