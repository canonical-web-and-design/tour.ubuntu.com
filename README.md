# tour.ubuntu.com - The Ubuntu online tour

This is the code for [tour.ubuntu.com](http://tour.ubuntu.com),
an in-browser demonstration
of [Ubuntu for desktops](http://www.ubuntu.com/desktop).

## Run the site locally

The site is just flat HTML pages, so running the site is as easy as
opening `en/index.html` with a browser, or running a simple server, e.g.:

``` bash
python -m SimpleHTTPServer 8000
```

And visiting <http://localhost:8000>.

## Translate into other languages

You can use the translation script to generate translated versions of the tour.

First, install [python polib](https://pypi.python.org/pypi/polib)
(`sudo apt install python-polib` on Ubuntu), then run:

``` bash
translate-html/bin/translate-html -t
```

This will generate a set of folders, one for each available language,
ready to publish online.

For further help using the translator, run `translate-html/bin/translate-html --help`.

## Compress the site files

To ensure the Online Tour has optimal download page weight
and in-browser performance, the tour is optimised on publishing, using `gulp`:

``` bash
npm install           # First install required node modules
gulp compress-html    # Minify HTML and bundle in optimised CSS and JS. NB: compresses HTML in-place
gulp compress-images  # Optimise image files to make them smaller
```
