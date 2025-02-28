.. |package-name| replace:: regexplain

.. |pypi-version| image:: https://img.shields.io/pypi/v/regexplain?label=PyPI%20Version&color=4BC51D
   :alt: PyPI Version
   :target: https://pypi.org/projects/regexplain/

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/regexplain?label=PyPI%20Downloads&color=037585
   :alt: PyPI Downloads
   :target: https://pypi.org/projects/regexplain/

regexplain
##########

|pypi-version| |pypi-downloads|

Description
***********

Provides Classes to build Python Regex in a more natural way, as well as given an Regex string, deconstruct it and explain in plain English.

This is a development version, and while it has been thoroughly tested, it will be battle-tested in a live project and updated as needed.

.. code-block:: python

   from regexplain import RegexTokenizer


   reg = RegexTokenizer(r"[^\w\s-]")
   reg.explain()

   # Explaining Full Pattern: [^\w\s-]
   # ┌──
   # │   [Span, Length] (0, 8), 8
   # │   [Flags] re.NOFLAG
   # │  ┌──
   # │──│ [^
   # │  │   [@0:Character Set] Matches any character not in the set
   # │  │   [Span, Length] (0, 8), 8
   # │  │   [Flags] re.NOFLAG
   # │  │  ┌──
   # │  │──│ \w
   # │  │  │   [@1:Character Class:Word] Matches any word character (alphanumeric and underscore)
   # │  │  │   [Span, Length] (2, 4), 2
   # │  │  │   [Flags] re.NOFLAG
   # │  │  └──
   # │  │  ┌──
   # │  │──│ \s
   # │  │  │   [@2:Character Class:Whitespace] Matches any whitespace character (space, tab, line-break
   # │  │  │   [Span, Length] (4, 6), 2
   # │  │  │   [Flags] re.NOFLAG
   # │  │  └──
   # │  │  ┌──
   # │  │──│ -
   # │  │  │   [@3:Literal] Matches a single character from the list '-' (case-sensitive)
   # │  │  │   [Span, Length] (6, 7), 1
   # │  │  │   [Flags] re.NOFLAG
   # │  │  └──
   # │  │ ]
   # │  │   [@0:Close Token]
   # │  └──
   # └──
