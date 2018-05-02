# Demo of how to use Frictionlessdata Packages

1. To retrieve HOT project datapackage.json files and download the datasets, run  `python process.py` 

based on https://github.com/frictionlessdata/datapackage-py


For working with tabular data and transforming it, joining, etc., see: 
https://hub.docker.com/r/frictionlessdata/datapackage-pipelines/

View the pipelines: 
```docker run -it -v `pwd`:/pipelines:rw frictionlessdata/datapackage-pipelines```

Run a pipeline
```docker run -it -v `pwd`:/pipelines:rw frictionlessdata/datapackage-pipelines run ./<pipeline name>```


