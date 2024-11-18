from pathlib import Path

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_text

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


DOCUMENTATION = """
    lookup: file
    author: Axel Haustant
    short_description: lookup file name or content relative to repository root
    description:
        - This lookup returns the contents or filename from a file in the inventory repository.
    options:
      _terms:
        description: path(s) of files to read
        required: True
    notes:
      - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
      - this lookup does not understand 'globing', use the fileglob lookup instead.
"""

EXAMPLES = """
- debug: msg="the value of foo.txt is {{lookup('repo', 'foo.txt') }}"

- name: display multiple file contents
  debug: var=item
  with_repo:
    - "foo.txt"
    - "bar.txt"
"""

RETURN = """
  _raw:
    description:
      - content of file(s) of filename(s) if the filename parameter is true
"""


def find_repo_root(path):
    '''
    Find a git root repository from a given path.
    Examine the path content and then parents until a `.git` directory is found.
    '''
    path = Path(path)
    while not (path / '.git').exists() and len(path.parents):
        path = path.parent
    return str(path) if (path / '.git').exists() else None


class LookupModule(LookupBase):

    def run(self, terms, variables=None, filename=False, **kwargs):
        root = find_repo_root(variables['inventory_dir'])
        if not root:
            raise AnsibleError('Cound not find a git repository')

        ret = []

        for term in terms:
            display.debug("Repository lookup term: %s" % term)

            # Find the file in the expected search path
            lookupfile = self.find_file_in_search_path({'ansible_search_path': [root]}, None, term)
            display.vvvv('File lookup using %s as file' % lookupfile)
            try:
                if not lookupfile:
                    raise AnsibleParserError()
                if filename:
                    ret.append(lookupfile)
                else:
                    b_contents, show_data = self._loader._get_file_contents(lookupfile)
                    contents = to_text(b_contents, errors='surrogate_or_strict')
                    ret.append(contents.rstrip())
            except AnsibleParserError:
                raise AnsibleError("could not locate file in lookup: %s" % term)

        return ret
