from xml.etree import ElementTree as ET

EXPECTED = {
    "test_single_requirement": {
        "requirements": ["B-DPPS-0123"],
        "usecases": [],
    },
    "test_multiple_requirements": {
        "requirements": ["B-DPPS-0123", "B-DPPS-0124", "B-DPPS-0125"],
        "usecases": [],
    },
    "test_usecase": {
        "requirements": [],
        "usecases": ["UC-130-1.2"],
    },
    "test_multiple_usecases": {
        "requirements": [],
        "usecases": ["UC-130-1.2.1", "UC-130-1.2.2"],
    },
    "test_mixed": {
        "requirements": ["B-DPPS-0123"],
        "usecases": ["UC-130-1.2.1", "UC-130-1.2.2"],
    },
    "test_fixture_mark": {
        "requirements": ["B-DPPS-0123"],
        "usecases": ["UC-130-1.2.1"],
    },
}


def collect_markers(test_case):
    markers = {"requirements": [], "usecases": []}
    for prop in test_case.iter("property"):
        if prop.attrib["name"] == "requirement_id":
            markers["requirements"].append(prop.attrib["value"])
        elif prop.attrib["name"] == "usecase_id":
            markers["usecases"].append(prop.attrib["value"])
    return markers


def test_plugin(pytester, tmp_path):
    pytester.copy_example("conftest.py")
    pytester.copy_example("test_requirements.py")

    report_path = tmp_path / "report.xml"
    result = pytester.runpytest(f"--junit-xml={report_path}")

    result.assert_outcomes(passed=6)

    # make sure the marker information is in the junit xml
    tree = ET.parse(report_path)

    test_cases = {
        test_case.attrib["name"]: test_case for test_case in tree.iter("testcase")
    }
    assert len(test_cases) == 6

    for key, expected in EXPECTED.items():
        markers = collect_markers(test_cases[key])
        for type_, expected_ids in expected.items():
            ids = markers[type_]
            assert len(ids) == len(expected_ids)
            assert set(ids) == set(expected_ids)


def test_version():
    from pytest_requirements import __version__

    assert __version__ != "0.0.0"
