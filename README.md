# [tour.ubuntu.com](http://tour.ubuntu.com)

An interactive web demo of the latest version of
[Ubuntu for desktops](http://www.ubuntu.com/desktop).

## Run the site locally

The site is just flat HTML pages, so running the site is as easy as opening `en/index.html` with a browser.

However, if you want to run a local server, first [install Docker](https://docs.docker.com/engine/installation/) (on Linux you may need to [add your user to the `docker` group](https://docs.docker.com/engine/installation/linux/linux-postinstall/)), and then use the `./run` script:

``` bash
./run
```

Once the containers are setup, you can visit <http://127.0.0.1:8012/en/> in your browser.

## Translate into other languages

You can use the translation script to generate translated versions of the tour.

First, install [python polib](https://pypi.python.org/pypi/polib)
(`sudo apt install python-polib` on Ubuntu), then run:

``` bash
translate-html/bin/translate-html -t
```

This will generate translated versions of the `en/` folder for each available language.

For further help using the translator, run `translate-html/bin/translate-html --help`.

## Compress the site files

To ensure the Online Tour has optimal download page weight and in-browser performance. To do this, install Docker as mentioned above, and run:

``` bash
./run build
```
