---
name: ios-design
description: Install the ios-design skill for your AI agent. Published on uizze.sh.
source: https://www.skills.sh/site/uizze.sh/ios-design
---

![](/api/image-proxy?url=https%3A%2F%2Fuizze.com%2Flanding%2Fanti-ui-slop-skill-banner.png&s=bc74230d439dbbef)

# iOS Design: iPhone UI/UX

Design and evaluate iPhone interfaces using native interaction patterns and real product references.

Use `ios-design` to define screen hierarchy, implement navigation and forms, and check layouts under keyboard, text-size, and device constraints. Work in SwiftUI, UIKit, or React Native without replacing the project's framework or visual identity.

With [Uizze](https://uizze.com) connected, your coding agent can retrieve real iOS screen references, fonts, and icons during implementation. It can examine how existing products handle a specific interface problem and adapt the relevant pattern to your app.

[Connect Uizze](https://uizze.com/docs)

This skill is free. The Uizze MCP connection requires paid access; browsing the public reference library does not.

## Establish the task and constraints

Read the requested screen and its surrounding navigation, shared components, and design tokens. Establish the primary task, supported iPhone sizes, minimum iOS version, and existing framework from the project. Ask only for missing information that would change the implementation.

Preserve SwiftUI, UIKit, React Native, or the framework already in use. Do not migrate the app, install a UI kit, or rebuild its navigation for a local screen change. Follow the user's scope: an audit produces findings; implementation changes only the requested flow.