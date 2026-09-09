# PlantUML quick cheatsheet

Full, example-rich docs (with live previews) live at `$PLANTUML_API_BASE/help`. This is a
condensed offline reference. Every diagram has its own start/end tags.

## Start/end tags by diagram type
| Diagram | Tags |
|---|---|
| UML (sequence, class, usecase, component, deployment, state, object, activity) | `@startuml` / `@enduml` |
| MindMap | `@startmindmap` / `@endmindmap` |
| WBS | `@startwbs` / `@endwbs` |
| Gantt | `@startgantt` / `@endgantt` |
| JSON | `@startjson` / `@endjson` |
| YAML | `@startyaml` / `@endyaml` |
| Salt (wireframe) | `@startsalt` / `@endsalt` (or `salt { }` inside `@startuml`) |
| Network (nwdiag) | `@startnwdiag` / `@endnwdiag` (wraps a `nwdiag { }` block) |

## Common commands (most UML diagrams)
- `title My Title`, `header ...`, `footer ...`, `caption ...`, `legend ... endlegend`
- `note left of X : text` · `note right`, `note top`, `note bottom` · multi-line `note ... end note`
- `skinparam <name> <value>` · `!theme <name>` (right after `@startuml`)
- comments: `' single line`, `/' block '/`
- colors: named (`#LightBlue`, `AliceBlue`) or hex (`#123456`); gradients `#red-blue`
- direction: `left to right direction` / `top to bottom direction`
- `!include <lib/...>` (bundled stdlib), preprocessing `!define`, `!$var = ...`, `!if/!endif`

## Sequence
```
@startuml
autonumber
actor User
participant "Web App" as Web
database DB
User -> Web: login
activate Web
Web -> DB: query
DB --> Web: rows
Web --> User: 200 OK
deactivate Web
alt success
  Web -> User: token
else failure
  Web -> User: 401
end
note over User,Web: handshake
@enduml
```
Arrows: `->` solid, `-->` dashed, `->>` thin, `-\` / `->x` lost, `<->` bidirectional.
Grouping: `alt/else`, `opt`, `loop`, `par`, `break`, `critical`, `group`.

## Class
```
@startuml
abstract class Shape {
  +area(): float
}
class Circle {
  -r: float
}
interface Drawable
class Point
Shape <|-- Circle
Circle ..|> Drawable
Circle "1" *-- "many" Point : has
@enduml
```
Relations: `<|--` inherit, `*--` composition, `o--` aggregation, `..>` dependency, `-->`
association. Visibility: `+` public `-` private `#` protected `~` package.

## Use case
```
@startuml
left to right direction
actor User
rectangle System {
  User --> (Login)
  (Login) .> (Authenticate) : include
}
@enduml
```

## Activity (modern/beta)
```
@startuml
start
:read request;
if (valid?) then (yes)
  :render;
else (no)
  :422;
endif
fork
  :log;
fork again
  :metrics;
end fork
stop
@enduml
```
Swimlanes: `|Lane A|`. Loops: `repeat ... repeat while (cond)`, `while (cond) ... endwhile`.

## State
```
@startuml
[*] --> Idle
Idle --> Running : start
state Running {
  [*] --> Working
  Working --> Paused : pause
}
Running --> [*] : stop
@enduml
```

## Component / Deployment
```
@startuml
package "Frontend" {
  [Web UI]
}
node "Server" {
  [API]
  database "DB"
  [API] --> "DB"
}
[Web UI] --> [API] : HTTPS
@enduml
```
Element keywords: actor, agent, artifact, boundary, card, cloud, component, database, file,
folder, frame, hexagon, interface, node, package, queue, rectangle, stack, storage, usecase.

## Object
```
@startuml
object user {
  name = "Ada"
}
map config {
  debug => true
}
user --> config
@enduml
```

## JSON / YAML
```
@startjson
{ "service": "plantuml", "formats": ["png","svg"], "auth": null }
@endjson
```
```
@startyaml
service: plantuml
formats: [png, svg]
@endyaml
```

## MindMap / WBS
```
@startmindmap
* Root
** Branch A
*** Leaf
** Branch B
@endmindmap
```
```
@startwbs
* Project
** Phase 1
*** Task 1.1
** Phase 2
@endwbs
```

## Gantt
```
@startgantt
Project starts 2026-01-01
[Design] lasts 5 days
[Build] lasts 10 days
[Build] starts at [Design]'s end
[Ship] lasts 2 days and starts at [Build]'s end
@endgantt
```

## Salt (wireframe)
```
@startsalt
{
  Login | .
  Name  | "         "
  Pass  | "         "
  [Cancel] | [  OK  ]
}
@endsalt
```

## Network (nwdiag)
```
@startnwdiag
nwdiag {
  network dmz {
    address = "10.0.0.0/24"
    web [address = "10.0.0.1"];
  }
  network internal {
    web;
    db [address = "10.1.0.2"];
  }
}
@endnwdiag
```

For architecture icons (AWS/Azure/K8s/C4/GCP/OSA/…) see `architecture-libraries.md`.
