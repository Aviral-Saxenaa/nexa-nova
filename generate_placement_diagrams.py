"""Create editable diagrams.net pages for the placement-system assignment."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5


COLORS = {
    "start": ("#d5e8d4", "#82b366"),
    "decision": ("#fff2cc", "#d6b656"),
    "student": ("#dae8fc", "#6c8ebf"),
    "admin": ("#e1d5e7", "#9673a6"),
    "company": ("#f8cecc", "#b85450"),
    "record": ("#d5e8d4", "#82b366"),
    "usecase": ("#ffffff", "#6c8ebf"),
    "actor": ("#ffffff", "#4d4d4d"),
    "default": ("#ffffff", "#6c8ebf"),
}


def add_vertex(root: ET.Element, cell_id: str, label: str, x: int, y: int,
               width: int = 190, height: int = 58, kind: str = "default") -> None:
    fill, stroke = COLORS[kind]
    shapes = {
        "decision": "rhombus",
        "start": "ellipse",
        "usecase": "ellipse",
        "actor": "umlActor",
    }
    shape = shapes.get(kind, "rounded")
    style = (
        f"shape={shape};whiteSpace=wrap;html=1;rounded=1;arcSize=16;"
        f"fillColor={fill};strokeColor={stroke};fontSize=13;fontFamily=Helvetica;"
        "align=center;verticalAlign=middle;spacing=6;"
    )
    if kind == "actor":
        style = (
            "shape=umlActor;html=1;verticalLabelPosition=bottom;verticalAlign=top;"
            "fillColor=none;strokeColor=#4d4d4d;fontSize=13;fontFamily=Helvetica;"
        )
    cell = ET.SubElement(
        root, "mxCell",
        {"id": cell_id, "value": label, "style": style, "vertex": "1", "parent": "1"},
    )
    ET.SubElement(
        cell, "mxGeometry",
        {"x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"},
    )


def add_edge(root: ET.Element, edge_id: str, source: str, target: str, label: str = "") -> None:
    style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;"
        "html=1;endArrow=block;endFill=1;strokeWidth=1.5;fontSize=11;"
    )
    cell = ET.SubElement(
        root, "mxCell",
        {
            "id": edge_id,
            "value": label,
            "style": style,
            "edge": "1",
            "parent": "1",
            "source": source,
            "target": target,
        },
    )
    ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})


def add_text(root: ET.Element, cell_id: str, label: str, x: int, y: int,
             width: int, height: int, style: str = "") -> None:
    base = (
        "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
        "fontFamily=Helvetica;fontSize=14;align=left;verticalAlign=middle;"
    )
    cell = ET.SubElement(
        root, "mxCell",
        {"id": cell_id, "value": label, "style": base + style, "vertex": "1", "parent": "1"},
    )
    ET.SubElement(
        cell, "mxGeometry",
        {"x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"},
    )


def make_page(name: str, nodes: list[tuple], edges: list[tuple] = ()) -> ET.Element:
    page_id = uuid5(NAMESPACE_URL, f"https://nexa-nova.local/diagrams/{name}").hex
    diagram = ET.Element("diagram", {"id": page_id, "name": name})
    model = ET.SubElement(
        diagram, "mxGraphModel",
        {
            "dx": "1280", "dy": "800", "grid": "1", "gridSize": "10",
            "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1",
            "fold": "1", "page": "1", "pageScale": "1",
            "pageWidth": "1200", "pageHeight": "850", "math": "0", "shadow": "0",
        },
    )
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
    for node in nodes:
        cell_id, label, x, y, *dimensions = node
        width = dimensions[0] if len(dimensions) > 0 else 190
        height = dimensions[1] if len(dimensions) > 1 else 58
        kind = dimensions[2] if len(dimensions) > 2 else "default"
        add_vertex(root, cell_id, label, x, y, width, height, kind)
    for index, edge in enumerate(edges, start=100):
        source, target, *label = edge
        add_edge(root, str(index), source, target, label[0] if label else "")
    return diagram


def overview_page() -> ET.Element:
    diagram = make_page(
        "01 - Synopsis",
        [
            ("2", "Student<br>Profile, resume, skills", 70, 130, 220, 90, "student"),
            ("3", "Placement Cell<br>Approvals, criteria, tracking", 470, 130, 250, 90, "admin"),
            ("4", "Company<br>Profile and job requirements", 880, 130, 220, 90, "company"),
            ("5", "Placement Management System", 390, 320, 380, 90, "default"),
            ("6", "Applications and opt-outs", 70, 550, 220, 70, "record"),
            ("7", "Interview rounds and status", 490, 550, 250, 70, "record"),
            ("8", "Selection and hiring history", 880, 550, 220, 70, "record"),
        ],
        [
            ("2", "5", "profile"),
            ("3", "5", "manage"),
            ("4", "5", "requirements"),
            ("5", "6", ""),
            ("5", "7", ""),
            ("5", "8", ""),
        ],
    )
    root = diagram.find("./mxGraphModel/root")
    add_text(root, "9", "SYSTEM SYNOPSIS", 70, 40, 700, 50, "fontSize=24;fontStyle=1;")
    add_text(root, "10", "One place to coordinate eligible openings, applications, interviews, and hiring outcomes.", 70, 690, 1050, 50)
    return diagram


def project_flow_page() -> ET.Element:
    return make_page(
        "02 - Project Flow",
        [
            ("2", "Student registers", 70, 70, 190, 58, "start"),
            ("3", "Admin reviews registration", 350, 70),
            ("4", "Profile completed<br>Resume uploaded", 630, 70, 200, 62, "student"),
            ("5", "Company submits job requirement", 910, 70, 220, 62, "company"),
            ("6", "Admin checks placement phase", 910, 210),
            ("7", "Eligibility criteria defined", 630, 210, 200, 62, "admin"),
            ("8", "Eligible students notified", 350, 210, 190, 58, "student"),
            ("9", "Student applies or opts out", 70, 210, 190, 58, "decision"),
            ("10", "Application tracked", 70, 360, 190, 58, "admin"),
            ("11", "Company reviews applicants", 350, 360, 190, 58, "company"),
            ("12", "Shortlist and schedule interview", 630, 360, 200, 62, "admin"),
            ("13", "Interview rounds recorded", 910, 360, 220, 62),
            ("14", "Final status and hiring history", 630, 540, 200, 62, "record"),
        ],
        [
            ("2", "3"), ("3", "4", "approved"), ("4", "5"), ("5", "6"),
            ("6", "7"), ("7", "8"), ("8", "9"), ("9", "10", "apply"),
            ("10", "11"), ("11", "12", "shortlisted"), ("12", "13"),
            ("13", "14"), ("9", "14", "opt out / rejected"),
        ],
    )


def activity_pages() -> list[ET.Element]:
    return [
        make_page(
            "03 - Activity - Student Profile",
            [
                ("2", "Start", 480, 40, 180, 48, "start"),
                ("3", "Register", 480, 120, 180, 55, "student"),
                ("4", "Registration approved?", 480, 210, 180, 70, "decision"),
                ("5", "Show registration status", 150, 330, 200, 58),
                ("6", "Log in", 480, 330, 180, 55, "student"),
                ("7", "Enter personal and education details", 480, 420, 220, 62),
                ("8", "Add skills, experience, projects and certifications", 480, 520, 240, 68),
                ("9", "Upload photo and resume", 480, 630, 220, 58),
                ("10", "Save completed profile", 480, 720, 220, 55, "record"),
            ],
            [("2", "3"), ("3", "4"), ("4", "5", "No"), ("4", "6", "Yes"),
             ("6", "7"), ("7", "8"), ("8", "9"), ("9", "10")],
        ),
        make_page(
            "04 - Activity - Job Application",
            [
                ("2", "Start", 480, 40, 180, 48, "start"),
                ("3", "Log in and view openings", 480, 120, 220, 58, "student"),
                ("4", "Review job and eligibility", 480, 220, 220, 58),
                ("5", "Eligible?", 480, 320, 180, 70, "decision"),
                ("6", "Do not apply", 160, 450, 190, 58),
                ("7", "Apply or opt out?", 480, 450, 190, 70, "decision"),
                ("8", "Submit application", 310, 600, 200, 58, "record"),
                ("9", "Record opt-out", 650, 600, 200, 58),
                ("10", "View application and interview status", 480, 720, 250, 58, "student"),
            ],
            [("2", "3"), ("3", "4"), ("4", "5"), ("5", "6", "No"),
             ("5", "7", "Yes"), ("7", "8", "Apply"), ("7", "9", "Opt out"),
             ("8", "10")],
        ),
        make_page(
            "05 - Activity - Selection Process",
            [
                ("2", "Application received", 440, 40, 220, 58, "start"),
                ("3", "Admin and company review", 440, 130, 220, 58),
                ("4", "Shortlisted?", 440, 230, 180, 70, "decision"),
                ("5", "Mark rejected and notify student", 80, 360, 230, 60),
                ("6", "Schedule interview<br>Date, time, location", 440, 360, 220, 65, "admin"),
                ("7", "Conduct interview round", 440, 470, 220, 58),
                ("8", "More rounds?", 440, 570, 180, 70, "decision"),
                ("9", "Selected?", 780, 570, 180, 70, "decision"),
                ("10", "Update hiring history", 780, 710, 220, 58, "record"),
            ],
            [("2", "3"), ("3", "4"), ("4", "5", "No"), ("4", "6", "Yes"),
             ("6", "7"), ("7", "8"), ("8", "7", "Yes"), ("8", "9", "No"),
             ("9", "10", "Yes"), ("9", "5", "No")],
        ),
    ]


def admin_page() -> ET.Element:
    return make_page(
        "06 - Admin Placement Cell",
        [
            ("2", "Admin login", 470, 40, 200, 55, "start"),
            ("3", "Credentials valid?", 470, 130, 200, 70, "decision"),
            ("4", "Approve / reject registrations", 470, 250, 240, 60, "admin"),
            ("5", "Add or update company", 470, 340, 240, 60, "admin"),
            ("6", "Post job and define eligibility", 470, 430, 240, 60, "admin"),
            ("7", "Filter eligible students", 470, 520, 240, 60),
            ("8", "Track applications and opt-outs", 470, 610, 240, 60),
            ("9", "Update status and interview rounds", 470, 700, 240, 60),
            ("10", "Company visits and hiring history", 830, 520, 250, 62, "record"),
            ("11", "Placement dashboard", 830, 650, 250, 62, "record"),
        ],
        [("2", "3"), ("3", "2", "No"), ("3", "4", "Yes"), ("4", "5"),
         ("5", "6"), ("6", "7"), ("7", "8"), ("8", "9"),
         ("9", "10"), ("10", "11")],
    )


def company_data_page() -> ET.Element:
    diagram = make_page(
        "07 - Company Data",
        [
            ("2", "COMPANY PROFILE", 90, 100, 420, 55, "company"),
            ("3", "Company ID<br>Name<br>Location • Domain<br>Head office<br>Phone • Branches<br>Email • LinkedIn", 90, 180, 420, 250),
            ("4", "JOB REQUIREMENT", 680, 100, 420, 55, "company"),
            ("5", "Job ID • Position<br>Domain • Qualification<br>Package • Location<br>Contract type<br>Skills • Experience<br>Eligibility criteria<br>Hiring status • Notes", 680, 180, 420, 290),
            ("6", "INTERVIEW / HIRING", 390, 560, 420, 55, "admin"),
            ("7", "Application status<br>Interview round<br>Date • Time • Location<br>Outcome • Hiring history", 390, 640, 420, 150, "record"),
        ],
        [("2", "3"), ("4", "5"), ("3", "5", "posts"), ("5", "6", "applications"),
         ("6", "7")],
    )
    root = diagram.find("./mxGraphModel/root")
    add_text(root, "8", "Company records support multiple requirements, future reposting, and company-visit photos.", 90, 470, 1010, 50)
    return diagram


def sequence_page() -> ET.Element:
    diagram = make_page(
        "08 - Sequence",
        [
            ("2", "Student", 60, 45, 170, 55, "student"),
            ("3", "System", 320, 45, 170, 55),
            ("4", "Placement Admin", 590, 45, 190, 55, "admin"),
            ("5", "Company", 900, 45, 170, 55, "company"),
            ("6", "Register / complete profile", 60, 145, 230, 55, "student"),
            ("7", "Registration pending review", 320, 225, 230, 55),
            ("8", "Approve registration", 590, 305, 230, 55, "admin"),
            ("9", "Submit job requirement", 900, 385, 230, 55, "company"),
            ("10", "Publish criteria / notify eligible", 320, 465, 250, 60),
            ("11", "Apply or opt out", 60, 550, 230, 55, "student"),
            ("12", "Share and review applicants", 590, 630, 240, 55, "admin"),
            ("13", "Shortlist / interview outcome", 900, 710, 240, 55, "company"),
            ("14", "Update status and hiring history", 320, 790, 250, 55, "record"),
        ],
        [("6", "7"), ("7", "8"), ("8", "9"), ("9", "10"), ("10", "11"),
         ("11", "12"), ("12", "13"), ("13", "14")],
    )
    root = diagram.find("./mxGraphModel/root")
    for cell_id, x in (("20", 145), ("21", 405), ("22", 685), ("23", 985)):
        add_vertex(root, cell_id, "", x, 115, 2, 700, "default")
        cell = root.find(f"./mxCell[@id='{cell_id}']")
        cell.set("style", "shape=line;strokeColor=#c7c7c7;dashed=1;")
    return diagram


def company_registration_page() -> ET.Element:
    return make_page(
        "09 - Company Registration Flow",
        [
            ("2", "Start", 470, 60, 200, 50, "start"),
            ("3", "Enter company code", 470, 150, 220, 58, "company"),
            ("4", "Enter company name", 470, 245, 220, 58),
            ("5", "Enter location", 470, 340, 220, 58),
            ("6", "Enter contact details", 470, 435, 220, 58),
            ("7", "Enter HR details", 470, 530, 220, 58),
            ("8", "Submit company record", 470, 625, 220, 58, "record"),
            ("9", "Stop", 470, 720, 200, 50, "start"),
        ],
        [("2", "3"), ("3", "4"), ("4", "5"), ("5", "6"), ("6", "7"), ("7", "8"), ("8", "9")],
    )


def class_page() -> ET.Element:
    diagram = make_page(
        "10 - Class Diagram",
        [
            ("2", "STUDENT<br>studentId<br>name, email, phone<br>address, passingYear<br>qualification, domain<br>skills, experience, resume<br>profileLinks", 40, 120, 260, 265, "student"),
            ("3", "COMPANY<br>companyId<br>name, location, domain<br>headOffice, phone<br>branches, email<br>linkedInProfile", 360, 120, 260, 235, "company"),
            ("4", "JOB REQUIREMENT<br>jobId<br>position, domain<br>qualification, package<br>location, contractType<br>skills, experience<br>eligibilityCriteria<br>hiringStatus", 700, 120, 270, 285),
            ("5", "APPLICATION<br>applicationId<br>appliedAt<br>status, optOut", 360, 530, 260, 160, "record"),
            ("6", "INTERVIEW<br>interviewId<br>round, date, time<br>location, status, notes", 700, 530, 270, 180),
            ("7", "ADMIN<br>adminId<br>name, email<br>approves, publishes,<br>tracks", 40, 550, 260, 170, "admin"),
        ],
        [("3", "4", "1 posts 0..*"), ("2", "5", "1 submits 0..*"),
         ("4", "5", "1 receives 0..*"), ("5", "6", "1 has 0..* rounds"),
         ("7", "2", "manages"), ("7", "4", "manages"), ("7", "5", "tracks")],
    )
    return diagram


def use_case_page() -> ET.Element:
    return make_page(
        "11 - Use Case Diagram",
        [
            ("2", "Student", 55, 270, 120, 100, "actor"),
            ("3", "Admin / Placement Cell", 1030, 270, 140, 110, "actor"),
            ("4", "Company", 530, 35, 120, 100, "actor"),
            ("5", "Register and log in", 270, 120, 200, 65, "usecase"),
            ("6", "Manage profile and resume", 270, 210, 210, 65, "usecase"),
            ("7", "View eligible openings", 270, 300, 200, 65, "usecase"),
            ("8", "Apply or opt out", 270, 390, 200, 65, "usecase"),
            ("9", "View application / interview status", 270, 480, 230, 70, "usecase"),
            ("10", "Approve student registration", 690, 120, 230, 65, "usecase"),
            ("11", "Register company / post jobs", 690, 210, 230, 65, "usecase"),
            ("12", "Filter eligible students", 690, 300, 220, 65, "usecase"),
            ("13", "Track applications / interviews", 690, 390, 230, 65, "usecase"),
            ("14", "Update hiring status / history", 690, 480, 230, 65, "usecase"),
        ],
        [("2", "5"), ("2", "6"), ("2", "7"), ("2", "8"), ("2", "9"),
         ("3", "10"), ("3", "11"), ("3", "12"), ("3", "13"), ("3", "14"),
         ("4", "11"), ("4", "13"), ("4", "14")],
    )


def state_page() -> ET.Element:
    return make_page(
        "12 - Application State",
        [
            ("2", "Registered", 60, 60, 180, 55, "start"),
            ("3", "Profile incomplete", 330, 60, 200, 55),
            ("4", "Profile complete", 630, 60, 200, 55, "student"),
            ("5", "Eligible", 920, 60, 180, 55),
            ("6", "Applied", 920, 190, 180, 55, "record"),
            ("7", "Under review", 630, 190, 200, 55),
            ("8", "Shortlisted", 330, 190, 200, 55, "admin"),
            ("9", "Interview scheduled", 330, 330, 220, 55),
            ("10", "Interview in progress", 630, 330, 220, 55),
            ("11", "More rounds?", 920, 330, 180, 70, "decision"),
            ("12", "Outcome selected?", 920, 470, 180, 70, "decision"),
            ("13", "Selected", 780, 630, 180, 55, "record"),
            ("14", "Rejected", 400, 630, 180, 55),
            ("15", "Opted out", 80, 330, 180, 55),
        ],
        [("2", "3"), ("3", "4"), ("4", "5"), ("5", "6", "apply"),
         ("5", "15", "opt out"), ("6", "7"), ("7", "8", "shortlisted"),
         ("7", "14", "rejected"), ("8", "9"), ("9", "10"), ("10", "11"),
         ("11", "9", "yes"), ("11", "12", "no"), ("12", "13", "yes"),
         ("12", "14", "no")],
    )


def main() -> None:
    pages = [
        overview_page(),
        project_flow_page(),
        *activity_pages(),
        admin_page(),
        company_data_page(),
        sequence_page(),
        company_registration_page(),
        class_page(),
        use_case_page(),
        state_page(),
    ]
    diagrams = ET.Element(
        "mxfile",
        {
            "host": "app.diagrams.net",
            "modified": "2026-10-24T00:00:00.000Z",
            "agent": "Python diagram generator",
            "version": "24.7.17",
            "type": "device",
        },
    )
    for page in pages:
        diagrams.append(page)
    output = Path(__file__).with_name("placement_project_diagrams.drawio")
    ET.indent(diagrams, space="  ")
    ET.ElementTree(diagrams).write(output, encoding="utf-8", xml_declaration=True)
    parsed = ET.parse(output).getroot()
    if len(parsed.findall("diagram")) != 12:
        raise ValueError("Expected 12 diagrams.net pages.")
    for page in parsed.findall("diagram"):
        cells = page.findall("./mxGraphModel/root/mxCell")
        cell_ids = {cell.get("id") for cell in cells}
        if len(cell_ids) != len(cells):
            raise ValueError(f"Duplicate cell ID on page: {page.get('name')}")
        for edge in (cell for cell in cells if cell.get("edge") == "1"):
            if edge.get("source") not in cell_ids or edge.get("target") not in cell_ids:
                raise ValueError(f"Invalid connector on page: {page.get('name')}")
    print(f"Generated {len(pages)} editable diagrams.net pages: {output}")


if __name__ == "__main__":
    main()
