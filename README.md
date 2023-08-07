# comparecaptcha

simple binary comparison of "sample.jpg" with all ".jpg" files in the folder "known".

when it matches, the filename (without extension) from the "known" folder is written to the file "results.txt".
when it does not match, the "sample.jpg" is moved to the folder "unknown" with a timestamp.
