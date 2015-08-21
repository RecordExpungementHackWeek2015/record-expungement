PDF Form Filler
===============

This little tool will fill PDF forms from command-line.

# Build

This is a very simple Qt4 project. It requires QJson and Poppler. In Debian:

```bash
$ sudo aptitude install libqt4-dev libpoppler-qt4-dev libqjson-dev
$ git clone https://github.com/ActivKonnect/pdf-form-filler.git
$ mkdir pdf-form-filler_build
$ cd pdf-form-filler_buid
$ qmake ../pdf-form-filler
$ make
```

This will produce a pdf-form-filler binary that you can run.

# Use

## List fields

You can list fields

```
pdf-form-filler list file.pdf
```

It will output a JSON list of all available fields. Currently only text fields
are handled.

## Fill form

You can also fill the form

```
pdf-form-filler fill file.pdf output.pdf
```

In that case, form data are expected to be given to STDIN in the following
format:

```javascript
[
	{
		"name": "Field Name",
		"page": 2,
		"type": "text",
		"value": "Some Value"
	}
]
```
