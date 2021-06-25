# changelog

Every noteable change is logged here.

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

## v1.5.5

## v1.5.4

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

## v1.2.2

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

## v0.13.3

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

## v0.12.1

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

## v0.9.1

## v0.9.0

### Feature

* add authors to extract list of authors (8dfc93770b12)
* add hyphen as possible page range separator (2da41473205d)
* add method to determine if token is a headline (54f559f4f60f)

## v0.8.6

## v0.8.5

## v0.8.4

## v0.8.3

## v0.8.2

## v0.8.1

## v0.8.0

### Feature

* add method mails to parse list of emails (69cdd1223aa3)

## v0.7.1

## v0.7.0

### Feature

* extend sentence closed validator (f6a6f7364ede)

## v0.6.9

## v0.6.8

## v0.6.7

## v0.6.6

## v0.6.5

## v0.6.4

## v0.6.3

## v0.6.2

## v0.6.1

## v0.6.0

### Feature

* move pattern to parse hyper links (4639f08557af)
* move dates and page numbers code from section project (37944be089fd)

## v0.5.4

## v0.5.3

## v0.5.2

## v0.5.1

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

## v0.3.14

## v0.3.13

## v0.3.12

## v0.3.11

## v0.3.10

## v0.3.9

## v0.3.8

## v0.3.7

## v0.3.6

## v0.3.5

### Fix

* fix index error when single quotation character occurs (d1671d4d28bd)

## v0.3.4

### Fix

* ensure to parse last word in invalid sentences (37dfe4106519)

## v0.3.3

## v0.3.2

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

## v0.2.3

## v0.2.2

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

