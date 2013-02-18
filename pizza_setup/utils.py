# encoding: utf-8

"""
Utility functions for setup.py.

"""

import filecmp
import logging
import os

ENCODING_DEFAULT = 'utf-8'

_log = logging.getLogger(os.path.basename(__name__))


def read(path, encoding=None):
    """
    Read and return the contents of a text file as a unicode string.

    """
    if encoding is None:
        encoding = ENCODING_DEFAULT

    # This implementation was chosen to be compatible across Python 2/3.
    with open(path, 'rb') as f:
        b = f.read()

    return b.decode(encoding)


def _write(b, path):
    """
    Write bytes to a path.

    """
    with open(path, 'wb') as f:
        f.write(b)

def write(u, path, encoding=None, description=None):
    """
    Write a unicode string to a file.

    """
    if encoding is None:
        encoding = ENCODING_DEFAULT

    desc = ('%s ' % description) if description else ''
    _log.info("writing %sto: %s" % (desc, path))
    # This implementation was chosen to be compatible across Python 2/3.
    b = u.encode(encoding)
    try:
        _write(b, path)
    except IOError:
        # Retry if directory wasn't there a la EAFP.
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            _log.info("creating directory: %s" % dirname)
            os.makedirs(dirname)
            _write(b, path)
        else:
            raise

# In setup.py, scraping the version number from the package is preferable to
# importing the package because setup.py should not have to be able to
# run the package in order to do its distribution-related tasks.  Also,
# importing might not always be possible anyways, for example if the package
# is written in Python 2 but setup.py is being run from Python 3.  See this
# e-mail exchange for a brief discussion, for example:
# http://mail.python.org/pipermail/python-porting/2012-May/000298.html
def scrape_version(package_dir):
    """
    Return the version string for a package without importing the package.

    For this function to work, the package's __init__.py file must contain
    a line of the following form:

        __version__ = '0.1.2-alpha'

    """
    init_path = os.path.join(package_dir, '__init__.py')
    text = read(init_path)

    needle = '__version__ ='
    try:
        line = next(line for line in text.splitlines()
                    if line.startswith(needle))
    except StopIteration:
        raise Exception("version string not found in: %s" % init_path)

    expr = line[len(needle):]
    # Using eval() is more robust than using a regular expression.
    # For example, this method can handle single and double quotes,
    # end-of-line comments, and more complex version string expressions.
    version = eval(expr)

    return version


class Results(object):

    attrs = ('project_only', 'sdist_only', 'not_skipped', 'sdist_funny')

    def __init__(self):
        for attr in self.attrs:
            setattr(self, attr, [])

class Differencer(object):

    """Comparse project directories to generated sdist directories."""

    def __init__(self, skip):
        self.skip = skip
        # Each element is a: (dircmp attribute name, filter function)
        # These yield the paths added to the Results object in each step of
        # the recursive comparison.
        self.dcmp_filters = (('left_only', lambda path: not skip(path)),
                             ('right_only', lambda path: True),
                             ('common_files', lambda path: skip(path)),
                             ('common_funny', lambda path: True))

    def _get_diff_paths(self, dcmp, results, rel_parent_dir=''):
        """
        Recursively compare the given directory pair.

        This method modifies the results object in place instead of returning
        a value.

        Arguments:

          dcmp: a filecmp.dircmp object

          results: a Results object.

          rel_parent_dir: the directory relative to the project/sdist root.

          skip: a function that accepts a path relative to the project
            directory and returns whether that file should be skipped instead
            of copied.

        """
        new_rel = lambda name: os.path.join(rel_parent_dir, name)

        for rattr, (dattr, filt) in zip(Results.attrs, self.dcmp_filters):
            result_paths = getattr(results, rattr)
            dcmp_paths = [new_rel(name) for name in getattr(dcmp, dattr)]
            result_paths.extend([path for path in dcmp_paths if filt(path)])

        not_skipped = results.not_skipped
        for name in dcmp.common_dirs:
            rel_path = new_rel(name)
            if self.skip(rel_path):
                not_skipped.append(rel_path)
            self._get_diff_paths(dcmp.subdirs[name], results,
                                 rel_parent_dir=rel_path)

    def get_results(self, project_dir, sdist_dir):
        """
        Return differences between directories as a Results object.

        """
        dcmp = filecmp.dircmp(project_dir, sdist_dir)
        results = Results()
        self._get_diff_paths(dcmp, results)
        return results


# TODO [template]: consider moving this formatting function to setup.py.
def describe_differences(project_dir, sdist_dir, skip=None, indent='  '):
    """
    Describe the differences between the project and sdist directories.

    Returns a string.

    Arguments:

      skip: a function that accepts a path relative to the project directory
        and returns whether that file should be skipped instead of copied.

    """
    if skip is None:
        skip = lambda path: False

    differencer = Differencer(skip)
    results = differencer.get_results(project_dir, sdist_dir)

    def format(header, paths):
        header = '%s:' % header
        if not paths:
            header += " none"
        strings = [header] + sorted(paths)
        glue = '\n' + indent
        return glue.join(strings)

    headers = ('Only in project', 'Only in sdist', 'Not skipped', 'Funny in sdist')

    sections = [format(header, getattr(results, attr))
                for header, attr in zip(headers, Results.attrs)]
    return "\n".join(sections)


def strip_html_comments(source_path):
    """
    Read the file, and strip HTML comments.

    Returns a unicode string.

    """
    # This function assumes no line mixes HTML comments and non-comments.
    text = read(source_path)
    lines = text.splitlines(True)  # preserve line endings.

    new_lines = []
    exclude = False
    for line in lines:
        if line.startswith("<!--"):
            exclude = True
        if not exclude:
            new_lines.append(line)
        if line.find("-->") >= 0:
            exclude = False

    return "".join(new_lines)


def make_temp_path(path, temp_dir, label=None, new_ext=None):
    """
    Arguments:

      new_ext: the new file extension, including the leading dot.
        Defaults to preserving the file extension.

    """
    if label is None:
        label = ''
    basename = os.path.basename(path)
    name, ext = os.path.splitext(basename)
    if new_ext is None:
        new_ext = ext
    name = "%s%s%s" % (name, label, new_ext)
    return os.path.join(temp_dir, name)


def _write_md_to_rst(source_path, target_path, docstring_path):
    """
    Convert the given file from markdown to reStructuredText.

    Returns the path to a UTF-8 encoded file.

    """
    # Pandoc uses UTF-8 for both input and output.
    command = "pandoc --write=rst --output=%s %s" % (target_path, source_path)
    _log.info("converting with pandoc: %s to %s\n-->%s" %
              (source_path, target_path, command))

    if os.path.exists(target_path):
        os.remove(target_path)

    os.system(command)

    if not os.path.exists(target_path):
        _log.error("Error running: %s\n"
                   "  Did you install pandoc per the %s docstring?" %
                   (command, docstring_path))
        sys.exit(1)

    return target_path


def convert_md_to_rst(source_path, temp_rst_path, docstring_path):
    """
    Convert the file contents from markdown to reStructuredText.

    Returns the converted contents as a unicode string.

    Arguments:

      source_path: the path to the UTF-8 encoded file to be converted.

      docstring_path: the path to the Python file whose docstring contains
        instructions on how to install pandoc.

    """
    _write_md_to_rst(source_path, temp_rst_path, __file__)
    return read(temp_rst_path, encoding='utf-8')


def update_description_file(source_paths, target_path, docstring_path,
                            temp_dir='temp'):
    """
    Write the long_description needed for setup.py to a file.

    The long description needs to be formatted as reStructuredText:

      http://docs.python.org/distutils/setupscript.html#additional-meta-data

    """
    # Remove our HTML comments because PyPI does not allow it.
    # See the setup.py docstring for more info on this.
    sections = [strip_html_comments(path) for path in source_paths]
    md_description = '\n\n'.join(sections)

    md_ext = os.path.splitext(source_paths[0])[1]  # e.g. '.md'
    temp_md_path = make_temp_path(target_path, temp_dir=temp_dir,
                                  label=".prelim", new_ext=md_ext)
    write(md_description, temp_md_path, encoding='utf-8',
          description='preliminary long_description')
    temp_rst_path = make_temp_path(target_path, temp_dir=temp_dir)
    rst_description = convert_md_to_rst(source_path=temp_md_path,
                                        temp_rst_path=temp_rst_path,
                                        docstring_path=docstring_path)

    # Comments in reST begin with two dots.
    intro_text = """\
.. This file is auto-generated by setup.py for PyPI using pandoc, so this
.. file should not be edited.  Edits should go into the files from which
.. this file is constructed.
..
.. This file contains the long_description argument to setup.py's setup().
.. It should be checked into source control and be part of the source
.. distribution so that setup() can be passed the long_description argument
.. by end-users even without pandoc (e.g. non-maintainers, etc).

"""

    rst_description = '\n'.join([intro_text, rst_description])


    write(rst_description, target_path,
          description='complete long_description')
