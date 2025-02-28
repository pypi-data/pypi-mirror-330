from sparv.api import (
    Config,
    AllSourceFilenames,
    Export,
    exporter
)

from sbx2hf import sbx2hf

@exporter("Upload corpus to Hugging Face using the sbx2hf tool", language="swe")
def upload_to_huggingface(
    out: Export = Export("sbx_sbx2hf.hf_repository/[metadata.id]"),
    source_files: AllSourceFilenames = AllSourceFilenames(),
    metadata = Config("metadata")
):
    sbx2hf_config = {}
    default_sbx2hf_args = {
        'hf_output_folder': out,
        'push_to_hub': False,
        'paths': [f'export/xml_export.pretty/{sf}_export.xml' for sf in source_files]
    }
    if sbx2hf is not None:
        merged_config = sbx2hf_config | default_sbx2hf_args
    merged_config['metadata'] = metadata
    sbx2hf(**merged_config)