from distutils.core import setup

setup(
    name = 'canadian-ham-exam',
    version = '1.0.1',
    description = 'Practice test for the Canadian Amateur Radio exam',
    author = 'Francois Marier',
    author_email = 'va7gpl@fmarier.org',
    url = 'https://launchpad.net/canadian-ham-exam',
    scripts = ['canadian-ham-exam'],
    keywords = ['ham'],
    license = 'AGPL-3.0+',
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        ],
    long_description = """\
Canadian Ham Exam uses the official question bank from Industry Canada
and allows aspiring hams to practice the section of their choice as
they are learning the material for the exam.

It requires a copy of the question bank, which can be downloaded
free of charge from the Industry Canada website:
https://www.ic.gc.ca/eic/site/025.nsf/eng/h_00004.html

Both the basic and the advanced exams are supported, in English and
French.

.. _project page: https://launchpad.net/canadian-ham-exam
"""
    )
