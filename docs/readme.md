# Easy creation of LMS learning material

> QUICZ is a very simple format for creating multiple choice questions based on markdown syntax with clear human-readability in mind. Repo comes with conversion scripts.

QUICZ aims to allow anyone to:

* create learning material
* while you are learning
* with minimal distraction
* in plain text

QUICZ also aims to 

* stick to the basics
* be useful and readable in plain text
* provide conversion to multiple standards and platforms

The name QUICZ comes from 'quiz'.

## How did it start?

I came up with the the quicz format when I was in need of learning a lot and learning it fast.
While ploughing through the material, I wanted to 
**simultanously generate learning content like multiple choice questions** on the fly to use them later
in [Moodle LMS](https://docs.moodle.org/400/en/Managing_questions) or other
[learning management system](https://en.wikipedia.org/wiki/Learning_management_system) or
[flashcard software](https://en.wikipedia.org/wiki/List_of_flashcard_software).

Over the years, I have defaulted to **markdown for most of my writing** and note taking.
I find it easy and intuitive to write.
One thing lead to another and I merged my immediate need with my comfort zone.

## Available alternatives

The most straight forward alternative formats I found: 

* [Aiken format](https://docs.moodle.org/400/en/Aiken_format)
* [GIFT format](https://docs.moodle.org/400/en/GIFT_format)

## Simple example explained

Here is an example of a valid multiple choice question in the quicz format:

~~~
> QUICZ is a very simple format for creating 
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
> QUICZ is a very simple format for creating 
  multiple choice questions with clear 
 human-readability in mind. What syntax is it 
inspired by and based on?

+ markdown was
the inspiration

-python lead the way
- html is markup as well 

as hypertext
~~~

## Tools / Scripts

Inside the `tools` directory are some scripts to do something with quicz files.
So let's see what we get when we convert lazy, sloppy quicz into json.
In the root of the cloned repo, type the following:

~~~
./scripts/quicz_convQuicz2Json.py -i tests/example-quicz.qcz
~~~

This will

1. read the file `example-quicz.qcz`
2. convert it to JSON
3. save the output to `example-quicz.json`

I decided to go through json as a *master* format for any conversion to other formats.

