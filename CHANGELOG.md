# Changelog

Every noteable change is logged here.

## v1.26.3

### Fix

* insert language parameter (8b7ef9edf68b)
* do not fail on regex mark match (02fdfd3bb86e)

## v1.26.2

### Feature

* compile pattern (4fdc52a49bda)

## v1.26.1

### Fix

* do not search patterns by type (1cdbbe9db8b1)

### Documentation

* extend interface documentation (a41bcaf4a839)

## v1.26.0

### Feature

* add parameter to normalize after tokenize (d9a14501b981)
* add verbose flag, make data static (f86ccebce80f)

### Fix

* skip too short ngram (18786de7670c)

### Documentation

* extend interface documentation (cc4075023afc)

## v1.25.0

### Feature

* add method to compute ngram (05e5a159e9d2)

## v1.24.0

### Feature

* add method to find abbreviation (548fa06ad415)
* add ability to stem multiple token in one invocation (b2aa76fa73b7)

## v1.23.1

### Fix

* adjust pagenumber skip at the start of a sentence (fac1aaafedf1)
* extend hyperlink parser (5e8b53387790)

## v1.23.0

### Feature

* add English page pattern (3a70e5833532)
* add method to convert token to plain text (600c77bf491b)

### Fix

* do not treat name as page number error (4151260e0afc)
* do not detect abbreviation as page error (41359d537bd7)

## v1.22.0

### Feature

* use escape to improve extraction (4cf49d9e8355)
* extend month pattern (191f865b8eaa)
* add method to automate escaping (a701a2358ccf)
* add method to escape dates (50b52a98d195)

### Fix

* just revert in finding, not on global text (e21762050d18)

## v1.21.5

### Feature

* allow white space before highnote pattern (1d126eb1bd6f)

## v1.21.4

### Fix

* adjust sentence end checker (cf7eae9ce9e9)

## v1.21.3

### Feature

* compile pattern (0f137c5180ae)

## v1.21.2

### Feature

* extend pattern (298a9e13d734)

## v1.21.1

### Feature

* extend access pattern (468fc246ab09)

## v1.21.0

### Feature

* add method to stem word (e09846f6b3d5)

## v1.20.0

### Feature

* add method to parse hyper links and local links (656b541b4445)
* add method to parse local links (b03070c2a49e)

## v1.19.2

### Fix

* make automata thread safe (502f57508e26)

## v1.19.1

### Fix

* do not use internal API (7cf0e5899a8b)
* improve sequence merger (e6768eb5fb47)

## v1.19.0

### Feature

* add regex pattern matcher (f4184d590821)

### Documentation

* extend interface documentation (f9fc176ec89f)

## v1.18.0

### Feature

* add magic pattern generator (3e735443e092)
* align highnote magic pattern to sentence before (e7392c155af1)

## v1.17.3

### Fix

* make href magic more strict (f66726e0499e)

## v1.17.2

## v1.17.1

### Feature

* lazy load data (9419de499c81)

## v1.17.0

### Feature

* add double colon improver (882982fa7502)
* use double colon as sentence end (dde74b275c60)
* add shebang (fa48e30ce4d9)

## v1.16.2

### Feature

* sort date by occurrence (86574882d6c9)
* add option to sort result (64458cdbe6d2)

## v1.16.1

### Feature

* do not detect names as missing page number (922c94251014)

## v1.16.0

### Feature

* add machine to detect text errors (e363a3838cb7)
* add error detected method name (52b9260006a5)
* add machine to ease error defining (f539d3e4e2b3)
* add enum to present writing error (d9e91a191b2d)

## v1.15.0

### Feature

* add method to select parser by guessed language (d070c7542127)
* add method to train improved English tokeniser (3751a6f9b29c)
* limit possible name length (f5f33a4333cf)

### Fix

* skip None extraction (3b935f1dade6)

### Documentation

* adjust modules path (95b1d0342db4)
* Happy New Year! (305ea5498962)

## v1.14.1

### Fix

* make href pattern more strict (31e3434c03f7)

## v1.14.0

### Feature

* add parameter to merge directed neighbours (2ef68dd508ca)
* add verbose option return token sequence also (4e917852c7ed)

### Fix

* merge connected neighbors (bb8e60dcfe7b)

## v1.13.2

### Feature

* improve nltk path insertion (6776c4b37440)
* lazy loader tagger (078d12b0e201)

## v1.13.1

### Feature

* change return type (ddae175cb47e)

## v1.13.0

### Feature

* add dates master to process all dates pattern (61996ef80367)
* add month year pattern (b3927d5e111b)
* extend month list (866c57cc5524)
* simplify pattern, remove chars separately (56a0d4310e66)
* add reversed date pattern (bece191e2541)
* increase max year (2a6448efed39)
* add verbose flag (d4eb3edf08a3)
* add more access (ae5dc330e906)
* extend access pattern (23668bcb398a)

### Fix

* flip raw and data (048a405cca68)
* add possible white spaces (9594105fd07c)

## v1.12.1

### Fix

* improve issn parser (5079aefa79e8)

## v1.12.0

### Feature

* add method to determine isbn, issn and doi (040b0fe0fdfa)

## v1.11.0

### Feature

* unite magic improver (452ec0321b7e)
* add methods to improve abbreviation and highnote (e9cd6a50bdd1)
* add method to improve links (273e49bed21f)
* use more caching to reduce lookup time (3d1ade3263d8)

### Fix

* load nltk on first lookup (cfe0170d8175)

## v1.10.2

## v1.10.1

### Feature

* merge neighbored unbalanced sentences (bf68bdf904de)
* improve splitting high note at sentence end (a0b07c5b9392)

## v1.10.0

### Feature

* add minimal matching ratio (4616c025acb1)
* add str as possible input (2093fe22e4d6)

## v1.9.2

### Feature

* improve text extraction quality (5fd562535463)

## v1.9.1

### Feature

* add verbose flag (a3e37903800a)

## v1.9.0

### Feature

* merge NoPerson's to a single NoPerson (fc2329026c25)

## v1.8.0

### Feature

* add verbose flag (eef89bedab71)
* make author immutable (232f07225cf5)
* add verbose flag to return parsed content (72ecf4889e97)
* add verbose flag to return parsed raw (871fdc0ba332)
* add double dot name pattern (b541768d5453)
* enable dutch authors (cafc2bfb3ca0)

### Fix

* improve pagination pattern (b112f6a7343a)
* remove dutch names from NoPerson list (f7931d452372)

## v1.7.1

### Fix

* increase no author list (adc154a64bb7)

## v1.7.0

### Feature

* add city decider (4ac0116cc199)
* use magic person list (7a3a6d103607)
* use magic publisher (ead1f7146c87)
* make checker more strict (febe03ae6ccd)
* add special sign to name detector (2ad47d2d64ae)

### Fix

* extend NoPerson parser (33a3036a302a)

## v1.6.1

### Feature

* return None if matching front or end is not possible (01fa0712c6e8)
* convert marks by language (4d2061d7b8cf)

## v1.6.0

### Feature

* add method select sentence by token (ca13b29959cf)
* add famous person (839583ebc048)

## v1.5.11

### Feature

* improve person checker (26a8354e4589)

### Fix

* do not split non person authors (9de511ed3fdd)

## v1.5.10

### Feature

* add german `and` (482985daa8a3)

### Documentation

* move doc tests to header (a352f72bfcea)

## v1.5.9

### Feature

* parse simple quotation marks (94848853cf9f)

### Fix

* do not out range quotation merger (6b8231aea846)

## v1.5.8

### Feature

* use modern nltk token splitter (18ab7dd05320)

## v1.5.7

## v1.5.6

### Feature

* make quotation parser language dependent (fdb4f4a0d54a)

### Fix

* remove marks from language test (11280f4cde1c)

## v1.5.3

### Feature

* extend no person list (33ddf1c75051)

## v1.5.2

### Feature

* extend hyperlink pattern (317ff03c3ec6)

## v1.5.1

### Feature

* use family name to verify authors (c1e6867a6b47)

## v1.5.0

### Feature

* add MONTH_REGEX (cd749de8c544)
* add month detector to public API (e63336122227)
* add month list (1b37f147694e)
* add improved month pattern (df34f5b82598)

## v1.4.0

### Feature

* extend month detector pattern (9bf6f026ff1e)
* use modern similar approach (1665b96be71c)
* add day-month-year pattern (dc524813e9f0)
* extend pattern (db01ecc41792)

## v1.3.2

### Feature

* add a new university (bfe8f237a2a6)

### Fix

* word bounding is not required (09f45801cb43)

## v1.3.1

### Feature

* use no-person detector to invalidate parsed authors (e15ed9a77138)

## v1.3.0

### Feature

* use negative person list (3f9615e2c97d)
* use lower cased set (ce28827d83d0)
* add dict of institution (2940f142fe30)
* add dict with no person names (95fa42199944)

## v1.2.5

### Feature

* moves pages code (981082204320)
* move accessed pattern (58006876503b)

## v1.2.4

### Feature

* add option to remove overlapping extraction (03b8940b35d2)
* extend hyperlink pattern (77645c2ed574)

## v1.2.3

### Fix

* write trained data to local repository (971a3e8510ca)

## v1.2.1

### Fix

* merge divis followed by upper case char correctly (02f7e253b6bf)

## v1.2.0

### Feature

* enable tokens as language input (d55c52e9636d)

## v1.1.0

### Feature

* add option to normalize sentence input (fdb28b7e6492)
* add predefined abbreviations (d1ead47f5d99)

## v1.0.0

### Feature

* enable quotation signs to sentence parser (ea19db44ebda)
* use science punkt tokeniser (0d6b38453cbe)
* add additional verbose flag (1c57755602dc)
* log number of training data (40a544681eed)
* prepare input text to improve parsing result (300aedf293bd)
* use improved test data (3ad2fb6c1aa0)
* add verbose logging to science text trainer (55442fe5eafd)
* add option to modify punkt regex (461104d36a2b)
* make train runnable by console (f83e04e04113)
* use more training data (23e8cce335d2)
* train science with hugedata (ea5dcf7baa76)
* add word tagger interface (03d15e57b61b)
* use crubadan approach to determine language (8145eb26d5eb)
* add science train package to improve train tokeniser (c90411c76420)
* use nltk data name table to improve name lookup (7aa2f231ad92)

### Fix

* move science parser to german_data (ba6dd67e8bd7)

### Documentation

* replace outdated module documentation (9c49f2bddd7c)
* improve interface documentation (8c737905d492)

## v0.13.9

### Feature

* improve press and names check (8643b30cfa2a)
* extend press list (bf060a4b64f4)
* extend magic names (e0c9bd076dd6)
* add Arabic pattern (798bbc2c8e6c)

## v0.13.8

### Fix

* harden author extractor (f464ca7787ce)

## v0.13.7

### Feature

* add simple rule to judge persons (b15f3d50f471)

## v0.13.6

### Feature

* names, names, names (5e7650bf890b)

## v0.13.5

### Feature

* improve author name first name selector (a914cd3b593a)
* extend names dict (39c87425042c)

### Documentation

* extend interface documentation (0e2ac7c1025e)
* Happy New Year! (1257cdc22067)

## v0.13.4

### Feature

* add sentence prepare method (62a9e2306d30)

## v0.13.2

### Feature

* add option to compare word type instead of word type and content (58124e3f6b9b)

## v0.13.1

### Feature

* split word number connections (30e6d7150bba)

## v0.13.0

### Feature

* extend names list (9527bb3c705c)
* add method to parse and decide if item is author (adc2c5f6c53d)
* use extended author from detector package (62a1484c864d)
* extend public API (f1ae79d5cc9d)
* clarify method name (aeb3679a0aaa)

## v0.12.0

### Feature

* reduce overlapping findings (792ea2aaaca2)
* use cache to improve word type determination (2c2a7dece6d7)

## v0.11.5

## v0.11.4

### Feature

* add and validate table shortcut splitting (9699477a3a59)

## v0.11.3

### Feature

* merge references together (69465a77bf43)
* add reference type detector (528c9df8be1f)
* merge unbalanced sentences together (79e715db10ee)

## v0.11.2

### Fix

* improve numbers parser (91a0d5724a37)

## v0.11.1

### Fix

* support single number (2330f7d31315)

## v0.11.0

### Feature

* add method to match sequences in text (8242eef64d7c)
* add method to extract multiple token types (acd6acfd928a)
* extend words splitter (8f0bb57200de)

## v0.10.0

### Feature

* do not end sentence on roman number (53949f88fd0f)
* add position flag and detect more special chars as link (89b234499b1f)

### Fix

* extend hyperlink parser (b6113d19c427)

## v0.9.2

## v0.9.0

### Feature

* add authors to extract list of authors (8dfc93770b12)
* add hyphen as possible page range separator (2da41473205d)
* add method to determine if token is a headline (54f559f4f60f)

## v0.8.0

### Feature

* add method mails to parse list of emails (69cdd1223aa3)

## v0.7.1

## v0.7.0

### Feature

* extend sentence closed validator (f6a6f7364ede)

## v0.6.9

## v0.6.0

### Feature

* move pattern to parse hyper links (4639f08557af)
* move dates and page numbers code from section project (37944be089fd)

## v0.5.4

## v0.5.0

### Feature

* add method to validate pattern (ff6dac9a20fb)
* add very simple approach to detect type of word (8b9d2d5a324e)
* add language quick check methods (3d9e251dcc2b)
* extend sentence end checker (34a9d6e4658f)

## v0.4.1

### Feature

* merge quotation close tag and number to sentence before (3c82a994346a)

## v0.4.0

### Feature

* add quotation parser (07eeedb40b14)
* extend text parser (be632112adb9)
* make word splitter language dependent (7b184133dda4)

### Fix

* no `result` value if using normalize=false (d42516291fc2)

## v0.3.16

### Feature

* add option to split_token (ab853947b6f5)

## v0.3.15

## v0.3.5

### Fix

* fix index error when single quotation character occurs (d1671d4d28bd)

## v0.3.4

### Fix

* ensure to parse last word in invalid sentences (37dfe4106519)

## v0.3.1

### Feature

* extend public API (ca1bcd07676c)

## v0.3.0

### Feature

* move modern text, sentence and words parser (51c05f985813)
* add first draft to detect French (3df4a7bd292c)

### Fix

* fix probability of English extraction (9e81cfd7baec)
* remove probability logging (9047817f51ab)

### Documentation

* add general purpose of this package (819f3a14262d)
* remove non existing doc link (a8484ab63dcb)

## v0.2.1

### Fix

* rename interface and extend support datatype (b7d552b0196b)

## v0.2.0

### Feature

* add likelihood of passed language (3c1ebfa8c6b7)

## v0.1.0

### Feature

* move code from words project (d65ff33371a3)

## v0.0.0 Initial release
