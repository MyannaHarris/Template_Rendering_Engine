# Template_Rendering_Engine
Template Rendering Engine in Python

Build a template rendering engine.

In a nutshell, we’re going to define syntax and features for a templating language (we'll use Handlebars syntax), and we’re going to implement a rendering engine that takes in a JSON string and a template string and outputs a template string. We’re going to be graded on the number of features we support (see below for details), and how long it takes your program to render the template.

i.e. One set of results for supporting feature A, one set for supporting A and B, one set for supporting A, B and C, etc. This way, if you only have time to do a basic key-value replace, you can still participate.
Template Features

### Feature #1 - Single Variable Replacement

Given a JSON document with only top-level keys and values, replace the keys in a template.

JSON document
```
{
  "name": "Jerry",
  "age": 52,
  "kids": 8
}
```
Template string
```
My name is {{name}} and I'm {{age}} years old. I have {{kids}} kids.
```
Result
```
My name is Jerry and I'm 52 years old. I have 8 kids.
```

### Feature #2 - Nested variable support

Given a JSON document with nested variables, replace the keys in a template.

JSON document
```
{
  "name": {
    "first": "Jerry",
    "last": "Ruckby"
  },
  "metadata": {
    "age": {
      "value": 52,
      "unit": "years"
    }
  }
}
```
Template string
```
My name is {{name.first}} {{name.last}} and I'm {{metadata.age.value}} {{metadata.age.unit}} old.
```
Result
```
My name is Jerry Ruckby and I'm 52 years old.
```

### Feature #3 - Commenting support

Given a template string with comments, render the template without including the comments.

JSON document
```
{
  "name": {
    "first": "Jerry",
    "last": "Ruckby"
  },
  "metadata": {
    "age": {
      "value": 52,
      "unit": "years"
    }
  }
}
```
Template string
```
{{! This template is used to start a person's biography. }}
My name is {{name.first}} {{name.last}} and I'm {{metadata.age.value}} {{metadata.age.unit}} old.
```
Result
```
My name is Jerry Ruckby and I'm 52 years old.
```

### Feature #4 - List support

Given a JSON document that includes a list of objects, render a template that iterates through the objects.

JSON document
```
{
  "name": {
    "first": "Jerry",
    "last": "Ruckby"
  },
  "metadata": {
    "age": {
      "value": 52,
      "unit": "years"
    }
  },
  "kids": [{
    "name": "Stan",
    "age": 22
  }, {
    "name": "Bob",
    "age": 18
  }]
}
```
Template string
```
My name is {{name.first}} {{name.last}} and I'm {{metadata.age.value}} {{metadata.age.unit}} old. I have some kids.{{#each kids}} {{name}}, who is {{age}} years old. {{/each}}
```
Result
```
My name is Jerry Ruckby and I'm 52 years old. Stan, who is 24 years old. Bob, who is 18 years old.
```

### Feature #5 - Boolean conditional support

Given a template string using boolean conditionals, render the template conditionally showing sections.

JSON document
```
{
  "name": {
    "first": "Jerry",
    "last": "Ruckby"
  },
  "metadata": {
    "age": {
      "value": 52,
      "unit": "years"
    }
  },
  "isAwesome": false,
  "isRich": true
}
```
Template string
```
My name is {{name.first}} {{name.last}} and I'm {{metadata.age.value}} {{metadata.age.unit}} old.{{#if isAwesome}} I'm an awesome dude.{{/if}}{{#if isRich}} I like money.{{/if}}
```
Result
```
My name is Jerry Ruckby and I'm 52 years old. I like money.
```

### Input/Output

Create a program that reads a JSON documents as the first line from stdin and a template string as the second line from stdin. Render the template and print the final string to stdout. The runner will execute this on a loop until you've been take X amount of time rendering templates. At that point, it will print out how many you were able to render in the time given.

stdin line 1
```
{"name": "Jerry","age": 52,"kids":8}
```
stdin line 2
```
My name is {{name}} and I'm {{age}} years old. I have {{kids}} kids.
```
stdout expected
```
My name is Jerry and I'm 52 years old. I have 8 kids.
```

### Exmple runs:

```
python template_filler.py 

{"name": "Jerry", "age": 52, "kids": 8}
My name is {{name}} and I'm {{age}} years old. I have {{kids}} kids.

My name is Jerry and I'm 52 years old. I have 8 kids.


{"name": {"first": "Jerry", "last": "Ruckby"}, "metadata": {"age": {"value": 52, "unit": "years"}}}
My name is {{name.first}} {{name.last}} and I'm {{metadata.age.value}} {{metadata.age.unit}} old.

My name is Jerry Ruckby and I'm 52 years old.


{"name": {"first": "Jerry", "last": "Ruckby"}, "metadata": {"age": {"value": 52, "unit": "years"}}}
{{! This template is used to start a person's biography. }}My name is {{name.first}} {{name.last}} and I'm {{metadata.age.value}} {{metadata.age.unit}} old.

My name is Jerry Ruckby and I'm 52 years old.


{"name": {"first": "Jerry", "last": "Ruckby"}, "metadata": {"age": {"value": 52, "unit": "years"}}, "kids": [{"name": "Stan", "age": 22}, {"name": "Bob", "age": 18}]}
My name is {{name.first}} {{name.last}} and I'm {{metadata.age.value}} {{metadata.age.unit}} old. I have some kids.{{#each kids}} {{name}}, who is {{age}} years old. {{/each}}

My name is Jerry Ruckby and I'm 52 years old. I have some kids. Stan, who is 22 years old.  Bob, who is 18 years old. 


{"name": {"first": "Jerry", "last": "Ruckby"}, "metadata": {"age": {"value": 52, "unit": "years"}}, "isAwesome": false, "isRich": true}
My name is {{name.first}} {{name.last}} and I'm {{metadata.age.value}} {{metadata.age.unit}} old.{{#if isAwesome}} I'm an awesome dude.{{/if}}{{#if isRich}} I like money.{{/if}}

My name is Jerry Ruckby and I'm 52 years old. I like money.
```
