
Small Lisp Interpretter Written in Python
=========================================

Why? Well, because it's easy to do and it is a lot of fun.

It'a actually a Scheme interpreter, but with FEXPR.

There are basically two ways to start it.

Start in command line:

```
python3 run_repl.py
```

Or, start as a little api web server (written in Flask):

```
python3 run_flask.py
```

Web server is started at localhost:8000 by default, and is able to receive POST requests like (using curl):

```
curl -X POST localhost:8000 -d "(+ 1 1)"
```

It returns 2.



Requirements
------------
Python 3 installed.


License
-------

Written by Sinisa Pavlovic, sipavlovic@gmail.com

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.




