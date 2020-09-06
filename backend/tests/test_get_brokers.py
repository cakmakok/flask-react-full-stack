import json
import pdb

def test_get_brokers(client, all_brokers):
    rv = client.get('/brokers')
    assert rv.status_code == 200
    assert len(all_brokers) == len(json.loads(rv.data))
