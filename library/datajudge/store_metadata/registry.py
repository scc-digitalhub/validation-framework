"""
MetadataStore registry.
"""
from datajudge.store_metadata.digitalhub_metadata_store import DigitalHubMetadataStore
from datajudge.store_metadata.dummy_metadata_store import DummyMetadataStore
from datajudge.store_metadata.local_metadata_store import LocalMetadataStore
from datajudge.utils.commons import STORE_DUMMY, STORE_HTTP, STORE_LOCAL

MD_STORES = {
    STORE_LOCAL: LocalMetadataStore,
    STORE_HTTP: DigitalHubMetadataStore,
    STORE_DUMMY: DummyMetadataStore,
}
