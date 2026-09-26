import io


def test_upload_list_and_delete_file(client, auth_headers):
    file_bytes = io.BytesIO(b"sample plan export content")
    res = client.post(
        "/upload",
        files={"file": ("plan.txt", file_bytes, "text/plain")},
        headers=auth_headers,
    )
    assert res.status_code == 201
    file_id = res.json()["file_id"]

    res = client.get("/files", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1

    res = client.delete(f"/files/{file_id}", headers=auth_headers)
    assert res.status_code == 204

    res = client.get("/files", headers=auth_headers)
    assert len(res.json()) == 0


def test_files_require_authentication(client):
    res = client.get("/files")
    assert res.status_code == 401
