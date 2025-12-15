# Summary

I did the first challenge very quickly, probably under 10 minutes without AI.

I struggled at the second challenge, even though my approach was sound. I was caught out by a something that suprised me.

In python:

test = [1,2,3,4,5]
test[:-3] = [1,2]
test[:-2] = [1,2,3]
test[:-1] = [1,2,3,4]
test[:-0] = []  # is empty ... I expected to be the whole string

hence -0 and empty are not the same in list splices. This messes up the for loop functions.
