from bigdata_client.connection import BigdataConnection, UploadsConnection
from bigdata_client.models.subscription import (
    OrganizationQuota,
    QuotaConsumption,
    SubscriptionDetails,
)


class Subscription:
    def __init__(
        self,
        api_connection: BigdataConnection,
        uploads_api_connection: UploadsConnection,
    ):
        self._api = api_connection
        self._uploads_api = uploads_api_connection

    def get_details(self) -> SubscriptionDetails:
        """Retrieve details of active user's subscription."""
        bigdata_quota = self._fetch_bigdata_quota()
        uploads_quota = self._fetch_uploads_quota()

        return SubscriptionDetails(
            organization_quota=OrganizationQuota(
                query_unit=bigdata_quota["query_unit"],
                file_upload_pages=uploads_quota["file_upload_pages"],
                pdf_upload_pages=uploads_quota["pdf_upload_pages"],
            )
        )

    def _fetch_bigdata_quota(self) -> dict:
        my_quota = self._api.get_my_quota()

        contextual_units_max_read = (
            my_quota.organization_quota.contextual_units_max_read
        )
        query_unit_used = int(my_quota.organization_consumed.contextual_units_read / 10)

        if contextual_units_max_read is None:
            query_unit_total = None
            query_unit_remaining = None
        else:
            query_unit_total = int(contextual_units_max_read / 10)
            query_unit_remaining = query_unit_total - query_unit_used
        return {
            "query_unit": QuotaConsumption(
                total=query_unit_total,
                used=query_unit_used,
                remaining=query_unit_remaining,
            )
        }

    def _fetch_uploads_quota(self) -> dict:
        upload_quota = self._uploads_api.get_my_quota()

        return {
            "file_upload_pages": QuotaConsumption(
                total=upload_quota.quota.subscription.max_units_allowed,
                used=upload_quota.quota.subscription.units_used,
                remaining=upload_quota.quota.subscription.units_remaining,
            ),
            "pdf_upload_pages": QuotaConsumption(
                total=upload_quota.quota.subscription.max_pages_allowed,
                used=upload_quota.quota.subscription.pages_used,
                remaining=upload_quota.quota.subscription.pages_remaining,
            ),
        }
