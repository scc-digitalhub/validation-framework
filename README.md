# Validation framework

Before processing data, we generally assume that *each record has a certain structure and certain properties hold true for its contents*.
For example, with tabular data, we expect entries to have a specific number of fields and each field to respect some rules: cannot be null, must be unique, must be a number, must follow a certain format...

Whether it's due to a bug, an unforeseen edge case, a conversion between formats, or something inserted by hand, it is not rare to have invalid values. When processed, these may halt execution, propagate errors, or generate misleading statistics.

Data validation aims to find these irregularities before they become problems. This means that, along with the data, another document, called *schema*, must be provided, listing what properties must be verified.

By combining the features of pre-existing validation and profiling libraries, as well as developing new software for additional purposes, we have created a platform to aid the whole process of data validation, from the initial step of acquiring the data, to archiving and inspecting the results.

## Structure

We developed the following components. More information on how to set them up, as well as how to use them, can be found in the respective *README* files of their sub-directories.
* **Datajudge**: a *Python* library which retrieves the data (which, along with its schema, may come from several commonly used storage tools, like *S3*, *Azure*, *FTP* servers...), combines the usage of pre-existing libraries for validation (currently supports [Frictionless](https://framework.frictionlessdata.io/)) and profiling (currently supports [pandas-profiling](https://github.com/pandas-profiling/pandas-profiling)) and generates a number of documents describing results, data and environment.
* **Back-end**: using a MongoDB instance for storage, it provides *Spring* REST APIs for CRUD operations on the generated documents.
* **UI**: developed with *React-Admin*, to inspect the documents.
