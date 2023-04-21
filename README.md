# Facility
This application is designed to manage devices used by members of Czech academy of science from UJEP institute. The stable code is pushed into **master** branch every unstable version of application shoul be in **development** branch. Every stable release is available as a zip package in **releases** section. Release is made from latest **master** branch commit and is pushed to [web](https://facility.ujep.cz) in production.

## Requirements
- HD Display resolution (1280x720) or higher
- [Google Chrome](https://www.google.com/intl/cs_CZ/chrome/), version 29.0 or higher
- [Edge](https://www.microsoft.com/cs-cz/edge?form=MA13FJ#evergreen), version 11.0 or higher
- Enabled javascript, [Chrome](https://support.google.com/adsense/answer/12654?hl=en), [Edge](https://www.whatismybrowser.com/guides/how-to-enable-javascript/edge)

_Note: Web is designed for desktop and mobile devices are not supported yet. Firefox browser may have destroyed layout of web. Javascript code is not supported by old browsers._

## Server configuration
- OS: Debian GNU/Linux 11 (bullseye)
- Apache/2.4.54 (Debian)
- PHP: 8.0.25 (cli)
- PHP sqlite3: 3.34.1

_Note: Server configuration files are not provided here for security reasons. PHP sqlite3 is module for PHP that is loaded by built-in module PDO._

## Installation
1. Make sure that your server configuration meets [Server configuration](#server-configuration) above.
2. Based on [Server configuration](#server-configuration) and [resources](/resources/) folder structure set up apache config and virtual hosts.
3. Extract relese files in folder specified in apache configuration.
4. Check Attachment and Picture liks in [fill.sql](/resources/database/fill.sql) and make corresponding symbolic links in [admin](/resources/admin/) and [facility](/resources/facility/) folders.
5. Allow `.htaccess` files in at least [admin](/resources/admin/) and [facility](/resources/facility/) folders in apache configuration.
6. Make sure that apache rewrite module is enabled. 
7. Make sure that `.htaccess` file is created and has rewrite rules below.

```apache
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}\.php -f
RewriteRule ^(.*)$ $1.php [NC,L]
RewriteCond %{REQUEST_FILENAME}\.html -f
RewriteRule ^(.*)$ $1.html [NC,L]
```

| Step | File | Description |
|---|:---:|:---:|
| 1. | [create](/resources/database/create.sql) | Creates database structure |
| 2. | [fill](/resources/database/fill.sql) | Inserts initial data to database |
| 3. | [views](/resources/database/views.sql) | Creates views for reading |
| 4. | [fts](/resources/database/fts.sql) | Enables Full text search |
| 5. | [triggers](/resources/database/triggers.sql) | do not use |


_Note: Queries above makes initial state of application and includes normalized initial data. [Triggers](/resources/database/triggers.sql) query is under development, it is here according to preparation for admin application development._
