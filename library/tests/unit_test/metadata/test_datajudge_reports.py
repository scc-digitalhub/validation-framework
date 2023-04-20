from datajudge.metadata.datajudge_reports import (
    DatajudgeProfile,
    DatajudgeReport,
    DatajudgeSchema,
)


class TestDatajudgeReports:
    def test_profile(self):
        data = DatajudgeProfile("test", "test", 1.0, {}, {})
        expected_data = {
            "lib_name": "test",
            "lib_version": "test",
            "duration": 1.0,
            "stats": {},
            "fields": {},
        }
        assert data.to_dict() == expected_data

    def test_report(self):
        data = DatajudgeReport("test", "test", 1.0, {}, True, {})
        expected_data = {
            "lib_name": "test",
            "lib_version": "test",
            "duration": 1.0,
            "constraint": {},
            "valid": True,
            "errors": {},
        }
        assert data.to_dict() == expected_data

    def test_schema(self):
        data = DatajudgeSchema("test", "test", 1.0, [])
        expected_data = {
            "lib_name": "test",
            "lib_version": "test",
            "duration": 1.0,
            "fields": [],
        }
        assert data.to_dict() == expected_data
