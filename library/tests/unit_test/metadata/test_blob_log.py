from datajudge.metadata.blob_log import BlobLog


class TestBlobLog:
    def test_to_dict(self):
        log = BlobLog("test", "test", "test", {"test": "test"})
        dict_ = {
            "runId": "test",
            "experimentName": "test",
            "datajudgeVersion": "test",
            "test": "test",
        }
        assert log.to_dict() == dict_
