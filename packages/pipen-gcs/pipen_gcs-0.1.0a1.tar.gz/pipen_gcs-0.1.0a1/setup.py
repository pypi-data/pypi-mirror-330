# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pipen_gcs']
install_requires = \
['google-cloud-storage>=3,<4', 'pipen>=0.16.0a1,<0.17.0']

setup_kwargs = {
    'name': 'pipen-gcs',
    'version': '0.1.0a1',
    'description': 'A plugin for pipen to handle file metadata in Google Cloud Storage',
    'long_description': '# pipen-gcs\n\nA plugin for [pipen][1] to handle files in Google Cloud Storage.\n\n> [!NOTE]\n> Since pipen v0.16.0, it introduced cloud support natively. See [here](https://pwwang.github.io/pipen/cloud/) for more information.\n> However, when the pipeline working directory is a local path, but the input/output files are in the cloud, we need to handle the cloud files ourselves and in the job script.\n> To avoid that, we can use this plugin to download the input files and upload the output files automatically.\n\n> [!NOTE]\n> Also note that this plugin does not synchronize the meta files to the cloud storage; they are already handled by pipen when needed. This plugin only handles the input/output files when the working directory is a local path. When the pipeline output directory is a cloud path, the output files will be uploaded to the cloud storage automatically.\n\n![pipen-gcs](pipen-gcs.png)\n\n## Installation\n\n```bash\npip install -U pipen-gcs\n```\n\n## Usage\n\n```python\nfrom pipen import Proc, Pipen\n\nclass MyProc(Proc):\n    input = "infile:file"\n    input_data = ["gs://bucket/path/to/file"]\n    output = "outfile:file:{{in.infile.name}}.out"\n    # We can deal with the files as if they are local\n    script = "cat {{in.infile}} > {{out.outfile}}"\n\nclass MyPipen(Pipen):\n    starts = MyProc\n    # input files/directories will be downloaded to /tmp\n    # output files/directories will be generated in /tmp and then uploaded\n    #   to the cloud storage\n    plugin_opts = {"gcs_cache": "/tmp"}\n\nif __name__ == "__main__":\n    # The working directory is a local path\n    # The output directory can be a local path, but if it is a cloud path,\n    #   the output files will be uploaded to the cloud storage automatically\n    MyPipen(workdir="./.pipen", outdir="./myoutput").run()\n```\n\n> [!NOTE]\n> When checking the meta information of the jobs, for example, whether a job is cached, the plugin will make `pipen` to use the cloud files.\n\n\n## Configuration\n\n- `gcs_cache`: The directory to save the cloud storage files.\n\n[1]: https://github.com/pwwang/pipen\n',
    'author': 'pwwang',
    'author_email': '1188067+pwwang@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
