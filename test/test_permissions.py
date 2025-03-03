from lakocie_dataset import permissions

ALLOWED_URL = "https://finance.yahoo.com/?guccounter=1&guce_referrer=aHR0cHM6Ly9kdWNrZHVja2dvLmNvbS8&guce_referrer_sig=AQAAAK3CHYa7WftAqrm00xvsX1tj3n_FHm5STsfby0s_6n6xhVQO25apiAGUF7CfnrRnzGIECJWYXf_c8HuBGNajgUqeV_ZgWgvi5dWde_17Vzy-rZWoD3Ksv5LSUSlteTGR4_y3HtF-DMBaLh0nMhtDbPR8Y76geLtU7DFXC_PgXXYW"
DISALLOWED_URL = "https://www.google.com/travel/flights"


def test_webscrapping_allowed():
    assert permissions.webscrapping_allowed(ALLOWED_URL) is True


def test_webscrapping_disallowed():
    assert permissions.webscrapping_allowed(DISALLOWED_URL) is False
