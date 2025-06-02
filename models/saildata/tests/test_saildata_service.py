import os
import pytest
import tempfile
from models.saildata.models.saildata import SailData
from models.saildata.models.factory import SailDataFactory
from models.saildata.saildata_service import SailDataService

@pytest.fixture
def temp_db_path():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    os.remove(path)

def test_saildata_factory_and_to_dict():
    saildata = SailDataFactory.create(1, 10, 5, 15, 7, codezero_i=12, jib_i=8, jib_j=4)
    d = saildata.to_dict()
    assert d["yacht_id"] == 1
    assert d["genoa_i"] == 10
    assert d["main_p"] == 15
    assert d["codezero_i"] == 12
    assert d["jib_i"] == 8
    assert d["jib_j"] == 4

def test_saildata_from_dict():
    data = {
        "yacht_id": 2,
        "genoa_i": 11,
        "genoa_j": 6,
        "main_p": 16,
        "main_e": 8,
        "codezero_i": 13,
        "jib_i": 9,
        "jib_j": 5
    }
    saildata = SailDataFactory.from_dict(data)
    assert saildata.yacht_id == 2
    assert saildata.genoa_i == 11
    assert saildata.main_p == 16
    assert saildata.codezero_i == 13
    assert saildata.jib_i == 9
    assert saildata.jib_j == 5

def test_saildata_service_save_and_get(temp_db_path):
    service = SailDataService(db_path=temp_db_path)
    saildata = SailDataFactory.create(3, 12, 7, 17, 9, staysail_i=14)
    service.save_saildata(saildata)
    loaded = service.get_saildata(3)
    assert loaded is not None
    assert loaded.yacht_id == 3
    assert loaded.staysail_i == 14
    service.close()

def test_saildata_service_save_from_dict(temp_db_path):
    service = SailDataService(db_path=temp_db_path)
    data = {
        "yacht_id": 4,
        "genoa_i": 13,
        "genoa_j": 8,
        "main_p": 18,
        "main_e": 10,
        "trisail_i": 15
    }
    service.save_saildata_from_dict(data)
    loaded = service.get_saildata(4)
    assert loaded is not None
    assert loaded.yacht_id == 4
    assert loaded.trisail_i == 15
    service.close()

def test_saildata_service_overwrite(temp_db_path):
    service = SailDataService(db_path=temp_db_path)
    saildata1 = SailDataFactory.create(5, 14, 9, 19, 11)
    saildata2 = SailDataFactory.create(5, 15, 10, 20, 12, jib_i=16)
    service.save_saildata(saildata1)
    service.save_saildata(saildata2)  # Should overwrite
    loaded = service.get_saildata(5)
    assert loaded is not None
    assert loaded.genoa_i == 15
    assert loaded.jib_i == 16
    service.close()

def test_saildata_service_get_nonexistent(temp_db_path):
    service = SailDataService(db_path=temp_db_path)
    loaded = service.get_saildata(999)
    assert loaded is None
    service.close()

def test_saildata_factory_kwargs():
    saildata = SailDataFactory.create(6, 16, 11, 21, 13, custom_field=42, jib_i=17)
    assert saildata.custom_field == 42
    assert saildata.jib_i == 17

def test_saildata_to_dict_and_from_dict_roundtrip():
    saildata = SailDataFactory.create(7, 18, 12, 22, 14, staysail_j=19)
    d = saildata.to_dict()
    saildata2 = SailDataFactory.from_dict(d)
    assert saildata2.yacht_id == 7
    assert saildata2.staysail_j == 19
