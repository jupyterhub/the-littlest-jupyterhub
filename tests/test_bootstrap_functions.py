# Unit test some functions from bootstrap.py
import os
import sys

import pytest

# Since bootstrap.py isn't part of the package, it's not automatically importable
GIT_REPO_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, GIT_REPO_PATH)
from bootstrap import bootstrap


@pytest.mark.parametrize(
    "requested,expected",
    [
        ((1,), (1, 1, 0)),
        ((1, 0), (1, 0, 1)),
        ((1, 2), None),
        ((2, 0, 0), (2, 0, 0)),
        ("latest", (2, 0, 1)),
    ],
)
def test_find_matching_version(requested, expected):
    all_versions = [
        (0, 0, 1),
        (1, 0, 0),
        (1, 0, 1),
        (1, 1, 0),
        (2, 0, 0),
        (2, 0, 1),
    ]
    r = bootstrap._find_matching_version(all_versions, requested)
    assert r == expected


# git ls-remote --tags --refs https://github.com/jupyterhub/jupyterhub.git
mock_git_ls_remote = """\
c345aa658eb482b8102b51f6ec3f0fc667b60520	refs/tags/0.1.0
e2cbc2fb41c04cfe416b19e83f36ea67b1a4e693	refs/tags/0.2.0
7fd56fe943bf0038cb14e7aa2af5a3e5ad929d47	refs/tags/0.3.0
89cf4c60a905b4093ba7584c4561073a9faa0d3d	refs/tags/0.4.0
bd08efc4a5485a9ecd17882e9bfcab9486d9956a	refs/tags/0.4.1
19c77d0c7016c08a4a0e883446114a430a551882	refs/tags/0.5.0
b4621d354b6bbc865373b7c033f29c6872237780	refs/tags/0.6.0
ed38f08daf4d5cf84f04b2d96327681221c579dd	refs/tags/0.6.1
d5cf9657f2ca16df080e2be21da792288e9f4f99	refs/tags/0.7.0
2cdb4be46a0eb291850fc706cfe044873889a9bc	refs/tags/0.7.1
e4dd65d2611e3c85fe486c561fc0efe9ca720042	refs/tags/0.7.2
4179668e49ceedb805cb1a38dc5a70e6a21fa685	refs/tags/0.8.0
9bab206eb96c6726ac936cf5da3f61eb9c9aa519	refs/tags/0.8.0b1
5f2c6d25fefcbe91d86945f530e6533822449c46	refs/tags/0.8.0b2
0d720103c5207d008947580b7b453e1eb0e7594a	refs/tags/0.8.0b3
a2458ffa402fa2d2905c558100c673e98789a8a8	refs/tags/0.8.0b4
b9e2838a4d9b35a9ad7c3353e62ab006b4ec10a4	refs/tags/0.8.0b5
a62fc1bc1c9b2408713511cb56e7751403ed5503	refs/tags/0.8.0rc1
a77ca08e3e25c14552e246e8ad3ca65a354ba192	refs/tags/0.8.0rc2
6eef64842a7d7939b3f1986558849d1977a0e121	refs/tags/0.8.1
de46a16029b7ae217293e7e64e14a9c2e06e5e60	refs/tags/0.9.0
9f612b52187db878f529458e304bd519fda82e42	refs/tags/0.9.0b1
ec4b038b93495eb769007a0d3d56e6d6a5ff000c	refs/tags/0.9.0b2
ea8a30b1a5b189b2f2f0dbfdb22f83427d1c9163	refs/tags/0.9.0b3
99c155a61a1d95a3a8ca41ebb684cdedc1fb170f	refs/tags/0.9.0rc1
1aeebd4e4937ea5185ce02f693f94272c30f4ebd	refs/tags/0.9.1
01b3601a12b52259b541b48eaa7a7afb3f7d988c	refs/tags/0.9.2
70ddc22e071bb7797528831d25c567f6f4920c67	refs/tags/0.9.3
7ecb093163a453ae2edfa6bc8bf1f7cfc2320627	refs/tags/0.9.4
3e83bc440b8d5abdc0a4336978bd542435402f77	refs/tags/0.9.5
cc07c706931c78f46367db9c0c20e6ed9f0f6f85	refs/tags/0.9.6
4e24276d40ad83fd113c7c2f1f8619a9ba3af0d8	refs/tags/1.0.0
582162c760e81995f4f5405e9c8908d2a76f4abf	refs/tags/1.0.0b1
1193f6a74c38b36594f6f57c786fa923a2747150	refs/tags/1.0.0b2
512dae6cd8a846dd490d77d21fd4e13f59c38961	refs/tags/1.1.0
a420c55391273852332ef5f454a0a3b9e0e5b71f	refs/tags/1.1.0b1
317f0efaf25eb7cb2de4503817cf20937ce110bd	refs/tags/1.2.0
f66e5d35b5f89a28f6328c91801a8f99e0855a8e	refs/tags/1.2.0b1
27e1196471729cf6f25fd3786286797e32de973a	refs/tags/1.2.1
af0c1ed932d00fa26ac91f066a5a9eafb49b7cb1	refs/tags/1.2.2
3794abfbdda0a92237f4c31985420691da70da36	refs/tags/1.3.0
e22ab5dc93dd8e724b828a0880032f6b5dc00231	refs/tags/1.4.0
0656586b75b30091583c0573b3d272cb3add24d2	refs/tags/1.4.1
5744ce73bcf0014cc3de6c946f12027448b136da	refs/tags/1.4.2
c6fb64d8f30686c2c2667b69b53402d506a3bac5	refs/tags/1.5.0
4ceb906435dbd4cf800b0480d413303f056e4900	refs/tags/2.0.0
61233698dfb353c703ea2e085312b9066ea2e92e	refs/tags/2.0.0b1
fe61c932409550dc352abf68bd6aaaa8871ac81f	refs/tags/2.0.0b2
a79c5c5a6bfe553af277f2835419d65b98ae0cb9	refs/tags/2.0.0b3
fa1098a998561321de29c6147235032fd6b0c3f5	refs/tags/2.0.0rc1
75b115c356983c138c2d8d92cb45f068ad3d9c9d	refs/tags/2.0.0rc2
ed8e25ef3f471d60b671f2a1cf2db17581c778a2	refs/tags/2.0.0rc3
4083307b3f37039075862034963ed42a459b1bdb	refs/tags/2.0.0rc4
baf1f36dbfe8d8264b3914650b4db6daed843389	refs/tags/2.0.0rc5
12961be3b13a10617d8f95f333da2bb67390a2c7	refs/tags/2.0.1
e40df3f1a5e284926f5c9ce66a1e57a814bb98f8	refs/tags/2.0.2
11d40c13860bd02816ad724979ad2e08b8bd103a	refs/tags/2.1.0
bde6b66287e3d157f2577bcaf2e986af020139f4	refs/tags/2.1.1
29f51794db562ecc4c7653525193d6e210151fdb	refs/tags/2.2.0
8cbafd25425b7eaf2fdc46e183cee437c09b53c1	refs/tags/2.2.1
1eada986101f2385ee7498395a799f28bcd167e8	refs/tags/2.2.2
1bb0ec38ae4c5e4e5c8b6cc3b89b7b20ea8bd400	refs/tags/2.3.0
69f926706be03505f9b9e30a5ad2d4f8c9f9d48d	refs/tags/2.3.1
"""


@pytest.mark.parametrize(
    "requested,expected",
    [
        ("1", "1.5.0"),
        ("1.0", "1.0.0"),
        ("1.2", "1.2.2"),
        ("1.100", None),
        ("2.0.0", "2.0.0"),
        ("random-branch", "random-branch"),
        ("1234567890abcdef", "1234567890abcdef"),
        ("2.0.0rc4", "2.0.0rc4"),
        ("latest", "2.3.1"),
    ],
)
def test_resolve_git_version(monkeypatch, requested, expected):
    def mock_run_subprocess(*args, **kwargs):
        return mock_git_ls_remote

    monkeypatch.setattr(bootstrap, "run_subprocess", mock_run_subprocess)

    if expected is None:
        with pytest.raises(Exception) as exc:
            bootstrap._resolve_git_version(requested)
        assert exc.value.args[0].startswith("No version matching 1.100 found")
    else:
        assert bootstrap._resolve_git_version(requested) == expected
