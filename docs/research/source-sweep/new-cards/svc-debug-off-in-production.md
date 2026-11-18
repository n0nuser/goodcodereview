---
id: svc-debug-off-in-production
level: service
tags: [security, configuration]
severity: should-fix
status: draft
lacks: orgs, OWASP backs debug modes and Microsoft backs Swagger UI; needs one more org per clause that turns debug tooling off in production
lang: core
applies_when: The service has a debug mode or serves API docs or a developer UI such as Swagger.
context: [server]
tool_gate: A smoke test against the production config that requests the docs path and expects 404, and a config check that debug is false.
borrowed_from:
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x22-V13-Configuration.md
  - https://learn.microsoft.com/en-us/aspnet/core/tutorials/first-web-api
---

**Rule.** Keep debug modes and developer tooling, such as Swagger UI, disabled in production.

**Why.** A debug mode prints stack traces, config values and sometimes an interactive console. A docs UI lists every endpoint, parameter and model, including internal ones. Both hand an attacker a map and secrets. Turn them on by environment, so the safe state is the default and a missing setting leaves them off.

**FAIL**

```csharp
var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();   // served in every environment
```

**PASS**

```csharp
var app = builder.Build();
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
```

**Counterpoint.** "We need the docs for partners in production." Publish the spec as a static artifact or behind authentication, and keep the live debug UI and debug mode off. Partners need the contract, not a try-it console on the production host.
