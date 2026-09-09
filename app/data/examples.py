"""Curated examples demonstrating what PlantUML — and this API — can do.

These cover classic UML, cloud architecture (AWS/Azure/Kubernetes/GCP), the C4
model, network/security, icon libraries, themes and PlantUML's non-UML diagram
types. Every source is validated to render on the pinned PlantUML version.
"""

from __future__ import annotations

from ..models import Example

EXAMPLES: list[Example] = [
    # ---- Classic UML --------------------------------------------------------
    Example(
        id="sequence-basic",
        title="Basic sequence diagram",
        description="A minimal request/response sequence — the classic PlantUML hello world.",
        category="UML",
        libraries=["uml"],
        source="@startuml\nAlice -> Bob: Authenticate\nBob --> Alice: Token\n"
        "Alice -> Bob: GET /profile\nBob --> Alice: 200 OK\n@enduml",
    ),
    Example(
        id="class-diagram",
        title="Class diagram",
        description="Classes, inheritance and associations.",
        category="UML",
        libraries=["uml"],
        source="@startuml\nabstract class Shape {\n  +area(): float\n}\n"
        "class Circle extends Shape {\n  -radius: float\n}\n"
        "class Rectangle extends Shape {\n  -w: float\n  -h: float\n}\n"
        "Shape <|-- Circle\nShape <|-- Rectangle\n@enduml",
    ),
    Example(
        id="component-diagram",
        title="Component diagram",
        description="Components, interfaces and dependencies.",
        category="UML",
        libraries=["uml"],
        source='@startuml\npackage "Frontend" {\n  [Web UI]\n}\n'
        'package "Backend" {\n  [API] as api\n  [Worker]\n}\n'
        'database "PostgreSQL" as db\n[Web UI] --> api : HTTPS\n'
        "api --> db\n[Worker] --> db\n@enduml",
    ),
    Example(
        id="activity-diagram",
        title="Activity diagram",
        description="Modern activity syntax with conditionals.",
        category="UML",
        libraries=["uml"],
        source="@startuml\nstart\n:Receive request;\nif (Valid?) then (yes)\n"
        "  :Render diagram;\nelse (no)\n  :Return 422;\nendif\n:Respond;\nstop\n@enduml",
    ),
    Example(
        id="state-diagram",
        title="State diagram",
        description="A finite-state machine.",
        category="UML",
        libraries=["uml"],
        source="@startuml\n[*] --> Idle\nIdle --> Rendering : request\n"
        "Rendering --> Idle : done\nRendering --> Error : failure\n"
        "Error --> Idle : retry\n@enduml",
    ),
    # ---- C4 -----------------------------------------------------------------
    Example(
        id="c4-context",
        title="C4 — System Context",
        description="Level-1 C4 context diagram using the bundled C4-PlantUML macros.",
        category="C4",
        libraries=["c4"],
        source="@startuml\n!include <C4/C4_Context>\n"
        'Person(user, "Developer", "Creates diagrams as code")\n'
        'System(puml, "PlantUML API", "Renders UML & architecture diagrams")\n'
        'System_Ext(ci, "CI/CD", "Generates diagrams in pipelines")\n'
        'Rel(user, puml, "Uses", "HTTPS/REST")\n'
        'Rel(ci, puml, "Calls", "HTTPS/REST")\n@enduml',
    ),
    Example(
        id="c4-container",
        title="C4 — Container",
        description="Level-2 C4 container diagram.",
        category="C4",
        libraries=["c4"],
        source="@startuml\n!include <C4/C4_Container>\n"
        'Person(user, "User")\nSystem_Boundary(s, "PlantUML Service") {\n'
        '  Container(web, "Landing + Editor", "nginx + PlantUML Server")\n'
        '  Container(api, "REST API", "FastAPI")\n'
        '  Container(puml, "PlantUML Server", "Jetty")\n}\n'
        'Rel(user, web, "Visits", "HTTPS")\nRel(user, api, "Calls", "HTTPS/REST")\n'
        'Rel(api, puml, "Renders via", "HTTP")\n@enduml',
    ),
    Example(
        id="c4-component",
        title="C4 — Component",
        description="Level-3 C4 component diagram.",
        category="C4",
        libraries=["c4"],
        source="@startuml\n!include <C4/C4_Component>\n"
        'Container_Boundary(api, "REST API") {\n'
        '  Component(router, "Routers", "FastAPI", "HTTP endpoints")\n'
        '  Component(client, "PlantUML Client", "httpx", "Talks to backend")\n'
        '  Component(enc, "Encoder", "Python", "PlantUML text encoding")\n}\n'
        'Rel(router, client, "Uses")\nRel(router, enc, "Uses")\n@enduml',
    ),
    Example(
        id="c4-deployment",
        title="C4 — Deployment",
        description="C4 deployment diagram mapping containers to infrastructure.",
        category="C4",
        libraries=["c4"],
        source="@startuml\n!include <C4/C4_Deployment>\n"
        'Deployment_Node(y0, "y0", "Ubuntu Docker host") {\n'
        '  Deployment_Node(dk, "Docker Compose", "") {\n'
        '    Container(gw, "Gateway", "nginx")\n'
        '    Container(api, "API", "FastAPI")\n'
        '    Container(puml, "PlantUML", "Jetty")\n  }\n}\n'
        'Rel(gw, api, "routes")\nRel(gw, puml, "routes /editor")\n@enduml',
    ),
    # ---- Cloud architecture -------------------------------------------------
    Example(
        id="aws-architecture",
        title="AWS architecture",
        description="A small AWS architecture using the official awslib icons.",
        category="AWS",
        libraries=["awslib"],
        source="@startuml\n!include <awslib/AWSCommon>\n"
        "!include <awslib/Compute/EC2>\n"
        "!include <awslib/Database/DynamoDB>\n"
        "!include <awslib/Storage/SimpleStorageService>\n"
        'EC2(web, "Web Server", "t3.micro")\n'
        'DynamoDB(db, "Sessions", "DynamoDB")\n'
        'SimpleStorageService(bucket, "Assets", "S3")\n'
        "web --> db\nweb --> bucket\n@enduml",
    ),
    Example(
        id="azure-architecture",
        title="Azure architecture",
        description="An Azure architecture using the Azure stdlib icons.",
        category="Azure",
        libraries=["azure"],
        source="@startuml\n!include <azure/AzureCommon>\n"
        "!include <azure/Compute/AzureVirtualMachine>\n"
        "!include <azure/Compute/AzureAppService>\n"
        "!include <azure/Databases/AzureSQLDatabase>\n"
        'AzureAppService(app, "App Service", "Web app")\n'
        'AzureVirtualMachine(vm, "VM", "Linux")\n'
        'AzureSqlDatabase(sql, "SQL Database", "PaaS")\n'
        "app --> vm\napp --> sql\n@enduml",
    ),
    Example(
        id="kubernetes-architecture",
        title="Kubernetes architecture",
        description="Kubernetes workloads and services using the K8s icon set.",
        category="Kubernetes",
        libraries=["kubernetes"],
        source="@startuml\n!include <k8s/Common>\n"
        "!include <k8s/OSS/KubernetesPod>\n"
        "!include <k8s/OSS/KubernetesSvc>\n"
        "!include <k8s/OSS/KubernetesDeploy>\n"
        'KubernetesDeploy(deploy, "web", "")\n'
        'KubernetesPod(pod, "web-pod", "")\n'
        'KubernetesSvc(svc, "web-svc", "")\n'
        "svc --> pod\ndeploy --> pod\n@enduml",
    ),
    Example(
        id="azure-kubernetes",
        title="Azure + Kubernetes (AKS)",
        description="Mixing two icon libraries in one diagram — Azure hosting AKS.",
        category="Kubernetes",
        libraries=["azure", "kubernetes"],
        source="@startuml\n!include <azure/AzureCommon>\n"
        "!include <azure/Containers/AzureKubernetesService>\n"
        "!include <k8s/Common>\n"
        "!include <k8s/OSS/KubernetesPod>\n"
        'AzureKubernetesService(aks, "AKS", "Managed K8s")\n'
        'KubernetesPod(pod, "workload", "")\n'
        "aks --> pod\n@enduml",
    ),
    Example(
        id="gcp-architecture",
        title="GCP architecture",
        description="Google Cloud architecture using the pinned, vendored GCP icon set.",
        category="GCP",
        libraries=["gcp"],
        source="@startuml\n!include <gcp/GCPCommon>\n"
        "!include <gcp/Compute/Compute_Engine>\n"
        "!include <gcp/Storage/Cloud_Storage>\n"
        'Compute_Engine(vm, "Compute Engine", "VM")\n'
        'Cloud_Storage(bucket, "Cloud Storage", "Bucket")\n'
        "vm --> bucket\n@enduml",
    ),
    # ---- Network & security -------------------------------------------------
    Example(
        id="network-security",
        title="Network & security (OSA)",
        description="A network/security diagram using Open Security Architecture icons.",
        category="Network & Security",
        libraries=["osa"],
        source="@startuml\n!include <aws/common>\n"
        "!include <osa/desktop/desktop>\n"
        "!include <osa/firewall/firewall>\n"
        "!include <osa/database/database>\n"
        'DESKTOP(client, "Client")\n'
        'FIREWALL(fw, "Firewall")\n'
        'DATABASE(db, "Database")\n'
        "client --> fw\nfw --> db\n@enduml",
    ),
    # ---- Icons & libraries --------------------------------------------------
    Example(
        id="mixed-icons",
        title="Mixed icon libraries",
        description="Combining logos/devicons sprites in a stack diagram.",
        category="Icons & Libraries",
        libraries=["logos", "tupadr3"],
        source="@startuml\n!include <logos/kubernetes>\n!include <logos/postgresql>\n"
        "!include <logos/react>\n"
        'rectangle "<$react>\\nFrontend" as fe\n'
        'rectangle "<$kubernetes>\\nCluster" as k8s\n'
        'rectangle "<$postgresql>\\nDatabase" as db\n'
        "fe --> k8s\nk8s --> db\n@enduml",
    ),
    # ---- Themes -------------------------------------------------------------
    Example(
        id="themed-sequence",
        title="Themed sequence diagram",
        description="The same diagram restyled with a PlantUML theme.",
        category="Themes",
        libraries=["uml"],
        source="@startuml\n!theme cerulean\ntitle Order processing\n"
        "actor Customer\nCustomer -> Web: Place order\nWeb -> Payments: Charge\n"
        "Payments --> Web: Approved\nWeb --> Customer: Confirmation\n@enduml",
    ),
    # ---- Diagrams as Code (non-UML) ----------------------------------------
    Example(
        id="mindmap",
        title="Mind map",
        description="PlantUML does more than UML — here's a mind map.",
        category="Diagrams as Code",
        libraries=["uml"],
        source="@startmindmap\n* Diagrams as Code\n** UML\n*** Sequence\n*** Class\n"
        "** Architecture\n*** AWS\n*** Azure\n*** Kubernetes\n** C4\n@endmindmap",
    ),
    Example(
        id="gantt",
        title="Gantt chart",
        description="Project planning as code.",
        category="Diagrams as Code",
        libraries=["uml"],
        source="@startgantt\nProject starts 2026-01-01\n[Design] lasts 5 days\n"
        "[Build] lasts 10 days\n[Build] starts at [Design]'s end\n"
        "[Ship] lasts 2 days\n[Ship] starts at [Build]'s end\n@endgantt",
    ),
    Example(
        id="json-data",
        title="JSON data",
        description="Visualise a JSON document.",
        category="Diagrams as Code",
        libraries=["uml"],
        source='@startjson\n{\n  "service": "plantuml-api-server",\n'
        '  "formats": ["png", "svg", "txt", "pdf"],\n'
        '  "libraries": ["awslib", "azure", "kubernetes", "c4"]\n}\n@endjson',
    ),
]

EXAMPLE_INDEX: dict[str, Example] = {ex.id: ex for ex in EXAMPLES}
