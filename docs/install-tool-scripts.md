# Installation

The scripts don't need to *installed* as such, but your life will be easier if they are available from anywhere in the command line.
The following explains how to make the scripts accessible in your terminal from anywhere in system.

(Note: I can only write this for Linux. Help vor Mac and Windows appreciated)

## Linux: symbolic links

Create links to the scripts, following these steps:

1. change into the `tools` folder in the repo
2. type `pwd` in the terminal to get the absolute path to this folder
    * this will return something like
    `/path/to/repo/quicz-means-quiz-markdown/tools`
3. create a symbolic link:

~~~
sudo ln -s /path/to/repo/quicz-means-quiz-markdown/tools/quicz_convQuicz2Json.py /usr/local/bin/quicz_convQuicz2Json
~~~

Now, if you type `quicz_convQuicz2Json` in your terminal, you should get something like this:

~~~
No source file specified. Use:
$ quicz_convQuicz2Json -i <source>
~~~

### Troubleshooting

The python scripts need to be *executable* in the repo folder.

~~~
chmod +x quicz_convJson2Gift.py
~~~

### Other links to create

Repeat the above steps for the scripts you want to be available in the command line, e.g.

~~~
sudo ln -s /path/to/repo/quicz-means-quiz-markdown/tools/quicz_convJson2Gift.py /usr/local/bin/quicz_convJson2Gift
~~~


