* pdfimpose-web 1.2.0 (2025-03-01)

    * Bug fixes

        * Server no longer crashes when it fails to read statistics from the database.
        * Fixed mistakes in French translation.
        * Fix minor HTML errors.

    * Visible enhancements

        * Add a menu to choose language (closes #3).
        * Add links to Mastodon account.

    * Under-the-hood enhancements

        * Renamed `fitz` python dependency to `pymupdf` (same library, new name).
        * Bootstrap files (css and js) have been copied to the repository, not to rely on external CDN.

    -- Louis Paternault <spalax@gresille.org>

* pdfimpose-web 1.1.0 (2024-12-27)

    * Add Python3.13 support.

    -- Louis Paternault <spalax@gresille.org>

* pdfimpose-web 1.0.1 (2024-06-24)

    * Bug fixes

        * pdfautonup option 'repeat=auto' did not work (closes #1).
        * App would fail and go back to main page without any explaination about the error (closes #2).
        * App would not run if database was not initialized, or if no configuration was present.
        * App would crash instead of reporting an error if the source file was to big.
        * Repeat limit was ignored (on server side).

    -- Louis Paternault <spalax@gresille.org>

* pdfimpose-web 1.0.0 (2024-03-05)

    * First published version.

    -- Louis Paternault <spalax@gresille.org>
