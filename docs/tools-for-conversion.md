
# Converting back and forth

I decided to go through json as a *master* format for any conversion to other formats.
This means that you first convert a quicz formatted file to json; and from there to other formats.

## Where are the conversion scripts?

Inside the `tools` directory are some scripts to do something with quicz files.
So let's see what we get when we convert lazy, sloppy quicz into json.
In the root of the cloned repo, type the following:

~~~
./scripts/quicz_convQuicz2Json.py -i tests/example-quicz.qcz
~~~

This will

1. read the file `example-quicz.qcz`
2. convert it to JSON
3. save the output to `example-quicz.json` in the folder `tests`

NOTE: see [install-tool-scripts.md](install-tool-scripts.md) for information on how to make these scripts available in your command line prompt.

