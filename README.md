# PLY Protobuf

[Protocol Buffers] [0] lexer &amp; parser written in Python for [PLY] [1].

With this library you can create and process parse trees of a Protocol Buffers files with Python. 
For example usage see `demo.py`.

My use case: automated refactoring of `.proto` files.

## Dependency
* This project has only one dependency, [PLY] [1].
* `ply/` subdirectory is present in this repo for demonstration purposes and completeness only. If you intend to use this project, prefer better original
 [PLY] [1] repository which is up-to-date.
 
## Contributions
* There may be bugs although it works for me for quite complicated protocol buffers files. 
If you find a bug, please feel free to submit a pull request or file an issue.

## Bugs
* `Oneof` is not implemented yet. 

## Acknowledgement
This work was inspired by:
* [plyj] [2], Java lexer &amp; parser for PLY.
* [pyparsing] [3], Protocol Buffers parsing example. 
* [PLYTalk] [4], nice tutorial for PLY I used.
 
## Disclaimer
* This project was created because I needed it for myself and I didn't find Protocol Buffers parser for PLY. 
It is my first PLY / parser generator project and the first version was created in couple hours so it is not polished code. 
* There already exist Protocol Buffer parsing variant as [pyparsing] [3] example, but my previous scripts used 
PLY for parsing Java so I chosen to stay with PLY and to create Protocol Buffer variant for PLY. I like the output I can get from PLY
(e.g., line, character position in the input text) so I can automatically process input files - e.g., refactoring.
* API for this project is not guaranteed to remain stable. In particular I mean model generated from `.proto` files.
Initial model may be considered suboptimal and changed at some point. This project is intended to serve as an 
inspiration or a starting point. You will probably adapt it for your own needs. 
 
 [0]: https://developers.google.com/protocol-buffers/
 [1]: https://github.com/dabeaz/ply
 [2]: https://github.com/musiKk/plyj
 [3]: http://pyparsing.wikispaces.com/
 [4]: http://www.dabeaz.com/ply/PLYTalk.pdf