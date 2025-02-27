import os.path
import zipfile

import yaml

from mitm_tooling.utilities.io_utils import FilePath, ByteSink, use_bytes_io
from .definitions import SupersetDefFile, SupersetDefFolder


def write_superset_def_as_zip(target: ByteSink, superset_def: SupersetDefFolder):
    folder_structure = superset_def.folder_dict
    with use_bytes_io(target, expected_file_ext='.zip', mode='wb', create_file_if_necessary=True) as f:
        with zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED) as zf:
            def mk_node(arg, prefix: str | None = None):
                if isinstance(arg, SupersetDefFile):
                    fn = f'{arg.filename}.yaml'
                    if prefix:
                        fn = os.path.join(prefix, fn)
                    dump = arg.model_dump(by_alias=True, mode='python', exclude_none=True)
                    s = yaml.dump(dump, default_flow_style=False)

                    zf.writestr(fn, s)
                    # with zf.open(fn, 'w') as df:
                    #    yaml.dump(dump, df)
                elif isinstance(arg, list):
                    for arg in arg:
                        mk_node(arg, prefix=prefix)
                elif isinstance(arg, dict):
                    for folder, folder_content in arg.items():
                        path = None
                        if folder != '.' and prefix:
                            path = os.path.join(prefix, folder)
                        elif prefix:
                            path = prefix
                        elif folder != '.':
                            path = folder
                        if folder != '.':
                            zf.mkdir(path)
                        mk_node(folder_content, prefix=path)

            mk_node(folder_structure)


def write_superset_assets_def(output_path: FilePath, superset_def: SupersetDefFolder):
    write_superset_def_as_zip(output_path, superset_def)
