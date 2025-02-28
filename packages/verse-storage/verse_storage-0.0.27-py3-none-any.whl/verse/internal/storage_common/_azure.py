def get_credential(
    credential_type,
    tenant_id,
    client_id,
    client_secret,
    certificate_path,
):
    credential_type = credential_type
    if credential_type == "default":
        from azure.identity import DefaultAzureCredential

        return DefaultAzureCredential()

    if credential_type == "client_secret":
        from azure.identity import ClientSecretCredential

        return ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        )

    if credential_type == "certificate":
        from azure.identity import CertificateCredential

        return CertificateCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            certificate_path=certificate_path,
        )

    if credential_type == "azure_cli":
        from azure.identity import AzureCliCredential

        return AzureCliCredential()

    if credential_type == "shared_token_cache":
        from azure.identity import SharedTokenCacheCredential

        return SharedTokenCacheCredential()

    if credential_type == "managed_identity":
        from azure.identity import ManagedIdentityCredential

        return ManagedIdentityCredential()
    return None


def aget_credential(
    credential_type,
    tenant_id,
    client_id,
    client_secret,
    certificate_path,
):
    credential_type = credential_type
    if credential_type == "default":
        from azure.identity.aio import DefaultAzureCredential

        return DefaultAzureCredential()

    if credential_type == "client_secret":
        from azure.identity.aio import ClientSecretCredential

        return ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        )

    if credential_type == "certificate":
        from azure.identity.aio import CertificateCredential

        return CertificateCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            certificate_path=certificate_path,
        )

    if credential_type == "azure_cli":
        from azure.identity.aio import AzureCliCredential

        return AzureCliCredential()

    if credential_type == "shared_token_cache":
        from azure.identity.aio import SharedTokenCacheCredential

        return SharedTokenCacheCredential()

    if credential_type == "managed_identity":
        from azure.identity.aio import ManagedIdentityCredential

        return ManagedIdentityCredential()
    return None
