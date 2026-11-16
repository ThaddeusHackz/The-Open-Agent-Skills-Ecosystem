---
name: xml
description: "XML/MyBatis mapper rules: namespace integrity, mapper-interface sync, well-formedness, embedded-SQL alignment."
---

* Shared examples and formatting reference: [references/EXAMPLE.md](references/EXAMPLE.md).
* Keep new guidance, snippets, and edits aligned with that file.

---

# Scope

Use this rule when:

* editing `.xml` files: Maven POM, Spring config, MyBatis mapper XML, log4j/logback config
* editing embedded SQL inside MyBatis mapper XML (`<select>`, `<insert>`, `<update>`, `<delete>`)
* changing element attributes, namespace declarations, or schema references
* adding or removing nodes that callers or frameworks depend on

When XML contains embedded SQL, **apply the `sql` skill in addition to this one**.

---

# Core Rules

* Preserve existing namespace declarations and `xsi:schemaLocation` unless explicitly changing them.
* Keep element indentation consistent (2 spaces preferred; match the file if already established).
* Do not self-close elements whose content model expects children.
* Use attributes for identity or metadata; use child elements for content or structured data.
* Validate that added elements match the expected schema or DTD.
* Do not break CDATA sections unnecessarily; preserve literal content inside `<![CDATA[...]]>`.

---

# MyBatis Mapper Contract

* Treat the mapper interface and XML as one contract.
* Keep `namespace`, `id`, `parameterType`, and `resultType` / `resultMap` synchronized with the mapper interface.
* Preserve column aliases and `resultMap` behavior when callers depend on them.
* Review `<if>`, `<choose>`, and `<foreach>` carefully — null, empty, and optional fragments included.
* Do not create `<sql>` snippets unless explicitly requested.

For SQL inside mapper XML — keyword casing, JOIN/WHERE single-line rules, alias conventions, performance rules, and dynamic-SQL guidance — follow the `sql` skill. This file does not duplicate those rules.

---

# Layering Boundary

* MyBatis mapper XML is for data retrieval and persistence only.
* Business logic and utility processing belong in Java (see `java` skill).
* Do not implement format conversion, string manipulation, conditional branching, calculation, or code mapping inside mapper XML queries.

---

# Formatting

* **Never use vertical alignment.** Do not pad spaces to align attribute values or element content into columns.
* Compact, standard style — no unnecessary whitespace padding.
* One attribute per line when an element has more than two attributes.
* Closing tag on its own line when the element contains block-level children.
* Exactly one space on both sides of binary operators inside embedded SQL and OGNL/test expressions.
* Do not use tabs, repeated spaces, or column alignment for visual formatting in any embedded expression.

---

# Validation Focus

* namespace correctness after changes
* MyBatis mapper/XML contract alignment (method name ↔ statement id, parameter type, result shape)
* embedded SQL parameter binding and result column stability
* dynamic SQL branch behavior (`<if>`, `<choose>`, `<foreach>`)
* well-formedness: unclosed tags, mismatched nesting, illegal characters
* schema or DTD validation when a validator is available
