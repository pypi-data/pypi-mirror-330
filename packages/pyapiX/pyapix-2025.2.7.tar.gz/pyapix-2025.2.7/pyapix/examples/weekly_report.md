# Week of  Feb 9, 2025

Lots of coding.
Good progress.  
Some good notes.

The goal for the week was to have something like Postman.
Specifically
- endpoint, verb, args, post-test 
- in a structured format (yaml/json) 
- separated from code

Parsing Postman
- OSDU
- NWS collection found at postman site.  All endpoints.  NO data.
- got familiar with the data structures.
- can extract desired parts (POC)

Ended up isolating and solving the sequence problem, eg. run a sequence of
calls, with test code after each.
Addresses the problem of pulling data from the env.
Does not address pushing data to the env.

Worked on the Petstore API.
- All test data now in YAML.
    - test and validate
    - Pet CRUD sequence
- separated code from test data
    - complete but untidy

Next step(s)
- review and cleanup
- another API
- use it
- sequence with multiple APIs


Found...
Found this on reddit.  Ten years ago there was a short-lived project somewhat
similar to mine (named Beekeeper.  The author posted a link on reddit soliciting
feedback.

This was the most interesting feedback...
"""
The most useful documentation you can ever write, especially when challenging
the status quo, are examples. Compelling, real-world examples. With detail that
compares against the status quo.
"""


# Week of  Feb 16, 2025

There are two parts to the current work.
- to effectively show the power of `pyapiX`.
- to work with Postman files.
    - eg OSDU pre-shipping
Postman is a good model for hitting lots of endpoints in a systematic way.
Because...
- it is popular
- it is a json document
- it has a json schema
But it is not perfect.
- complex but not super functional
- seems to be javascript centric

## More about last week

I started the week working with Postman files (OSDU and NWS).  But finished by
defining a new ad-hoc yaml format working with the Petstore API.  
All Petstore data is now transferred into the new format.
Both are important, especially if working with OSDU.


## Current goals

- run Postman files directly in Python, without Postman.
    - run `npm` subprocess for tests?
        - not for OSDU.  Their tests are rudimentary.
    - work on template interpretation (or something) for environment vars.
        DONE
- API client for OSDU services.
    - with validation only atm.
        POC DONE
    - needs auth to call endpoints.
- pull data from PM for sending to `pyapiX` API client    
    POC DONE!
- decode parameters tacked onto a url.
    DONE

NOTE:  Postman DOES run multiple services ala vez DUH!
       Because it hits individual urls, not services.



## Current progress

- cleanup from last week (Petstore)
- extracting data from Postman (OSDU, NWS)
- inserting values to templates ala Postman
- updating and pulling from a hierarchy of environments ala Postman
- normalizing postman urls

## Bottom line

Solid progress toward...
- using Postman files as a data source for `pyapiX` 
- replacing Postman


# Week of  Feb 23, 2025

