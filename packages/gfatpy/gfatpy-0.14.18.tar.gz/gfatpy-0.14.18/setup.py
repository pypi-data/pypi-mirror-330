# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gfatpy',
 'gfatpy.aeronet',
 'gfatpy.atmo',
 'gfatpy.cli',
 'gfatpy.cli.lidar',
 'gfatpy.cli.lidar.plot',
 'gfatpy.cloudnet',
 'gfatpy.generalife',
 'gfatpy.generalife.licel',
 'gfatpy.lidar',
 'gfatpy.lidar.depolarization',
 'gfatpy.lidar.depolarization.GHK',
 'gfatpy.lidar.depolarization.GHK.system_settings',
 'gfatpy.lidar.depolarization.deprecated',
 'gfatpy.lidar.nc_convert',
 'gfatpy.lidar.plot',
 'gfatpy.lidar.preprocessing',
 'gfatpy.lidar.quality_assurance',
 'gfatpy.lidar.retrieval',
 'gfatpy.lidar.retrieval.synthetic',
 'gfatpy.lidar.scc',
 'gfatpy.lidar.scc.licel2scc',
 'gfatpy.lidar.scc.licel2scc.systems',
 'gfatpy.lidar.scc.plot',
 'gfatpy.lidar.scc.scc_configFiles',
 'gfatpy.lidar.utils',
 'gfatpy.parsivel',
 'gfatpy.parsivel.michi_to_convert',
 'gfatpy.parsivel.plot',
 'gfatpy.radar',
 'gfatpy.radar.leonie von Terzi',
 'gfatpy.radar.plot',
 'gfatpy.radar.retrieve',
 'gfatpy.utils',
 'gfatpy.worker']

package_data = \
{'': ['*'],
 'gfatpy': ['assets/*', 'env_files/info_scc_example.yml'],
 'gfatpy.lidar': ['info/*', 'nc_convert/configs/*', 'scc/scc_campaigns/*'],
 'gfatpy.parsivel': ['scattering_databases/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'atmospheric_lidar>=0.5.4,<0.6.0',
 'dask>=2022.7.1,<2023.0.0',
 'linc>=1.8.0,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'matplotlib==3.9.2',
 'netCDF4>=1.6.2,<2.0.0',
 'numba==0.61.0',
 'numpy>=1.23.1,<2.0.0',
 'pyarrow>=10.0.1,<11.0.0',
 'requests>=2.28.1,<3.0.0',
 'rpgpy>=0.15.1,<0.16.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'scipy>=1.9.0,<2.0.0',
 'seaborn>=0.12.0,<0.13.0',
 'selenium>=4.1.0,<5.0.0',
 'statsmodels>=0.13.0,<0.14.0',
 'typer[all]>=0.6.1,<0.7.0',
 'typing-extensions>=4.3.0,<5.0.0',
 'xarray[h5netcdf]>=2023.6.0,<2024.0.0']

extras_require = \
{'docs': ['pdoc>=12.0.2,<13.0.0']}

entry_points = \
{'console_scripts': ['gfatpy = gfatpy.cli.main:app']}

setup_kwargs = {
    'name': 'gfatpy',
    'version': '0.14.18',
    'description': 'A python package for GFAT utilities',
    'long_description': '# gfatpy\n\nA python package for GFAT utilities\n\n\n[![pipeline status](https://gitlab.com/gfat1/gfatpy/badges/main/pipeline.svg)](https://gitlab.com/gfat1/gfatpy/-/commits/main)\n\n\n---\n**Documentation** : [https://gfat1.gitlab.io/gfatpy](https://gfat1.gitlab.io/gfatpy/gfatpy.html)  \n**Source Code** : [https://gitlab.com/gfat1/gfatpy](https://gitlab.com/gfat1/gfatpy)  \n\n---\n\n## Create package\nFollowing guide at: https://packaging.python.org/en/latest/tutorials/packaging-projects/#classifiers\n\nin gfatpy directory, run in terminal: python -m build\nIt creates "dist" directory .whl and tar.gz files\n\n## Install package in a virtual environment\npip install [path]/dist/gfatpy-0.0.0.tar.gz\nNB: install pip: conda install pip\nNB: install python: conda install ipython\n\n# gitlab stuff\n## Getting started\n\nTo make it easy for you to get started with GitLab, here\'s a list of recommended next steps.\n\nAlready a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!\n\n## Add your files\n\n- [ ] [Create](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files\n- [ ] [Add files using the command line](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:\n\n```\ncd existing_repo\ngit remote add origin https://gitlab.com/gfat1/gfatpy.git\ngit branch -M main\ngit push -uf origin main\n```\n\n## Integrate with your tools\n\n- [ ] [Set up project integrations](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://gitlab.com/gfat1/gfatpy/-/settings/integrations)\n\n## Collaborate with your team\n\n- [ ] [Invite team members and collaborators](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/user/project/members/)\n- [ ] [Create a new merge request](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)\n- [ ] [Automatically close issues from merge requests](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)\n- [ ] [Enable merge request approvals](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)\n- [ ] [Automatically merge when pipeline succeeds](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)\n\n## Test and Deploy\n\nUse the built-in continuous integration in GitLab.\n\n- [ ] [Get started with GitLab CI/CD](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/ci/quick_start/index.html)\n- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/user/application_security/sast/)\n- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/topics/autodevops/requirements.html)\n- [ ] [Use pull-based deployments for improved Kubernetes management](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/user/clusters/agent/)\n- [ ] [Set up protected environments](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://docs.gitlab.com/ee/ci/environments/protected_environments.html)\n\n***\n\n# Editing this README\n\nWhen you\'re ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!).  Thank you to [makeareadme.com](https://gitlab.com/-/experiment/new_project_readme_content:3a94b1732a94fc66f6509822a9d9c9d8?https://www.makeareadme.com/) for this template.\n\n## Suggestions for a good README\nEvery project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.\n\n## Name\nChoose a self-explaining name for your project.\n\n## Description\nLet people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.\n\n## Badges\nOn some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.\n\n## Visuals\nDepending on what you are making, it can be a good idea to include screenshots or even a video (you\'ll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.\n\n## Installation\nWithin a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.\n\n## Usage\nUse examples liberally, and show the expected output if you can. It\'s helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.\n\n## Support\nTell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.\n\n## Roadmap\nIf you have ideas for releases in the future, it is a good idea to list them in the README.\n\n## Contributing\nState if you are open to contributions and what your requirements are for accepting them.\n\nFor people who want to make changes to your project, it\'s helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.\n\nYou can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.\n\n## Authors and acknowledgment\nShow your appreciation to those who have contributed to the project.\n\n## License\nFor open source projects, say how it is licensed.\n\n## Project status\nIf you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.\n',
    'author': 'Juan Diego De la Rosa',
    'author_email': 'jdidelarc@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gfat1.gitlab.io/gfatpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
