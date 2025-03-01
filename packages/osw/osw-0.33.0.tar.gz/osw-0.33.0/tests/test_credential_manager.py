import os
import tempfile

import yaml

from osw.auth import CredentialManager


def test_cred_mngr():
    data = {"test.domain.com": {"username": "testuser", "password": "pass123"}}
    data2 = {
        "test.domain.com:80": {"username": "testuser2", "password": "pass1234"},
        "domain.com:80": {"username": "testuser23", "password": "pass12345"},
        "other.domain.com:80": {"username": "h23123", "password": "p3454"},
    }
    with tempfile.TemporaryDirectory() as td:
        f_name = os.path.join(td, "test.yaml")
        with open(f_name, "w") as credfile:
            yaml.dump(data, credfile, default_flow_style=False)
        f_name2 = os.path.join(td, "test2.yaml")
        with open(f_name, "w") as credfile:
            yaml.dump(data, credfile, default_flow_style=False)
        with open(f_name2, "w") as credfile2:
            yaml.dump(data2, credfile2, default_flow_style=False)

        cm = CredentialManager(cred_filepath=credfile.name)
        cred = cm.get_credential(CredentialManager.CredentialConfig(iri="domain.com"))
        assert (
            cred.username == data["test.domain.com"]["username"]
            and cred.password == data["test.domain.com"]["password"]
        )

        cm = CredentialManager(cred_filepath=[credfile.name, credfile2.name])
        cred = cm.get_credential(
            CredentialManager.CredentialConfig(iri="domain.com:80")
        )
        assert (
            cred.username == data2["domain.com:80"]["username"]
            and cred.password == data2["domain.com:80"]["password"]
        )

        extra_cred = CredentialManager.UserPwdCredential(
            username="testuserX", password="pass123X", iri="domainX.com"
        )
        cm.add_credential(extra_cred)
        cred = cm.get_credential(CredentialManager.CredentialConfig(iri="domainX.com"))
        assert (
            cred.username == extra_cred.username
            and cred.password == extra_cred.password
        )
