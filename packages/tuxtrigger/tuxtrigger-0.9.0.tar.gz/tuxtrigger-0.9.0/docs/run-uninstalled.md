# Running TuxTrigger uninstalled


!!! note
    TuxTrigger requires Python 3.6 or newer.

If you don't want to or can't install TuxTrigger, you can run it directly from the
source directory. After getting the sources via git or something else, there is
a `run` script that will do the right thing for you: you can either use that
script directly, or symlink it to a directory in your `PATH`.

```shell
/path/to/TuxTrigger/run --help
sudo ln -s /path/to/TuxTrigger/run /usr/local/bin/TuxTrigger && TuxTrigger --help
```
