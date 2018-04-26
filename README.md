See: https://hub.docker.com/r/frictionlessdata/datapackage-pipelines/

View the pipelines: 
```docker run -it -v `pwd`:/pipelines:rw frictionlessdata/datapackage-pipelines```

Run a pipeline
```docker run -it -v `pwd`:/pipelines:rw frictionlessdata/datapackage-pipelines run ./<pipeline name>```


