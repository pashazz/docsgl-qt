# docsgl-qt

## installation
Obtain latest version from [http://docs.gl/docs.gl.zip](http://docs.gl/docs.gl.zip)

Unpack it to the same directory where `docsgl.py` resides

in `docs.gl.js` replace line `81`:

```javascript
$(this).attr("href", "../" + version_directory + "/" + $(this).text());`
```
to

```javascript
$(this).attr("href", "../" + version_directory + "/" + $(this).text().trim() + '.html');
```

The script `docsgl.py` adds `.html` extension to HTML files and creates a Qt Help Project file.

## creating Qt Help file
````
qcollectiongenerator docsgl.qhcp
````

creates a Qt Help file with qch extension. The help file is suited for [GLBinding library](https://github.com/cginternals/glbinding) and intented to be imported into Qt Creator
