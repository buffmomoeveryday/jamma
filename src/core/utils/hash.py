# hash(daily_salt + website_domain + ip_address + user_agent)


def user_agent_hashing(secret_key, website_domain, ip_address, user_aget) -> str:
    hash = str(hash(secret_key, website_domain, ip_address, user_aget))
    return hash
