0.4.2 (2022.02.04)
==================

* Fix decoding problems in email payload reading (#22)

0.4.1 (2021.08.29)
==================

* Add new oauth open mailbox keyword (#20)

0.4.0 (2021.08.29)
==================

0.3.2 (2019.08.99)
==================

* Properly release the fork as robotframework-imaplibrary2

0.3.0 (2016.11.09)
==================

* Use imaplib `uid` function to avoid races with concurrent IMAP clients.
  Thanks to @gsikorski

0.2.5 (2016.10.31)
==================

* Added custom folder support for `Open Mailbox` and `Wait For Email`.
  Thanks to @jhoward321

0.2.4 (2016.09.17)
==================

* Fix is_secure parameter. Thanks to @davidrums

0.2.3 (2016.01.19)
==================

* Multi-words email subject search bugfixes
* Adjust documentation
* Adjust test cases

0.2.2 (2016.01.19)
==================

* Adjust documentation
* Add Python 3.x support

0.2.1 (2015.12.20)
==================

* Add subject and text filters
* Add non-secure connection support
* Adjust documentation
* Add more unit test
* Add backward compatible support
* Add `Delete All Emails`, `Delete Email`, `Mark All Emails As Read`,
  and `Mark Email As Read` keywords
* Add alternative keyword to deprecated keywords

0.2.0 (2015.12.15)
==================

* Transition from previous project maintainer
* Follow Python code style guide
* Initial project infrastructure

0.1.4 (2014.04.23)
==================

* Fix multipart-mime reading (thanks to Frank Berthold)

0.1.3 (2014.02.28)
==================

* Fix Gmail search contributed by https://github.com/martinhill

0.1.2 (2014.01.16)
==================

* Throw exception when IMAP server responds with error

0.1.1 (2013.12.20)
==================

* Add multipart email capabilities

0.1.0 (2012.12.21)
==================

* Add status filter to ``wait_for_mail`` keyword
* Fix opened page encoding to ``open_link_from_mail`` keyword

0.0.8 (2012.11.28)
==================

* Get email body - another attempt

0.0.7 (2012.11.27)
==================

* Get email body

0.0.6 (2012.11.27)
==================

* Mark emails as read

0.0.5 (2012.09.25)
==================

* Add build environment and unit test

0.0.4 (2012.09.13)
==================

* Add get links from email keyword

0.0.3 (2012.08.20)
==================

* Documents and Apache license

0.0.2 (2012.08.20)
==================

* from and to email are not required

0.0.1 (2012.08.20)
==================

* Initial version
