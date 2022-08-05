# quicz-means-quiz-markdown

> The Quicz format is a very simple format for creating multiple choice questions based on existing markdown syntaxa clear human-readable format in a text file.

I *invented* the quicz format when I was in need of learning a lot and learning it fast.
While ploughing through the material, I wanted to generate
multiple choice questions on the fly to use them later in flashcard software.

The most simple format I could find was the [Aiken format](https://docs.moodle.org/400/en/Aiken_format)
but I find that still not intuitive enough.

Over the years, I have defaulted to markdown for most of my writing and note taking.
I find it easy and intuitive to write.
One thing lead to another and I merged the two.

## Simple example explained

Here is an example of a valid multiple choice question in the quicz format:

~~~
> Quicz is a very simple format for creating 
multiple choice questions with clear 
human-readability in mind. What syntax is it 
inspired by and based on?

+ markdown
- python
- html 
~~~

(The correct answers is 'markdown')

In markdown syntax:

- the question is a blockquote
- all possible answers are an unordered list.

In a list, if you use '+' the following content is correct.
Anything following a '-' bullet is incorrect.

## Lazy writing

The quicz format allows *lazy* writing, meaning the following will also be valid quicz format:

~~~
> Quicz is a very simple format for creating 
  multiple choice questions with clear 
 human-readability in mind. What syntax is it 
inspired by and based on?

+ markdown was
the inspiration

-python lead the way
- html is markup as well 

as hypertext
~~~

Inside the `tools` directory are some scripts to do something with quicz files.
So let's see what we get when we convert lazy, sloppy quicz into json.
In the root of the cloned repo, type the following:

## Tools / Scripts

~~~
./scripts/quicz_convQuicz2Json.py -i tests/example-quicz.qcz
~~~

This will

1. read the file `example-quicz.qcz`

This will create a json file of the quicz content. 
I decided to go through json as a *master* format.

