# encoding: utf-8

"""
Utility functions for setup.py.

"""

import filecmp
import logging
import os

ENCODING_DEFAULT = 'utf-8'
TEMP_EXTENSION = '.temp'

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
    with open(path, 'wb') as f:
        f.write(b)


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


def _get_diff_paths(dir_path1, dir_path2, results, rel_parent_dir='',
                    ignore=None):
    """
    Recursively examine the given directories, and modify results in place.

    Arguments:

      results: a three-tuple of (left_only, right_only, diff_files).

    """
    if ignore is None:
        ignore = lambda path: False

    rewrite_name = lambda name: os.path.join(rel_parent_dir, name)

    def get_relative(names):
        return [rewrite_name(name) for name in names if not ignore(name)]

    dcmp = filecmp.dircmp(dir_path1, dir_path2)

    results[0].extend(get_relative(dcmp.left_only))
    results[1].extend(get_relative(dcmp.right_only))
    results[2].extend(get_relative(dcmp.diff_files))

    for dir_name in dcmp.common_dirs:
        dir1 = os.path.join(dir_path1, dir_name)
        dir2 = os.path.join(dir_path2, dir_name)
        new_rel_dir = rewrite_name(dir_name)

        _get_diff_paths(dir1, dir2, results, ignore=ignore,
                        rel_parent_dir=new_rel_dir)


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

    def format(header, elements):
        header = '%s:' % header
        if not elements:
            header += " none"
        strings = [header] + sorted(elements)
        glue = '\n' + indent

        return glue.join(strings)

    # The 3-tuple is (left_only, right_only, diff_files).
    results = tuple([] for i in range(3))

    _get_diff_paths(sdist_dir, project_dir, results)

    project_only = results[1]
    # Slice notation modifies the list in place.
    project_only[:] = filter(lambda path: not skip(path), project_only)

    headers = ['Only in %s' % sdist_dir,
               'Only in %s' % project_dir]

    strings = [format(header, sorted(paths)) for header, paths
               in zip(headers, results)]

    return "\n".join(strings)


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


def make_temp_path(path, new_ext=None):
    """
    Arguments:

      new_ext: the new file extension, including the leading dot.
        Defaults to preserving the file extension.

    """
    root, ext = os.path.splitext(path)
    if new_ext is None:
        new_ext = ext
    temp_path = root + TEMP_EXTENSION + new_ext

    return temp_path


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
    rst = read(temp_rst_path, encoding='utf-8')
    # Make sure images aren't centered.
    # TODO: remove this hack once pandoc releases this change:
    # https://github.com/jgm/pandoc/commit/9d0b011869d06be2e540feac99070683e10d33da
    # See also: https://groups.google.com/d/topic/pandoc-discuss/rxjyzxx9oF0/discussion
    lines = rst.splitlines(True)
    lines = [line for line in lines if not ":align: center" in line]
    return "".join(lines)


def update_description_file(source_paths, target_path, docstring_path):
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
    temp_md_path = make_temp_path(target_path, new_ext=md_ext)

    write(md_description, temp_md_path, encoding='utf-8',
          description='preliminary long_description')

    temp_rst_path = make_temp_path(target_path)
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
