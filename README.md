# nlpExercises
Experimenting with problems in NLP (English gerund formation using an FST, sentence generation, parsing and context free grammars)

## verb-morphology
Using a Finite State Transducer, derive the correct American English gerundative form for a subset of 360 verbs. 
Within the 360verbs.txt list, all verb stems are at least three letters long. 

The -ing form consists of producing <stem> + ing for most cases, however there are three other primary cases that must be handled:

* 1. Drop word-final -e if it is preceded by a consonant or by a u (e.g. arguing, making)
* 2. Drop word-final -ie and add -y (e.g. tying)
* 3. Double -n, -p, -t, -r when it is immediately preceded by a vowel (e.g. putting, running).
