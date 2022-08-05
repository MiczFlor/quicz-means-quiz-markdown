
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

> NOTE: see [the installation file](INSTALL.md) for information on how to make these scripts available in your command line prompt.

## Convert QUICZ to JSON

`quicz_convQuicz2Json.py`

## Convert JSON to GIFT

`quicz_convJson2Gift.py`

## Convert JSON to PDF questionnaire

* Requires `pandoc` to be installed.
* Will create an A4 sized pen and paper questionnaire as handout
* Last page contains all the answers

`quicz_convJson2PdfQuestionnaire.py`

## Convert JSON to PDF Flashcards

* Requires `pandoc` to be installed.
* Will create small A6 sized flashcards
* Alternating pages: 
    * first page shows question without answers
    * second page shows correct answers

`quicz_convJson2PdfFlashcards.py`

 
