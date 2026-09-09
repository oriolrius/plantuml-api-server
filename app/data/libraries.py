"""Curated catalogue of PlantUML standard-library (and one pinned external) icon
and architecture libraries.

PlantUML ships a rich standard library ("stdlib"); every ``builtin: true`` entry
below is bundled with the pinned PlantUML version and works under
``SECURITY_PROFILE=INTERNET`` because no remote fetch is needed (GCP included — this
PlantUML build bundles a ``gcp`` namespace).
"""

from __future__ import annotations

from ..models import Library

LIBRARIES: list[Library] = [
    Library(
        id="uml",
        name="Core UML",
        builtin=True,
        description="Classic UML — sequence, class, component, deployment, activity, "
        "state, use-case, object and timing diagrams. No include required.",
        include="",
        docs_url="https://plantuml.com/",
        categories=["sequence", "class", "component", "deployment", "activity", "state"],
    ),
    Library(
        id="c4",
        name="C4 model",
        builtin=True,
        description="C4 architecture-as-code (Context, Container, Component, Deployment, "
        "Dynamic) via the bundled C4-PlantUML macros.",
        include="!include <C4/C4_Container>",
        docs_url="https://github.com/plantuml-stdlib/C4-PlantUML",
        categories=["C4_Context", "C4_Container", "C4_Component", "C4_Deployment", "C4_Dynamic"],
    ),
    Library(
        id="awslib",
        name="AWS Architecture Icons",
        builtin=True,
        description="Official AWS Architecture icons (modern awslib) — Compute, Storage, "
        "Database, Networking, groups and more.",
        include="!include <awslib/AWSCommon>",
        docs_url="https://github.com/awslabs/aws-icons-for-plantuml",
        categories=["Compute", "Storage", "Database", "Networking", "Groups", "Analytics"],
    ),
    Library(
        id="azure",
        name="Azure Icons",
        builtin=True,
        description="Microsoft Azure service icons for cloud architecture diagrams.",
        include="!include <azure/AzureCommon>",
        docs_url="https://github.com/plantuml-stdlib/Azure-PlantUML",
        categories=["Compute", "Storage", "Databases", "Networking", "Containers"],
    ),
    Library(
        id="kubernetes",
        name="Kubernetes Icons",
        builtin=True,
        description="Kubernetes / K8s resource icons (Pods, Services, Deployments, "
        "Ingress, control-plane components).",
        include="!include <k8s/Common>",
        docs_url="https://github.com/dcasati/kubernetes-PlantUML",
        categories=["Workloads", "Networking", "ControlPlane", "Storage"],
    ),
    Library(
        id="osa",
        name="Open Security Architecture",
        builtin=True,
        description="OSA network & security icons — firewalls, routers, servers, actors "
        "— for network and security architecture diagrams. Requires the legacy "
        "`<aws/common>` helper.",
        include="!include <aws/common>\n!include <osa/firewall/firewall>",
        docs_url="https://github.com/plantuml-stdlib/Open-Security-Architecture-PlantUML",
        categories=["network", "security", "hardware", "user"],
    ),
    Library(
        id="material",
        name="Material Design Icons",
        builtin=True,
        description="Google Material Design icon set — thousands of general-purpose "
        "sprites usable as supplementary architecture symbols. Reference sprites as "
        "`<$icon>` after including the icon file.",
        include="!include <material2.1.19/common>",
        docs_url="https://github.com/Templarian/MaterialDesign",
        categories=["general", "device", "action", "communication"],
    ),
    Library(
        id="office",
        name="Microsoft Office / Infrastructure Icons",
        builtin=True,
        description="Microsoft Office and infrastructure icons (servers, clients, "
        "devices, users). Requires the `<tupadr3/common>` helper.",
        include="!include <tupadr3/common>\n!include <office/Servers/database_server>",
        docs_url="https://github.com/plantuml-stdlib/Azure-PlantUML",
        categories=["Servers", "Clients", "Devices", "Users", "Concepts"],
    ),
    Library(
        id="logos",
        name="Technology Logos",
        builtin=True,
        description="Vendor & technology logos (SVG-quality sprites) for stacks and "
        "integration diagrams.",
        include="!include <logos/kubernetes>",
        docs_url="https://plantuml.com/stdlib",
        categories=["cloud", "languages", "databases", "tools"],
    ),
    Library(
        id="archimate",
        name="ArchiMate",
        builtin=True,
        description="ArchiMate enterprise-architecture modelling elements and relationships.",
        include="!include <archimate/Archimate>",
        docs_url="https://github.com/plantuml-stdlib/Archimate-PlantUML",
        categories=["business", "application", "technology", "motivation"],
    ),
    Library(
        id="elastic",
        name="Elastic Stack Icons",
        builtin=True,
        description="Elastic (ELK) product and component icons.",
        include="!include <elastic/common>",
        docs_url="https://github.com/plantuml-stdlib/elastic-plantuml",
        categories=["elasticsearch", "kibana", "logstash", "beats"],
    ),
    Library(
        id="tupadr3",
        name="Devicons & Font Awesome",
        builtin=True,
        description="Devicons and Font Awesome sprite sets (via the bundled tupadr3 "
        "helper) for technology and general-purpose icons.",
        include="!include <tupadr3/common>",
        docs_url="https://github.com/tupadr3/plantuml-icon-font-sprites",
        categories=["devicons", "font-awesome", "material", "weather"],
    ),
    Library(
        id="gcp",
        name="Google Cloud Platform Icons",
        builtin=True,
        description="Google Cloud Platform architecture icons, bundled in this PlantUML "
        "stdlib. Include `<gcp/GCPCommon>` then per-service files such as "
        "`<gcp/Compute/Compute_Engine>` (snake_case macro names). Works under "
        "SECURITY_PROFILE=INTERNET with no external dependency.",
        include="!include <gcp/GCPCommon>",
        docs_url="https://plantuml.com/stdlib",
        categories=["Compute", "Storage", "Databases", "Networking"],
    ),
]

LIBRARY_INDEX: dict[str, Library] = {lib.id: lib for lib in LIBRARIES}

#: Convenience `!include` lines injected when a render request lists a library id.
INCLUDE_LINES: dict[str, list[str]] = {
    lib.id: [ln for ln in lib.include.split("\n") if ln.strip() and not ln.strip().startswith("'")]
    for lib in LIBRARIES
}
